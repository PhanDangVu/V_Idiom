import sys
from pathlib import Path
import numpy as np

# Thêm thư mục gốc labse_pipeline vào sys.path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.labse_engine import LaBSEOntologyEngine
from core.text_builder import build_labse_input
from core.ontology_scorer import compute_ontology_similarity


def evaluate_cross_lingual_retrieval(engine: LaBSEOntologyEngine, mode: str) -> dict:
    """
    Đánh giá bài toán Truy xuất Song ngữ (Cross-Lingual Retrieval VI -> EN) trên 100 cặp câu:
    Cho câu Tiếng Việt thứ i, tìm câu Tiếng Anh tương ứng trong 100 câu Tiếng Anh.
    Tính: Recall@1 (Top-1 Acc), Recall@5 (Top-5 Acc), và MRR (Mean Reciprocal Rank).
    """
    corpus = engine.get_corpus_embeddings(mode=mode)
    vi_vecs = corpus["vi_vecs"]  # (100, 768)
    en_vecs = corpus["en_vecs"]  # (100, 768)

    # Ma trận tương đồng Cosine (100 x 100)
    sim_matrix = np.dot(vi_vecs, en_vecs.T)

    n = len(engine.records)
    top1_hits = 0
    top5_hits = 0
    rr_sum = 0.0
    diag_sims = []

    for i in range(n):
        sims = sim_matrix[i]
        diag_sims.append(float(sims[i]))
        # Xếp hạng giảm dần
        ranked_indices = np.argsort(-sims)
        # Lưu ý: một số câu có chung câu tiếng Anh (vd: Diamond_cut_diamond, Spend_money_like_water)
        target_en = engine.records[i]["en_name"]
        matching_targets = {
            idx for idx, r in enumerate(engine.records) if r["en_name"] == target_en
        }

        # Tìm vị trí đầu tiên của câu tiếng Anh đúng trong danh sách xếp hạng
        rank = None
        for r_pos, cand_idx in enumerate(ranked_indices, start=1):
            if cand_idx in matching_targets:
                rank = r_pos
                break

        if rank == 1:
            top1_hits += 1
        if rank is not None and rank <= 5:
            top5_hits += 1
        if rank is not None:
            rr_sum += 1.0 / rank

    return {
        "mode": mode,
        "mean_pair_cosine": round(float(np.mean(diag_sims)), 4),
        "recall_at_1": round(top1_hits / n * 100, 2),
        "recall_at_5": round(top5_hits / n * 100, 2),
        "mrr": round(rr_sum / n * 100, 2),
    }


