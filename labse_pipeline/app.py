import os
import time
import json
import requests
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from core.labse_engine import LaBSEOntologyEngine
from core.text_builder import CRITERIA_CATALOG

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / "idiom-web" / ".env")
load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
PROMPT_PATH = BASE_DIR / "prompts" / "prompt_labse_extract.md"

app = FastAPI(
    title="V-Idiom: LaBSE + Ontology Hybrid UI & API",
    description="Giao diện thử nghiệm toàn trình: LLM (Groq) -> [Khung + Gloss] -> LaBSE + Bản thể học",
    version="1.0.0",
)

engine = LaBSEOntologyEngine()
# Khởi tạo sẵn mô hình LaBSE và toàn bộ cache vector khi bật server để truy vấn trên UI mượt tức thì (~25ms)
engine._ensure_model()
engine.get_corpus_embeddings(mode="frame_and_gloss")
engine.get_corpus_embeddings(mode="gloss_only")
engine.get_corpus_embeddings(mode="raw_and_frame")
engine.get_corpus_embeddings(mode="raw_only")


def _clean_null(val) -> str:
    if val is None:
        return ""
    s = str(val).strip()
    return "" if s.lower() in ["null", "none", "nan"] else s


def call_groq_llm(idiom_input: str) -> tuple[dict, float, str]:
    """Gọi Groq API với model cấu hình trong file .env để trích xuất 4 trục tiêu chí & nghĩa Gloss."""
    groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
    groq_model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b").strip()

    if not groq_api_key:
        raise HTTPException(
            status_code=400,
            detail="Không tìm thấy GROQ_API_KEY trong file .env!"
        )

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    payload = {
        "model": groq_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Phân tích thành ngữ/tục ngữ này: {idiom_input}"},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
    }

    t0 = time.time()
    try:
        resp = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=35,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lỗi kết nối Groq API: {e}")

    elapsed_ms = round((time.time() - t0) * 1000, 1)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=f"Groq API lỗi: {resp.text}")

    try:
        content = resp.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed, elapsed_ms, groq_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể đọc JSON từ LLM: {e}")


class FullFlowRequest(BaseModel):
    idiom: str
    top_k: Optional[int] = 10


class ManualMatchRequest(BaseModel):
    idiom: str
    en_idiom_suggested: Optional[str] = ""
    gloss_vi: Optional[str] = ""
    gloss_en: Optional[str] = ""
    boi_canh: Optional[str] = ""
    hanh_dong: Optional[str] = ""
    ket_qua: Optional[str] = ""
    muc_dich: Optional[str] = ""
    lang: Optional[str] = "vi"
    top_k: Optional[int] = 10


class SaveIdiomRequest(BaseModel):
    thanh_ngu_vn: str
    thanh_ngu_en: str
    boi_canh: Optional[str] = ""
    hanh_dong: Optional[str] = ""
    ket_qua: Optional[str] = ""
    muc_dich: Optional[str] = ""
    giai_thich_vn: Optional[str] = ""
    giai_thich_en: Optional[str] = ""


@app.get("/api/info")
def api_info():
    return {
        "ok": True,
        "groq_model": os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
        "labse_model": engine.model_name,
        "corpus_size": len(engine.records),
        "weights": {"alpha_labse": engine.alpha, "beta_ontology": round(1 - engine.alpha, 2)},
        "thresholds": {
            "exact": engine.exact_threshold,
            "near": engine.near_threshold,
            "s_onto_near": engine.s_onto_near_threshold,
            "semantic_floor": engine.semantic_floor,
        },
        "criteria_catalog": CRITERIA_CATALOG,
    }


@app.get("/api/corpus")
def api_corpus():
    return {"ok": True, "records": engine.records}


