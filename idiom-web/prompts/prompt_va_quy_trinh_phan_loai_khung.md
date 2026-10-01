# Quy Trình Phân Loại Thành Ngữ & Khai Báo Khung Tự Động (v4)

Tài liệu này hướng dẫn chi tiết quy trình chuẩn hóa để **Xác định Khung tiêu chí** cho một câu thành ngữ/tục ngữ mới nhập vào, đối soát với Cơ sở dữ liệu Ontology v4, và thực hiện quyết định:
- **Trường hợp 1 (Khung đã tồn tại):** Xuất danh sách các câu thành ngữ **đồng nghĩa** (cả Tiếng Việt & Tiếng Anh) đang chia sẻ chung khung này.
- **Trường hợp 2 (Khung chưa tồn tại):** Khai báo **Khung mới (New Frame)**, khởi tạo mã STT tiếp theo và đề xuất cập nhật vào Ontology.

---

## 1. Sơ Đồ Quy Trình (Decision Flowchart)

```
[Nhập Thành Ngữ Mới]
       │
       ▼
[System Prompt LLM] ──► Trích xuất 4 Thuộc tính Tiêu chí (BC_, HD_, KQ_, MD_)
       │
       ▼
[Bộ Đối Soát Khung (Matcher)] ◄── Đối chiếu với CSĐL Ontology (thanh_ngu_tuc_ngu_100_cau_v4.csv)
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[Khung ĐÃ TỒN TẠI (Matched)]            [Khung MỚI (No Match)]
       │                                         │
       ├─► Hiện Mã STT Khung Trùng               ├─► Khai báo Khung Mới (STT = Max + 1)
       ├─► Hiện Các Câu Đồng Nghĩa (Việt & Anh) ├─► Hiển thị Bộ mã Tiêu chí mới
       └─► Hiển thị Lời giải nghĩa hệ thống      └─► Đề xuất Cập nhật vào CSĐL CSV/OWL
```

---

## 2. System Prompt Dành Cho LLM (Frame Extractor)

Dán đoạn System Prompt dưới đây vào LLM (ChatGPT, Gemini, Claude) để yêu cầu mô hình đóng vai trò **Bộ trích xuất Khung Tiêu Chí**:

