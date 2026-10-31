from typing import Dict, Tuple

# Trọng số tầm quan trọng của 4 trục trong Bản thể học
AXIS_WEIGHTS = {
    "bc": 0.20,  # Bối cảnh
    "hd": 0.30,  # Hành động (Cơ chế tác động)
    "kq": 0.35,  # Kết quả (Hệ quả nhân - quả)
    "md": 0.15,  # Mục đích
}

# Các cặp Kết quả đối lập hoàn toàn về cực tính (Opposing Polarity Pairs)
OPPOSING_RESULTS = [
    ({"KQ_Thành_công", "KQ_May_mắn", "KQ_Tối_ưu_hóa", "KQ_Đạt_được_thỏa_thuận"},
     {"KQ_Thất_bại", "KQ_Tổn_thất_tài_sản", "KQ_Tổn_thương", "KQ_Gieo_tai_họa", "KQ_Gặp_trở_ngại", "KQ_Mất_quan_hệ"}),
    ({"KQ_Bình_yên", "KQ_An_toàn", "KQ_Gắn_kết", "KQ_Hòa_nhập"},
     {"KQ_Tổn_thương", "KQ_Gieo_tai_họa", "KQ_Mất_quan_hệ", "KQ_Hối_hận"}),
]


def _norm(val: str) -> str:
    if not val:
        return ""
    s = str(val).strip()
    return "" if s.lower() in ["null", "none", "nan"] else s


def is_opposing_result(kq1: str, kq2: str) -> bool:
    """Kiểm tra xem 2 tiêu chí Kết quả có đối lập cực tính (Tích cực vs Tiêu cực) không."""
    if not kq1 or not kq2 or kq1 == kq2:
        return False
    for pos_set, neg_set in OPPOSING_RESULTS:
        if (kq1 in pos_set and kq2 in neg_set) or (kq1 in neg_set and kq2 in pos_set):
            return True
    return False


def compute_ontology_similarity(
    frame_a: Dict[str, str],
    frame_b: Dict[str, str]
) -> Tuple[float, Dict[str, str]]:
    """
    Tính điểm tương đồng cấu trúc Khung Bản thể học S_onto thuộc [0.0, 1.0].
    Trả về: (score, details_dict)
    """
    a = {k: _norm(frame_a.get(k, "")) for k in ["bc", "hd", "kq", "md"]}
    b = {k: _norm(frame_b.get(k, "")) for k in ["bc", "hd", "kq", "md"]}

    # 1. Kiểm tra Trùng Khung Tuyệt đối (Exact Frame Match -> Property Chain Có_nghĩa)
    if a == b and any(a.values()):
        return 1.0, {"match_type": "TRÙNG_KHUNG_TUYỆT_ĐỐI", "veto": False}

    # 2. Kiểm tra Luật Phủ quyết Nhân - Quả (Causal Hard Veto)
    # Nếu kết quả (KQ) đối lập trực tiếp (vd: Thành công vs Thất bại/Tai họa) -> Veto = 0
    if is_opposing_result(a["kq"], b["kq"]):
        return 0.0, {"match_type": "PHỦ_QUYẾT_NGƯỢC_KẾT_QUẢ", "veto": True}

    # Nếu cả hai đều có Hành động và Kết quả, nhưng lệch hoàn toàn cả Hành động lẫn Kết quả -> Veto = 0
    if a["hd"] and b["hd"] and a["kq"] and b["kq"]:
        if a["hd"] != b["hd"] and a["kq"] != b["kq"]:
            return 0.0, {"match_type": "PHỦ_QUYẾT_KHÁC_CƠ_CHẾ_NHÂN_QUẢ", "veto": True}

    # 3. Tính điểm khớp mềm có trọng số (Weighted Soft Frame Overlap)
    active_weight_sum = 0.0
    matched_weight_sum = 0.0
    shared_axes = []

    for axis, w in AXIS_WEIGHTS.items():
        val_a, val_b = a[axis], b[axis]
        if not val_a and not val_b:
            continue
        active_weight_sum += w
        if val_a and val_b and val_a == val_b:
            matched_weight_sum += w
            shared_axes.append(axis.upper())

    if active_weight_sum == 0.0:
        return 0.0, {"match_type": "KHÔNG_CÓ_TIÊU_CHÍ", "veto": False}

    score = matched_weight_sum / active_weight_sum
    match_type = f"KHỚP_MỀM ({','.join(shared_axes)})" if shared_axes else "KHÁC_KHUNG"
    return round(float(score), 4), {"match_type": match_type, "veto": False}
