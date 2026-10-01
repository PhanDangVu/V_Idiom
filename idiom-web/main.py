from fastapi import FastAPI, Query as Q, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from owlready2 import *
import csv, os, json, requests
from pathlib import Path
from dotenv import load_dotenv

# ─── Load Environment Variables ───────────────────────────────
load_dotenv(Path(__file__).parent / ".env")
load_dotenv()

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

# ─── CSV Paths & Headers ─────────────────────────────────────
# File CSV chuẩn v4 của toàn bộ dự án
CSV_V4_PATH = Path(__file__).parent.parent / "thanh_ngu_tuc_ngu_100_cau_v4.csv"
V4_HEADER = [
    "STT",
    "Thành_ngữ_Tiếng_Việt",
    "Thành_ngữ_Tiếng_Anh",
    "Bối_cảnh",
    "Hành_động",
    "Kết_quả",
    "Mục_đích",
    "Giải_thích_nghĩa_Tiếng_Việt",
    "Giải_thích_nghĩa_Tiếng_Anh"
]

# File CSV lưu thành ngữ mới trong thư mục idiom-web (tương thích ngược)
CSV_PATH = Path(__file__).parent / "data" / "new_idioms.csv"
CSV_PATH.parent.mkdir(exist_ok=True)
HEADER = ["name", "language", "boi_canh", "hanh_dong", "ket_qua", "muc_dich", "giai_thich"]

def ensure_csv_header():
    """Đảm bảo file CSV luôn có header dù bị xoá hay chưa tạo."""
    if not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0:
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(HEADER)
        return
    with open(CSV_PATH, encoding="utf-8") as f:
        first_line = f.readline().strip()
    if not first_line.startswith("name"):
        with open(CSV_PATH, encoding="utf-8") as f:
            existing = f.read()
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            f.write(",".join(HEADER) + "\n" + existing)

ensure_csv_header()

# ─── Khởi động Reasoner & Load Cache ──────────────────────────
print("Đang khởi động HermiT Reasoner để sinh các thuộc tính suy luận...")
with onto:
    try:
        sync_reasoner(x=world, infer_property_values=True)
        print("✅ Reasoner chạy xong!")
    except Exception as e:
        print(f"⚠️ Reasoner cảnh báo: {e}")

def build_cache():
    lk = {}
    f_idx = {}
    
    def extract_info(inst, lang):
        khung = inst.Có_khung[0] if inst.Có_khung else None

        # 1. Tìm các câu đồng nghĩa từ thuộc tính suy luận Có_nghĩa
        syn_vn = [i for i in inst.Có_nghĩa if type(i) is VN_cls and i != inst]
        syn_en = [i for i in inst.Có_nghĩa if type(i) is EN_cls and i != inst]
        
        # 2. Bổ sung các câu cùng khung (đảm bảo đồng nghĩa tức thì khi thêm mới)
        if khung:
            for sibling in getattr(khung, "Là_khung_của", []):
                if type(sibling) is VN_cls and sibling != inst and sibling not in syn_vn:
                    syn_vn.append(sibling)
                elif type(sibling) is EN_cls and sibling != inst and sibling not in syn_en:
                    syn_en.append(sibling)

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
            
    for fname in f_idx:
        f_idx[fname]["vn"] = sorted(list(f_idx[fname]["vn"]))
        f_idx[fname]["en"] = sorted(list(f_idx[fname]["en"]))
        
    return lk, f_idx

lookup, frame_index = build_cache()

# ─── Load Criteria Labels (Thread-safe Cache) ──────────────────
CRITERIA_LABELS_CACHE = {}
def refresh_criteria_cache():
    global CRITERIA_LABELS_CACHE
    CRITERIA_LABELS_CACHE = {}
    for cls in [BC_cls, HD_cls, KQ_cls, MD_cls]:
        for inst in cls.instances():
            if inst.comment and len(inst.comment) > 0:
                CRITERIA_LABELS_CACHE[inst.name] = str(inst.comment[0])
            else:
                CRITERIA_LABELS_CACHE[inst.name] = inst.name.replace("_", " ")

