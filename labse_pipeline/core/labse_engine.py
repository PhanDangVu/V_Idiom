import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any

from .text_builder import (
    CRITERIA_CATALOG,
    FLAT_CRITERIA,
    build_labse_input,
    build_frame_prefix,
)
from .ontology_scorer import compute_ontology_similarity

DATA_DIR = Path(__file__).parent.parent / "data"
CSV_PATH = DATA_DIR / "thanh_ngu_tuc_ngu_100_cau_v4.csv"
RDF_PATH = DATA_DIR / "v-idiomV5_final.rdf"


class LaBSEOntologyEngine:
    """
    Hệ thống Lai ghép Neuro-Symbolic (LaBSE + Bản thể học OWL 2):
    - Mã hóa chuỗi '[Khung Bản thể học] : <Nghĩa bóng Gloss>' qua mô hình đa ngôn ngữ LaBSE.
    - Kết hợp điểm ngữ nghĩa liên tục S_LaBSE và điểm cấu trúc khung S_onto.
    - Tự động lọc bỏ các câu trùng khung giả (False Positives) và cứu các câu đồng nghĩa lệch khung (False Negatives).
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/LaBSE",
        csv_path: Path = CSV_PATH,
        alpha: float = 0.65,
        exact_threshold: float = 0.80,
        near_threshold: float = 0.68,
        semantic_floor: float = 0.62,
    ):
        self.model_name = model_name
        self.csv_path = Path(csv_path)
        self.alpha = alpha
        self.exact_threshold = exact_threshold
        self.near_threshold = near_threshold
        self.semantic_floor = semantic_floor

        self.model = None
        self.df = pd.read_csv(self.csv_path).fillna("")
        self.records: List[Dict[str, Any]] = []
        self.embeddings_cache: Dict[str, Dict[str, np.ndarray]] = {}
        self.criteria_embeddings: Dict[str, Dict[str, Any]] = {}

        self._load_records()

    def _ensure_model(self):
        """Khởi tạo mô hình LaBSE (Lazy loading)."""
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            print(f"🔄 Đang tải mô hình đa ngôn ngữ: {self.model_name} ...")
            self.model = SentenceTransformer(self.model_name)
            print(f"✅ Đã tải xong mô hình {self.model_name}!")

    def _load_records(self):
        """
        Đọc dữ liệu 100 cặp thành ngữ, 4 trục tiêu chí Khung và nghĩa Gloss.
        Kết hợp đồng bộ từ file CSV chuẩn (thanh_ngu_tuc_ngu_100_cau_v4.csv)
        và thuộc tính rdfs:comment (@vi, @en) trong file RDF Ontology (v-idiomV5_final.rdf).
        """
        rdf_comments_vi = {}
        rdf_comments_en = {}
        if RDF_PATH.exists():
            try:
                from owlready2 import World
                BASE_IRI = "http://www.semanticweb.org/phandangvu/ontologies/2026/8/v-idiomv2#"
                w = World()
                onto = w.get_ontology(str(RDF_PATH)).load()
                vn_cls = w[BASE_IRI + "Vietnamese_idiom"]
                en_cls = w[BASE_IRI + "English_Idiom"]
                if vn_cls:
                    for inst in vn_cls.instances():
                        if inst.comment:
                            rdf_comments_vi[inst.name] = str(inst.comment[0]).strip()
                if en_cls:
                    for inst in en_cls.instances():
                        if inst.comment:
                            rdf_comments_en[inst.name] = str(inst.comment[0]).strip()
            except Exception as e:
                print(f"⚠️ Cảnh báo đọc RDF comment: {e}")

        self.df = pd.read_csv(self.csv_path).fillna("")
        self.records = []
        for _, row in self.df.iterrows():
            stt = int(row["STT"]) if str(row["STT"]).strip().isdigit() else len(self.records) + 1
            bc = str(row["Bối_cảnh"]).strip()
            hd = str(row["Hành_động"]).strip()
            kq = str(row["Kết_quả"]).strip()
            md = str(row["Mục_đích"]).strip()
            vi_name = str(row["Thành_ngữ_Tiếng_Việt"]).strip()
            en_name = str(row["Thành_ngữ_Tiếng_Anh"]).strip()

            # Ưu tiên lấy nghĩa Gloss từ rdfs:comment trong RDF Ontology, đối chiếu với cột Giải_thích trong CSV
            vi_gloss = rdf_comments_vi.get(vi_name) or str(row["Giải_thích_nghĩa_Tiếng_Việt"]).strip()
            en_gloss = rdf_comments_en.get(en_name) or str(row["Giải_thích_nghĩa_Tiếng_Anh"]).strip()

            self.records.append({
                "stt": stt,
                "vi_name": vi_name,
                "en_name": en_name,
                "vi_display": vi_name.replace("_", " "),
                "en_display": en_name.replace("_", " "),
                "bc": bc,
                "hd": hd,
                "kq": kq,
                "md": md,
                "frame_key": f"{bc}|{hd}|{kq}|{md}",
                "vi_gloss": vi_gloss,
                "en_gloss": en_gloss,
            })

    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """Mã hóa danh sách chuỗi thành ma trận vector chuẩn hóa L2 (Cosine = Dot Product)."""
        self._ensure_model()
        vecs = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vecs

    def get_corpus_embeddings(self, mode: str = "frame_and_gloss", force_recompute: bool = False) -> Dict[str, np.ndarray]:
        """
        Trả về bộ vector đã mã hóa cho toàn bộ 100 cặp thành ngữ (Tiếng Việt & Tiếng Anh)
        theo chế độ ghép chuỗi `mode`. Có lưu cache ra đĩa để tăng tốc.
        """
        if mode in self.embeddings_cache and not force_recompute:
            return self.embeddings_cache[mode]

        cache_file = DATA_DIR / f"labse_vectors_{mode}.npz"
        if cache_file.exists() and not force_recompute:
            data = np.load(cache_file)
            if len(data["vi_vecs"]) == len(self.records):
                self.embeddings_cache[mode] = {
                    "vi_vecs": data["vi_vecs"],
                    "en_vecs": data["en_vecs"],
                }
                return self.embeddings_cache[mode]

        vi_texts = [
            build_labse_input(
                idiom_surface=r["vi_name"],
                gloss=r["vi_gloss"],
                bc=r["bc"], hd=r["hd"], kq=r["kq"], md=r["md"],
                lang="vi", mode=mode
            )
            for r in self.records
        ]
        en_texts = [
            build_labse_input(
                idiom_surface=r["en_name"],
                gloss=r["en_gloss"],
                bc=r["bc"], hd=r["hd"], kq=r["kq"], md=r["md"],
                lang="en", mode=mode
            )
            for r in self.records
        ]

        vi_vecs = self.encode_texts(vi_texts)
        en_vecs = self.encode_texts(en_texts)

        np.savez_compressed(cache_file, vi_vecs=vi_vecs, en_vecs=en_vecs)
        self.embeddings_cache[mode] = {"vi_vecs": vi_vecs, "en_vecs": en_vecs}
        return self.embeddings_cache[mode]

    def predict_criteria_zero_shot(
        self,
        gloss_text: str,
        threshold: float = 0.42
    ) -> Dict[str, Any]:
        """
        Dùng chính mô hình LaBSE để tự động gợi ý bộ 4 tiêu chí từ Bể tiêu chí
        dựa trên độ tương đồng ngữ nghĩa giữa câu giải nghĩa và định nghĩa từng tiêu chí.
        """
        if not self.criteria_embeddings:
            for axis_name, items in CRITERIA_CATALOG.items():
                codes = list(items.keys())
                descs = [
                    f"{meta['label_vi']}: {meta['desc_vi']} ({meta['label_en']}: {meta['desc_en']})"
                    for meta in items.values()
                ]
                vecs = self.encode_texts(descs)
                self.criteria_embeddings[axis_name] = {
                    "codes": codes,
                    "vecs": vecs,
                }

        q_vec = self.encode_texts([gloss_text])[0]
        axis_map = {
            "Bối_cảnh": "bc",
            "Hành_động": "hd",
            "Kết_quả": "kq",
            "Mục_đích": "md",
        }

        best_per_axis = {}
        for axis_name, short_key in axis_map.items():
            c_info = self.criteria_embeddings[axis_name]
            sims = np.dot(c_info["vecs"], q_vec)
            best_idx = int(np.argmax(sims))
            best_per_axis[short_key] = {
                "code": c_info["codes"][best_idx],
                "score": float(sims[best_idx]),
            }

        # Áp dụng nguyên tắc v4: Chọn các trục >= threshold, nhưng đảm bảo tối thiểu 2 tiêu chí cao điểm nhất
        selected = {k: (v["code"] if v["score"] >= threshold else "") for k, v in best_per_axis.items()}
        non_empty = [k for k, val in selected.items() if val]
        if len(non_empty) < 2:
            sorted_axes = sorted(best_per_axis.keys(), key=lambda k: best_per_axis[k]["score"], reverse=True)
            for k in sorted_axes[:2]:
                selected[k] = best_per_axis[k]["code"]

        return {
            "predicted_frame": selected,
            "axis_scores": best_per_axis,
        }

    def match_idiom(
        self,
        idiom_surface: str,
        gloss_vi: str = "",
        gloss_en: str = "",
        bc: str = "",
        hd: str = "",
        kq: str = "",
        md: str = "",
        lang: str = "vi",
        mode: str = "frame_and_gloss",
        top_k: int = 10,
    ) -> Dict[str, Any]:
        """
        Thực hiện quy trình Đối soát Lai ghép (LaBSE + Bản thể học):
        1. Nếu chưa có tiêu chí, tự động dùng LaBSE Zero-Shot gợi ý từ Bể tiêu chí.
        2. Ghép chuỗi '[Khung Bản thể học] : <Nghĩa bóng Gloss>'.
        3. Mã hóa bằng LaBSE lấy vector 768 chiều.
        4. Tính điểm S_LaBSE, S_onto và điểm tổng hợp S_hybrid.
        5. Phân loại theo ngưỡng: Đồng nghĩa tuyệt đối (>= 0.80) và Đồng nghĩa mềm (0.68 - 0.80).
        """
        active_gloss = gloss_vi if (lang == "vi" and gloss_vi) else (gloss_en or gloss_vi or idiom_surface)

        # Tự động gán tiêu chí bằng LaBSE nếu người dùng chưa truyền đủ tối thiểu 2 tiêu chí
        provided_criteria = [x for x in [bc, hd, kq, md] if x and str(x).strip()]
        auto_predicted = False
        if len(provided_criteria) < 2:
            pred = self.predict_criteria_zero_shot(active_gloss)
            p_frame = pred["predicted_frame"]
            bc = bc or p_frame["bc"]
            hd = hd or p_frame["hd"]
            kq = kq or p_frame["kq"]
            md = md or p_frame["md"]
            auto_predicted = True

        query_frame = {"bc": bc, "hd": hd, "kq": kq, "md": md}
        labse_input_str = build_labse_input(
            idiom_surface=idiom_surface,
            gloss=active_gloss,
            bc=bc, hd=hd, kq=kq, md=md,
            lang=lang, mode=mode,
        )

        # Mã hóa chuỗi đầu vào bằng LaBSE (cả bản Khung+Gloss và bản Gloss thuần để kiểm tra sàn ngữ nghĩa)
        gloss_only_str = build_labse_input(
            idiom_surface=idiom_surface,
            gloss=active_gloss,
            bc=bc, hd=hd, kq=kq, md=md,
            lang=lang, mode="gloss_only",
        )
        encoded_pair = self.encode_texts([labse_input_str, gloss_only_str])
        q_vec = encoded_pair[0]
        q_gloss_vec = encoded_pair[1]

        # Lấy ma trận vector của toàn bộ kho dữ liệu (đã cache sẵn)
        corpus = self.get_corpus_embeddings(mode=mode)
        corpus_gloss = self.get_corpus_embeddings(mode="gloss_only")

        sims_vi = np.dot(corpus["vi_vecs"], q_vec)
        sims_en = np.dot(corpus["en_vecs"], q_vec)

        sims_gloss_vi = np.dot(corpus_gloss["vi_vecs"], q_gloss_vec)
        sims_gloss_en = np.dot(corpus_gloss["en_vecs"], q_gloss_vec)

        exact_synonyms = []
        near_synonyms = []
        filtered_false_positives = []
        all_candidates = []

        norm_input_name = idiom_surface.strip().lower().replace(" ", "_")

        for idx, rec in enumerate(self.records):
            # Bỏ qua chính câu đó nếu trùng tên hoàn toàn
            if norm_input_name in [rec["vi_name"].lower(), rec["en_name"].lower()]:
                continue

            # Điểm LaBSE trên chuỗi [Khung + Gloss]
            s_labse_vi = float(sims_vi[idx])
            s_labse_en = float(sims_en[idx])
            s_labse = max(s_labse_vi, s_labse_en)

            # Điểm LaBSE trên Nghĩa Gloss thuần (dùng làm Bộ lọc Sàn Ngữ Nghĩa chống trùng khung giả)
            s_gloss_pure = max(float(sims_gloss_vi[idx]), float(sims_gloss_en[idx]))

            # Điểm cấu trúc Khung Bản thể học
            cand_frame = {"bc": rec["bc"], "hd": rec["hd"], "kq": rec["kq"], "md": rec["md"]}
            s_onto, onto_meta = compute_ontology_similarity(query_frame, cand_frame)

            # Tính điểm Lai ghép S_hybrid
            if onto_meta["veto"]:
                # Bị phủ quyết do ngược Kết quả hoặc khác hoàn toàn cơ chế Nhân-Quả
                s_hybrid = 0.45 * s_labse
            else:
                s_hybrid = self.alpha * s_labse + (1.0 - self.alpha) * s_onto

            item_result = {
                "stt": rec["stt"],
                "vi_idiom": rec["vi_display"],
                "en_idiom": rec["en_display"],
                "frame": cand_frame,
                "vi_gloss": rec["vi_gloss"],
                "en_gloss": rec["en_gloss"],
                "s_labse": round(s_labse, 4),
                "s_gloss_pure": round(s_gloss_pure, 4),
                "s_labse_vi": round(s_labse_vi, 4),
                "s_labse_en": round(s_labse_en, 4),
                "s_onto": round(s_onto, 4),
                "s_hybrid": round(s_hybrid, 4),
                "onto_match_type": onto_meta["match_type"],
            }

            # Kiểm tra hiện tượng "Trùng Khung Giả" (Ontology = 1.0 nhưng nghĩa Gloss thuần < semantic_floor)
            if s_onto == 1.0 and s_gloss_pure < self.semantic_floor:
                item_result["status"] = "LOẠI_BỎ_TRÙNG_KHUNG_GIẢ"
                filtered_false_positives.append(item_result)
                all_candidates.append(item_result)
                continue

            # Phân tầng theo Ngưỡng (Threshold)
            if s_hybrid >= self.exact_threshold and s_gloss_pure >= self.semantic_floor and not onto_meta["veto"]:
                item_result["status"] = "ĐỒNG_NGHĨA_TUYỆT_ĐỐI"
                exact_synonyms.append(item_result)
            elif s_hybrid >= self.near_threshold and s_gloss_pure >= 0.48 and not onto_meta["veto"]:
                item_result["status"] = "ĐỒNG_NGHĨA_MỀM_CẬN_NGHĨA"
                near_synonyms.append(item_result)
            else:
                item_result["status"] = "KHÔNG_ĐỒNG_NGHĨA"

            all_candidates.append(item_result)

        exact_synonyms.sort(key=lambda x: x["s_hybrid"], reverse=True)
        near_synonyms.sort(key=lambda x: x["s_hybrid"], reverse=True)
        all_candidates.sort(key=lambda x: x["s_hybrid"], reverse=True)

        # Kiểm tra xem Khung 4 trục đã tồn tại trong CSDL chưa
        q_frame_key = f"{bc}|{hd}|{kq}|{md}"
        existing_frame_stts = [r["stt"] for r in self.records if r["frame_key"] == q_frame_key]
        frame_status = "KHUNG_ĐÃ_TỒN_TẠI" if existing_frame_stts else "KHUNG_MỚI"

        return {
            "input_idiom": idiom_surface,
            "encoded_string_for_labse": labse_input_str,
            "auto_predicted_criteria": auto_predicted,
            "frame_status": frame_status,
            "matched_frame_stts": existing_frame_stts,
            "query_frame": query_frame,
            "thresholds": {
                "alpha_labse_weight": self.alpha,
                "ontology_weight": round(1.0 - self.alpha, 2),
                "exact_synonym_threshold": self.exact_threshold,
                "near_synonym_threshold": self.near_threshold,
                "semantic_floor": self.semantic_floor,
            },
            "exact_synonyms": exact_synonyms[:top_k],
            "near_synonyms": near_synonyms[:top_k],
            "filtered_false_positives": filtered_false_positives,
            "top_candidates": all_candidates[:top_k],
        }