```markdown
Bạn là một Chuyên gia Bản thể học (Ontology Engineer) và Ngôn ngữ học Song ngữ Việt - Anh.
Nhiệm vụ của bạn là phân tích một câu thành ngữ/tục ngữ do người dùng nhập vào và trích xuất đúng Khung tiêu chí ngữ nghĩa (Semantic Frame) dựa trên Bể tiêu chí v4.

### ĐÃ LƯU Ý RÀNG BUỘC
1. Bắt buộc chọn ÍT NHẤT 2 TIÊU CHÍ và tối đa 4 tiêu chí trong các nhóm (`BC_`, `HD_`, `KQ_`, `MD_`). KHÔNG ĐƯỢC chỉ trả về 1 tiêu chí đơn lẻ.
2. Không cưỡng ép gán mã giả. Nếu câu là tục ngữ chỉ sự thật/quy luật tự nhiên không có Hành động hay Mục đích, hãy để ô `HD_` hoặc `MD_` là `null`.
3. Chỉ sử dụng các Mã Tiêu Chí thuộc danh mục 79 mã dưới đây:

### DANH MỤC 79 MÃ TIÊU CHÍ HỢP LỆ
- Bối cảnh (BC_): BC_Giao_tiếp, BC_Thương_mại, BC_Xung_đột, BC_Nguy_hiểm, BC_Sinh_hoạt, BC_Rủi_ro, BC_Đánh_giá, BC_Bảo_mật, BC_Sự_kiện_hiếm, BC_Cơ_hội, BC_Cảm_xúc, BC_Thực_thi_mục_tiêu, BC_Hậu_quả, BC_Nhận_thức, BC_Đối_nhân_xử_thế, BC_Bệnh_tật, BC_Cuộc_sống, BC_Gia_đình, BC_Lao_động, BC_Đạo_đức, BC_Môi_trường_mới.
- Hành động (HD_): HD_Né_tránh, HD_Đối_mặt, HD_Liều_lĩnh, HD_Tấn_công, HD_Đánh_giá_sai, HD_Tham_lam, HD_Nỗ_lực, HD_Thổi_phồng, HD_Lợi_dụng, HD_Che_giấu, HD_Trì_hoãn, HD_Nắm_bắt, HD_Kiên_nhẫn, HD_Tiêu_xài_hoang_phí, HD_Kìm_nén_cảm_xúc, HD_Thích_ứng, HD_Bắt_chước, HD_Đồng_lòng, HD_So_sánh.
- Kết quả (KQ_): KQ_Thành_công, KQ_Thất_bại, KQ_Tổn_thất_tài_sản, KQ_Tổn_thương, KQ_Hối_hận, KQ_Lộ_tẩy, KQ_May_mắn, KQ_Tối_ưu_hóa, KQ_Mất_quan_hệ, KQ_Bình_yên, KQ_An_toàn, KQ_Đạt_được_thỏa_thuận, KQ_Kết_thúc, KQ_Bị_khống_chế, KQ_Gieo_tai_họa, KQ_Gắn_kết, KQ_Nhầm_lẫn, KQ_Hòa_nhập, KQ_Tương_xứng_giá_trị, KQ_Gặp_trở_ngại, KQ_Xác_nhận_sự_thật, KQ_Tích_lũy_kinh_nghiệm, KQ_Tích_lũy_tri_thức, KQ_Trân_trọng_bản_chất, KQ_Hình_thành_nhân_cách, KQ_Khác_biệt_quan_điểm, KQ_Tồn_tại_khuyết_điểm, KQ_Lưu_danh_hậu_thế, KQ_Đối_mặt_thực_tế, KQ_Ngoại_cảnh_chi_phối.
- Mục đích (MD_): MD_Bảo_vệ_bản_thân, MD_Giải_quyết_vấn_đề, MD_Che_đậy, MD_Hạ_bệ, MD_Né_tránh_trách_nhiệm, MD_Giao_hảo, MD_Hòa_giải, MD_Trân_trọng_thời_gian, MD_Bảo_vệ_tài_sản.

### ĐỊNH DẠNG ĐẦU RA (JSON DỰNG SẴN)
Trả về duy nhất định dạng JSON sau:
```json
{
  "Thành_ngữ_Gốc": "<Chuỗi_thành_ngữ_nhập_vào>",
  "Bối_cảnh": "<Mã_BC_hoặc_null>",
  "Hành_động": "<Mã_HD_hoặc_null>",
  "Kết_quả": "<Mã_KQ_hoặc_null>",
  "Mục_đích": "<Mã_MD_hoặc_null>",
  "Giải_thích_nghĩa_Tiếng_Việt": "<Đoạn_diễn_giải_nghĩa_ngắn_gọn>",
  "Giải_thích_nghĩa_Tiếng_Anh": "<English_gloss_definition>"
}
```
```

---

## 3. Mã Python Đối Soát Khung Tự Động (`idiom_frame_pipeline.py`)

Dưới đây là mã Python hoàn chỉnh đọc trực tiếp file CSV database (`thanh_ngu_tuc_ngu_100_cau_v4.csv`) và nhận JSON từ LLM để đưa ra kết quả phân loại:

```python
import pandas as pd
import json

class IdiomOntologyMatcher:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.frame_db = {}
        self._build_frame_index()

    def _build_frame_index(self):
        """Tạo chỉ mục Khung từ Cơ sở dữ liệu CSV."""
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
        """Đối soát JSON từ LLM với CSĐL Ontology."""
        bc = str(extracted_json.get('Bối_cảnh') or '').strip()
        hd = str(extracted_json.get('Hành_động') or '').strip()
        kq = str(extracted_json.get('Kết_quả') or '').strip()
        md = str(extracted_json.get('Mục_đích') or '').strip()
        
        # Xử lý chuỗi rỗng
        if bc.lower() in ['null', 'none']: bc = ''
        if hd.lower() in ['null', 'none']: hd = ''
        if kq.lower() in ['null', 'none']: kq = ''
        if md.lower() in ['null', 'none']: md = ''

        key = (bc, hd, kq, md)
        input_idiom = extracted_json.get('Thành_ngữ_Gốc', '')

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

# Chạy thử nghiệm
matcher = IdiomOntologyMatcher('thanh_ngu_tuc_ngu_100_cau_v4.csv')

# Ví dụ 1: Nhập câu đồng nghĩa với STT 8
res1 = matcher.process_llm_json({
    "Thành_ngữ_Gốc": "Chơi với dao có ngày đứt tay",
    "Bối_cảnh": "BC_Rủi_ro",
    "Hành_động": "HD_Liều_lĩnh",
    "Kết_quả": "KQ_Gieo_tai_họa",
    "Mục_đích": None
})
print("=== VÍ DỤ 1: TRÙNG KHUNG (CÂU ĐỒNG NGHĨA) ===")
print(json.dumps(res1, ensure_ascii=False, indent=2))

# Ví dụ 2: Nhập câu mang khung mới hoàn toàn
res2 = matcher.process_llm_json({
    "Thành_ngữ_Gốc": "Một con ngựa đau cả tàu bỏ cỏ",
    "Bối_cảnh": "BC_Gia_đình",
    "Hành_động": "HD_Đồng_lòng",
    "Kết_quả": "KQ_Tổn_thương",
    "Mục_đích": "MD_Giao_hảo",
    "Giải_thích_nghĩa_Tiếng_Việt": "Khi một người trong tập thể gặp hoạn nạn thì cả tập thể đều lo lắng, sẻ chia.",
    "Giải_thích_nghĩa_Tiếng_Anh": "When one member of a group suffers, all others feel empathy and share the pain."
})
print("\n=== VÍ DỤ 2: KHUNG MỚI ===")
print(json.dumps(res2, ensure_ascii=False, indent=2))
```

---

## 4. Ví Dụ Kết Quả Thực Tế (Execution Outputs)

### Ví dụ A: Khi Nhập Câu Đồng Nghĩa (Trùng Khung STT 8)
* **Câu nhập vào:** `"Chơi với dao có ngày đứt tay"`
* **Kết quả trả về:**
```json
{
  "Kết_Quả_Đánh_Giá": "KHUNG_ĐÃ_TỒN_TẠI",
  "Mã_Khung_STT": 8,
  "Thành_Ngữ_Mới_Nhập": "Chơi với dao có ngày đứt tay",
  "Bộ_Tiêu_Chí_Khung": {
    "Bối_cảnh": "BC_Rủi_ro",
    "Hành_động": "HD_Liều_lĩnh",
    "Kết_quả": "KQ_Gieo_tai_họa",
    "Mục_đích": null
  },
  "Các_Câu_Đồng_Nghĩa_Cùng_Khung": {
    "Tiếng_Việt": [
      "Đi_đêm_lắm_có_ngày_gặp_ma"
    ],
    "Tiếng_Anh": [
      "The_pitcher_goes_so_often_to_the_well_that_it_is_broken_at_last"
    ]
  },
  "Giải_Thích_Nghĩa_Gốc": {
    "Tiếng_Việt": "Làm điều sai trái lén lút nhiều lần thì thế nào cũng có ngày gặp tai họa.",
    "Tiếng_Anh": "Repeatedly doing risky or wrong things will inevitably lead to exposure or disaster."
  }
}
```

### Ví dụ B: Khi Nhập Câu Mang Khung Mới
* **Câu nhập vào:** `"Một con ngựa đau cả tàu bỏ cỏ"`
* **Kết quả trả về:**
```json
{
  "Kết_Quả_Đánh_Giá": "KHUNG_MỚI",
  "Mã_Khung_STT_Khởi_Tạo": 101,
  "Thành_Ngữ_Mới_Nhập": "Một con ngựa đau cả tàu bỏ cỏ",
  "Bộ_Tiêu_Chí_Khung_Mới": {
    "Bối_cảnh": "BC_Gia_đình",
    "Hành_động": "HD_Đồng_lòng",
    "Kết_quả": "KQ_Tổn_thương",
    "Mục_đích": "MD_Giao_hảo"
  },
  "Thông_Báo": "Không tìm thấy khung trùng khớp. Đã đề xuất tạo Khung mới STT 101.",
  "Giải_Thích_Nghĩa_Đề_Xuất": {
    "Tiếng_Việt": "Khi một người trong tập thể gặp hoạn nạn thì cả tập thể đều lo lắng, sẻ chia.",
    "Tiếng_Anh": "When one member of a group suffers, all others feel empathy and share the pain."
  }
}
```
