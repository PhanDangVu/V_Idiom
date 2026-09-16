# Bể Tiêu Chí Chung (Controlled Vocabulary) Cho Ontology Thành Ngữ

Đây là danh sách từ vựng kiểm soát (chuẩn hóa) được thiết kế để giải quyết vấn đề "bùng nổ thực thể". Thay vì mỗi thành ngữ tạo ra một tiêu chí mới, từ nay mọi thành ngữ sẽ chỉ được phép "lắp ráp" từ các tiêu chí có sẵn trong bể này.

Nếu có hai hoặc nhiều thành ngữ mang chung một bộ 4 tiêu chí (Bối cảnh, Hành động, Kết quả, Mục đích), hệ thống sẽ tự động xếp chúng vào chung 1 Khung, qua đó tự động suy luận ra chúng đồng nghĩa với nhau.

---

## 1. Bối cảnh (Contexts)
Đại diện cho môi trường, tình huống, hoặc trạng thái nền tảng diễn ra câu chuyện của thành ngữ.

| Individual (ID) | Ý nghĩa / Áp dụng cho trường hợp |
| :--- | :--- |
| `BC_Giao_tiep` | Tình huống nói chuyện, đàm phán, tranh luận, trao đổi thông tin. |
| `BC_Thuong_mai` | Mua bán, kinh doanh, trao đổi vật chất, tiền bạc. |
| `BC_Xung_dot` | Cãi vã, chiến đấu, mâu thuẫn giữa các cá nhân/tập thể. |
| `BC_Kho_khan` | Nghịch cảnh, nguy hiểm, áp lực công việc, tình huống tồi tệ. |
| `BC_Sinh_hoat` | Đời sống hàng ngày, thói quen sinh hoạt bình thường. |
| `BC_Rui_ro` | Tình huống mang tính đánh đổi cao, không chắc chắn. |
| `BC_Danh_gia` | Khi đang nhìn nhận, đánh giá, phán xét một đối tượng mới. |
| `BC_Hop_tac` | Làm việc nhóm, nhờ vả, tương trợ lẫn nhau. |
| `BC_Bao_mat` | Tình huống liên quan đến bí mật, thông tin ẩn giấu. |
| `BC_May_man` | Tình huống hiếm gặp, cơ hội bất ngờ xảy ra. |

---

## 2. Hành động (Actions)
Hành động cốt lõi mang tính quyết định (hoặc sai lầm) mà chủ thể thực hiện trong bối cảnh đó.

| Individual (ID) | Ý nghĩa / Áp dụng cho trường hợp |
| :--- | :--- |
| `HD_Tranh_ne` | Né tránh vấn đề, vòng vo, thoái thác trách nhiệm. |
| `HD_Doi_mat` | Chấp nhận đương đầu với rủi ro, khó khăn. |
| `HD_Lieu_linh` | Làm liều, làm việc mà không suy nghĩ kỹ, không kiểm tra. |
| `HD_Che_giau` | Cố tình giấu diếm, che đậy sự thật. |
| `HD_Tiet_lo` | Nói hớ, làm lộ bí mật, vạch áo cho người xem lưng. |
| `HD_Tan_cong` | Công kích, chê bai, làm hại người khác (hoặc nhầm người). |
| `HD_Danh_gia_sai`| Nhìn mặt bắt hình dong, nhận định sai về bản chất. |
| `HD_Tham_lam` | Ôm đồm quá nhiều việc, đòi hỏi quá mức. |
| `HD_Bo_cuoc` | Đầu hàng, buông xuôi giữa chừng. |
| `HD_No_luc` | Cày cuốc, thức khuya dậy sớm, dồn hết sức lực. |
| `HD_Thoi_phong` | Làm quá vấn đề lên, bé xé ra to. |
| `HD_Loi_dung` | Vô ơn, qua cầu rút ván, lợi dụng lòng tốt. |

---

## 3. Kết quả (Results)
Hệ quả trực tiếp sinh ra từ Hành động của chủ thể.