refresh_criteria_cache()

# ─── CSV Helper ──────────────────────────────────────────────
def read_csv_idioms():
    """Đọc dữ liệu từ file CSV chính và CSV phụ."""
    rows = []
    # Đọc từ thanh_ngu_tuc_ngu_100_cau_v4.csv
    if CSV_V4_PATH.exists():
        try:
            with open(CSV_V4_PATH, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    vn = (row.get("Thành_ngữ_Tiếng_Việt") or "").strip()
                    en = (row.get("Thành_ngữ_Tiếng_Anh") or "").strip()
                    bc = (row.get("Bối_cảnh") or "").strip()
                    hd = (row.get("Hành_động") or "").strip()
                    kq = (row.get("Kết_quả") or "").strip()
                    md = (row.get("Mục_đích") or "").strip()
                    gt_vn = (row.get("Giải_thích_nghĩa_Tiếng_Việt") or "").strip()
                    gt_en = (row.get("Giải_thích_nghĩa_Tiếng_Anh") or "").strip()
                    if vn:
                        rows.append({
                            "name": vn,
                            "language": "vn",
                            "boi_canh": bc, "hanh_dong": hd, "ket_qua": kq, "muc_dich": md,
                            "giai_thich": gt_vn,
                            "giai_thich_en": gt_en
                        })
                    if en:
                        rows.append({
                            "name": en,
                            "language": "en",
                            "boi_canh": bc, "hanh_dong": hd, "ket_qua": kq, "muc_dich": md,
                            "giai_thich": gt_vn,
                            "giai_thich_en": gt_en
                        })
        except Exception as e:
            print(f"Lỗi đọc {CSV_V4_PATH}: {e}")

    # Đọc từ new_idioms.csv
    if CSV_PATH.exists():
        try:
            with open(CSV_PATH, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("name"):
                        if "giai_thich" not in row: row["giai_thich"] = ""
                        if "giai_thich_en" not in row: row["giai_thich_en"] = ""
                        rows.append(row)
        except Exception:
            pass
    return rows

# ─── PHẦN 1: GROQ CLOUD VÀ LLM PROMPT ────────────────────────
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

PROMPT_FILE_PATH = Path(__file__).parent / "prompts" / "prompt_phan_loai_thanh_ngu.md"

def load_prompt_template() -> str:
    """Đọc template prompt từ file Markdown."""
    if not PROMPT_FILE_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file prompt tại: {PROMPT_FILE_PATH}")
    with open(PROMPT_FILE_PATH, mode="r", encoding="utf-8") as f:
        return f.read()

def build_ai_prompt(idiom_input: str) -> tuple[str, str]:
    """Trả về (system_prompt, user_prompt) dựa trên template và input."""
    system_prompt = load_prompt_template()
    user_prompt = f"Phân loại câu thành ngữ này: {idiom_input}"
    return system_prompt, user_prompt

def call_groq_api(prompts: tuple[str, str]) -> dict:
    """Gọi Groq Cloud API qua endpoint OpenAI-compatible."""
    system_prompt, user_prompt = prompts
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not groq_api_key:
        raise HTTPException(
            status_code=400,
            detail="Chưa cấu hình biến môi trường GROQ_API_KEY. Vui lòng thiết lập trong file .env hoặc biến môi trường."
        )

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lỗi kết nối tới Groq Cloud API: {str(e)}")

    if resp.status_code != 200:
        error_detail = f"Groq API báo lỗi: {resp.text}"
        try:
            error_data = resp.json()
            if "error" in error_data and "message" in error_data["error"]:
                msg = error_data["error"]["message"]
                if "rate limit" in msg.lower():
                    import re
                    wait_time = re.search(r'in (\d+\.?\d*)s', msg)
                    if wait_time:
                        seconds = float(wait_time.group(1))
                        error_detail = f"⚠️ Đạt giới hạn gọi AI (Rate Limit). Prompt hiện tại khá dài do chứa danh sách khung. Vui lòng thử lại sau {int(seconds) + 1} giây!"
                    else:
                        error_detail = "⚠️ Đạt giới hạn gọi AI (Rate Limit). Vui lòng chờ 1 phút rồi thử lại."
        except:
            pass
        raise HTTPException(status_code=resp.status_code, detail=error_detail)
    try:
        raw_text = resp.json()["choices"][0]["message"]["content"]
        data = json.loads(raw_text)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể phân tích dữ liệu JSON từ Groq: {str(e)}")

# ─── PHẦN 2: TỰ ĐỘNG HÓA LƯU TRỮ (ONTOLOGY & CSV) ─────────────
def save_to_csv(
    vn_name: str,
    en_name: str,
    bc: str = "",
    hd: str = "",
    kq: str = "",
    md: str = "",
    giai_thich_vn: str = "",
    giai_thich_en: str = ""
) -> int:
    """Lưu cặp thành ngữ vào CSV theo định dạng chuẩn của thanh_ngu_tuc_ngu_100_cau_v4.csv."""
    vn_clean = vn_name.strip().replace(" ", "_")
    en_clean = en_name.strip().replace(" ", "_")

    # Xác định STT tiếp theo
    next_stt = 1
    if CSV_V4_PATH.exists():
        with open(CSV_V4_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            stt_list = []
            for row in reader:
                if row and row[0].strip().isdigit():
                    stt_list.append(int(row[0].strip()))
            if stt_list:
                next_stt = max(stt_list) + 1
    else:
        with open(CSV_V4_PATH, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(V4_HEADER)

    # Ghi vào file v4 chính
    with open(CSV_V4_PATH, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            next_stt,
            vn_clean,
            en_clean,
            bc.strip(),
            hd.strip(),
            kq.strip(),
            md.strip(),
            giai_thich_vn.strip(),
            giai_thich_en.strip()
        ])

    # Ghi đồng bộ vào new_idioms.csv (cho các phần mềm/endpoint cũ)
    try:
        ensure_csv_header()
        with open(CSV_PATH, mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([vn_clean, "vn", bc.strip(), hd.strip(), kq.strip(), md.strip(), giai_thich_vn.strip()])
            writer.writerow([en_clean, "en", bc.strip(), hd.strip(), kq.strip(), md.strip(), giai_thich_en.strip()])
    except Exception as e:
        print(f"Lỗi đồng bộ new_idioms.csv: {e}")

    return next_stt

def save_to_ontology(
    vn_name: str,
    en_name: str,
    bc: str = "",
    hd: str = "",
    kq: str = "",
    md: str = "",
    giai_thich_vn: str = "",
    giai_thich_en: str = ""
) -> dict:
    """Tự động thêm tiêu chí (nếu mới), gắn khung và lưu thành ngữ vào Ontology RDF."""
    global lookup, frame_index

    bc = bc.strip() if bc else ""
    hd = hd.strip() if hd else ""
    kq = kq.strip() if kq else ""
    md = md.strip() if md else ""

    with onto:
        # 1. Quản lý / khởi tạo cá thể Tiêu chí nếu chưa có trong Ontology
        bc_inst = None
        if bc:
            bc_inst = world[BASE_IRI + bc] or getattr(onto, bc, None)
            if not bc_inst:
                bc_inst = BC_cls(bc)
                bc_inst.comment = [bc.replace("_", " ")]

        hd_inst = None
        if hd:
            hd_inst = world[BASE_IRI + hd] or getattr(onto, hd, None)
            if not hd_inst:
                hd_inst = HD_cls(hd)
                hd_inst.comment = [hd.replace("_", " ")]

        kq_inst = None
        if kq:
            kq_inst = world[BASE_IRI + kq] or getattr(onto, kq, None)
            if not kq_inst:
                kq_inst = KQ_cls(kq)
                kq_inst.comment = [kq.replace("_", " ")]

        md_inst = None
        if md:
            md_inst = world[BASE_IRI + md] or getattr(onto, md, None)
            if not md_inst:
                md_inst = MD_cls(md)
                md_inst.comment = [md.replace("_", " ")]

        # 2. Tìm hoặc tạo Khung_Bản_Thể_học
        target_frame = None
        for f in Khung_cls.instances():
            f_bc = f.Có_bối_cảnh[0].name if f.Có_bối_cảnh else ""
            f_hd = f.Có_hành_động[0].name if f.Có_hành_động else ""
            f_kq = f.Có_kết_quả[0].name if f.Có_kết_quả else ""
            f_md = f.Có_mục_đích[0].name if f.Có_mục_đích else ""
            if (f_bc, f_hd, f_kq, f_md) == (bc, hd, kq, md):
                target_frame = f
                break

        if not target_frame:
            max_num = 0
            for f in Khung_cls.instances():
                digits = "".join(filter(str.isdigit, f.name))
                if digits:
                    max_num = max(max_num, int(digits))
            frame_name = f"Khung{max_num + 1}"
            target_frame = Khung_cls(frame_name)
            if bc_inst: target_frame.Có_bối_cảnh.append(bc_inst)
            if hd_inst: target_frame.Có_hành_động.append(hd_inst)
            if kq_inst: target_frame.Có_kết_quả.append(kq_inst)
            if md_inst: target_frame.Có_mục_đích.append(md_inst)

        # 3. Tạo / cập nhật cá thể Thành ngữ Tiếng Việt
        vn_clean = vn_name.strip().replace(" ", "_")
        vn_inst = world[BASE_IRI + vn_clean] or getattr(onto, vn_clean, None)
        if not vn_inst:
            vn_inst = VN_cls(vn_clean)
        if target_frame not in vn_inst.Có_khung:
            vn_inst.Có_khung.append(target_frame)
        if giai_thich_vn:
            vn_inst.comment = [locstr(giai_thich_vn.strip(), lang="vi")]

        # 4. Tạo / cập nhật cá thể Thành ngữ Tiếng Anh
        en_clean = (
            en_name.strip()
            .replace(" ", "_")
            .replace("?", "")
            .replace("!", "")
            .replace(",", "")
            .replace("'", "")
        )
        en_inst = world[BASE_IRI + en_clean] or getattr(onto, en_clean, None)
        if not en_inst:
            en_inst = EN_cls(en_clean)
        if target_frame not in en_inst.Có_khung:
            en_inst.Có_khung.append(target_frame)
        if giai_thich_en:
            en_inst.comment = [locstr(giai_thich_en.strip(), lang="en")]

        # 5. Lưu vào file Ontology RDF
        onto.save(file=ONTO_PATH, format="rdfxml")

    # 6. Làm mới bộ nhớ cache và danh sách nhãn
    refresh_criteria_cache()
    lookup, frame_index = build_cache()

    return {
        "frame": target_frame.name,
        "vn_name": vn_clean,
        "en_name": en_clean,
        "synonyms_vn": frame_index.get(target_frame.name, {}).get("vn", []),
        "synonyms_en": frame_index.get(target_frame.name, {}).get("en", []),
    }

# ─── Pydantic Models ─────────────────────────────────────────
class AIAnalyzeRequest(BaseModel):
    idiom: str

class AISaveRequest(BaseModel):
    thanh_ngu_vn: str
    thanh_ngu_en: str
    boi_canh: str = ""
    hanh_dong: str = ""
    ket_qua: str = ""
    muc_dich: str = ""
    giai_thich_vn: str = ""
    giai_thich_en: str = ""

# ─── AI Endpoints ────────────────────────────────────────────
@app.api_route("/api/ai/analyze", methods=["GET", "POST"])
def api_ai_analyze(idiom: str = Q(None), body: AIAnalyzeRequest = Body(None)):
    """Phân tích thành ngữ tiếng Việt và gợi ý thành ngữ tiếng Anh cùng 4 trục tiêu chí qua Groq Cloud."""
    target_idiom = ""
    if body and body.idiom:
        target_idiom = body.idiom
    elif idiom:
        target_idiom = idiom

    if not target_idiom or not target_idiom.strip():
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp thành ngữ cần phân tích.")

    prompt = build_ai_prompt(target_idiom.strip())
    result = call_groq_api(prompt)
    print("GROQ RESULT:", result)

    try:
        matcher = IdiomOntologyMatcher(CSV_V4_PATH)
        if "Thành_ngữ_Gốc" not in result and "Thành_ngữ_Tiếng_Việt" in result:
            result["Thành_ngữ_Gốc"] = result["Thành_ngữ_Tiếng_Việt"]
        elif "Thành_ngữ_Gốc" not in result:
            result["Thành_ngữ_Gốc"] = target_idiom.strip()

        final_result = matcher.process_llm_json(result)
        return {
            "ok": True,
            "data": final_result
        }
    except Exception as e:
        print("Lỗi xử lý matcher:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/save")
def api_ai_save(req: AISaveRequest):
    """Lưu kết quả phân tích thành ngữ vào đồng thời Ontology và CSV."""
    if not req.thanh_ngu_vn or not req.thanh_ngu_en:
        raise HTTPException(status_code=400, detail="Yêu cầu phải có cả Thành ngữ tiếng Việt và Thành ngữ tiếng Anh.")

    # 1. Lưu vào CSV
    stt = save_to_csv(
        vn_name=req.thanh_ngu_vn,
        en_name=req.thanh_ngu_en,
        bc=req.boi_canh,
        hd=req.hanh_dong,
        kq=req.ket_qua,
        md=req.muc_dich,
        giai_thich_vn=req.giai_thich_vn,
        giai_thich_en=req.giai_thich_en
    )

    # 2. Lưu vào Ontology
    onto_res = save_to_ontology(
        vn_name=req.thanh_ngu_vn,
        en_name=req.thanh_ngu_en,
        bc=req.boi_canh,
        hd=req.hanh_dong,
        kq=req.ket_qua,
        md=req.muc_dich,
        giai_thich_vn=req.giai_thich_vn,
        giai_thich_en=req.giai_thich_en
    )

    return {
        "ok": True,
        "msg": f"Đã lưu thành công vào Ontology và CSV (STT: {stt})!",
        "stt": stt,
        "frame": onto_res["frame"],
        "synonyms_vn": onto_res["synonyms_vn"],
        "synonyms_en": onto_res["synonyms_en"]
    }

@app.post("/api/ai/auto-process")
def api_ai_auto_process(req: AIAnalyzeRequest):
    """Quy trình tự động hoá 1 chạm: Phân tích bằng Groq Cloud -> Tự động lưu vào CSV và Ontology."""
    if not req.idiom or not req.idiom.strip():
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp thành ngữ.")

    # 1. Phân tích qua Groq
    prompt = build_ai_prompt(req.idiom.strip())
    res = call_groq_api(prompt)

    thanh_ngu_vn = res.get("Thành_ngữ_Tiếng_Việt") or res.get("Thanh_ngu_VN") or req.idiom.strip()
    thanh_ngu_en = res.get("Thành_ngữ_Tiếng_Anh") or res.get("Thanh_ngu_EN") or ""

    bc = res.get("Bối_cảnh") or ""
    hd = res.get("Hành_động") or ""
    kq = res.get("Kết_quả") or ""
    md = res.get("Mục_đích") or ""

    bc = bc if bc else ""
    hd = hd if hd else ""
    kq = kq if kq else ""
    md = md if md else ""

    giai_thich_vn = res.get("Giải_thích_nghĩa_Tiếng_Việt") or ""
    giai_thich_en = res.get("Giải_thích_nghĩa_Tiếng_Anh") or ""
    
    sac_thai = ""
    co_che = ""
    phan_bien = ""
    kiem_tra_nguoc = ""

    # 2. Lưu vào CSV
    stt = save_to_csv(
        vn_name=thanh_ngu_vn,
        en_name=thanh_ngu_en,
        bc=bc,
        hd=hd,
        kq=kq,
        md=md,
        giai_thich_vn=giai_thich_vn,
        giai_thich_en=giai_thich_en
    )

    # 3. Lưu vào Ontology
    onto_res = save_to_ontology(
        vn_name=thanh_ngu_vn,
        en_name=thanh_ngu_en,
        bc=bc,
        hd=hd,
        kq=kq,
        md=md,
        giai_thich_vn=giai_thich_vn,
        giai_thich_en=giai_thich_en
    )

    return {
        "ok": True,
        "msg": f"Đã tự động phân tích và lưu thành công (STT: {stt})!",
        "stt": stt,
        "thanh_ngu_vn": thanh_ngu_vn,
        "thanh_ngu_en": thanh_ngu_en,
        "tieu_chi": {
            "Boi_canh": bc,
            "Hanh_dong": hd,
            "Ket_qua": kq,
            "Muc_dich": md
        },
        "giai_thich_vn": giai_thich_vn,
        "giai_thich_en": giai_thich_en,
        "sac_thai": sac_thai,
        "co_che": co_che,
        "phan_bien": phan_bien,
        "kiem_tra_nguoc": kiem_tra_nguoc,
        "frame": onto_res["frame"],
        "synonyms_vn": onto_res["synonyms_vn"],
        "synonyms_en": onto_res["synonyms_en"]
    }

# ─── Standard API Endpoints ──────────────────────────────────
@app.get("/api/criteria")
def get_criteria():
    return {
        "boi_canh":  sorted([i.name for i in BC_cls.instances()]),
        "hanh_dong": sorted([i.name for i in HD_cls.instances()]),
        "ket_qua":   sorted([i.name for i in KQ_cls.instances()]),
        "muc_dich":  sorted([i.name for i in MD_cls.instances()]),
    }

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

    # 2. Tìm trong CSV
    for row in read_csv_idioms():
        if row["name"].lower().replace(" ", "_") == key:
            return {
                "found": True,
                "source": "csv",
                "name": row["name"],
                "language": row.get("language", "vn"),
                "criteria": {
                    "bc": row.get("boi_canh", ""),
                    "hd": row.get("hanh_dong", ""),
                    "kq": row.get("ket_qua", ""),
                    "md": row.get("muc_dich", ""),
                },
                "synonyms_vn": [],
                "synonyms_en": [],
                "meaning_vn": row.get("giai_thich", ""),
                "meaning_en": row.get("giai_thich_en", ""),
                "note": "Câu này được lưu trong CSV dữ liệu hệ thống."
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

    # Ghi vào CSV
    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerow([name, language, boi_canh, hanh_dong, ket_qua, muc_dich, giai_thich])

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

    for fname, info in frame_index.items():
        if boi_canh  and info["bc"] != boi_canh:  continue
        if hanh_dong and info["hd"] != hanh_dong: continue
        if ket_qua   and info["kq"] != ket_qua:   continue
        if muc_dich  and info["md"] != muc_dich:  continue
        matched_frames.append(fname)
        synonyms_vn.extend(info["vn"])
        synonyms_en.extend(info["en"])

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
import pandas as pd
import json

class IdiomOntologyMatcher:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.frame_db = {}
        self._build_frame_index()

    def _build_frame_index(self):
        self.frame_db = {}
        for idx, row in self.df.iterrows():
            bc = str(row['Bối_cảnh']).strip() if pd.notna(row['Bối_cảnh']) else ''
            hd = str(row['Hành_động']).strip() if pd.notna(row['Hành_động']) else ''
            kq = str(row['Kết_quả']).strip() if pd.notna(row['Kết_quả']) else ''
            md = str(row['Mục_đích']).strip() if pd.notna(row['Mục_đích']) else ''
            
            key = (bc, hd, kq, md)
            if key not in self.frame_db:
                self.frame_db[key] = {
                    'stt': row['STT'],
                    'vi_list': [],
                    'en_list': [],
                    'meaning_vi': str(row['Giải_thích_nghĩa_Tiếng_Việt']) if pd.notna(row['Giải_thích_nghĩa_Tiếng_Việt']) else '',
                    'meaning_en': str(row['Giải_thích_nghĩa_Tiếng_Anh']) if pd.notna(row['Giải_thích_nghĩa_Tiếng_Anh']) else ''
                }
            
            if pd.notna(row['Thành_ngữ_Tiếng_Việt']) and str(row['Thành_ngữ_Tiếng_Việt']).strip():
                vi = str(row['Thành_ngữ_Tiếng_Việt']).strip()
                if vi not in self.frame_db[key]['vi_list']:
                    self.frame_db[key]['vi_list'].append(vi)

            if pd.notna(row['Thành_ngữ_Tiếng_Anh']) and str(row['Thành_ngữ_Tiếng_Anh']).strip():
                en = str(row['Thành_ngữ_Tiếng_Anh']).strip()
                if en not in self.frame_db[key]['en_list']:
                    self.frame_db[key]['en_list'].append(en)

    def process_llm_json(self, extracted_json):
        bc = str(extracted_json.get('Bối_cảnh') or '').strip()
        hd = str(extracted_json.get('Hành_động') or '').strip()
        kq = str(extracted_json.get('Kết_quả') or '').strip()
        md = str(extracted_json.get('Mục_đích') or '').strip()
        
        if bc.lower() in ['null', 'none']: bc = ''
        if hd.lower() in ['null', 'none']: hd = ''
        if kq.lower() in ['null', 'none']: kq = ''
        if md.lower() in ['null', 'none']: md = ''

        key = (bc, hd, kq, md)
        input_idiom = extracted_json.get('Thành_ngữ_Gốc') or extracted_json.get('Thành_ngữ_Tiếng_Việt') or ''

        if key in self.frame_db:
            matched = self.frame_db[key]
            return {
                "Kết_Quả_Đánh_Giá": "KHUNG_ĐÃ_TỒN_TẠI",
                "Mã_Khung_STT": matched['stt'],
                "Thành_Ngữ_Mới_Nhập": input_idiom,
                "Bộ_Tiêu_Chí_Khung": {
                    "Bối_cảnh": bc or None,
                    "Hành_động": hd or None,
                    "Kết_quả": kq or None,
                    "Mục_đích": md or None
                },
                "Các_Câu_Đồng_Nghĩa_Cùng_Khung": {
                    "Tiếng_Việt": matched['vi_list'],
                    "Tiếng_Anh": matched['en_list']
                },
                "Giải_Thích_Nghĩa_Gốc": {
                    "Tiếng_Việt": matched['meaning_vi'],
                    "Tiếng_Anh": matched['meaning_en']
                },
                "Giải_Thích_Nghĩa_Đề_Xuất": {
                    "Tiếng_Việt": extracted_json.get('Giải_thích_nghĩa_Tiếng_Việt', ''),
                    "Tiếng_Anh": extracted_json.get('Giải_thích_nghĩa_Tiếng_Anh', '')
                }
            }
        else:
            max_stt = max([item['stt'] for item in self.frame_db.values()]) if self.frame_db else 100
            new_stt = max_stt + 1
            return {
                "Kết_Quả_Đánh_Giá": "KHUNG_MỚI",
                "Mã_Khung_STT_Khởi_Tạo": new_stt,
                "Thành_Ngữ_Mới_Nhập": input_idiom,
                "Bộ_Tiêu_Chí_Khung_Mới": {
                    "Bối_cảnh": bc or None,
                    "Hành_động": hd or None,
                    "Kết_quả": kq or None,
                    "Mục_đích": md or None
                },
                "Thông_Báo": f"Không tìm thấy khung trùng khớp. Đã đề xuất tạo Khung mới STT {new_stt}.",
                "Giải_Thích_Nghĩa_Đề_Xuất": {
                    "Tiếng_Việt": extracted_json.get('Giải_thích_nghĩa_Tiếng_Việt', ''),
                    "Tiếng_Anh": extracted_json.get('Giải_thích_nghĩa_Tiếng_Anh', '')
                }
            }
