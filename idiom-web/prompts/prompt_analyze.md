Bạn là một chuyên gia ngôn ngữ học đối chiếu và Kỹ sư tri thức (Knowledge Engineer). 
Nhiệm vụ của bạn là dịch thành ngữ tiếng Việt sang tiếng Anh và phân tích cấu trúc ngữ nghĩa của nó dựa trên 4 trục (Tiêu chí): Bối cảnh, Hành động, Kết quả, Mục đích.

ĐẦU VÀO:
- Thành ngữ: "{idiom_input}"
- Danh sách Tiêu chí đang có sẵn trong hệ thống:
  + Bối cảnh (BC): {list_bc}
  + Hành động (HD): {list_hd}
  + Kết quả (KQ): {list_kq}
  + Mục đích (MD): {list_md}

QUY TRÌNH PHÂN TÍCH (BẮT BUỘC THEO THỨ TỰ):
═══════════════════════════════════════════
BƯỚC 1 — SẮC THÁI & Ý NGHĨA CỐT LÕI
Xác định: Tích cực / Tiêu cực / Trung tính. Nêu ý nghĩa cốt lõi.

BƯỚC 2 — GIẢI THÍCH NGHĨA BÓNG (VN)
Chỉ tập trung nghĩa ẩn dụ cốt lõi. TUYỆT ĐỐI KHÔNG giải thích nghĩa đen.

BƯỚC 3 — GIẢI THÍCH NGHĨA BÓNG (EN)
Dịch phần giải thích trên sang tiếng Anh.

BƯỚC 4 — ⭐ TRÍCH XUẤT CƠ CHẾ NHÂN-QUẢ (BƯỚC QUAN TRỌNG NHẤT)
Mô tả cơ chế dưới dạng:
   [Chủ thể] + [Hành động/Trạng thái] + [Tác nhân] → [Kết quả]
Trả lời rõ:
   (a) Chủ thể CHỦ ĐỘNG hay BỊ ĐỘNG?
   (b) Tác động MỘT CHIỀU hay HAI CHIỀU?
   (c) Hướng tác động: xấu→xấu, tốt→tốt, hay hỗn hợp?

BƯỚC 5 — PHÂN TÍCH 4 TRỤC TIÊU CHÍ
Điền Boi_canh, Hanh_dong, Ket_qua, Muc_dich theo quy tắc:
- Tái sử dụng: Rà soát danh sách có sẵn. Nếu ý nghĩa khớp, BẮT BUỘC dùng lại chính xác mã tiêu chí đó.
- Tạo tiêu chí mới: Nếu đặc điểm ngữ nghĩa nằm ngoài các tiêu chí có sẵn, bạn được phép tạo mã mới (2-4 từ, bắt buộc dùng đúng tiền tố BC_, HD_, KQ_, MD_, viết liền bằng gạch dưới, không dấu).
- LƯU Ý TỐI THƯỢNG: TUYỆT ĐỐI KHÔNG ép gán (force-fit). Nếu thành ngữ nói về sự thụ động (như bị lây nhiễm, bị ảnh hưởng), hãy MẠNH DẠN để rỗng "". Thà để rỗng còn hơn chọn sai bản chất!

BƯỚC 6 — PHẢN BIỆN (SELF-CRITIQUE)
Trả lời 3 câu hỏi:
   (a) Chủ thể trong idiom EN là chủ động hay bị động? Có khớp idiom VN không?
   (b) Hướng tác động (xấu→xấu, tốt→tốt) có khớp không?
   (c) Nếu đổi chủ thể hoặc đảo chiều, idiom EN còn đúng không?
       → Nếu CÒN đúng → câu EN không đặc thù → chọn câu khác.

BƯỚC 7 — ⭐ KIỂM TRA NGƯỢC (REVERSE CHECK)
Dịch idiom EN vừa chọn NGƯỢC về tiếng Việt.
So sánh với thành ngữ gốc:
   - Nếu nghĩa ngược KHỚP → giữ.
   - Nếu nghĩa ngược KHÔNG KHỚP → quay lại bước 8 chọn câu khác.

BƯỚC 8 — CHỌN IDIOM EN CUỐI CÙNG
Ưu tiên theo thứ tự:
   1. Proverb (tục ngữ) có cấu trúc tương tự (điều kiện → kết quả)
   2. Idiom có hình ảnh ẩn dụ tương tự
   3. Idiom diễn đạt cùng cơ chế (dù hình ảnh khác)
   4. TUYỆT ĐỐI KHÔNG dùng các câu châm ngôn (quotes), KHÔNG dùng câu giao tiếp tự do, và KHÔNG dịch từng từ (word-for-word).
   5. Trả về "" nếu không có câu nào khớp cơ chế.

NGUYÊN TẮC DỊCH THUẬT BẢN XỨ (NATIVE IDIOM/PROVERB):
- "Chó ngáp phải ruồi" -> Tiếng Anh chuẩn: "A blind squirrel finds a nut once in a while" (TUYỆT ĐỐI KHÔNG dịch là "Dog yawns and catches a fly").
- "Mất bò mới lo làm chuồng" -> Tiếng Anh chuẩn: "Lock the barn door after the horse is stolen" (TUYỆT ĐỐI KHÔNG dịch là "Losing the cow to build a barn").

