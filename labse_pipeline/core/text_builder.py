import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent.parent / "data" / "criteria_catalog.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    CRITERIA_CATALOG = json.load(f)

# Tạo bảng tra cứu phẳng (Flat Lookup) từ mã tiêu chí -> thông tin nhãn & mô tả
FLAT_CRITERIA = {}
for axis_name, items in CRITERIA_CATALOG.items():
    for code, meta in items.items():
        FLAT_CRITERIA[code] = {
            "axis": axis_name,
            **meta
        }


def get_criterion_label(code: str, lang: str = "vi", include_desc: bool = False) -> str:
    """Chuyển mã tiêu chí (vd: BC_Rủi_ro) sang nhãn tự nhiên để đưa vào LaBSE."""
    if not code or str(code).strip().lower() in ["", "null", "none", "nan"]:
        return ""
    code = str(code).strip()
    info = FLAT_CRITERIA.get(code)
    if not info:
        # Nếu là tiêu chí mới do người dùng/LLM tự sinh chưa có trong catalog
        clean = code.split("_", 1)[-1].replace("_", " ")
        return clean

    if lang == "en":
        lbl = info["label_en"]
        desc = info["desc_en"]
    else:
        lbl = info["label_vi"]
        desc = info["desc_vi"]

    if include_desc:
        return f"{lbl} ({desc})"
    return lbl


def build_frame_prefix(
    bc: str = "",
    hd: str = "",
    kq: str = "",
    md: str = "",
    lang: str = "vi"
) -> str:
    """
    Tạo chuỗi Khung Bản thể học chuẩn hóa làm mỏ neo cấu trúc (Structural Anchor).
    Ví dụ (VI): "[Bối cảnh: Rủi ro | Hành động: Liều lĩnh | Kết quả: Gieo tai họa]"
    Ví dụ (EN): "[Context: Risk and Uncertainty | Action: Recklessness | Result: Retribution and Disaster]"
    """
    parts = []
    if lang == "en":
        axis_names = [
            ("Context", bc),
            ("Action", hd),
            ("Result", kq),
            ("Purpose", md),
        ]
    else:
        axis_names = [
            ("Bối cảnh", bc),
            ("Hành động", hd),
            ("Kết quả", kq),
            ("Mục đích", md),
        ]

    for axis_label, code in axis_names:
        lbl = get_criterion_label(code, lang=lang)
        if lbl:
            parts.append(f"{axis_label}: {lbl}")

    if not parts:
        return ""
    return "[" + " | ".join(parts) + "]"


def build_labse_input(
    idiom_surface: str = "",
    gloss: str = "",
    bc: str = "",
    hd: str = "",
    kq: str = "",
    md: str = "",
    lang: str = "vi",
    mode: str = "frame_and_gloss"
) -> str:
    """
    Ghép chuỗi đầu vào cho mô hình LaBSE theo 4 chế độ:
      1. 'frame_and_gloss' (Khuyên dùng - Tối ưu nhất):
         "[Khung Bản thể học] : <Nghĩa bóng Gloss>"
      2. 'full' (Câu gốc + Khung + Nghĩa Gloss):
         "<Câu gốc> [Khung Bản thể học] : <Nghĩa bóng Gloss>"
      3. 'raw_and_frame' (Câu gốc + Khung Bản thể học - Không có Gloss):
         "<Câu gốc> | [Khung Bản thể học]"
      4. 'gloss_only' (Chỉ Nghĩa bóng Gloss):
         "<Nghĩa bóng Gloss>"
      5. 'raw_only' (Chỉ Câu thành ngữ gốc):
         "<Câu gốc>"
    """
    clean_surface = str(idiom_surface or "").strip().replace("_", " ")
    clean_gloss = str(gloss or "").strip()
    frame_str = build_frame_prefix(bc, hd, kq, md, lang=lang)

    if mode == "raw_only":
        return clean_surface

    if mode == "gloss_only":
        return clean_gloss if clean_gloss else clean_surface

    if mode == "raw_and_frame":
        if frame_str and clean_surface:
            return f"{clean_surface} | {frame_str}"
        return clean_surface or frame_str

    if mode == "full":
        segments = [s for s in [clean_surface, frame_str] if s]
        head = " ".join(segments)
        if head and clean_gloss:
            return f"{head} : {clean_gloss}"
        return head or clean_gloss

    # Mặc định: 'frame_and_gloss' (Khung Bản thể học + Nghĩa Gloss)
    if frame_str and clean_gloss:
        return f"{frame_str} : {clean_gloss}"
    elif clean_gloss:
        return clean_gloss
    elif frame_str and clean_surface:
        return f"{frame_str} : {clean_surface}"
    return clean_surface
