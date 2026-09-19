from fastapi import FastAPI, Query as Q
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from owlready2 import *
import csv, os
from pathlib import Path

app = FastAPI(title="V-Idiom API")

# ─── Ontology ────────────────────────────────────────────────
BASE_IRI = "http://www.semanticweb.org/phandangvu/ontologies/2026/8/v-idiomv2#"
ONTO_PATH = str(Path(__file__).parent.parent / "ontology_protege" / "v-idiomV5_final.rdf")

world = World()
onto = world.get_ontology(ONTO_PATH).load()

Khung_cls = world[BASE_IRI + "Khung_Bản_Thể_học"]
VN_cls    = world[BASE_IRI + "Vietnamese_idiom"]
EN_cls    = world[BASE_IRI + "English_Idiom"]
BC_cls    = world[BASE_IRI + "Bối_cảnh"]
HD_cls    = world[BASE_IRI + "Hành_động"]
KQ_cls    = world[BASE_IRI + "Kết_quả"]
MD_cls    = world[BASE_IRI + "Mục_đích"]

# ─── CSV lưu thành ngữ mới ────────────────────────────────────
CSV_PATH = Path(__file__).parent / "data" / "new_idioms.csv"
CSV_PATH.parent.mkdir(exist_ok=True)

HEADER = ["name", "language", "boi_canh", "hanh_dong", "ket_qua", "muc_dich", "giai_thich"]

def ensure_csv_header():
    """Đảm bảo file CSV luôn có header dù bị xoá hay chưa tạo."""
    if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(HEADER)
        return
    # Kiểm tra dòng đầu có phải header không
    with open(CSV_PATH, encoding="utf-8") as f:
        first_line = f.readline().strip()
    if not first_line.startswith("name"):
        # Thêm header vào đầu file
        with open(CSV_PATH, encoding="utf-8") as f:
            existing = f.read()
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            f.write(",".join(HEADER) + "\n" + existing)

ensure_csv_header()


# ─── Khởi động Reasoner & Load Cache ──────────────────────────
# Dùng Reasoner suy luận trực tiếp thuộc tính Có_nghĩa từ Ontology (thay vì nhóm chay bằng Python)
print("Đang khởi động HermiT Reasoner để sinh các thuộc tính suy luận...")
with onto:
    sync_reasoner(x=world, infer_property_values=True)
print("✅ Reasoner chạy xong!")

# Caching toàn bộ dữ liệu vào memory (tránh lỗi Thread-safe của owlready2 khi gọi từ API)
def build_cache():
    lk = {}
    f_idx = {}
    
    # Hàm phụ trợ trích xuất thông tin từ một entity idiom
    def extract_info(inst, lang):
        # Tìm các câu đồng nghĩa từ thuộc tính suy luận Có_nghĩa
        syn_vn = [i for i in inst.Có_nghĩa if type(i) is VN_cls and i != inst]
        syn_en = [i for i in inst.Có_nghĩa if type(i) is EN_cls and i != inst]
        
        # Ý nghĩa của câu hiện tại
        meaning_vn = str(inst.comment[0]) if lang == "vn" and inst.comment else ""
        meaning_en = str(inst.comment[0]) if lang == "en" and inst.comment else ""
        
        # Rút ý nghĩa ngôn ngữ còn lại từ cụm đồng nghĩa (để hiển thị song ngữ)
        if lang == "vn" and not meaning_en:
            for en_inst in syn_en:
                if en_inst.comment:
                    meaning_en = str(en_inst.comment[0])
                    break
        elif lang == "en" and not meaning_vn:
            for vn_inst in syn_vn:
                if vn_inst.comment:
                    meaning_vn = str(vn_inst.comment[0])
                    break
        
        khung = inst.Có_khung[0] if inst.Có_khung else None
        
        return {
            "lang": lang,
            "fname": khung.name if khung else "",
            "bc": khung.Có_bối_cảnh[0].name if khung and khung.Có_bối_cảnh else "",
            "hd": khung.Có_hành_động[0].name if khung and khung.Có_hành_động else "",
            "kq": khung.Có_kết_quả[0].name if khung and khung.Có_kết_quả else "",
            "md": khung.Có_mục_đích[0].name if khung and khung.Có_mục_đích else "",
            "synonyms_vn": sorted([i.name.replace("_", " ") for i in syn_vn]),
            "synonyms_en": sorted([i.name.replace("_", " ") for i in syn_en]),
            "meaning_vn": meaning_vn,
            "meaning_en": meaning_en,
        }

    for vi in VN_cls.instances():
        info = extract_info(vi, "vn")
        lk[vi.name.lower().replace("_", " ")] = info
        
        fname = info["fname"]
        if fname:
            if fname not in f_idx:
                f_idx[fname] = {"bc": info["bc"], "hd": info["hd"], "kq": info["kq"], "md": info["md"], "vn": set(), "en": set()}
            f_idx[fname]["vn"].add(vi.name.replace("_", " "))
            f_idx[fname]["vn"].update(info["synonyms_vn"])
        
    for en in EN_cls.instances():
        info = extract_info(en, "en")
        lk[en.name.lower().replace("_", " ")] = info
        
        fname = info["fname"]
        if fname:
            if fname not in f_idx:
                f_idx[fname] = {"bc": info["bc"], "hd": info["hd"], "kq": info["kq"], "md": info["md"], "vn": set(), "en": set()}
            f_idx[fname]["en"].add(en.name.replace("_", " "))
            f_idx[fname]["en"].update(info["synonyms_en"])
            
    # Chuyển set thành list cho f_idx
    for fname in f_idx:
        f_idx[fname]["vn"] = sorted(list(f_idx[fname]["vn"]))
        f_idx[fname]["en"] = sorted(list(f_idx[fname]["en"]))
        
    return lk, f_idx

