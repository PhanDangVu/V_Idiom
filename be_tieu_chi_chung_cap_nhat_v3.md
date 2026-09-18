# Bể Tiêu Chí Chung (Bản Cập Nhật v3 - Giới Hạn Tối Thiểu 2 Tiêu Chí)

Bản cập nhật **v3** nâng cấp toàn bộ hệ thống phân loại thành ngữ - tục ngữ Việt - Anh với nguyên tắc: **Mỗi câu thành ngữ/tục ngữ bắt buộc phải có ÍT NHẤT 2 TIÊU CHÍ** (kết hợp tự nhiên giữa _Bối cảnh_, _Hành động_, _Kết quả_, và _Mục đích_) để đảm bảo rõ nghĩa, không bị mơ hồ hay tối nghĩa khi truy vấn và suy luận trên Ontology.

---

## Nguyên Tắc Phân Loại v3

1. **Giới hạn tối thiểu 2 tiêu chí:** Không có câu nào chỉ mang 1 tiêu chí đơn lẻ. Việc kết hợp ít nhất 2 chiều thông tin (ví dụ: `Bối cảnh` + `Kết quả`, `Bối cảnh` + `Hành động`, `Hành động` + `Mục đích`) giúp định nghĩa chính xác và minh bạch diện mạo ngữ nghĩa của thành ngữ.
2. **Không cưỡng ép 4 tiêu chí:** Giữ nguyên tính tự nhiên và không gượng ép. Các câu không chứa Hành động hay Mục đích rõ ràng (như câu tục ngữ về sự thật/quy luật khách quan) sẽ dùng sự kết hợp linh hoạt giữa `Bối cảnh` và `Kết quả` thay vì gán mã giả.
3. **Chuẩn hóa định dạng:** Tên thành ngữ viết có dấu, phân cách bằng dấu `_`. Mã tiêu chí giữ đúng quy chuẩn `BC_`, `HD_`, `KQ_`, `MD_`.

---

## Danh Mục Bể Tiêu Chí Đầy Đủ v3

### 1. Bối Cảnh (Contexts) - Ký hiệu: `BC_` (21)

| Individual (ID)          | Ý nghĩa                                                  | Trạng thái |
| :----------------------- | :------------------------------------------------------- | :--------- |
| **BC_Giao_tiếp**         | Tình huống nói chuyện, đàm phán, phô trương ý kiến.      | Gốc        |
| **BC_Thương_mại**        | Mua bán, kinh doanh, trao đổi tiền bạc, giá cả.          | Gốc        |
| **BC*Xung*đột**          | Cãi vã, chiến đấu, mâu thuẫn, đối đầu.                   | Gốc        |
| **BC_Nguy_hiểm**         | Tình huống đe dọa đến an toàn, rủi ro cao.               | Gốc        |
| **BC_Sinh_hoạt**         | Đời sống hàng ngày, thói quen, sinh hoạt gia đình.       | Gốc        |
| **BC_Rủi_ro**            | Đánh cược, tình huống không chắc chắn, làm điều lén lút. | Gốc        |
| **BC_Đánh_giá**          | Nhìn nhận, phán xét người hoặc vật.                      | Gốc        |
| **BC_Bảo_mật**           | Tình huống liên quan đến bí mật, thông tin ẩn giấu.      | Gốc        |
| **BC_Sự_kiện_hiếm**      | Hiện tượng tự nhiên hoặc sự kiện hiếm gặp/bất ngờ.       | Gốc        |
| **BC_Cơ_hội**            | Thời cơ tốt xuất hiện.                                   | Gốc        |
| **BC_Cảm_xúc**           | Trạng thái tâm lý, xáo trộn nội tâm, so sánh.            | Gốc        |
| **BC_Thực_thi_mục_tiêu** | Quá trình đang nỗ lực đạt một đích đến.                  | Gốc        |
| **BC_Hậu_quả**           | Giai đoạn sự việc quá sát hoặc hậu quả đã xảy ra.        | Gốc        |
| **BC_Nhận_thức**         | Trạng thái biết, tin tưởng hoặc chứng kiến sự việc.      | Gốc        |
| **BC_Đối_nhân_xử_thế**   | Giao tiếp xã hội, ứng xử giữa người với người.           | Gốc        |
| **BC_Bệnh_tật**          | Tình trạng sức khỏe kém, bệnh tật.                       | Gốc        |
| **BC_Cuộc_sống**         | Quy luật đời sống, thực tế xã hội.                       | Mới v2     |
| **BC\_*Gia*đình**        | Quan hệ huyết thống, gia tộc, cha con, anh em.           | Mới v2     |
| **BC\_*Lao*động**        | Quá trình học tập, rèn luyện, lao động sản xuất.         | Mới v2     |
| **BC\_*Đạo*đức**         | Chuẩn mực đạo đức, nhân cách, lòng biết ơn.              | Mới v2     |
| **BC_Môi_trường_mới**    | Hoàn cảnh sống hoặc môi trường văn hóa mới.              | Mới v2     |