| Individual (ID) | Ý nghĩa / Áp dụng cho trường hợp |
| :--- | :--- |
| `KQ_Thanh_cong` | Đạt được mục tiêu, giải quyết triệt để vấn đề. |
| `KQ_That_bai` | Hỏng việc, thua cuộc, mất trắng. |
| `KQ_Ton_that` | Mất tiền, mua phải hàng giả, thiệt hại tài sản (Đắt cắt cổ). |
| `KQ_Ton_thuong` | Tổn hại thể chất, rước họa vào thân. |
| `KQ_Hoi_han` | Hối hận muộn màng, không thể thay đổi được gì nữa. |
| `KQ_Mat_thoi_gian`| Tốn công vô ích, không giải quyết được gì. |
| `KQ_Lo_tay` | Bí mật bị phơi bày, bị bắt quả tang. |
| `KQ_Bat_ngo` | Có niềm vui bất ngờ trong lúc khó khăn (Trong rủi có may). |
| `KQ_Toi_uu_hoa` | Đạt được nhiều mục đích cùng lúc (Một mũi tên trúng hai đích). |

---

## 4. Mục đích (Purposes)
Động cơ sâu xa khiến chủ thể thực hiện hành động đó.

| Individual (ID) | Ý nghĩa / Áp dụng cho trường hợp |
| :--- | :--- |
| `MD_Bao_ve_ban_than` | Giữ an toàn, tránh thương vong, tránh rắc rối. |
| `MD_Truc_loi` | Mong mỏi kiếm lợi nhuận tối đa, thỏa mãn lòng tham. |
| `MD_Giai_quyet_van_de`| Mong muốn hoàn thành công việc, đạt được đích đến. |
| `MD_The_hien` | Muốn chứng tỏ bản thân giỏi, tự cao tự đại. |
| `MD_Che_day` | Trốn tội, giấu lỗi lầm. |
| `MD_Thoa_man_to_mo` | Hành động chỉ vì tò mò chuyện người khác. |
| `MD_Gay_chu_y` | Thích làm trung tâm, muốn người khác chú ý. |
| `MD_Tiet_kiem` | Lười biếng, muốn nhanh gọn lẹ, tiết kiệm công sức. |
| `MD_Ha_be` | Muốn bêu xấu, tấn công danh dự kẻ khác. |

---

## 💡 Ví dụ áp dụng (Cơ chế Tái sử dụng)

Thay vì tạo ra vô số Khung rời rạc, hãy xem cách các thành ngữ kết hợp từ Bể tiêu chí này:

**Tổ hợp 1:** `BC_Thuong_mai` + `HD_Lieu_linh` + `KQ_Ton_that` + `MD_Tiet_kiem`
*   Thành ngữ khớp: *"Buy a pig in a poke"* (Anh), *"Mua mèo trong bao"* (Việt).
*   Hệ thống kiểm tra thấy chưa có Khung nào mang 4 tiêu chí này $\rightarrow$ Tạo **Khung A**.

**Tổ hợp 2:** `BC_Bao_mat` + `HD_Tiet_lo` + `KQ_Lo_tay` + `MD_Gay_chu_y`
*   Thành ngữ khớp: *"Spill the beans"* (Anh), *"Vạch áo cho người xem lưng"* (Việt).
*   Hệ thống tạo **Khung B**.

Giả sử sau này bạn nạp thêm câu *"Cái kim trong bọc có ngày lòi ra"*. Bạn phân tích và gán nó vào `BC_Bao_mat`, `HD_Tiet_lo`, `KQ_Lo_tay`, `MD_Gay_chu_y`. 
$\rightarrow$ Hệ thống tự nhận diện: *"À! Tổ hợp này y hệt Khung B"*. Nó sẽ tự động gán câu này vào **Khung B** mà không sinh thêm rác vào Ontology. Cả 3 câu tự động liên kết thành đồng nghĩa với nhau!