lookup, frame_index = build_cache()

# ─── Helpers ─────────────────────────────────────────────────
def read_csv_idioms():
    """Đọc CSV an toàn, bỏ qua các dòng thiếu cột."""
    rows = []
    try:
        with open(CSV_PATH, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("name"): 
                    # Hỗ trợ file cũ chưa có cột giai_thich
                    if "giai_thich" not in row:
                        row["giai_thich"] = ""
                    if "giai_thich_en" not in row:
                        row["giai_thich_en"] = ""
                    rows.append(row)
    except Exception:
        pass
    return rows

# ─── API ─────────────────────────────────────────────────────
@app.get("/api/criteria")
def get_criteria():
    return {
        "boi_canh":  sorted([i.name for i in BC_cls.instances()]),
        "hanh_dong": sorted([i.name for i in HD_cls.instances()]),
        "ket_qua":   sorted([i.name for i in KQ_cls.instances()]),
        "muc_dich":  sorted([i.name for i in MD_cls.instances()]),
    }
# ─── Load Criteria Labels (Thread-safe Cache) ───────────────────
# owlready2 gặp lỗi NameError 'l2' nếu truy vấn instances() bằng nhiều thread qua FastAPI
# Vì vậy, ta load danh sách labels 1 lần duy nhất khi khởi động server
CRITERIA_LABELS_CACHE = {}
for cls in [BC_cls, HD_cls, KQ_cls, MD_cls]:
    for inst in cls.instances():
        if inst.comment and len(inst.comment) > 0:
            CRITERIA_LABELS_CACHE[inst.name] = str(inst.comment[0])
        else:
            CRITERIA_LABELS_CACHE[inst.name] = inst.name.replace("_", " ")

@app.get("/api/criteria-labels")
def get_criteria_labels():
    """Trả về dict {id -> label} từ bộ nhớ đệm an toàn."""
    return CRITERIA_LABELS_CACHE


@app.get("/api/search")
def search(q: str = Q(..., min_length=1)):
    key = q.strip().lower().replace(" ", "_")
    norm_key = key.replace("_", " ")

    # 1. Tìm trong ontology
    if norm_key in lookup:
        info = lookup[norm_key]
        
        return {
            "found": True,
            "source": "ontology",
            "name": q.strip(),
            "frame": info["fname"],
            "language": info["lang"],
            "criteria": {"bc": info["bc"], "hd": info["hd"], "kq": info["kq"], "md": info["md"]},
            "synonyms_vn": info["synonyms_vn"],
            "synonyms_en": info["synonyms_en"],
            "meaning_vn": info["meaning_vn"],
            "meaning_en": info["meaning_en"]
        }

    # 2. Tìm trong CSV mới
    for row in read_csv_idioms():
        if row["name"].lower().replace(" ", "_") == key:
            return {
                "found": True,
                "source": "csv",
                "name": row["name"],
                "language": row["language"],
                "criteria": {
                    "bc": row["boi_canh"], "hd": row["hanh_dong"],
                    "kq": row["ket_qua"],  "md": row["muc_dich"],
                },
                "synonyms_vn": [],
                "synonyms_en": [],
                "meaning": row.get("giai_thich", ""),
                "note": "Câu này mới được thêm thủ công, chưa có trong ontology chính thức."
            }

    return {"found": False, "query": q.strip()}

@app.post("/api/add")
def add_idiom(
    name:       str = Q(...),
    language:   str = Q(..., pattern="^(vn|en)$"),
    boi_canh:   str = Q(""),
    hanh_dong:  str = Q(""),
    ket_qua:    str = Q(""),
    muc_dich:   str = Q(""),
    giai_thich: str = Q("")
):
    name = name.strip().replace(" ", "_")
    key = name.lower()

    # Kiểm tra trùng trong ontology
    if key in lookup:
        return JSONResponse({"ok": False, "msg": "Đã tồn tại trong ontology!"}, status_code=400)

    # Kiểm tra trùng trong CSV (so sánh chuẩn hoá về lowercase + underscore)
    for row in read_csv_idioms():
        existing_key = row.get("name", "").lower().replace(" ", "_")
        if existing_key == key:
            return JSONResponse({"ok": False, "msg": "Đã được thêm trước đó rồi!"}, status_code=400)

    # Ghi vào CSV
    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([name, language, boi_canh, hanh_dong, ket_qua, muc_dich, giai_thich])

    # Trả về đồng nghĩa người dùng thấy ngay sau khi lưu
    matched_frames, syns_vn, syns_en = [], [], []
    for fname, info in frame_index.items():
        if boi_canh  and info["bc"] != boi_canh:  continue
        if hanh_dong and info["hd"] != hanh_dong: continue
        if ket_qua   and info["kq"] != ket_qua:   continue
        if muc_dich  and info["md"] != muc_dich:  continue
        matched_frames.append(fname)
        syns_vn.extend(info["vn"])
        syns_en.extend(info["en"])

    return {
        "ok": True,
        "msg": f"Đã lưu '{name.replace('_',' ')}' vào danh sách mới!",
        "matched_frames": matched_frames,
        "synonyms_vn": list(dict.fromkeys(syns_vn)),
        "synonyms_en": list(dict.fromkeys(syns_en)),
    }

@app.get("/api/preview-synonyms")
def preview_synonyms(
    boi_canh:  str = Q(""),
    hanh_dong: str = Q(""),
    ket_qua:   str = Q(""),
    muc_dich:  str = Q(""),
):
    """Tìm các Khung khớp với bộ tiêu chí + câu CSV có tiêu chí đó."""
    if not any([boi_canh, hanh_dong, ket_qua, muc_dich]):
        return {"matched_frames": [], "synonyms_vn": [], "synonyms_en": []}

    matched_frames, synonyms_vn, synonyms_en = [], [], []

    # Tìm trong ontology frame_index
    for fname, info in frame_index.items():
        if boi_canh  and info["bc"] != boi_canh:  continue
        if hanh_dong and info["hd"] != hanh_dong: continue
        if ket_qua   and info["kq"] != ket_qua:   continue
        if muc_dich  and info["md"] != muc_dich:  continue
        matched_frames.append(fname)
        synonyms_vn.extend(info["vn"])
        synonyms_en.extend(info["en"])

    # Tìm thêm trong CSV (câu mới được thêm thủ công)
    for row in read_csv_idioms():
        r_bc = row.get("boi_canh",  "")
        r_hd = row.get("hanh_dong", "")
        r_kq = row.get("ket_qua",   "")
        r_md = row.get("muc_dich",  "")
        if boi_canh  and r_bc != boi_canh:  continue
        if hanh_dong and r_hd != hanh_dong: continue
        if ket_qua   and r_kq != ket_qua:   continue
        if muc_dich  and r_md != muc_dich:  continue
        label = row["name"].replace("_", " ") + " ★"
        if row.get("language") == "en":
            synonyms_en.append(label)
        else:
            synonyms_vn.append(label)

    return {
        "matched_frames": matched_frames,
        "synonyms_vn": list(dict.fromkeys(synonyms_vn)),
        "synonyms_en": list(dict.fromkeys(synonyms_en)),
    }

# ─── Serve frontend ──────────────────────────────────────────
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "static"), html=True), name="static")
