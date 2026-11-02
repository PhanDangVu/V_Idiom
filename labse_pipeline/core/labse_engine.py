import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from .text_builder import (
    CRITERIA_CATALOG,
    FLAT_CRITERIA,
    build_labse_input,
    build_frame_prefix,
)
from .ontology_scorer import compute_ontology_similarity, is_related_criterion, get_criteria_similarity

DATA_DIR = Path(__file__).parent.parent / "data"
CSV_PATH = DATA_DIR / "200_idioms-v5.csv"
RDF_PATH = DATA_DIR / "v-idiomV6.rdf"
PROTEGE_RDF_PATH = Path(__file__).resolve().parent.parent.parent / "ontology_protege" / "v-idiomV6.rdf"


def sanitize_iri_name(name: str) -> str:
    """Chuẩn hóa chuỗi thành ngữ sang định danh IRI hợp lệ trong OWL/RDF."""
    s = str(name or "").strip()
    for ch in [",", "'", "’", "?", "!", '"', ";", ":"]:
        s = s.replace(ch, "")
    return "_".join(s.split())


class LaBSEOntologyEngine:
    """
    Hệ thống Lai ghép Neuro-Symbolic (LaBSE + Bản thể học OWL 2 v6):
    - Biểu diễn và truy vấn TỪNG CÂU THÀNH NGỮ ĐỘC LẬP (200 câu Tiếng Việt + 182 câu Tiếng Anh = 382 cá thể trong v-idiomV6.rdf).
    - Mã hóa chuỗi '[Khung Bản thể học] : <Nghĩa bóng Gloss>' qua mô hình đa ngôn ngữ LaBSE.
    - Áp dụng bộ lọc sàn ngữ nghĩa S_Gloss >= 0.60 đúng theo Flowchart để chặn trùng khung giả.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/LaBSE",
        csv_path: Path = CSV_PATH,
        alpha: float = 0.65,
        exact_threshold: float = 0.80,
        near_threshold: float = 0.62,
        semantic_floor: float = 0.60,
        s_onto_near_threshold: float = 0.50,
    ):
        self.model_name = model_name
        self.is_bge_m3 = "bge-m3" in model_name.lower()
        self.cache_prefix = "bge_m3" if self.is_bge_m3 else "labse"
        self.csv_path = Path(csv_path)
        self.alpha = alpha
        self.exact_threshold = exact_threshold
        self.near_threshold = near_threshold
        self.semantic_floor = semantic_floor
        self.s_onto_near_threshold = s_onto_near_threshold

        self.model = None
        self.df = pd.read_csv(self.csv_path, encoding="utf-8-sig").fillna("")
        # Danh sách từng câu thành ngữ độc lập (Vietnamese_idiom & English_Idiom)
        self.records: List[Dict[str, Any]] = []
        self.frame_map: Dict[str, str] = {}
        self.embeddings_cache: Dict[str, np.ndarray] = {}
        self.criteria_embeddings: Dict[str, Dict[str, Any]] = {}

        self._load_records()

    def _ensure_model(self):
        """Khởi tạo mô hình LaBSE."""
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            print(f"🔄 Đang tải mô hình đa ngôn ngữ: {self.model_name} ...")
            self.model = SentenceTransformer(self.model_name)
            print(f"✅ Đã tải xong mô hình {self.model_name}!")

    def _load_records(self):
        """
        Đọc dữ liệu từ 200_idioms-v5.csv và v-idiomV6.rdf, tách thành TỪNG CÂU THÀNH NGỮ ĐỘC LẬP
        (mỗi câu Tiếng Việt là 1 cá thể Vietnamese_idiom, mỗi câu Tiếng Anh là 1 cá thể English_Idiom)
        đúng theo cấu trúc Bản thể học v-idiomV6.rdf.
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

        self.df = pd.read_csv(self.csv_path, encoding="utf-8-sig").fillna("")
        self.records = []
        self.frame_map = {}
        seen_individuals = set()

        for idx, row in self.df.iterrows():
            row_num = idx + 1
            bc = str(row.get("Bối cảnh", row.get("Bối_cảnh", ""))).strip()
            hd = str(row.get("Hành động", row.get("Hành_động", ""))).strip()
            kq = str(row.get("Kết quả", row.get("Kết_quả", ""))).strip()
            md = str(row.get("Mục đích", row.get("Mục_đích", ""))).strip()

            frame_key = f"{bc}|{hd}|{kq}|{md}"
            if frame_key not in self.frame_map:
                self.frame_map[frame_key] = f"Khung{len(self.frame_map) + 1}"
            frame_name = self.frame_map[frame_key]

            vi_raw = str(row.get("Thành Ngữ Việt Nam", row.get("Thành_ngữ_Tiếng_Việt", ""))).strip()
            en_raw = str(row.get("Thành ngữ Tiếng Anh", row.get("Thành_ngữ_Tiếng_Anh", ""))).strip()

            csv_vi_gloss = str(row.get("Giải nghĩa tiếng Việt", row.get("Giải_thích_nghĩa_Tiếng_Việt", ""))).strip()
            csv_en_gloss = str(row.get("giải nghĩa tiếng Anh", row.get("Giải_thích_nghĩa_Tiếng_Anh", ""))).strip()

            # 1. Thêm cá thể Thành ngữ Tiếng Việt (Vietnamese_idiom)
            if vi_raw:
                vi_iri = sanitize_iri_name(vi_raw)
                if ("vi", vi_iri, frame_key) not in seen_individuals:
                    seen_individuals.add(("vi", vi_iri, frame_key))
                    vi_gloss = csv_vi_gloss or rdf_comments_vi.get(vi_iri, "")
                    self.records.append({
                        "stt": len(self.records) + 1,
                        "row_id": row_num,
                        "lang": "vi",
                        "idiom": vi_raw.replace("_", " "),
                        "iri_name": vi_iri,
                        "gloss": vi_gloss,
                        "frame_name": frame_name,
                        "bc": bc,
                        "hd": hd,
                        "kq": kq,
                        "md": md,
                        "frame_key": frame_key,
                    })

            # 2. Thêm cá thể Thành ngữ Tiếng Anh (English_Idiom)
            if en_raw:
                en_iri = sanitize_iri_name(en_raw)
                if ("en", en_iri, frame_key) not in seen_individuals:
                    seen_individuals.add(("en", en_iri, frame_key))
                    en_gloss = csv_en_gloss or rdf_comments_en.get(en_iri, "")
                    self.records.append({
                        "stt": len(self.records) + 1,
                        "row_id": row_num,
                        "lang": "en",
                        "idiom": en_raw.replace("_", " "),
                        "iri_name": en_iri,
                        "gloss": en_gloss,
                        "frame_name": frame_name,
                        "bc": bc,
                        "hd": hd,
                        "kq": kq,
                        "md": md,
                        "frame_key": frame_key,
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

    def get_corpus_embeddings(self, mode: str = "frame_and_gloss", force_recompute: bool = False) -> np.ndarray:
        """
        Trả về ma trận vector (N, 768) cho toàn bộ các câu thành ngữ độc lập (382 câu: 200 VI + 182 EN)
        theo chế độ ghép chuỗi `mode`. Có lưu cache ra đĩa (.npz) để tăng tốc.
        """
        if mode in self.embeddings_cache and not force_recompute:
            return self.embeddings_cache[mode]

        cache_file = DATA_DIR / f"{self.cache_prefix}_single_vectors_{mode}.npz"
        if cache_file.exists() and not force_recompute:
            data = np.load(cache_file)
            if "vecs" in data and len(data["vecs"]) == len(self.records):
                self.embeddings_cache[mode] = data["vecs"]
                return self.embeddings_cache[mode]

        texts = [
            build_labse_input(
                idiom_surface=r["idiom"],
                gloss=r["gloss"],
                bc=r["bc"],
                hd=r["hd"],
                kq=r["kq"],
                md=r["md"],
                lang=r["lang"],
                mode=mode,
            )
            for r in self.records
        ]

        vecs = self.encode_texts(texts)
        np.savez_compressed(cache_file, vecs=vecs)
        self.embeddings_cache[mode] = vecs
        return self.embeddings_cache[mode]

    def predict_criteria_zero_shot(
        self,
        gloss_text: str,
        threshold: float = 0.42
    ) -> Dict[str, Any]:
        """Dùng LaBSE tự động gợi ý bộ 4 tiêu chí từ Bể tiêu chí v5 (236 mã)."""
        if not self.criteria_embeddings:
            crit_vec_path = DATA_DIR / f"{self.cache_prefix}_criteria_vectors.npz"
            if crit_vec_path.exists():
                data = np.load(crit_vec_path)
                c_codes = list(data["codes"])
                c_axes = list(data["axes"])
                c_vecs = data["vecs"]
                for axis_name in CRITERIA_CATALOG.keys():
                    indices = [i for i, a in enumerate(c_axes) if a == axis_name]
                    if indices:
                        self.criteria_embeddings[axis_name] = {
                            "codes": [c_codes[i] for i in indices],
                            "vecs": c_vecs[indices],
                        }
            else:
                for axis_name, items in CRITERIA_CATALOG.items():
                    codes = list(items.keys())
                    descs = [
                        f"{meta['label_vi']}: {meta['desc_vi']} ({meta['label_en']})"
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

    def lookup_ontology_record(self, idiom_input: str) -> Optional[Dict[str, Any]]:
        """
        Tra cứu xem câu thành ngữ nhập vào đã tồn tại sẵn trong Ontology (v-idiomV6.rdf) hay chưa.
        Nếu có sẵn, trả về chính xác bản ghi (gồm description rdfs:comment và 4 trục tiêu chí của nó trong Ontology)
        để hệ thống dùng trực tiếp chứ không gọi LLM tự suy luận lại.
        """
        if not idiom_input or not str(idiom_input).strip():
            return None
        q_raw = str(idiom_input).strip().lower()
        q_iri = sanitize_iri_name(idiom_input).lower()
        # Hỗ trợ biến thể phổ biến có/không có từ 'always'
        q_alt = q_raw.replace(" always ", " ")

        for rec in self.records:
            r_disp = rec["idiom"].lower()
            r_iri = rec["iri_name"].lower()
            if q_raw == r_disp or q_iri == r_iri or q_alt == r_disp:
                # Tìm câu đồng nghĩa cùng khung (nếu có) chỉ để hiển thị tham khảo tên câu tương đương
                siblings = [
                    s["idiom"]
                    for s in self.records
                    if s["frame_key"] == rec["frame_key"] and s["iri_name"] != rec["iri_name"]
                ]
                return {
                    **rec,
                    "siblings": siblings,
                }
        return None

    def _compare_frame_axes(self, q_frame: Dict[str, str], c_frame: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        """So sánh chi tiết từng trục (BC, HD, KQ, MD) giữa Khung truy vấn và Khung ứng viên."""
        axis_details = {}
        m_type = "bge_m3" if self.is_bge_m3 else "labse"
        for ax in ["bc", "hd", "kq", "md"]:
            qv = (q_frame.get(ax) or "").strip()
            cv = (c_frame.get(ax) or "").strip()
            if not qv and not cv:
                status = "BOTH_EMPTY"
            elif qv and cv and qv == cv:
                status = "EXACT_MATCH"
            elif qv and cv and is_related_criterion(qv, cv, model_type=m_type):
                sim = get_criteria_similarity(qv, cv, model_type=m_type)
                status = f"NEAR_MATCH ({sim:.2f})"
            else:
                status = "MISMATCH"
            axis_details[ax] = {"query": qv, "candidate": cv, "status": status}
        return axis_details

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
        top_k: int = 12,
    ) -> Dict[str, Any]:
        """
        Đối soát Lai ghép (LaBSE + Bản thể học v6) trên TỪNG CÂU THÀNH NGỮ ĐỘC LẬP:
        - Sàn ngữ nghĩa bắt buộc: S_Gloss >= 0.60 (chặn trùng khung giả).
        - Công thức kết hợp: S_hybrid = 0.65 * S_LaBSE + 0.35 * S_onto.
        - Phân 3 nhánh đúng theo Flowchart:
          1. ĐỒNG NGHĨA TUYỆT ĐỐI (S_hybrid >= 0.80 và S_Gloss >= 0.60)
          2. ĐỒNG NGHĨA MỀM / CẬN NGHĨA (0.65 <= S_hybrid < 0.80 và S_Gloss >= 0.60)
          3. KHÁC NGHĨA / LOẠI BỎ TRÙNG KHUNG GIẢ (S_Gloss < 0.60 hoặc S_hybrid < 0.65)
        """
        has_vi = bool(gloss_vi and str(gloss_vi).strip())
        has_en = bool(gloss_en and str(gloss_en).strip())
        primary_lang = "en" if (has_en and not has_vi) else ("vi" if has_vi else lang)
        primary_gloss = (gloss_vi if primary_lang == "vi" else gloss_en) or gloss_vi or gloss_en or idiom_surface
        primary_gloss = str(primary_gloss).strip()

        provided_criteria = [x for x in [bc, hd, kq, md] if x and str(x).strip()]
        auto_predicted = False
        if len(provided_criteria) < 2:
            pred = self.predict_criteria_zero_shot(primary_gloss)
            p_frame = pred["predicted_frame"]
            bc = bc or p_frame["bc"]
            hd = hd or p_frame["hd"]
            kq = kq or p_frame["kq"]
            md = md or p_frame["md"]
            auto_predicted = True

        query_frame = {"bc": bc, "hd": hd, "kq": kq, "md": md}

        # Chuỗi biểu diễn theo đúng ngôn ngữ có mặt (không ghép lẫn khung Anh với gloss Việt hoặc ngược lại)
        str_fg_primary = build_labse_input(idiom_surface, primary_gloss, bc, hd, kq, md, lang=primary_lang, mode="frame_and_gloss")
        str_gloss_primary = build_labse_input(idiom_surface, primary_gloss, bc, hd, kq, md, lang=primary_lang, mode="gloss_only")
        str_rf_primary = build_labse_input(idiom_surface, primary_gloss, bc, hd, kq, md, lang=primary_lang, mode="raw_and_frame")
        str_raw_primary = build_labse_input(idiom_surface, primary_gloss, bc, hd, kq, md, lang=primary_lang, mode="raw_only")

        if has_vi and has_en:
            str_fg_vi = build_labse_input(idiom_surface, str(gloss_vi).strip(), bc, hd, kq, md, lang="vi", mode="frame_and_gloss")
            str_fg_en = build_labse_input(idiom_surface, str(gloss_en).strip(), bc, hd, kq, md, lang="en", mode="frame_and_gloss")
            str_gloss_vi = build_labse_input(idiom_surface, str(gloss_vi).strip(), bc, hd, kq, md, lang="vi", mode="gloss_only")
            str_gloss_en = build_labse_input(idiom_surface, str(gloss_en).strip(), bc, hd, kq, md, lang="en", mode="gloss_only")
        else:
            str_fg_vi = str_fg_primary
            str_fg_en = str_fg_primary
            str_gloss_vi = str_gloss_primary
            str_gloss_en = str_gloss_primary

        q_vecs = self.encode_texts([str_fg_vi, str_fg_en, str_gloss_vi, str_gloss_en, str_rf_primary, str_raw_primary])
        q_fg_vi, q_fg_en, q_gloss_vi, q_gloss_en, q_rf_vec, q_raw_vec = (
            q_vecs[0],
            q_vecs[1],
            q_vecs[2],
            q_vecs[3],
            q_vecs[4],
            q_vecs[5],
        )

        corpus_fg = self.get_corpus_embeddings(mode="frame_and_gloss")
        corpus_gloss = self.get_corpus_embeddings(mode="gloss_only")
        corpus_rf = self.get_corpus_embeddings(mode="raw_and_frame")
        corpus_raw = self.get_corpus_embeddings(mode="raw_only")

        sims_fg_vi = np.dot(corpus_fg, q_fg_vi)
        sims_fg_en = np.dot(corpus_fg, q_fg_en)

        sims_gloss_vi = np.dot(corpus_gloss, q_gloss_vi)
        sims_gloss_en = np.dot(corpus_gloss, q_gloss_en)

        sims_rf = np.dot(corpus_rf, q_rf_vec)
        sims_raw = np.dot(corpus_raw, q_raw_vec)

        exact_synonyms = []
        near_synonyms = []
        filtered_false_positives = []
        all_candidates = []

        norm_input_iri = sanitize_iri_name(idiom_surface).lower()
        norm_input_disp = idiom_surface.strip().lower()

        for idx, rec in enumerate(self.records):
            # Không tự so sánh câu nhập tiếng Việt/Anh với chính bản thân nó trong kho
            if norm_input_iri == rec["iri_name"].lower() or norm_input_disp == rec["idiom"].lower():
                continue

            cand_frame = {"bc": rec["bc"], "hd": rec["hd"], "kq": rec["kq"], "md": rec["md"]}
            m_type = "bge_m3" if self.is_bge_m3 else "labse"
            s_onto, onto_meta = compute_ontology_similarity(query_frame, cand_frame, model_type=m_type)
            axis_comparison = self._compare_frame_axes(query_frame, cand_frame)

            # Nếu Khung Bản thể học trùng khớp hoàn toàn 100% (s_onto == 1.0):
            # -> Kết luận ĐỒNG NGHĨA CỨNG / ĐỒNG NGHĨA TUYỆT ĐỐI ngay lập tức, không cần tính toán LaBSE nữa
            if s_onto == 1.0 and onto_meta["match_type"] == "TRÙNG_KHUNG_TUYỆT_ĐỐI":
                item_result = {
                    "stt": rec["stt"],
                    "row_id": rec["row_id"],
                    "lang": rec["lang"],
                    "idiom": rec["idiom"],
                    "iri_name": rec["iri_name"],
                    "frame_name": rec["frame_name"],
                    "frame": cand_frame,
                    "axis_comparison": axis_comparison,
                    "gloss": rec["gloss"],
                    "hard_onto_match": True,
                    "s_raw_only": None,
                    "s_raw_frame": None,
                    "s_gloss_pure": None,
                    "s_labse": None,
                    "s_onto": 1.0,
                    "s_hybrid": 1.0,
                    "onto_match_type": "TRÙNG_KHUNG_TUYỆT_ĐỐI (Đồng nghĩa cứng — Không cần tính LaBSE)",
                    "status": "ĐỒNG_NGHĨA_TUYỆT_ĐỐI",
                }
                exact_synonyms.append(item_result)
                all_candidates.append(item_result)
                continue

            # Chỉ khi Khung KHÔNG trùng hoàn toàn (s_onto < 1.0) mới tính toán khoảng cách LaBSE
            s_labse = max(float(sims_fg_vi[idx]), float(sims_fg_en[idx]))
            s_gloss_pure = max(float(sims_gloss_vi[idx]), float(sims_gloss_en[idx]))
            s_raw_frame = float(sims_rf[idx])
            s_raw_only = float(sims_raw[idx])

            if onto_meta["veto"]:
                s_hybrid = 0.45 * s_labse
            else:
                s_hybrid = self.alpha * s_labse + (1.0 - self.alpha) * s_onto

            item_result = {
                "stt": rec["stt"],
                "row_id": rec["row_id"],
                "lang": rec["lang"],
                "idiom": rec["idiom"],
                "iri_name": rec["iri_name"],
                "frame_name": rec["frame_name"],
                "frame": cand_frame,
                "axis_comparison": axis_comparison,
                "gloss": rec["gloss"],
                "hard_onto_match": False,
                "s_raw_only": round(s_raw_only, 4),
                "s_raw_frame": round(s_raw_frame, 4),
                "s_gloss_pure": round(s_gloss_pure, 4),
                "s_labse": round(s_labse, 4),
                "s_onto": round(s_onto, 4),
                "s_hybrid": round(s_hybrid, 4),
                "onto_match_type": onto_meta["match_type"],
            }

            # 1. Bộ lọc sàn ngữ nghĩa S_Gloss >= 0.60 khi S_hybrid >= 0.80 nhưng S_Gloss < 0.60
            if s_hybrid >= self.exact_threshold and s_gloss_pure < self.semantic_floor:
                item_result["status"] = "LOẠI_BỎ_TRÙNG_KHUNG_GIẢ"
                filtered_false_positives.append(item_result)
                all_candidates.append(item_result)
                continue

            # 2. Phân tầng theo Ngưỡng:
            # - Nhánh 1 (Đồng nghĩa tuyệt đối): S_hybrid >= 0.80 & S_onto >= 0.75 & S_Gloss >= 0.60
            # - Nhánh 2 (Đồng nghĩa mềm / Cận nghĩa): S_hybrid >= 0.62 & S_onto >= 0.50 & S_Gloss >= 0.60
            if s_hybrid >= self.exact_threshold and s_onto >= 0.75 and s_gloss_pure >= self.semantic_floor and not onto_meta["veto"]:
                item_result["status"] = "ĐỒNG_NGHĨA_TUYỆT_ĐỐI"
                exact_synonyms.append(item_result)
            elif s_hybrid >= self.near_threshold and s_onto >= self.s_onto_near_threshold and s_gloss_pure >= self.semantic_floor and not onto_meta["veto"]:
                item_result["status"] = "ĐỒNG_NGHĨA_MỀM_CẬN_NGHĨA"
                near_synonyms.append(item_result)
            else:
                item_result["status"] = "KHÔNG_ĐỒNG_NGHĨA"

            all_candidates.append(item_result)

        exact_synonyms.sort(key=lambda x: x["s_hybrid"], reverse=True)
        near_synonyms.sort(key=lambda x: x["s_hybrid"], reverse=True)
        filtered_false_positives.sort(key=lambda x: x["s_hybrid"], reverse=True)
        all_candidates.sort(key=lambda x: x["s_hybrid"], reverse=True)

        q_frame_key = f"{bc}|{hd}|{kq}|{md}"
        matched_frame_name = self.frame_map.get(q_frame_key, "")
        frame_status = "KHUNG_ĐÃ_TỒN_TẠI" if matched_frame_name else "KHUNG_MỚI"

        return {
            "input_idiom": idiom_surface,
            "encoded_string_for_labse": str_fg_primary,
            "encoded_gloss_only_for_labse": str_gloss_primary,
            "encoded_raw_and_frame": str_rf_primary,
            "auto_predicted_criteria": auto_predicted,
            "frame_status": frame_status,
            "matched_frame_name": matched_frame_name,
            "query_frame": query_frame,
            "thresholds": {
                "alpha_labse_weight": self.alpha,
                "ontology_weight": round(1.0 - self.alpha, 2),
                "exact_synonym_threshold": self.exact_threshold,
                "near_synonym_threshold": self.near_threshold,
                "s_onto_near_threshold": self.s_onto_near_threshold,
                "semantic_floor": self.semantic_floor,
            },
            "exact_synonyms": exact_synonyms[:top_k],
            "near_synonyms": near_synonyms[:top_k],
            "filtered_false_positives": filtered_false_positives[:top_k],
            "top_candidates": all_candidates[:top_k],
        }

    def save_idiom_to_local_store(
        self,
        vi_name: str,
        en_name: str,
        bc: str = "",
        hd: str = "",
        kq: str = "",
        md: str = "",
        vi_gloss: str = "",
        en_gloss: str = "",
    ) -> Dict[str, Any]:
        import csv
        import shutil
        vi_surface = vi_name.strip().replace("_", " ")
        en_surface = en_name.strip().replace("_", " ")
        vi_clean = sanitize_iri_name(vi_surface)
        en_clean = sanitize_iri_name(en_surface)
        bc = (bc or "").strip()
        hd = (hd or "").strip()
        kq = (kq or "").strip()
        md = (md or "").strip()
        vi_gloss = (vi_gloss or "").strip()
        en_gloss = (en_gloss or "").strip()

        with open(self.csv_path, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow([vi_surface, vi_gloss, en_gloss, bc, md, hd, kq, en_surface])

        frame_name = ""
        if RDF_PATH.exists():
            try:
                from owlready2 import World, locstr
                BASE_IRI = "http://www.semanticweb.org/phandangvu/ontologies/2026/8/v-idiomv2#"
                w = World()
                onto = w.get_ontology(str(RDF_PATH)).load()
                Khung_cls = w[BASE_IRI + "Khung_Bản_Thể_học"]
                VN_cls = w[BASE_IRI + "Vietnamese_idiom"]
                EN_cls = w[BASE_IRI + "English_Idiom"]
                BC_cls = w[BASE_IRI + "Bối_cảnh"]
                HD_cls = w[BASE_IRI + "Hành_động"]
                KQ_cls = w[BASE_IRI + "Kết_quả"]
                MD_cls = w[BASE_IRI + "Mục_đích"]

                with onto:
                    bc_inst = (w[BASE_IRI + bc] or BC_cls(bc)) if bc else None
                    hd_inst = (w[BASE_IRI + hd] or HD_cls(hd)) if hd else None
                    kq_inst = (w[BASE_IRI + kq] or KQ_cls(kq)) if kq else None
                    md_inst = (w[BASE_IRI + md] or MD_cls(md)) if md else None

                    target_frame = None
                    for f_inst in Khung_cls.instances():
                        f_bc = f_inst.Có_bối_cảnh[0].name if f_inst.Có_bối_cảnh else ""
                        f_hd = f_inst.Có_hành_động[0].name if f_inst.Có_hành_động else ""
                        f_kq = f_inst.Có_kết_quả[0].name if f_inst.Có_kết_quả else ""
                        f_md = f_inst.Có_mục_đích[0].name if f_inst.Có_mục_đích else ""
                        if (f_bc, f_hd, f_kq, f_md) == (bc, hd, kq, md):
                            target_frame = f_inst
                            break

                    if not target_frame:
                        max_num = 0
                        for f_inst in Khung_cls.instances():
                            digits = "".join(filter(str.isdigit, f_inst.name))
                            if digits:
                                max_num = max(max_num, int(digits))
                        frame_name = f"Khung{max_num + 1}"
                        target_frame = Khung_cls(frame_name)
                        if bc_inst: target_frame.Có_bối_cảnh.append(bc_inst)
                        if hd_inst: target_frame.Có_hành_động.append(hd_inst)
                        if kq_inst: target_frame.Có_kết_quả.append(kq_inst)
                        if md_inst: target_frame.Có_mục_đích.append(md_inst)
                    else:
                        frame_name = target_frame.name

                    if vi_clean:
                        vi_inst = w[BASE_IRI + vi_clean] or VN_cls(vi_clean)
                        if target_frame not in vi_inst.Có_khung:
                            vi_inst.Có_khung.append(target_frame)
                        if vi_gloss:
                            vi_inst.comment = [locstr(vi_gloss, lang="vi")]

                    if en_clean:
                        en_inst = w[BASE_IRI + en_clean] or EN_cls(en_clean)
                        if target_frame not in en_inst.Có_khung:
                            en_inst.Có_khung.append(target_frame)
                        if en_gloss:
                            en_inst.comment = [locstr(en_gloss, lang="en")]

                    onto.save(file=str(RDF_PATH), format="rdfxml")
                    if PROTEGE_RDF_PATH.parent.exists():
                        shutil.copy2(RDF_PATH, PROTEGE_RDF_PATH)
            except Exception as e:
                print(f"⚠️ Cảnh báo lưu RDF: {e}")

        # Tự động cập nhật tiêu chí mới vào Catalog, Vector NPZ và Ma trận khoảng cách
        self._sync_new_criteria_if_any([("Bối_cảnh", bc), ("Hành_động", hd), ("Kết_quả", kq), ("Mục_đích", md)])

        self._load_records()
        self.get_corpus_embeddings(mode="frame_and_gloss", force_recompute=True)
        self.get_corpus_embeddings(mode="gloss_only", force_recompute=True)
        self.get_corpus_embeddings(mode="raw_and_frame", force_recompute=True)
        self.get_corpus_embeddings(mode="raw_only", force_recompute=True)

        return {
            "stt": len(self.records),
            "frame_name": frame_name,
            "total_records": len(self.records),
        }

    def _sync_new_criteria_if_any(self, axis_criterion_pairs: List[Tuple[str, str]]):
        """
        Nếu người dùng hoặc LLM thêm một tiêu chí mới chưa có trong Bể tiêu chí (criteria_catalog.json):
        1. Thêm vào criteria_catalog.json
        2. Sinh vector LaBSE và cập nhật vào labse_criteria_vectors.npz
        3. Tính lại khoảng cách Cosine với các tiêu chí cùng trục và cập nhật vào criteria_similarity_matrix.json
        """
        crit_cat_path = DATA_DIR / "criteria_catalog.json"
        crit_vec_path = DATA_DIR / "labse_criteria_vectors.npz"
        crit_mat_path = DATA_DIR / "criteria_similarity_matrix.json"

        with open(crit_cat_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        new_entries = []
        for axis_name, code in axis_criterion_pairs:
            if not code or str(code).strip() in ["", "null", "none", "nan"]:
                continue
            code = code.strip()
            if axis_name not in catalog:
                catalog[axis_name] = {}
            if code not in catalog[axis_name]:
                # Tiêu chí mới
                clean_lbl = code.split("_", 1)[-1].replace("_", " ")
                catalog[axis_name][code] = {
                    "label_vi": clean_lbl,
                    "label_en": clean_lbl,
                    "desc_vi": f"Tiêu chí bổ sung: {clean_lbl}",
                    "desc_en": f"Supplementary criterion: {clean_lbl}",
                }
                new_entries.append((axis_name, code, catalog[axis_name][code]))

        if not new_entries:
            return  # Không có tiêu chí mới, không cần cập nhật

        # 1. Lưu catalog mới
        with open(crit_cat_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)

        # 2. Cập nhật vector vào labse_criteria_vectors.npz
        if crit_vec_path.exists():
            data = np.load(crit_vec_path)
            c_codes = list(data["codes"])
            c_axes = list(data["axes"])
            c_labels_vi = list(data["labels_vi"])
            c_labels_en = list(data["labels_en"])
            c_vecs = list(data["vecs"])
        else:
            c_codes, c_axes, c_labels_vi, c_labels_en, c_vecs = [], [], [], [], []

        new_texts = [f"{m['label_vi']}: {m['desc_vi']} ({m['label_en']})" for _, _, m in new_entries]
        new_vecs = self.encode_texts(new_texts)

        for i, (ax, cd, m) in enumerate(new_entries):
            c_codes.append(cd)
            c_axes.append(ax)
            c_labels_vi.append(m["label_vi"])
            c_labels_en.append(m["label_en"])
            c_vecs.append(new_vecs[i])

        np.savez_compressed(
            crit_vec_path,
            codes=np.array(c_codes),
            axes=np.array(c_axes),
            labels_vi=np.array(c_labels_vi),
            labels_en=np.array(c_labels_en),
            vecs=np.array(c_vecs),
        )

        # 3. Cập nhật ma trận khoảng cách tương đồng (criteria_similarity_matrix.json)
        sim_map = {}
        if crit_mat_path.exists():
            with open(crit_mat_path, "r", encoding="utf-8") as f:
                sim_map = json.load(f)

        c_axes_arr = np.array(c_axes)
        c_vecs_arr = np.array(c_vecs)

        for i, (ax, cd, _) in enumerate(new_entries):
            v_new = new_vecs[i]
            same_axis_indices = [idx for idx, a in enumerate(c_axes_arr) if a == ax and c_codes[idx] != cd]
            if same_axis_indices:
                other_vecs = c_vecs_arr[same_axis_indices]
                cos_sims = np.dot(other_vecs, v_new)
                for j, score in enumerate(cos_sims):
                    if score >= 0.70:
                        other_code = c_codes[same_axis_indices[j]]
                        sim_map[f"{cd}|{other_code}"] = round(float(score), 4)
                        sim_map[f"{other_code}|{cd}"] = round(float(score), 4)

        with open(crit_mat_path, "w", encoding="utf-8") as f:
            json.dump(sim_map, f, ensure_ascii=False, indent=2)

        # Xóa cache RAM để nạp lại
        self.criteria_embeddings = {}
        print(f"✅ Đã tự động đồng bộ {len(new_entries)} tiêu chí mới vào Catalog, Vector NPZ và Ma trận khoảng cách.")
