# V-Idiom: Pipeline Lai Ghép LaBSE + Bản Thể Học (Neuro-Symbolic Hybrid)

Thư mục `labse_pipeline/` là một nhánh thực nghiệm **hoàn toàn độc lập**, triển khai phương pháp kết hợp **Mô hình ngôn ngữ đa ngữ LaBSE (Language-agnostic BERT Sentence Embedding)** và **Bản thể học (Ontology OWL 2)** cho bài toán căn chỉnh và suy luận đồng nghĩa thành ngữ Tiếng Việt – Tiếng Anh.

> **Cam kết cô lập dữ liệu:** Toàn bộ dữ liệu CSV, RDF, Vector Cache và API trong thư mục này hoạt động riêng biệt tại `labse_pipeline/data/` (cổng `8001`), **không chỉnh sửa hay ảnh hưởng** tới bất kỳ file nào của dự án gốc.

---

## 1. Kiến trúc Phương pháp luận (Methodology)

### 1.1. Công thức Ghép chuỗi Neo Bản thể học (Ontology-Grounded Gloss)
Để giải quyết triệt để **bẫy nghĩa đen (Metaphor Trap)** của thành ngữ và **bẫy trùng khung giả (False Positive Frame)** của Ontology thuần, chuỗi đưa vào mô hình **LaBSE** được chuẩn hóa theo cấu trúc:

$$\text{Input}_{\text{LaBSE}} = \text{"[Bối cảnh: } BC \text{ | Hành động: } HD \text{ | Kết quả: } KQ \text{ | Mục đích: } MD \text{] : } \text{Nghĩa bóng Gloss"}$$

### 1.2. Công thức Tính Điểm Lai Ghép ($S_{\text{hybrid}}$)
Với hai thành ngữ $A$ và $B$:
1. **Điểm tương đồng ngữ nghĩa LaBSE ($S_{\text{LaBSE}} \in [-1, 1]$):**
   $$S_{\text{LaBSE}}(A, B) = \cos\big(\text{LaBSE}(\text{Input}_A), \text{LaBSE}(\text{Input}_B)\big)$$
2. **Điểm tương đồng cấu trúc Khung Bản thể học ($S_{\text{onto}} \in [0, 1]$):**
   * Tính độ khớp có trọng số trên 4 trục: Kết quả ($0.35$), Hành động ($0.30$), Bối cảnh ($0.20$), Mục đích ($0.15$).
   * **Luật Phủ quyết Nhân - Quả (Causal Hard Veto):** Nếu 2 câu có Kết quả đối lập trực tiếp (ví dụ `KQ_Thành_công` vs `KQ_Thất_bại`) hoặc lệch hoàn toàn cả Hành động lẫn Kết quả $\rightarrow S_{\text{onto}} = 0$.
3. **Điểm Tổng hợp ($S_{\text{hybrid}}$):**
   $$S_{\text{hybrid}}(A, B) = 0.65 \cdot S_{\text{LaBSE}}(A, B) + 0.35 \cdot S_{\text{onto}}(A, B)$$

### 1.3. Hệ thống Ngưỡng Quyết định (Thresholds)
* **Điều kiện sàn ngữ nghĩa (Semantic Floor):** Bắt buộc $S_{\text{LaBSE}} \ge 0.62$. Nếu $S_{\text{onto}} = 1.0$ (trùng Khung) nhưng $S_{\text{LaBSE}} < 0.62$ $\rightarrow$ Hệ thống tự động gắn cờ **`LOẠI_BỎ_TRÙNG_KHUNG_GIẢ`** (ví dụ: loại bỏ cặp *"Của thiên trả địa"* và *"Của rẻ là của ôi"*).
* **Mức 1 — Đồng nghĩa Tuyệt đối:** $S_{\text{hybrid}} \ge 0.80$ và $S_{\text{LaBSE}} \ge 0.72$.
* **Mức 2 — Đồng nghĩa Mềm (Cận nghĩa):** $0.68 \le S_{\text{hybrid}} < 0.80$ và $S_{\text{LaBSE}} \ge 0.62$.
* **Mức 3 — Không đồng nghĩa:** $S_{\text{hybrid}} < 0.68$ hoặc $S_{\text{LaBSE}} < 0.62$.

---

## 2. Cấu trúc Thư mục

```text
labse_pipeline/
├── README.md                              # Tài liệu hướng dẫn và công thức phương pháp luận
├── requirements.txt                       # Các thư viện Python cần thiết
├── app.py                                 # FastAPI Server độc lập (chạy ở cổng 8001)
├── data/
│   ├── thanh_ngu_tuc_ngu_100_cau_v4.csv   # Bản sao độc lập của bộ 100 cặp thành ngữ
│   ├── v-idiomV5_final.rdf                # Bản sao độc lập của Ontology
│   ├── criteria_catalog.json              # Bể tiêu chí kèm nhãn song ngữ & định nghĩa
│   └── labse_vectors_*.npz                # Bộ nhớ đệm Vector 768 chiều của LaBSE
├── core/
│   ├── text_builder.py                    # Bộ ghép chuỗi [Khung Bản thể học] + [Nghĩa Gloss]
│   ├── ontology_scorer.py                 # Bộ chấm điểm cấu trúc Khung & Luật phủ quyết
│   └── labse_engine.py                    # Engine trung tâm LaBSE + Ontology Hybrid
├── experiments/
│   └── run_ablation_study.py              # Script đánh giá thực nghiệm 4 phương pháp & Case Study
└── diagrams/
    ├── generate_labse_flowchart.py        # Script vẽ Flowchart PNG
    └── labse_hybrid_flowchart.png         # Ảnh Flowchart phương pháp luận (300 DPI)
```

---

## 3. Hướng dẫn Chạy Thực nghiệm & Ứng dụng

### Chạy kịch bản đánh giá thực nghiệm (Ablation Study & Case Studies)
```bash
python3 labse_pipeline/experiments/run_ablation_study.py
```

### Khởi chạy API Server độc lập (Cổng 8001)
```bash
cd labse_pipeline
python3 app.py
```