def evaluate_case_studies(engine: LaBSEOntologyEngine):
    """
    Kiểm chứng trực tiếp các ca điển hình chứng minh sự vượt trội của Hướng 3:
    [Khung Bản thể học + Nghĩa Gloss] kết hợp LaBSE + Ontology.
    """
    print("\n" + "=" * 88)
    print("PHẦN 2: KIỂM CHỨNG CÁC CA ĐIỂN HÌNH (CASE STUDIES TRÊN BỘ 100 CÂU)")
    print("=" * 88)

    corpus_fg = engine.get_corpus_embeddings(mode="frame_and_gloss")
    corpus_gloss = engine.get_corpus_embeddings(mode="gloss_only")
    corpus_rf = engine.get_corpus_embeddings(mode="raw_and_frame")
    corpus_raw = engine.get_corpus_embeddings(mode="raw_only")

    def compare_pair(stt_a: int, stt_b: int, label: str):
        idx_a, idx_b = stt_a - 1, stt_b - 1
        rec_a, rec_b = engine.records[idx_a], engine.records[idx_b]

        sim_raw = float(np.dot(corpus_raw["vi_vecs"][idx_a], corpus_raw["vi_vecs"][idx_b]))
        sim_rf = float(np.dot(corpus_rf["vi_vecs"][idx_a], corpus_rf["vi_vecs"][idx_b]))
        sim_gloss = float(np.dot(corpus_gloss["vi_vecs"][idx_a], corpus_gloss["vi_vecs"][idx_b]))
        sim_fg = float(np.dot(corpus_fg["vi_vecs"][idx_a], corpus_fg["vi_vecs"][idx_b]))

        frame_a = {"bc": rec_a["bc"], "hd": rec_a["hd"], "kq": rec_a["kq"], "md": rec_a["md"]}
        frame_b = {"bc": rec_b["bc"], "hd": rec_b["hd"], "kq": rec_b["kq"], "md": rec_b["md"]}
        s_onto, meta = compute_ontology_similarity(frame_a, frame_b)

        # Áp dụng luật sàn ngữ nghĩa trên Gloss thuần & công thức lai ghép trên [Khung + Gloss]
        if s_onto == 1.0 and sim_gloss < engine.semantic_floor:
            decision = f"❌ LOẠI BỎ (Phát hiện Trùng Khung Giả vì S_Gloss = {sim_gloss:.4f} < {engine.semantic_floor})"
            s_hybrid = engine.alpha * sim_fg + (1 - engine.alpha) * s_onto
        else:
            s_hybrid = engine.alpha * sim_fg + (1 - engine.alpha) * s_onto
            if s_hybrid >= engine.exact_threshold and sim_gloss >= engine.semantic_floor:
                decision = "✅ ĐỒNG NGHĨA TUYỆT ĐỐI (S_hybrid >= 0.80)"
            elif s_hybrid >= engine.near_threshold and sim_gloss >= 0.42:
                decision = "🟢 ĐỒNG NGHĨA MỀM / CẬN NGHĨA (0.68 <= S_hybrid < 0.80)"
            else:
                decision = "❌ KHÔNG ĐỒNG NGHĨA"

        print(f"\n▶ {label}")
        print(f"  • Câu [{stt_a}]: {rec_a['vi_display']} ({rec_a['en_display']})")
        print(f"    Khung: ({rec_a['bc']}, {rec_a['hd']}, {rec_a['kq']}, {rec_a['md']})")
        print(f"  • Câu [{stt_b}]: {rec_b['vi_display']} ({rec_b['en_display']})")
        print(f"    Khung: ({rec_b['bc']}, {rec_b['hd']}, {rec_b['kq']}, {rec_b['md']})")
        print(f"  • Điểm khớp Khung (S_onto):          {s_onto:.4f} ({meta['match_type']})")
        print(f"  • LaBSE (Chỉ Câu gốc):               {sim_raw:.4f}")
        print(f"  • LaBSE (Câu gốc + Khung):           {sim_rf:.4f}")
        print(f"  • LaBSE (Chỉ Nghĩa Gloss - Sàn lọc): {sim_gloss:.4f}")
        print(f"  • LaBSE (Khung + Nghĩa Gloss):       {sim_fg:.4f}")
        print(f"  • Điểm Lai Ghép (S_hybrid):          {s_hybrid:.4f}  ==> {decision}")

    # Ca 1: Đồng nghĩa thật sự cùng Khung
    compare_pair(48, 58, "CA 1: Cặp Đồng nghĩa Thật sự (Cùng Khung & Cùng Nghĩa)")
    compare_pair(25, 60, "CA 2: Cặp Đồng nghĩa Thật sự (Tiêu xài hoang phí)")

    # Ca 2: Trùng Khung Giả (Ontology cũ bị nhận nhầm là đồng nghĩa, LaBSE + Gloss lọc bỏ thành công)
    compare_pair(13, 85, "CA 3: Bẫy 'Trùng Khung Giả' #1 (Ontology cũ báo đồng nghĩa sai, LaBSE chặn lại)")
    compare_pair(66, 84, "CA 4: Bẫy 'Trùng Khung Giả' #2 (Đầu xuôi đuôi lọt vs Thất bại là mẹ thành công)")

    # Ca 3: Cận nghĩa nhưng Lệch Khung (Ontology cũ trả về 0, LaBSE + Ontology cứu lại)
    compare_pair(5, 22, "CA 5: Cặp Gần nghĩa nhưng Lệch Khung trong Ontology (Nếm mật nằm gai vs Có công mài sắt)")


