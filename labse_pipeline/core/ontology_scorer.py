import json
from pathlib import Path
from typing import Dict, Tuple, Optional

AXES = ["bc", "hd", "kq", "md"]

SIM_MATRIX_PATH = Path(__file__).parent.parent / "data" / "criteria_similarity_matrix.json"

CRITERIA_SIM_MAP: Dict[str, float] = {}
if SIM_MATRIX_PATH.exists():
    with open(SIM_MATRIX_PATH, "r", encoding="utf-8") as f:
        CRITERIA_SIM_MAP = json.load(f)


def _norm(val: str) -> str:
    if not val:
        return ""
    s = str(val).strip()
    return "" if s.lower() in ["null", "none", "nan"] else s


def get_criteria_similarity(c1: str, c2: str) -> float:
    """
    Trả về độ tương đồng ngữ nghĩa LaBSE giữa 2 mã tiêu chí trong cùng trục:
    - Nếu trùng mã: 1.0
    - Nếu khác mã nhưng có độ tương đồng LaBSE >= 0.70: trả về giá trị thực >= 0.70
    - Ngược lại: 0.0
    """
    c1, c2 = _norm(c1), _norm(c2)
    if not c1 or not c2:
        return 0.0
    if c1 == c2:
        return 1.0
    key = f"{c1}|{c2}"
    return CRITERIA_SIM_MAP.get(key, 0.0)


def is_related_criterion(c1: str, c2: str, threshold: float = 0.70) -> bool:
    """Kiểm tra 2 tiêu chí có độ tương đồng ngữ nghĩa LaBSE >= 0.70 không."""
    return get_criteria_similarity(c1, c2) >= threshold


def compute_ontology_similarity(
    frame_a: Dict[str, str],
    frame_b: Dict[str, str],
    related_weight: float = 0.75,
) -> Tuple[float, Dict[str, str]]:
    """
    Tính điểm tương đồng cấu trúc Khung Bản thể học S_onto:
    - Trọng số các trục bằng nhau (không trục nào nhiều hơn trục nào).
    - Mẫu số (total_axes): số lượng trục có xuất hiện tiêu chí ở ít nhất một trong hai khung.
    - Tử số:
      + Nếu trục trùng khớp chính xác 100%: cộng 1.0 (Exact match)
      + Nếu trục khác mã nhưng độ tương đồng LaBSE >= 0.70: cộng 0.75 (Related match)
      + Nếu khác mã và LaBSE < 0.70: cộng 0.0
    - S_onto = Tử số / Mẫu số.
    """
    a = {k: _norm(frame_a.get(k, "")) for k in AXES}
    b = {k: _norm(frame_b.get(k, "")) for k in AXES}

    # 1. Trùng Khung Tuyệt đối
    if a == b and any(a.values()):
        matched_axes = [k.upper() for k in AXES if a[k]]
        return 1.0, {
            "match_type": "TRÙNG_KHUNG_TUYỆT_ĐỐI",
            "matched_axes": matched_axes,
            "related_axes": [],
            "matched_ratio": f"{len(matched_axes)}/{len(matched_axes)}",
            "veto": False,
        }

    active_axes = []
    matched_axes = []
    related_axes = []
    matched_score_sum = 0.0

    for axis in AXES:
        val_a, val_b = a[axis], b[axis]
        if not val_a and not val_b:
            continue
        axis_name = axis.upper()
        active_axes.append(axis_name)

        if val_a and val_b:
            if val_a == val_b:
                matched_score_sum += 1.0
                matched_axes.append(axis_name)
            else:
                sim = get_criteria_similarity(val_a, val_b)
                if sim >= 0.70:
                    matched_score_sum += related_weight  # Nhân hệ số 0.75
                    related_axes.append(f"~{axis_name}({sim:.2f})")

    total_count = len(active_axes)
    if total_count == 0:
        return 0.0, {
            "match_type": "KHÔNG_CÓ_TIÊU_CHÍ",
            "matched_axes": [],
            "related_axes": [],
            "matched_ratio": "0/0",
            "veto": False,
        }

    score = round(matched_score_sum / total_count, 4)

    parts = []
    if matched_axes:
        parts.append(f"Trùng {','.join(matched_axes)}")
    if related_axes:
        parts.append(f"Gần {','.join(related_axes)}")

    match_desc = " + ".join(parts) if parts else "Khác khung"
    match_type = f"{score:.2f} ({matched_score_sum:.2f}/{total_count}: {match_desc})"

    return score, {
        "match_type": match_type,
        "matched_axes": matched_axes,
        "related_axes": related_axes,
        "matched_ratio": f"{matched_score_sum:.2f}/{total_count}",
        "veto": False,
    }