---

### 2. Hành Động (Actions) - Ký hiệu: `HD_` (19)

| Individual (ID)           | Ý nghĩa                                            | Trạng thái |
| :------------------------ | :------------------------------------------------- | :--------- |
| **HD_Né_tránh**           | Vòng vo, thoái thác, trốn tránh nguy cơ.           | Gốc        |
| **HD_Đối_mặt**            | Chấp nhận đương đầu, dấn thân vào gian khó.        | Gốc        |
| **HD_Liều_lĩnh**          | Làm điều sai trái lén lút, rủi ro cao.             | Gốc        |
| **HD_Tấn_công**           | Công kích, chê bai, làm hại người khác.            | Gốc        |
| **HD_Đánh_giá_sai**       | Nhìn mặt bắt hình dong, áp đặt chủ quan.           | Gốc        |
| **HD_Tham_lam**           | Ôm đồm, lấn tới, đòi hỏi vô lý.                    | Gốc        |
| **HD_Nỗ_lực**             | Làm việc chăm chỉ, dốc hết sức.                    | Gốc        |
| **HD_Thổi_phồng**         | Khoa trương, phô trương quá đà.                    | Gốc        |
| **HD_Lợi_dụng**           | Vô ơn, ăn cháo đá bát, đổ lỗi.                     | Gốc        |
| **HD_Che_giấu**           | Cố tình đậy điệm, giữ kín bí mật.                  | Gốc        |
| **HD_Trì_hoãn**           | Chậm trễ, ăn xổi ở thì, để nước đến chân mới nhảy. | Gốc        |
| **HD_Nắm_bắt**            | Chớp lấy cơ hội ngay lập tức.                      | Gốc        |
| **HD_Kiên_nhẫn**          | Nhẫn nại, kiên trì chịu đựng.                      | Gốc        |
| **HD_Tiêu_xài_hoang_phí** | Tiêu tốn tiền bạc không tiếc của.                  | Gốc        |
| **HD_Kìm_nén_cảm_xúc**    | Giữ bình tĩnh, ứng xử mềm mỏng.                    | Gốc        |
| **HD\_*Thích*ứng**        | Hòa nhập, điều chỉnh theo môi trường mới.          | Mới v2     |
| **HD_Bắt_chước**          | Kế thừa, mô phỏng hoặc bị ảnh hưởng thói quen.     | Mới v2     |
| **HD_Đồng_lòng**          | Đoàn kết, hợp lực cùng nhau.                       | Mới v2     |
| **HD_So_sánh**            | Nhìn nhận và ảo tưởng về hoàn cảnh người khác.     | Mới v2     |

---

### 3. Kết Quả (Results) - Ký hiệu: `KQ_` (30)

