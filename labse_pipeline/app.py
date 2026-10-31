import os
import json
import requests
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query as Q
from pydantic import BaseModel
from dotenv import load_dotenv

from core.labse_engine import LaBSEOntologyEngine
from core.text_builder import CRITERIA_CATALOG

# Tải biến môi trường từ thư mục hiện tại hoặc thư mục idiom-web cũ (chỉ đọc, không sửa)
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / "idiom-web" / ".env")
load_dotenv()

app = FastAPI(
    title="V-Idiom LaBSE + Ontology Hybrid API",
    description="API đối soát và suy luận đồng nghĩa thành ngữ Việt - Anh sử dụng LaBSE + Bản thể học (Độc lập)",
    version="1.0.0",
)

engine = LaBSEOntologyEngine()


class HybridQueryRequest(BaseModel):
    idiom: str
    gloss_vi: Optional[str] = ""
    gloss_en: Optional[str] = ""
    boi_canh: Optional[str] = ""
    hanh_dong: Optional[str] = ""
    ket_qua: Optional[str] = ""
    muc_dich: Optional[str] = ""
    lang: Optional[str] = "vi"
    mode: Optional[str] = "frame_and_gloss"
    top_k: Optional[int] = 10


@app.get("/api/health")
def health_check():
    return {
        "ok": True,
        "model": engine.model_name,
        "corpus_size": len(engine.records),
        "thresholds": {
            "exact": engine.exact_threshold,
            "near": engine.near_threshold,
            "semantic_floor": engine.semantic_floor,
        },
    }


@app.get("/api/criteria")
def list_criteria():
    return CRITERIA_CATALOG


@app.post("/api/hybrid/match")
def api_hybrid_match(req: HybridQueryRequest):
    """
    Endpoint đối soát thành ngữ bằng phương pháp Lai ghép:
    Ghép chuỗi '[Khung Bản thể học] + [Nghĩa Gloss]' -> Mã hóa LaBSE -> Kết hợp điểm S_LaBSE và S_onto.
    Nếu không truyền sẵn tiêu chí, hệ thống tự động dùng LaBSE Zero-Shot để gán tiêu chí từ Bể tiêu chí.
    """
    if not req.idiom or not req.idiom.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập thành ngữ.")

    res = engine.match_idiom(
        idiom_surface=req.idiom.strip(),
        gloss_vi=req.gloss_vi or "",
        gloss_en=req.gloss_en or "",
        bc=req.boi_canh or "",
        hd=req.hanh_dong or "",
        kq=req.ket_qua or "",
        md=req.muc_dich or "",
        lang=req.lang or "vi",
        mode=req.mode or "frame_and_gloss",
        top_k=req.top_k or 10,
    )
    return {"ok": True, "data": res}


if __name__ == "__main__":
    import uvicorn
    # Chạy ở cổng 8001 để hoàn toàn tách biệt với ứng dụng cũ ở cổng 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