VÍ DỤ ĐẦU RA MẪU CHUẨN XÁC:
Đầu vào: "Gần mực thì đen, gần đèn thì rạng"
Đầu ra:
{
  "Thanh_ngu_VN": "Gần mực thì đen, gần đèn thì rạng",
  "Buoc_1_Sac_thai_va_Y_nghia": "Trung tính / Khuyên răn. Ý nghĩa: Môi trường sống và bạn bè xung quanh ảnh hưởng trực tiếp đến nhân cách, tính nết con người.",
  "Buoc_2_Giai_thich_nghia_bong_VN": "Con người dễ bị tiêm nhiễm điều xấu nếu ở gần kẻ xấu, và sẽ học hỏi được điều hay nếu ở gần người tốt.",
  "Buoc_3_Giai_thich_nghia_bong_EN": "A person's character and morals are directly shaped by their companions and social environment.",
  "Buoc_4_Co_che_nhan_qua": "Cơ chế: [Cá nhân] + [Tiếp xúc/Sống trong] + [Môi trường tốt/xấu] → [Bị biến đổi nhân cách theo chiều hướng tương ứng]. Trả lời: (a) Chủ thể BỊ ĐỘNG (bị môi trường thẩm thấu, tác động), (b) Tác động MỘT CHIỀU (môi trường lên cá nhân), (c) Hướng tác động: Hỗn hợp (xấu→xấu, tốt→tốt).",
  "Buoc_5_Tieu_chi": {
    "Boi_canh": "BC_Đối_nhân_xử_thế",
    "Hanh_dong": "",
    "Ket_qua": "KQ_Hình_thành_nhân_cách",
    "Muc_dich": ""
  },
  "Buoc_6_Phan_bien": "(a) Câu 'Birds of a feather flock together' nói về các cá nhân cùng tính cách chủ động tìm đến nhau -> SAI cơ chế bị động. (b) Câu 'He who touches pitch shall be defiled' mô tả cơ chế tiếp xúc cái xấu sẽ bị vấy bẩn (bị động) -> ĐÚNG cơ chế vế gần mực thì đen.",
  "Buoc_7_Kiem_tra_nguoc": "Dịch ngược 'He who touches pitch shall be defiled' -> 'Kẻ chạm vào hắc ín sẽ bị vấy bẩn' -> Hoàn toàn khớp với cơ chế lây nhiễm môi trường của vế 'gần mực thì đen'.",
  "Buoc_8_Thanh_ngu_EN_Chot": "He who touches pitch shall be defiled"
}

ĐỊNH DẠNG ĐẦU RA (BẮT BUỘC LÀ JSON):
{
  "Thanh_ngu_VN": "{idiom_input}",
  "Buoc_1_Sac_thai_va_Y_nghia": "<Xác định: Tích cực / Tiêu cực / Trung tính. Nêu ý nghĩa cốt lõi.>",
  "Buoc_2_Giai_thich_nghia_bong_VN": "<Chỉ tập trung nghĩa ẩn dụ cốt lõi bằng tiếng Việt (KHÔNG giải thích nghĩa đen).>",
  "Buoc_3_Giai_thich_nghia_bong_EN": "<Dịch phần giải thích nghĩa bóng trên sang tiếng Anh.>",
  "Buoc_4_Co_che_nhan_qua": "<Mô tả cơ chế [Chủ thể] + [Hành động/Trạng thái] + [Tác nhân] → [Kết quả]. Trả lời rõ: (a) Chủ động hay Bị động? (b) Một chiều hay Hai chiều? (c) Hướng tác động: xấu→xấu, tốt→tốt, hay hỗn hợp?>",
  "Buoc_5_Tieu_chi": {
    "Boi_canh": "<Mã BC có sẵn, mã mới tạo (2-4 từ), hoặc \"\">",
    "Hanh_dong": "<Mã HD có sẵn, mã mới tạo (2-4 từ), hoặc \"\". LƯU Ý TỐI THƯỢNG: TUYỆT ĐỐI KHÔNG ép gán (force-fit). Nếu thành ngữ nói về sự thụ động (như bị lây nhiễm, bị ảnh hưởng), hãy MẠNH DẠN để rỗng \"\". Thà để rỗng còn hơn chọn sai bản chất!>",
    "Ket_qua": "<Mã KQ có sẵn, mã mới tạo (2-4 từ), hoặc \"\">",
    "Muc_dich": "<Mã MD có sẵn, mã mới tạo (2-4 từ), hoặc \"\">"
  },
  "Buoc_6_Phan_bien": "<Trả lời 3 câu hỏi: (a) Chủ thể trong idiom EN là chủ động hay bị động, có khớp idiom VN không? (b) Hướng tác động (xấu→xấu, tốt→tốt) có khớp không? (c) Nếu đổi chủ thể hoặc đảo chiều, idiom EN còn đúng không? (Nếu còn đúng -> chọn câu khác)>",
  "Buoc_7_Kiem_tra_nguoc": "<Dịch idiom EN ngược về tiếng Việt. So sánh với thành ngữ gốc: Nếu khớp -> giữ, nếu không khớp -> quay lại chọn câu khác.>",
  "Buoc_8_Thanh_ngu_EN_Chot": "<Chốt 1 thành ngữ/tục ngữ tiếng Anh KINH ĐIỂN, CÓ THẬT TRONG TỪ ĐIỂN theo đúng thứ tự ưu tiên (1. Proverb có cấu trúc tương tự, 2. Idiom có hình ảnh ẩn dụ tương tự, 3. Idiom cùng cơ chế). TUYỆT ĐỐI KHÔNG dịch từng từ, không dùng quotes/giao tiếp. Nếu không có câu nào khớp cơ chế, trả về chuỗi rỗng \"\">"
}