| Individual (ID)             | Ý nghĩa                                                | Trạng thái |
| :-------------------------- | :----------------------------------------------------- | :--------- |
| **KQ_Thành_công**           | Đạt kết quả tốt đẹp, hoàn thành mục tiêu.              | Gốc        |
| **KQ_Thất_bại**             | Hỏng việc, không như ý.                                | Gốc        |
| **KQ_Tổn_thất_tài_sản**     | Mất tiền của, thiệt hại vật chất.                      | Gốc        |
| **KQ_Tổn_thương**           | Thiệt hại thể chất hoặc tinh thần.                     | Gốc        |
| **KQ_Hối_hận**              | Lời đã nói/viết ra không cứu vãn được.                 | Gốc        |
| **KQ_Lộ_tẩy**               | Bản chất xấu xa hay bí mật bị phơi bày.                | Gốc        |
| **KQ_May_mắn**              | Bất ngờ đạt quả tốt do may mắn.                        | Gốc        |
| **KQ*Tối*ưu_hóa**           | Một công đôi việc, tiết kiệm công sức.                 | Gốc        |
| **KQ_Mất_quan_hệ**          | Gây thù chuốc oán, mất lòng tin.                       | Gốc        |
| **KQ_Bình_yên**             | Giữ được sự êm ấm, ổn định.                            | Gốc        |
| **KQ_An_toàn**              | Thoát khỏi nguy hiểm, giữ trọn bản thân.               | Gốc        |
| **KQ*Đạt*được_thỏa_thuận**  | Thống nhất ý kiến, giải quyết bất đồng.                | Gốc        |
| **KQ_Kết_thúc**             | Mọi sự việc hay điều tốt đẹp đều dừng lại.             | Gốc        |
| **KQ_Bị_khống_chế**         | Kẻ gớm ghê bị người cao tay hơn trừng trị.             | Mới v2     |
| **KQ_Gieo_tai_họa**         | Nhận lại hậu quả thảm khốc do mình gây ra.             | Mới v2     |
| **KQ_Gắn_kết**              | Duy trì tình nghĩa ruột thịt, thắt chặt mối quan hệ.   | Mới v2     |
| **KQ_Nhầm_lẫn**             | Nhầm lẫn do áp đặt suy nghĩ chủ quan.                  | Mới v2     |
| **KQ_Hòa_nhập**             | Hòa nhập an toàn vào môi trường mới.                   | Mới v2     |
| **KQ_Tương_xứng_giá_trị**   | Giá trị nhận được tương ứng với chi phí bỏ ra.         | **Mới v3** |
| **KQ_Gặp_trở_ngại**         | Công việc bắt đầu hoặc thực hiện gặp nhiều khó khăn.   | **Mới v3** |
| **KQ_Xác_nhận_sự_thật**     | Tận mắt chứng kiến giúp kiểm chứng chân lý.            | **Mới v3** |
| **KQ_Tích_lũy_kinh_nghiệm** | Tuổi tác và trải nghiệm đem lại sự sắc sảo.            | **Mới v3** |
| **KQ_Tích_lũy_tri_thức**    | Đi nhiều trải nghiệm giúp mở rộng tầm mắt.             | **Mới v3** |
| **KQ_Trân_trọng_bản_chất**  | Nhìn nhận giá trị phẩm chất bên trong quan trọng hơn.  | **Mới v3** |
| **KQ_Hình_thành_nhân_cách** | Môi trường và hoàn cảnh rèn luyện nên con người.       | **Mới v3** |
| **KQ*Khác_biệt_quan*điểm**  | Mỗi người có suy nghĩ, sở thích riêng biệt.            | **Mới v3** |
| **KQ*Tồn_tại_khuyết*điểm**  | Thừa nhận con người không ai hoàn hảo.                 | **Mới v3** |
| **KQ_Lưu_danh_hậu_thế**     | Danh tiếng tốt đẹp lưu truyền mãi về sau.              | **Mới v3** |
| **KQ_Đối_mặt_thực_tế**      | Chấp nhận cuộc sống có nhiều gai góc.                  | **Mới v3** |
| **KQ_Ngoại_cảnh_chi_phối**  | Quyền lực tự nhiên/ngoại cảnh nằm ngoài tầm kiểm soát. | **Mới v3** |

---

### 4. Mục Đích (Purposes) - Ký hiệu: `MD_` (9)

| Individual (ID)             | Ý nghĩa                                   | Trạng thái |
| :-------------------------- | :---------------------------------------- | :--------- |
| **MD_Bảo_vệ_bản_thân**      | Giữ an toàn, tránh rắc rối cho mình.      | Gốc        |
| **MD*Giải_quyết_vấn*đề**    | Muốn hoàn thành mục tiêu, vượt gian khó.  | Gốc        |
| **MD*Che*đậy**              | Cố tình giấu giếm bí mật, mâu thuẫn.      | Gốc        |
| **MD_Hạ_bệ**                | Đánh bại, trừng phạt đối thủ.             | Gốc        |
| **MD_Né_tránh_trách_nhiệm** | Đổ lỗi, thoái thác cho người khác.        | Gốc        |
| **MD_Giao_hảo**             | Giữ trọn đạo lý, giữ mối quan hệ tốt đẹp. | Mới v2     |
| **MD_Hòa_giải**             | Tha thứ, bao dung người biết nhận lỗi.    | Mới v2     |
| **MD_Trân_trọng_thời_gian** | Ý thức giá trị quý báu của thời gian.     | **Mới v3** |
| **MD_Bảo_vệ_tài_sản**       | Trân trọng và giữ gìn thành quả lao động. | **Mới v3** |

---

## Bảng So Sánh Cấu Trúc Các Phiên Bản

| Phiên bản         | Số câu | Tiêu chí tối thiểu | Đặc điểm chính                                                                        |
| :---------------- | :----: | :----------------: | :------------------------------------------------------------------------------------ |
| **v1**            |  100   |         4          | Ép cứng 4 tiêu chí cho toàn bộ 100 câu (dễ gây gượng ép ngữ nghĩa).                   |
| **v2**            |  100   |         1          | Cho phép câu tục ngữ sự thật chỉ dùng 1 tiêu chí (nhưng bị tối nghĩa).                |
| **v3 (Hiện tại)** |  100   |       **2**        | **Cân bằng tối ưu: Ít nhất 2 tiêu chí/câu**, hoàn toàn tự nhiên, minh bạch ngữ nghĩa. |

---

_(Tài liệu này đi kèm file dữ liệu `thanh_ngu_tuc_ngu_100_cau_v3.csv` chứa 100 cặp thành ngữ - tục ngữ được phân loại theo đúng chuẩn v3)._