@app.post("/api/pipeline/full-flow")
def api_full_flow(req: FullFlowRequest):
    """
    Chạy trọn vẹn 6 bước trong Flowchart:
    Bước 1: Nhận câu thành ngữ đầu vào.
    Bước 2:
      - Nếu câu ĐÃ CÓ SẴN trong Ontology (v-idiomV6.rdf): Lấy trực tiếp Description (rdfs:comment) và 4 trục tiêu chí của nó từ Ontology (KHÔNG gọi LLM tự suy luận).
      - Nếu là câu MỚI hoàn toàn: Gọi LLM (Groq API + model trong .env) tách nghĩa bóng Gloss & 4 trục tiêu chí.
    Bước 3: Ghép chuỗi '[Khung Bản thể học] : <Nghĩa bóng Gloss>'.
    Bước 4A & 4B: Mã hóa LaBSE 768 chiều & Đối soát Khung Bản thể học.
    Bước 5: Tính điểm S_hybrid, lọc sàn S_Gloss >= 0.60 và phân nhánh 3 mức ngưỡng.
    """
    idiom_str = (req.idiom or "").strip()
    if not idiom_str:
        raise HTTPException(status_code=400, detail="Vui lòng nhập câu thành ngữ cần phân tích.")

    # Bước 2: Kiểm tra xem câu nhập đã có sẵn trong Ontology (v-idiomV6.rdf) chưa
    onto_rec = engine.lookup_ontology_record(idiom_str)
    if onto_rec is not None:
        llm_ms = 0.0
        source_type = "ONTOLOGY_V6"
        model_used = f"Ontology Lookup (v-idiomV6.rdf — {onto_rec['frame_name']})"
        active_lang = onto_rec["lang"]
        bc = onto_rec["bc"]
        hd = onto_rec["hd"]
        kq = onto_rec["kq"]
        md = onto_rec["md"]
        siblings_str = ", ".join(onto_rec.get("siblings", []))
        if active_lang == "vi":
            vi_idiom = onto_rec["idiom"]
            en_suggested = siblings_str
            gloss_vi = onto_rec["gloss"]
            gloss_en = ""
        else:
            vi_idiom = onto_rec["idiom"]
            en_suggested = siblings_str
            gloss_vi = ""
            gloss_en = onto_rec["gloss"]
        llm_json = {
            "source": "ONTOLOGY_V6",
            "frame_name": onto_rec["frame_name"],
            "idiom": onto_rec["idiom"],
            "lang": active_lang,
            "rdfs_comment": onto_rec["gloss"],
            "Bối_cảnh": bc,
            "Hành_động": hd,
            "Kết_quả": kq,
            "Mục_đích": md,
        }
    else:
        source_type = "LLM"
        llm_json, llm_ms, model_used = call_groq_llm(idiom_str)
        active_lang = "vi"
        vi_idiom = _clean_null(llm_json.get("Thành_ngữ_Tiếng_Việt")) or idiom_str
        en_suggested = _clean_null(llm_json.get("Thành_ngữ_Tiếng_Anh_Gợi_Ý")) or _clean_null(llm_json.get("Thành_ngữ_Tiếng_Anh"))
        bc = _clean_null(llm_json.get("Bối_cảnh"))
        hd = _clean_null(llm_json.get("Hành_động"))
        kq = _clean_null(llm_json.get("Kết_quả"))
        md = _clean_null(llm_json.get("Mục_đích"))
        gloss_vi = _clean_null(llm_json.get("Giải_thích_nghĩa_Tiếng_Việt"))
        gloss_en = _clean_null(llm_json.get("Giải_thích_nghĩa_Tiếng_Anh"))

    # Bước 3, 4A, 4B, 5: Chạy LaBSE + Bản thể học
    t1 = time.time()
    hybrid_res = engine.match_idiom(
        idiom_surface=vi_idiom,
        gloss_vi=gloss_vi,
        gloss_en=gloss_en,
        bc=bc,
        hd=hd,
        kq=kq,
        md=md,
        lang=active_lang,
        mode="frame_and_gloss",
        top_k=req.top_k or 10,
    )
    labse_ms = round((time.time() - t1) * 1000, 1)

    return {
        "ok": True,
        "timing": {
            "llm_ms": llm_ms,
            "labse_ontology_ms": labse_ms,
            "total_ms": round(llm_ms + labse_ms, 1),
        },
        "llm_step": {
            "source": source_type,
            "frame_name": onto_rec["frame_name"] if onto_rec else "",
            "model": model_used,
            "raw_output": llm_json,
            "thanh_ngu_vn": vi_idiom,
            "thanh_ngu_en_goi_y": en_suggested,
            "boi_canh": bc,
            "hanh_dong": hd,
            "ket_qua": kq,
            "muc_dich": md,
            "giai_thich_vn": gloss_vi,
            "giai_thich_en": gloss_en,
        },
        "hybrid_step": hybrid_res,
    }


@app.post("/api/pipeline/re-evaluate")
def api_re_evaluate(req: ManualMatchRequest):
    """
    Chạy lại trực tiếp bước 3 -> 5 (LaBSE + Bản thể học) khi người dùng chỉnh sửa
    tiêu chí hoặc nghĩa Gloss trên UI mà không cần gọi lại LLM.
    """
    t0 = time.time()
    hybrid_res = engine.match_idiom(
        idiom_surface=req.idiom.strip(),
        gloss_vi=(req.gloss_vi or "").strip(),
        gloss_en=(req.gloss_en or "").strip(),
        bc=(req.boi_canh or "").strip(),
        hd=(req.hanh_dong or "").strip(),
        kq=(req.ket_qua or "").strip(),
        md=(req.muc_dich or "").strip(),
        lang=req.lang or "vi",
        mode="frame_and_gloss",
        top_k=req.top_k or 10,
    )
    labse_ms = round((time.time() - t0) * 1000, 1)
    return {
        "ok": True,
        "timing": {"labse_ontology_ms": labse_ms},
        "hybrid_step": hybrid_res,
    }


@app.post("/api/pipeline/save")
def api_save_idiom(req: SaveIdiomRequest):
    """Bước 6: Lưu vào bản sao CSV, RDF Ontology và cập nhật Vector .npz trong labse_pipeline/data/."""
    if not req.thanh_ngu_vn or not req.thanh_ngu_en:
        raise HTTPException(status_code=400, detail="Cần có cả Thành ngữ Tiếng Việt và Tiếng Anh.")

    res = engine.save_idiom_to_local_store(
        vi_name=req.thanh_ngu_vn,
        en_name=req.thanh_ngu_en,
        bc=req.boi_canh or "",
        hd=req.hanh_dong or "",
        kq=req.ket_qua or "",
        md=req.muc_dich or "",
        vi_gloss=req.giai_thich_vn or "",
        en_gloss=req.giai_thich_en or "",
    )
    return {
        "ok": True,
        "msg": f"Đã lưu thành công vào Bảng dữ liệu, RDF Ontology (Khung: {res['frame_name']}) & cập nhật Vector LaBSE (STT: {res['stt']})!",
        "data": res,
    }


STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=False)