def demo_new_idiom_query(engine: LaBSEOntologyEngine):
    print("\n" + "=" * 88)
    print("PHẦN 3: THỬ NGHIỆM TRUY VẤN THÀNH NGỮ MỚI NGOÀI TẬP DỮ LIỆU")
    print("=" * 88)

    res = engine.match_idiom(
        idiom_surface="Chơi với dao có ngày đứt tay",
        gloss_vi="Làm việc liều lĩnh, mạo hiểm hoặc sai trái nhiều lần thì sớm muộn cũng gặp tai họa.",
        gloss_en="Repeatedly taking reckless risks or doing dangerous things will eventually lead to harm.",
        bc="BC_Rủi_ro",
        hd="HD_Liều_lĩnh",
        kq="KQ_Gieo_tai_họa",
        md="",
        lang="vi",
        mode="frame_and_gloss",
        top_k=5,
    )

    print(f"Câu nhập mới:    {res['input_idiom']}")
    print(f"Chuỗi vào LaBSE: {res['encoded_string_for_labse']}")
    print(f"Trạng thái Khung: {res['frame_status']} (Khớp STT: {res['matched_frame_stts']})")

    print("\n--- Các câu ĐỒNG NGHĨA TUYỆT ĐỐI (>= 0.80) ---")
    for item in res["exact_synonyms"]:
        print(f"  [STT {item['stt']}] VI: {item['vi_idiom']} | EN: {item['en_idiom']}")
        print(f"          S_LaBSE = {item['s_labse']:.4f} | S_onto = {item['s_onto']:.4f} => S_hybrid = {item['s_hybrid']:.4f}")

    print("\n--- Các câu ĐỒNG NGHĨA MỀM / CẬN NGHĨA (0.68 - 0.80) ---")
    for item in res["near_synonyms"]:
        print(f"  [STT {item['stt']}] VI: {item['vi_idiom']} | EN: {item['en_idiom']}")
        print(f"          S_LaBSE = {item['s_labse']:.4f} | S_onto = {item['s_onto']:.4f} ({item['onto_match_type']}) => S_hybrid = {item['s_hybrid']:.4f}")


if __name__ == "__main__":
    engine = LaBSEOntologyEngine()

    print("=" * 88)
    print("PHẦN 1: THỰC NGHIỆM SO SÁNH 4 PHƯƠNG PHÁP BIỂU DIỄN ĐẦU VÀO CHO LaBSE (100 CẶP VIỆT - ANH)")
    print("=" * 88)
    modes = [
        ("raw_only", "1. Chỉ Câu gốc (Raw Idiom Surface)"),
        ("raw_and_frame", "2. Câu gốc + Khung Bản thể học (Raw + Frame)"),
        ("gloss_only", "3. Chỉ Nghĩa bóng (Gloss Only)"),
        ("frame_and_gloss", "4. Khung Bản thể học + Nghĩa Gloss (Đề xuất)"),
    ]
    print(f"{'Phương pháp biểu diễn đầu vào LaBSE':<46} | {'Cosine TB':<10} | {'Recall@1':<10} | {'Recall@5':<10} | {'MRR':<8}")
    print("-" * 96)
    for m_code, m_label in modes:
        metrics = evaluate_cross_lingual_retrieval(engine, mode=m_code)
        print(f"{m_label:<46} | {metrics['mean_pair_cosine']:<10.4f} | {metrics['recall_at_1']:>8.2f}% | {metrics['recall_at_5']:>8.2f}% | {metrics['mrr']:>6.2f}%")

    evaluate_case_studies(engine)
    demo_new_idiom_query(engine)
