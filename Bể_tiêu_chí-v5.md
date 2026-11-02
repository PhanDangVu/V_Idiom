# Bể tiêu chí — bản rà soát ngữ nghĩa 2.0

Ngày sửa: 09/10/2026. Đi kèm `200_idioms.csv`, 200 dòng dữ liệu và 8 cột theo đúng thứ tự đã yêu cầu.

## 1. Ưu tiên và phạm vi

**Không ép nghĩa là ưu tiên cao hơn đồng nhất nhãn.** Trước hết phải có một nghĩa sử dụng hợp lý ở cả câu Việt và câu Anh; sau đó mới xác định phần lõi và nhãn. Nếu phải bỏ một nét nghĩa quyết định, tự thêm động cơ hay dựng một tình huống bất thường mới ghép được, cặp được thay. Không sửa giải nghĩa của thành ngữ chỉ để khớp với câu đã chọn.

Bản này đã rà lại 200 dòng, thay đổi **57 cặp đối chiếu** (trong đó **36 mục tiếng Việt được thay**) và sửa bộ nhãn ở **102 dòng** so với bản 1.0. Có **236 mã đang dùng**, so với 265 mã ở bản trước. “Bối cảnh” được đưa về các khung ngữ nghĩa rộng, không tùy dòng trộn một biến cố riêng với một lĩnh vực hành vi.

Đây vẫn là bộ dữ liệu do LLM biên soạn và rà soát, có tra cứu chọn mẫu cách dùng từ điển; không phải bộ chuẩn được chuyên gia song ngữ xác nhận độc lập. “Không ép nghĩa” ở đây là quy tắc tuyển chọn và kiểm tra, không phải tuyên bố mọi cặp tương đương tuyệt đối trong mọi câu văn.

Phạm vi thực hành gồm thành ngữ, thành ngữ so sánh và một số lối nói cố định mang tính châm ngôn. Ví dụ “What's done is done” là một cách nói cố định dạng câu; “Empty-handed” là tính từ có nghĩa bóng. Không dùng câu dịch sáng tác như thể đó là thành ngữ đã có.

## 2. Đơn vị nghĩa và các vai trò

Mỗi dòng mô tả **một nghĩa sử dụng** của câu Việt và cách dùng tương ứng của câu Anh. Giải nghĩa Việt giữ nghĩa của mục Việt; giải nghĩa Anh giải thích cách dùng câu Anh trong cặp. Câu có nhiều nghĩa phải nói rõ nghĩa đang chọn, như “lạnh như tiền” chỉ thái độ, không phải nhiệt độ. Giới hạn thông dụng như nghĩa tài chính hay nghĩa quan hệ được phép chọn rõ; không tự dựng một sự kiện để ép hai câu gặp nhau.

| Vai trò | Hỏi điều gì? | Không được suy thêm |
| --- | --- | --- |
| HD — Hành động | Chủ thể làm gì hoặc quá trình nào thực sự được diễn đạt? | Không biến mọi trạng thái thành một hành động; không dùng hình ảnh nghĩa đen. |
| MD — Mục đích | Chủ thể muốn đạt điều gì? | Không lấy kết quả đã xảy ra hoặc bài học cho người đọc làm ý định của chủ thể. |
| KQ — Kết quả | Kết cục, trạng thái hoặc triển vọng nào được câu khẳng định? | Không biến nguy cơ thành sự kiện đã xảy ra, hay biến cảm xúc thành hậu quả của một hành động tự đặt ra. |
| BC — Bối cảnh | Khung tình huống/lĩnh vực ngữ nghĩa cần để hiểu câu là gì? | Không tự gán một nghề, nhân vật, nơi chốn hoặc biến cố cụ thể. |

### Quy ước bắt buộc khi đọc KQ

Để giữ đúng cấu trúc bốn cột và vẫn biểu diễn các thành ngữ tĩnh, cột KQ được sử dụng cho **kết quả hoặc trạng thái được diễn đạt**. Từ điển ở phần 5 phân loại từng mã KQ thành **hệ quả/kết cục**, **trạng thái/thuộc tính**, hoặc **nguy cơ/triển vọng**. Đây là quy ước mở rộng của bộ dữ liệu này, không phải khẳng định trạng thái luôn là một kết quả nhân quả.

Ví dụ: `KQ_Vui_sướng` chỉ trạng thái vui; `KQ_Can_đảm` chỉ thuộc tính gan dạ; `KQ_Nguy_cơ_phản_bội` chỉ khả năng có hại về sau. Không được diễn giải thành “đã làm X nên vui”, “đã trở nên can đảm”, hay “đã bị phản bội”. Nếu nghiên cứu chỉ chấp nhận KQ là kết quả nhân quả theo nghĩa hẹp, cần loại hoặc tách các nhãn trạng thái/triển vọng khi sử dụng; không ép chúng thành kết quả.

### Cùng nghĩa và gần nghĩa

- Cùng nghĩa sử dụng và cùng mức khái quát: dùng cùng khung, bất kể hình ảnh của hai thành ngữ khác nhau.
- Gần nghĩa: chia sẻ phần lõi; chỉ thêm nhãn khi câu thực sự có thêm hành động, trạng thái hoặc điều kiện quan trọng.
- Cùng chuỗi chữ tiếng Anh nhưng khác nghĩa: có thể khác khung, song phải ghi rõ nghĩa riêng. Bản hiện tại không sử dụng ngoại lệ đa nghĩa này cho các mục Anh bị lặp.
- Khung giống nhau không chứng minh hai thành ngữ giống nhau mọi mặt. Khung là biểu diễn có chọn lọc, không bao trọn sắc thái văn hóa, mức độ trang trọng và cấu trúc ngữ pháp.
- Nét riêng như hình ảnh điển tích hoặc sắc thái chê có thể ghi ở giải nghĩa. Một nét quyết định làm đổi sự việc, như “độc ác” so với “thiếu thương cảm”, không được xóa đi để tạo tương đương giả.

## 3. Định dạng và sử dụng lại

Thứ tự cột: **Thành Ngữ Việt Nam, Giải nghĩa tiếng Việt, giải nghĩa tiếng Anh, Bối cảnh, Mục đích, Hành động, Kết quả, Thành ngữ Tiếng Anh**. Mã giữ dấu tiếng Việt, dùng gạch dưới: `HD_Trì_hoãn`, `MD_Tiết_kiệm`, `KQ_Vui_sướng`, `BC_Giao_tiếp`. Không có dấu ngoặc sau tiền tố, theo ví dụ người dùng đưa ra.

Mỗi ô hiện có tối đa một nhãn. Mỗi dòng có ít nhất hai **vai trò khác rỗng**. Ô trống nghĩa là chưa đủ căn cứ ngữ nghĩa để gán, không phải lỗi thiếu dữ liệu cần tự động điền. Không thêm nhãn chỉ để làm một câu giống khung câu khác.

CSV dùng dấu phẩy, mã hóa UTF-8 có BOM và xuống dòng CRLF. Có thể đọc bằng Python với `encoding='utf-8-sig'` và `newline=''`. Hai cột giải nghĩa dùng văn bản tự biên soạn, không sao chép định nghĩa từ điển nguyên văn.

Khi mở rộng: đọc nghĩa đang dùng → xác định nét bắt buộc → tìm khung gần nhất → tái sử dụng các mã đã có → chỉ tạo mã khi có khác biệt cần phân biệt. Mã mới phải có định nghĩa đầy đủ và ví dụ; không âm thầm đổi nghĩa mã cũ. Không tự quy hai nhãn thành đồng nghĩa vì chúng xuất hiện ở câu dịch chung một câu Anh.

## 4. Kiểm tra tính nhất quán

| Vai trò | Số mã đang dùng | Số dòng được gán |
| --- | ---: | ---: |
| BC | 28 | 200 |
| MD | 21 | 25 |
| HD | 97 | 124 |
| KQ | 90 | 130 |

Phân bố: 126 dòng có 2 tiêu chí; 69 dòng có 3 tiêu chí; 5 dòng có 4 tiêu chí. Có 182 mục Anh khác nhau và 18 nhóm lặp nguyên câu Anh; **không có nhóm lặp cùng nghĩa Anh mà khung khác nhau** trong bản xuất này.

Kiểm tra bằng mã: 200 mục Việt không trùng, 200 cặp không trùng, đúng 8 cột, đúng tiền tố theo cột, tối thiểu hai vai trò/dòng, mọi nhãn đều có định nghĩa; đối chiếu toàn bộ nhóm trùng câu Anh; kiểm tra các nhóm nghĩa được liệt kê dưới đây và các cặp cần phân biệt. Đây là kiểm tra nhất quán trên quyết định ngữ nghĩa đã biên soạn, không phải phép chứng minh chất lượng dịch tự động.

### Các nhóm nghĩa đã kiểm tra chung khung

Số thứ tự dưới đây tính theo bản ghi từ 1, không tính dòng tiêu đề CSV. Đây là các nhóm được chọn sau khi đọc nghĩa, không phải chỉ gom tự động vì chuỗi nhãn trùng.

| Nhóm nghĩa | Các mục tiếng Việt | Khung chung |
| --- | --- | --- |
| Nói thẳng | 1. Nói toạc móng heo; 2. Thẳng như ruột ngựa | `BC_Giao_tiếp`; `HD_Nói_thẳng` |
| Nói liên tục, nhiều | 6. Nói như khướu; 17. Nói như nước chảy | `BC_Giao_tiếp`; `HD_Nói_nhiều` |
| Giữ kín thông tin | 10. Ngậm miệng như hến; 11. Kín như bưng | `BC_Thông_tin`; `HD_Giữ_kín`; `KQ_Không_tiết_lộ` |
| Khuyên bảo không được tiếp thu | 16. Nước đổ đầu vịt; 176. Nước đổ lá khoai | `BC_Giao_tiếp`; `HD_Khuyên_bảo`; `KQ_Không_tiếp_thu` |
| Vẻ ngoài tử tế che giấu bản chất xấu | 21. Khẩu Phật tâm xà; 22. Miệng nam mô, bụng một bồ dao găm | `BC_Ứng_xử`; `HD_Giả_tử_tế` |
| Kiếm lợi từ tình thế rối ren | 31. Đục nước béo cò; 32. Thừa nước đục thả câu | `BC_Lợi_ích`; `MD_Trục_lợi`; `HD_Lợi_dụng_rối_ren` |
| Dung dưỡng người có thể phản lại mình | 35. Nuôi ong tay áo; 36. Nuôi cáo trong nhà | `BC_Quan_hệ`; `HD_Dung_dưỡng_kẻ_xấu`; `KQ_Nguy_cơ_phản_bội` |
| Bản chất xấu bị lộ | 38. Cháy nhà ra mặt chuột; 39. Lòi đuôi cáo | `BC_Ứng_xử`; `HD_Bộc_lộ_bản_chất`; `KQ_Lộ_bản_chất` |
| Bị hai phía kìm kẹp | 44. Trên đe dưới búa; 97. Một cổ hai tròng | `BC_Xung_đột`; `KQ_Bị_kẹp_hai_phía` |
| Tình thế cực kỳ mong manh | 45. Ngàn cân treo sợi tóc; 46. Chỉ mành treo chuông | `BC_Nguy_hiểm`; `KQ_Bấp_bênh` |
| Đối đầu với khả năng thắng rất thấp | 55. Châu chấu đá xe; 56. Trứng chọi đá | `BC_Xung_đột`; `HD_Đối_đầu`; `KQ_Khó_thành_công` |
| Soi tìm khuyết điểm | 60. Bới lông tìm vết; 61. Vạch lá tìm sâu | `BC_Đánh_giá`; `MD_Bắt_lỗi`; `HD_Soi_lỗi` |
| Công sức vô ích | 63. Dã tràng xe cát; 64. Công dã tràng | `BC_Công_việc`; `HD_Cố_gắng`; `KQ_Vô_ích` |
| Lao động cật lực | 71. Làm như trâu ngựa; 72. Cày sâu cuốc bẫm; 77. Một nắng hai sương | `BC_Công_việc`; `HD_Làm_cật_lực` |
| Quá nhiều việc | 73. Đầu tắt mặt tối; 74. Tối mặt tối mũi | `BC_Công_việc`; `KQ_Quá_tải` |
| Cắt giảm chi tiêu | 106. Thắt lưng buộc bụng; 107. Bóp mồm bóp miệng | `BC_Tài_chính`; `MD_Tiết_kiệm`; `HD_Cắt_chi_tiêu` |
| Nghèo khó | 108. Nghèo rớt mồng tơi; 109. Khố rách áo ôm | `BC_Tài_chính`; `KQ_Nghèo_khó` |
| Công việc hoặc vị thế tiến triển tốt | 114. Ăn nên làm ra; 115. Diều gặp gió | `BC_Công_việc`; `KQ_Tiến_triển_tốt` |
| Có thế lực, ảnh hưởng | 117. Tai to mặt lớn; 118. Có máu mặt | `BC_Quyền_lực`; `KQ_Có_thế_lực` |
| Hợp sức | 122. Đồng tâm hiệp lực; 123. Chung lưng đấu cật; 124. Kề vai sát cánh | `BC_Tập_thể`; `HD_Hợp_tác` |
| Sẵn lòng chia cả phần mình cần | 126. Con chấy cắn đôi; 127. Nhường cơm sẻ áo | `BC_Quan_hệ`; `HD_Chia_sẻ_tận_tình` |
| Đồng hành qua tốt xấu | 128. Đồng cam cộng khổ; 129. Chia ngọt sẻ bùi | `BC_Quan_hệ`; `HD_Đồng_hành`; `KQ_Gắn_bó` |
| Chưa tin hoàn toàn | 130. Nửa tin nửa ngờ; 186. Bán tín bán nghi | `BC_Nhận_thức`; `HD_Tiếp_nhận_dè_dặt`; `KQ_Hoài_nghi` |
| Chấm dứt đồng hành | 139. Dứt áo ra đi; 140. Đường ai nấy đi | `BC_Quan_hệ`; `HD_Cắt_đứt`; `KQ_Tách_rời` |
| Rất vui sướng | 141. Vui như mở cờ trong bụng; 142. Mừng như bắt được vàng; 143. Sướng như tiên | `BC_Cảm_xúc`; `KQ_Vui_sướng` |
| Rất lo lắng | 145. Ruột gan như lửa đốt; 146. Đứng ngồi không yên; 147. Lo sốt vó | `BC_Cảm_xúc`; `KQ_Lo_lắng` |
| Sợ hãi mạnh | 148. Sợ mất mật; 149. Hồn vía lên mây; 150. Dựng tóc gáy | `BC_Cảm_xúc`; `KQ_Sợ_hãi` |
| Trạng thái giận dữ | 152. Giận tím mặt; 154. Sôi máu | `BC_Cảm_xúc`; `KQ_Giận_dữ` |
| Đau khổ tinh thần | 157. Đau như cắt; 158. Đứt từng khúc ruột | `BC_Cảm_xúc`; `KQ_Đau_khổ` |
| Việc đã thành, không thể đảo ngược | 174. Ván đã đóng thuyền; 175. Gạo đã nấu thành cơm | `BC_Quyết_định`; `KQ_Không_thể_đảo_ngược` |
| Một việc đạt hai lợi ích | 178. Một công đôi việc; 179. Một mũi tên trúng hai đích | `BC_Công_việc`; `HD_Kết_hợp_việc`; `KQ_Lợi_ích_kép` |
| Can đảm | 182. Gan vàng dạ sắt; 183. Gan lì tướng quân | `BC_Tính_cách`; `KQ_Can_đảm` |
| Cố chấp | 190. Ngang như cua; 191. Cứng đầu cứng cổ | `BC_Tính_cách`; `HD_Cố_chấp` |

### Những trường hợp phải giữ khác biệt

| Hai mục | Vì sao không đồng nhất toàn bộ khung? |
| --- | --- |
| 15. Đàn gảy tai trâu / 16. Nước đổ đầu vịt | Không hiểu/không biết thưởng thức điều có giá trị khác với lời khuyên không được tiếp thu. |
| 43. Tiến thoái lưỡng nan / 44. Trên đe dưới búa | Khó chọn giữa các khả năng khác với bị hai lực gây sức ép. |
| 73. Đầu tắt mặt tối / 71. Làm như trâu ngựa | Có quá nhiều việc không tự chứng minh đang lao động cật lực. |
| 103. Ném tiền qua cửa sổ / 105. Ăn tiêu như phá | Chi vào việc vô ích khác với tiêu tiền rất nhiều, thiếu tiết chế. |
| 108. Nghèo rớt mồng tơi / 111. Chạy ăn từng bữa | Nghèo khó nói chung khác với chỉ đủ sống trước mắt, không có dự trữ. |
| 125. Như hình với bóng / 128. Đồng cam cộng khổ | Luôn gần nhau khác với trung thành đồng hành qua cả thuận lợi lẫn khó khăn. |
| 152. Giận tím mặt / 153. Nổi trận lôi đình | Đang giận dữ khác với bùng phát thành cơn giận. |
| 184. Lạnh như tiền / 185. Lòng dạ sắt đá | Lạnh nhạt trong giao tiếp khác với không có lòng thương cảm. |
| 197. Như hai giọt nước / 200. Cá mè một lứa | Giống hình dáng khác với cùng kiểu tính cách hoặc bản chất. |
| 5. Khua môi múa mép / 133. Nói một đằng, làm một nẻo | Nói mà không làm khác với có làm nhưng trái điều đã nói. |

## 5. Từ điển đầy đủ của các nhãn

Mỗi nhãn có nghĩa đầy đủ, kiểu vai trò, ví dụ và số lần dùng. Không có mã dự phòng chưa được dùng trong bản CSV này. Với KQ, cột “Kiểu” giúp tránh lẫn trạng thái với kết quả nhân quả.

### HD — Hành động (97 mã)

| Mã | Nghĩa đầy đủ và giới hạn | Kiểu | Ví dụ | Số dòng |
| --- | --- | --- | --- | ---: |
| `HD_Bàn_tán` | Nhiều người trao đổi, đồn đoán hoặc bình luận về người hay việc khác; không tự khẳng định nội dung bàn tán đúng hay sai. | Hành động / quá trình | 13. Lời ra tiếng vào | 1 |
| `HD_Bày_mưu` | Sắp đặt một kế hoạch có tính toán nhằm tác động đến người khác; mục tiêu hại người được xác định riêng bằng MD khi có căn cứ. | Hành động / quá trình | 41. Gậy ông đập lưng ông | 1 |
| `HD_Bỏ_nhỏ_cầu_lớn` | Bỏ ra hoặc chấp nhận rủi ro mất một thứ ít giá trị để có cơ hội nhận thứ có giá trị lớn hơn. Chưa khẳng định đã thu lợi lớn. | Hành động / quá trình | 196. Thả con săn sắt, bắt con cá rô | 1 |
| `HD_Bỏ_rơi` | Rút lại hoặc từ chối sự quan tâm, giúp đỡ hay hỗ trợ trong một quan hệ. Không nhất thiết có âm mưu gây hại. | Hành động / quá trình | 135. Quay lưng trở mặt | 1 |
| `HD_Bộc_lộ_bản_chất` | Thể hiện ra đặc điểm thật hoặc ý đồ từng bị che giấu; có thể là vô tình lộ ra chứ không phải cố ý công khai. | Hành động / quá trình | 38. Cháy nhà ra mặt chuột; 39. Lòi đuôi cáo | 2 |
| `HD_Bộc_lộ_cảm_xúc` | Để người khác dễ nhận thấy tình cảm qua lời nói, nét mặt hoặc hành vi, thay vì giấu trong lòng. | Hành động / quá trình | 12. Ruột để ngoài da | 1 |
| `HD_Bội_bạc` | Rút bỏ sự biết ơn, trung thành hoặc hỗ trợ, hay quay lại đối xử xấu với người từng có quan hệ gắn bó hoặc giúp đỡ mình. | Hành động / quá trình | 34. Ăn cháo đá bát | 1 |
| `HD_Bù_chỗ_thiếu` | Chuyển tiền hoặc nguồn lực từ nhu cầu này sang nhu cầu khác để tạm lấp thiếu hụt, có thể tạo ra thiếu hụt ở nơi bị lấy đi. | Hành động / quá trình | 110. Giật gấu vá vai | 1 |
| `HD_Bùng_giận` | Phản ứng giận dữ xuất hiện đột ngột và mạnh, có thể thể hiện bằng lời nói hoặc hành vi; khác với chỉ đang cảm thấy giận. | Hành động / quá trình | 153. Nổi trận lôi đình | 1 |
| `HD_Cai_quản_cứng_rắn` | Điều hành và áp đặt kỷ luật bằng cách nghiêm khắc, ít chấp nhận sự không tuân theo. | Hành động / quá trình | 119. Bàn tay sắt | 1 |
| `HD_Cãi_vã` | Trao đổi lời nói mang tính đối chọi hoặc gay gắt giữa các bên; không đồng nhất với bất đồng được trình bày ôn hòa. | Hành động / quá trình | 132. Như chó với mèo | 1 |
| `HD_Cắt_chi_tiêu` | Giảm các khoản tiền dùng cho sinh hoạt hoặc nhu cầu khác để giữ lại nguồn lực. | Hành động / quá trình | 106. Thắt lưng buộc bụng; 107. Bóp mồm bóp miệng | 2 |
| `HD_Cắt_đứt` | Chấm dứt việc gắn bó hoặc tiếp tục tham gia một quan hệ hay sự việc, theo nghĩa đã chọn ở từng dòng. | Hành động / quá trình | 139. Dứt áo ra đi; 140. Đường ai nấy đi | 2 |
| `HD_Cắt_giao_tiếp` | Ngừng nói chuyện hoặc tiếp xúc với người khác do quan hệ bị tổn hại; không tự khẳng định mọi liên hệ đều chấm dứt. | Hành động / quá trình | 134. Cạch mặt nhau | 1 |
| `HD_Chạy_nhanh` | Di chuyển bằng cách chạy với tốc độ cao. Không tự thêm mục đích chạy trốn hoặc bắt đuổi. | Hành động / quá trình | 76. Ba chân bốn cẳng | 1 |
| `HD_Chặn_cơ_hội` | Làm người khác không thể tiếp cận con đường hoặc điều kiện tạo lợi ích mà chủ thể đã sử dụng hoặc đang nắm giữ. | Hành động / quá trình | 33. Qua cầu rút ván | 1 |
| `HD_Chi_lãng_phí` | Sử dụng tiền quá mức hoặc vào việc không đem lại giá trị tương xứng; không đồng nhất với mọi khoản chi lớn. | Hành động / quá trình | 103. Ném tiền qua cửa sổ | 1 |
| `HD_Chi_phung_phí` | Tiêu tiền rất nhiều và thiếu tiết chế. Khác HD_Chi_lãng_phí ở chỗ không cần khẳng định từng khoản chi đều không đem lại giá trị. | Hành động / quá trình | 105. Ăn tiêu như phá | 1 |
| `HD_Chi_quá_sức` | Chi tiêu vượt mức thu nhập hoặc nguồn tiền có thể đáp ứng, dù khoản chi chưa chắc là vô ích. | Hành động / quá trình | 104. Vung tay quá trán | 1 |
| `HD_Chia_rẽ` | Tác động khiến hai bên nghi kỵ, đối đầu hoặc xa nhau hơn, thường bằng cách kích động giữa các bên. | Hành động / quá trình | 177. Đâm bị thóc, chọc bị gạo | 1 |
| `HD_Chia_sẻ_tận_tình` | Sẵn lòng chia cả phần mình đang cần hoặc phần rất ít còn lại cho người khác. Không mặc định chỉ làm vậy với người thân. | Hành động / quá trình | 126. Con chấy cắn đôi; 127. Nhường cơm sẻ áo | 2 |
| `HD_Chịu_đựng` | Tiếp nhận và gánh một hoàn cảnh đau khổ, khó khăn hoặc khó chấp nhận mà chưa thoát khỏi nó; không tự gán mục tiêu phục thù. | Hành động / quá trình | 51. Cắn răng chịu đựng; 156. Ngậm đắng nuốt cay | 2 |
| `HD_Cố_chấp` | Giữ khăng khăng ý kiến hoặc cách làm, không chịu nghe lời khuyên hay cân nhắc điều chỉnh. | Hành động / quá trình | 190. Ngang như cua; 191. Cứng đầu cứng cổ | 2 |
| `HD_Cố_gắng` | Bỏ công sức để thực hiện một việc hoặc vượt trở ngại; nhãn không đảm bảo nỗ lực sẽ thành công. | Hành động / quá trình | 63. Dã tràng xe cát; 64. Công dã tràng | 2 |
| `HD_Cung_cấp_thừa` | Đưa thêm một thứ vào nơi đã có dư hoặc không cần thêm thứ ấy, khiến đóng góp trở nên không cần thiết. | Hành động / quá trình | 67. Chở củi về rừng | 1 |
| `HD_Dạy_người_đã_thạo` | Đưa chỉ dẫn cho người vốn đã biết rất rõ việc ấy, khiến lời chỉ dẫn không cần thiết. Khác việc truyền đạt kiến thức cho người chưa biết. | Hành động / quá trình | 94. Dạy khỉ leo cây | 1 |
| `HD_Dấn_thân` | Bước vào hoặc tiếp tục tham gia một tình thế có rủi ro, khiến bản thân bị cuốn vào hệ quả của nó. | Hành động / quá trình | 54. Cưỡi lên lưng hổ | 1 |
| `HD_Dung_dưỡng_kẻ_xấu` | Cho nơi ở, sự hỗ trợ hoặc quyền tiếp cận đối với người có thể phản lại và gây hại cho mình hoặc cộng đồng. | Hành động / quá trình | 35. Nuôi ong tay áo; 36. Nuôi cáo trong nhà | 2 |
| `HD_Đánh_tráo` | Dùng một thứ để thu hút hoặc tạo kỳ vọng rồi thay bằng thứ khác không tương ứng, thường có chất lượng hay giá trị kém hơn. | Hành động / quá trình | 23. Treo đầu dê, bán thịt chó | 1 |
| `HD_Đáp_trả_tương_xứng` | Phản ứng lại việc người khác làm bằng hành động tương tự hoặc tương xứng, thường mang sắc thái trả đũa trong ngữ cảnh xung đột. | Hành động / quá trình | 58. Ăn miếng trả miếng | 1 |
| `HD_Điều_chỉnh_theo_nguồn_lực` | Sắp xếp kế hoạch hay mức chi cho phù hợp với điều kiện thực có. Không nhất thiết giảm chi nếu khả năng hiện tại đã đủ. | Hành động / quá trình | 194. Liệu cơm gắp mắm | 1 |
| `HD_Đòi_hỏi_quá_mức` | Yêu cầu thêm lợi ích hoặc sự nhượng bộ vượt mức hợp lý, nhất là sau khi đã được đáp ứng. | Hành động / quá trình | 193. Được voi đòi tiên | 1 |
| `HD_Đối_đầu` | Trực tiếp chống lại hoặc tranh đấu với một bên khác, không tự quy định bên nào mạnh hơn. | Hành động / quá trình | 55. Châu chấu đá xe; 56. Trứng chọi đá | 2 |
| `HD_Đổi_lập_trường` | Thay đổi thái độ, ý kiến hoặc phía mình ủng hộ; động cơ cơ hội chỉ được ghi khi có căn cứ riêng. | Hành động / quá trình | 84. Gió chiều nào che chiều ấy | 1 |
| `HD_Đồng_hành` | Ở bên và chia sẻ những trải nghiệm thuận lợi lẫn khó khăn với người khác qua thời gian. | Hành động / quá trình | 128. Đồng cam cộng khổ; 129. Chia ngọt sẻ bùi | 2 |
| `HD_Đốt_giai_đoạn` | Vội thực hiện bước cao hoặc việc khó khi chưa đạt kỹ năng và điều kiện nền tảng. Khác chỉ bắt đầu sớm hơn thời điểm đã định. | Hành động / quá trình | 98. Chưa học bò đã lo học chạy | 1 |
| `HD_Đưa_bằng_chứng` | Nêu dữ kiện, dẫn chứng hoặc nguồn có thể kiểm tra để làm căn cứ cho một khẳng định. | Hành động / quá trình | 4. Nói có sách, mách có chứng | 1 |
| `HD_Gán_tội` | Đẩy lỗi hoặc trách nhiệm làm sai sang một người không phải người gây ra, khiến họ có nguy cơ chịu hậu quả thay. | Hành động / quá trình | 29. Gắp lửa bỏ tay người | 1 |
| `HD_Gây_trở_ngại` | Can thiệp hoặc tạo điều kiện bất lợi khiến công việc đang diễn ra bị vướng mắc, khó tiến triển bình thường. | Hành động / quá trình | 49. Chọc gậy bánh xe | 1 |
| `HD_Giả_thương_cảm` | Thể hiện buồn thương hoặc cảm thông không chân thành. Không tự thêm mục đích trục lợi, xin tha hay gây thiện cảm nếu chưa có căn cứ. | Hành động / quá trình | 26. Nước mắt cá sấu | 1 |
| `HD_Giả_tử_tế` | Thể hiện sự hiền lành, đạo đức hoặc thương cảm không tương ứng với bản chất hay cảm xúc thật. | Hành động / quá trình | 21. Khẩu Phật tâm xà; 22. Miệng nam mô, bụng một bồ dao găm | 2 |
| `HD_Giả_vờ_không_biết` | Tỏ ra không biết, không nghe hoặc không hiểu trong khi thực tế có biết hoặc có hiểu. | Hành động / quá trình | 25. Giả câm giả điếc | 1 |
| `HD_Giữ_kín` | Không nói ra, không công bố hoặc ngăn người khác tiếp cận thông tin; mục đích cụ thể chỉ gán thêm khi đã rõ. | Hành động / quá trình | 10. Ngậm miệng như hến; 11. Kín như bưng | 2 |
| `HD_Gợi_ý_gián_tiếp` | Đưa dấu hiệu hoặc nói bóng gió để người nghe tự nhận ra ý, thay vì diễn đạt trực tiếp toàn bộ điều muốn nói. | Hành động / quá trình | 19. Nói bóng nói gió | 1 |
| `HD_Hồi_phục` | Dần trở lại tình trạng ổn định hơn sau giai đoạn nguy kịch hoặc gần sụp đổ; mức hồi phục cụ thể do giải nghĩa xác định. | Hành động / quá trình | 168. Chết đi sống lại | 1 |
| `HD_Hợp_tác` | Nhiều người phối hợp công sức, ý chí hoặc sự hỗ trợ để cùng thực hiện một việc. | Hành động / quá trình | 122. Đồng tâm hiệp lực; 123. Chung lưng đấu cật | 3 |
| `HD_Hùa_theo` | Đi theo ý kiến, hành động hoặc xu hướng của người khác mà không thể hiện sự cân nhắc độc lập đầy đủ. | Hành động / quá trình | 86. A dua a tòng | 1 |
| `HD_Hưởng_không_đóng_góp` | Nhận lợi ích mà không bỏ công hoặc nguồn lực tương xứng. Không nhất thiết là trộm cắp hoặc lừa đảo. | Hành động / quá trình | 37. Ngồi mát ăn bát vàng | 1 |
| `HD_Kết_hợp_việc` | Thực hiện một cách làm chung để phục vụ đồng thời nhiều mục tiêu, thay vì xử lý từng mục tiêu bằng hành động riêng. | Hành động / quá trình | 178. Một công đôi việc; 179. Một mũi tên trúng hai đích | 2 |
| `HD_Khiêu_khích` | Cố ý chọc giận, thách thức hoặc kích phản ứng từ một đối tượng có thể đáp trả. | Hành động / quá trình | 53. Vuốt râu hùm | 1 |
| `HD_Không_chọn_bên` | Giữ thái độ chưa đứng hẳn về lựa chọn hoặc phe nào; có thể do phân vân hoặc né cam kết. | Hành động / quá trình | 83. Đứng giữa hai dòng nước | 1 |
| `HD_Không_hành_động` | Đứng ngoài hoặc không can thiệp trong một tình huống cần phản ứng. Không tự suy thêm rằng người đó đang chờ lợi ích tự đến. | Hành động / quá trình | 195. Khoanh tay đứng nhìn | 1 |
| `HD_Khuyên_bảo` | Đưa lời chỉ dẫn, dạy bảo, giải thích hoặc phê bình với nội dung người nghe được kỳ vọng sẽ hiểu hay tiếp thu. | Hành động / quá trình | 16. Nước đổ đầu vịt; 176. Nước đổ lá khoai | 2 |
| `HD_Kiếm_tiền` | Thu được tiền từ hoạt động làm ăn, công việc hoặc nguồn thu khác; số tiền lớn hay nhỏ được ghi ở KQ khi rõ. | Hành động / quá trình | 102. Tiền vào như nước | 1 |
| `HD_Làm_căng_thẳng` | Nói hoặc làm điều làm tăng sự tức giận hay đối đầu đã có. Không tự khẳng định người làm cố ý muốn gây xung đột. | Hành động / quá trình | 30. Đổ dầu vào lửa | 1 |
| `HD_Làm_cật_lực` | Bỏ sức làm việc với cường độ cao, thời gian dài hoặc trong điều kiện rất nhọc nhằn. | Hành động / quá trình | 71. Làm như trâu ngựa; 72. Cày sâu cuốc bẫm | 3 |
| `HD_Làm_chậm` | Di chuyển, phản ứng hoặc thực hiện việc với tốc độ thấp; không suy ra chủ thể cố tình trì hoãn. | Hành động / quá trình | 188. Chậm như rùa | 1 |
| `HD_Làm_hòa` | Giải quyết hoặc gác lại mâu thuẫn để khôi phục quan hệ thân thiện giữa các bên. | Hành động / quá trình | 138. Gương vỡ lại lành | 1 |
| `HD_Làm_nhanh` | Di chuyển, phản ứng hoặc thực hiện việc với tốc độ rất cao; không tự hàm ý làm ẩu. | Hành động / quá trình | 75. Vắt chân lên cổ; 189. Nhanh như chớp | 2 |
| `HD_Làm_ô_danh` | Làm một người hoặc nhóm bị mang tiếng xấu. Không tự khẳng định việc ấy dùng lời nói dối hay do chủ ý ác độc. | Hành động / quá trình | 28. Bôi tro trát trấu | 1 |
| `HD_Lộng_quyền` | Hành xử như thể quyền lực của mình vượt trên các quy tắc hoặc sự kiềm chế thông thường. | Hành động / quá trình | 120. Ra oai tác quái | 1 |
| `HD_Lờ_đi` | Cố tình không chú ý hoặc không phản ứng với điều đã biết, dù điều đó có vấn đề hoặc cần được xử lý. | Hành động / quá trình | 87. Nhắm mắt làm ngơ | 1 |
| `HD_Lợi_dụng_rối_ren` | Khai thác sự hỗn loạn hoặc bất ổn để kiếm lợi. Phải có nét rối ren trong nghĩa đang chọn, không dùng cho mọi cơ hội thuận lợi. | Hành động / quá trình | 31. Đục nước béo cò; 32. Thừa nước đục thả câu | 2 |
| `HD_Lừa_dối` | Dẫn người khác đến nhận thức sai hoặc không thấy sự thật bằng lời nói hay cách sắp đặt có chủ ý. | Hành động / quá trình | 24. Đánh lận con đen | 1 |
| `HD_Mạo_hiểm` | Thực hiện việc có khả năng gây tổn thất đáng kể hoặc nguy hiểm cho bản thân; không mặc định mức liều lĩnh là đúng hay sai. | Hành động / quá trình | 52. Vào sinh ra tử; 80. Được ăn cả, ngã về không | 2 |
| `HD_Né_tránh` | Rời xa hoặc tránh trực tiếp đối diện với một điều khó khăn hay bất lợi; đây là hành động, khác với MD_Né_tránh là ý định. | Hành động / quá trình | 42. Tránh vỏ dưa, gặp vỏ dừa | 1 |
| `HD_Nghe_hời_hợt` | Nghe mà không chú ý đủ hoặc không giữ lại nội dung. Khác với không có khả năng hiểu ngôn ngữ đang được nói. | Hành động / quá trình | 96. Nghe tai này lọt tai kia | 1 |
| `HD_Ngủ_say` | Ngủ sâu và ít bị các tác động thông thường làm thức giấc. Không suy thêm về thời gian ngủ hay bệnh lý. | Hành động / quá trình | 162. Ngủ như chết | 1 |
| `HD_Nịnh_nọt` | Dùng lời ngọt ngào, đề cao hoặc dễ nghe hướng tới người khác, thường để tạo thiện cảm hay thuyết phục. | Hành động / quá trình | 18. Nói như rót mật vào tai | 1 |
| `HD_Nói_dối` | Phát biểu điều biết là không đúng sự thật hoặc bịa ra điều không có; khác với sai do thiếu thông tin. | Hành động / quá trình | 9. Ăn không nói có | 1 |
| `HD_Nói_hớ` | Nói ra điều thiếu cân nhắc hoặc không phù hợp, có thể khiến bản thân hay người nghe gặp rắc rối. | Hành động / quá trình | 89. Lỡ mồm lỡ miệng | 1 |
| `HD_Nói_làm_bất_nhất` | Hành động thực tế không phù hợp hoặc trái với điều chủ thể nói hay hứa. Khác HD_Nói_suông: có thể đã hành động nhưng theo hướng ngược lời nói. | Hành động / quá trình | 133. Nói một đằng, làm một nẻo | 1 |
| `HD_Nói_nhiều` | Nói liên tục hoặc với lượng lời lớn; chỉ riêng nhãn này không quy định lời nói đúng, sai, khoe khoang hay vô ích. | Hành động / quá trình | 6. Nói như khướu; 17. Nói như nước chảy | 2 |
| `HD_Nói_suông` | Đưa ra lời hứa hoặc lời nói có vẻ đáng kể nhưng thiếu hành động thực chất tương ứng. | Hành động / quá trình | 5. Khua môi múa mép | 1 |
| `HD_Nói_thẳng` | Diễn đạt ý kiến hoặc sự thật trực tiếp, không vòng vo hay làm nhẹ lời đến mức mất nội dung. | Hành động / quá trình | 1. Nói toạc móng heo; 2. Thẳng như ruột ngựa | 2 |
| `HD_Nói_vòng_vo` | Nói quanh chủ đề hoặc kéo dài mà chưa đi thẳng vào điểm chính cần đề cập. | Hành động / quá trình | 3. Vòng vo tam quốc | 1 |
| `HD_Phản_bội` | Quay lại chống người hoặc phía từng được mình trung thành, hay ngầm làm hại người tin cậy mình. Không đồng nhất với chỉ rời khỏi một quan hệ. | Hành động / quá trình | 27. Đâm sau lưng; 136. Thay lòng đổi dạ | 2 |
| `HD_Phản_kháng` | Chống lại sự dồn ép hoặc đối xử bất lợi sau khi đã phải chịu đựng; hình thức phản kháng không mặc định là bạo lực. | Hành động / quá trình | 155. Tức nước vỡ bờ | 1 |
| `HD_Phóng_đại` | Diễn tả mức độ, quy mô hoặc tính chất lớn hơn thực tế; không mặc định mọi phóng đại đều nhằm lừa gạt. | Hành động / quá trình | 7. Thêm mắm dặm muối; 8. Chuyện bé xé ra to | 2 |
| `HD_Phỏng_đoán` | Đưa ra một hoặc nhiều khả năng giải thích khi chưa có đủ dữ liệu chắc chắn. | Hành động / quá trình | 95. Đoán già đoán non | 1 |
| `HD_Quyết_chiến` | Đấu tranh hoặc nỗ lực đến cùng, không dễ nhượng bộ, khi việc thắng thua được xem là rất quan trọng. | Hành động / quá trình | 59. Ăn thua đủ | 1 |
| `HD_So_sánh_thiên_lệch` | Đánh giá lựa chọn khác có vẻ tốt hơn điều mình đang có mà chưa cân nhắc đầy đủ các mặt. | Hành động / quá trình | 192. Đứng núi này trông núi nọ | 1 |
| `HD_Soi_lỗi` | Tìm rất kỹ các khuyết điểm hoặc lỗi nhỏ ở người hay sự vật, thường để bắt bẻ. | Hành động / quá trình | 60. Bới lông tìm vết; 61. Vạch lá tìm sâu | 2 |
| `HD_Suy_nghĩ` | Huy động trí nhớ, lập luận hoặc sự tập trung để tìm câu trả lời, đặc biệt khi việc ấy đòi hỏi nỗ lực trí óc. | Hành động / quá trình | 93. Vắt óc suy nghĩ | 1 |
| `HD_Tái_kết_nối_tình_cảm` | Nối lại tình cảm yêu đương từng có. Khác với bắt đầu yêu một người mới hoặc chỉ làm hòa sau tranh cãi. | Hành động / quá trình | 137. Nối lại tình xưa | 1 |
| `HD_Theo_hai_phía` | Duy trì sự theo đuổi, liên hệ hoặc cam kết với hai lựa chọn hay hai bên có thể không tương thích. | Hành động / quá trình | 81. Bắt cá hai tay | 1 |
| `HD_Thoát_hiểm` | Ra khỏi một tình trạng đe dọa hoặc giai đoạn rất khó khăn; mức an toàn sau đó được thể hiện ở KQ nếu câu có nêu. | Hành động / quá trình | 166. Thoát chết trong gang tấc | 1 |
| `HD_Tiếp_nhận_dè_dặt` | Tiếp nhận thông tin nhưng chưa tin hoàn toàn, vẫn giữ sự nghi ngờ. Không tự khẳng định thông tin ấy là sai. | Hành động / quá trình | 130. Nửa tin nửa ngờ; 186. Bán tín bán nghi | 2 |
| `HD_Tìm_kiếm` | Bỏ công để xác định vị trí hoặc nhận ra đối tượng cần tìm trong một phạm vi hay tập hợp. | Hành động / quá trình | 62. Mò kim đáy bể | 1 |
| `HD_Trả_tiền_ngay` | Thanh toán ngay trong giao dịch thay vì nhận nợ hoặc để trả sau. Không đồng nhất với chi tiêu nhiều hay lãng phí. | Hành động / quá trình | 173. Tiền trao cháo múc | 1 |
| `HD_Trao_điều_có_giá_trị` | Đưa đến người khác lời hay, sự tinh tế hoặc điều hữu ích để họ tiếp nhận. Không tự suy rằng người nhận có khả năng trân trọng. | Hành động / quá trình | 15. Đàn gảy tai trâu | 1 |
| `HD_Trao_đổi` | Các bên nói hoặc truyền đạt thông tin cho nhau; chất lượng hiểu nhau được xác định bằng nhãn khác. | Hành động / quá trình | 20. Ông nói gà, bà nói vịt | 1 |
| `HD_Trì_hoãn` | Đẩy việc phải làm sang thời điểm muộn hơn, đặc biệt đến sát hạn; khác với làm chậm do tốc độ thấp. | Hành động / quá trình | 68. Nước đến chân mới nhảy | 1 |
| `HD_Truyền_tin` | Chuyển nội dung từ người này sang người khác hoặc qua nhiều bước; không mặc định nội dung còn nguyên vẹn. | Hành động / quá trình | 14. Tam sao thất bản | 1 |
| `HD_Tự_gây_hại` | Hành động của chính chủ thể tạo bất lợi cho họ, dù họ không nhất thiết muốn tự làm hại mình. | Hành động / quá trình | 40. Tự đào hố chôn mình | 1 |
| `HD_Tự_lo_phần_mình` | Ưu tiên tự bảo đảm lợi ích của mình trong tình thế thiếu sự hỗ trợ chung. Không tự suy rằng chủ thể chủ động hại người khác. | Hành động / quá trình | 85. Mạnh ai nấy lo | 1 |
| `HD_Xem_qua_loa` | Chỉ tiếp xúc hoặc xem xét sơ lược, chưa đi sâu vào các chi tiết và bản chất cần hiểu. | Hành động / quá trình | 69. Cưỡi ngựa xem hoa | 1 |

### MD — Mục đích (21 mã)

| Mã | Nghĩa đầy đủ và giới hạn | Kiểu | Ví dụ | Số dòng |
| --- | --- | --- | --- | ---: |
| `MD_Bắt_lỗi` | Chủ thể muốn tìm được chỗ sai để chê trách hoặc bắt bẻ; chỉ dùng khi mục tiêu phê phán là một phần rõ ràng của nghĩa. | Ý định | 60. Bới lông tìm vết; 61. Vạch lá tìm sâu | 2 |
| `MD_Cản_trở` | Chủ thể muốn làm người khác khó thực hiện, chậm tiến hành hoặc không hoàn thành công việc và kế hoạch của họ. | Ý định | 49. Chọc gậy bánh xe | 1 |
| `MD_Che_giấu_sự_thật` | Chủ thể muốn người khác không nhận ra tình hình thật, thường để tránh bất lợi hoặc duy trì sự lừa dối. | Ý định | 24. Đánh lận con đen | 1 |
| `MD_Chứng_minh` | Chủ thể muốn người nghe tin hoặc chấp nhận một khẳng định dựa trên chứng cứ có thể kiểm tra. | Ý định | 4. Nói có sách, mách có chứng | 1 |
| `MD_Đổ_lỗi` | Chủ thể muốn chuyển trách nhiệm hoặc hậu quả của lỗi sang người khác thay vì đúng người gây ra. | Ý định | 29. Gắp lửa bỏ tay người | 1 |
| `MD_Giành_thắng_lợi` | Chủ thể muốn thắng cuộc hoặc đạt thành công quyết định trước thử thách hay đối thủ. | Ý định | 80. Được ăn cả, ngã về không | 1 |
| `MD_Giữ_lợi_thế` | Chủ thể muốn duy trì vị trí có lợi, phần hưởng hoặc sự thuận lợi mình đang nắm giữ. | Ý định | 84. Gió chiều nào che chiều ấy | 1 |
| `MD_Hãm_hại` | Chủ thể muốn gây thiệt hại cho người khác về an toàn, quyền lợi hoặc danh tiếng; không gán chỉ vì hành động vô tình gây hại. | Ý định | 41. Gậy ông đập lưng ông | 1 |
| `MD_Hưởng_lợi_hai_phía` | Chủ thể muốn nhận lợi ích từ cả hai lựa chọn hoặc hai bên, dù chúng có thể cạnh tranh hay mâu thuẫn. | Ý định | 81. Bắt cá hai tay | 1 |
| `MD_Kiểm_soát` | Chủ thể muốn duy trì hoặc gia tăng quyền chi phối hành vi của người khác hay tình hình chung. | Ý định | 119. Bàn tay sắt | 1 |
| `MD_Lấy_lòng` | Chủ thể muốn người khác có thiện cảm, đồng ý hoặc dành ưu ái cho mình thông qua cách tiếp cận dễ nghe. | Ý định | 18. Nói như rót mật vào tai | 1 |
| `MD_Lợi_lớn_hơn` | Chủ thể muốn thu được thứ có giá trị lớn hơn điều đã bỏ ra. Không đảm bảo ý định đó sẽ thành công. | Ý định | 196. Thả con săn sắt, bắt con cá rô | 1 |
| `MD_Lừa_người_mua` | Chủ thể muốn người mua tin vào một đề nghị hoặc chất lượng không đúng với thứ thực sự cung cấp. | Ý định | 23. Treo đầu dê, bán thịt chó | 1 |
| `MD_Né_tránh` | Chủ thể muốn tránh phải đối diện, trả lời hoặc xử lý trực tiếp một vấn đề; khác với hành động né tránh đã thực hiện. | Ý định | 25. Giả câm giả điếc | 1 |
| `MD_Thoát_nguy` | Chủ thể muốn rời khỏi tình trạng nguy hiểm hoặc khó khăn đang gặp; không mặc định việc thoát đã thành công. | Ý định | 42. Tránh vỏ dưa, gặp vỏ dừa | 1 |
| `MD_Tiết_kiệm` | Chủ thể muốn giảm hao tốn và giữ lại tiền hoặc nguồn lực để đáp ứng nhu cầu hay dự phòng. | Ý định | 106. Thắt lưng buộc bụng; 107. Bóp mồm bóp miệng | 2 |
| `MD_Tìm_lời_giải` | Chủ thể muốn nhớ ra, hiểu được hoặc giải quyết một câu hỏi hay vấn đề chưa có câu trả lời. | Ý định | 93. Vắt óc suy nghĩ | 1 |
| `MD_Tìm_ra` | Chủ thể muốn xác định được đối tượng đang tìm, chưa nói đến việc đã tìm thấy hay chưa. | Ý định | 62. Mò kim đáy bể | 1 |
| `MD_Trục_lợi` | Chủ thể muốn kiếm lợi riêng bằng cách khai thác hoàn cảnh hoặc người khác, thường mang sắc thái cơ hội hay thiếu công bằng. | Ý định | 31. Đục nước béo cò; 32. Thừa nước đục thả câu | 3 |
| `MD_Vừa_sức` | Chủ thể muốn mức chi hoặc kế hoạch phù hợp với nguồn lực thực có. Không mặc định muốn giảm mọi chi tiêu xuống thấp nhất. | Ý định | 194. Liệu cơm gắp mắm | 1 |
| `MD_Xoay_xở` | Chủ thể muốn giải quyết nhu cầu trước mắt bằng cách điều chuyển nguồn lực đang thiếu, không nhất thiết xử lý được nguyên nhân gốc. | Ý định | 110. Giật gấu vá vai | 1 |

### KQ — Kết quả, trạng thái và triển vọng (90 mã)

| Mã | Nghĩa đầy đủ và giới hạn | Kiểu | Ví dụ | Số dòng |
| --- | --- | --- | --- | ---: |
| `KQ_Bấp_bênh` | Tình trạng thiếu ổn định, có thể thất bại hoặc gặp tai họa chỉ bởi một thay đổi nhỏ. | Nguy cơ / triển vọng | 45. Ngàn cân treo sợi tóc; 46. Chỉ mành treo chuông | 2 |
| `KQ_Bất_hòa` | Quan hệ không còn hòa thuận, có mâu thuẫn hoặc đối kháng; mức độ có thể từ khó chịu đến xung đột gay gắt. | Trạng thái / thuộc tính | 131. Cơm không lành, canh không ngọt; 132. Như chó với mèo | 3 |
| `KQ_Bất_lợi_cho_mình` | Chủ thể chịu hoặc đứng trước hậu quả xấu do lời nói, quyết định hay hành động của chính mình. | Hệ quả / kết cục | 40. Tự đào hố chôn mình | 1 |
| `KQ_Bị_đe_dọa` | An toàn, quyền lợi hoặc sự tồn tại đang đứng trước khả năng bị tổn hại; nhãn chỉ nguy cơ, không khẳng định tổn hại đã xảy ra. | Nguy cơ / triển vọng | 50. Hang hùm miệng sói; 52. Vào sinh ra tử | 3 |
| `KQ_Bị_hạn_chế` | Phạm vi hành động bị thu hẹp đến mức không thể làm điều muốn làm; không suy ra chủ thể thiếu năng lực. | Trạng thái / thuộc tính | 100. Trói tay trói chân | 1 |
| `KQ_Bị_kẹp_hai_phía` | Chịu tác động hoặc sự khống chế đồng thời của hai lực gây sức ép. Không nhất thiết đang chủ động chọn giữa hai phương án. | Trạng thái / thuộc tính | 44. Trên đe dưới búa; 97. Một cổ hai tròng | 2 |
| `KQ_Buồn_bã` | Trạng thái buồn, ủ rũ hoặc mất tinh thần được câu mô tả; không suy ra một nguyên nhân cụ thể nếu chưa được nêu. | Trạng thái / thuộc tính | 144. Buồn như đưa đám | 1 |
| `KQ_Can_đảm` | Có sự gan dạ trước thử thách hay nguy hiểm. Không đồng nhất với chỉ giữ vẻ mặt bình tĩnh hoặc không có phản ứng sinh lý vì sợ. | Trạng thái / thuộc tính | 182. Gan vàng dạ sắt; 183. Gan lì tướng quân | 2 |
| `KQ_Chen_chúc` | Người hoặc vật ở quá sát nhau trong không gian hạn chế. Không tự suy số lượng tuyệt đối lớn nếu diện tích vốn rất nhỏ. | Trạng thái / thuộc tính | 164. Chật như nêm | 1 |
| `KQ_Chỉ_đủ_trước_mắt` | Nguồn sống chỉ đủ cho nhu cầu thiết yếu hiện tại, ít hoặc không có phần dự trữ. Không khẳng định chắc chắn đang thiếu ăn mỗi ngày. | Trạng thái / thuộc tính | 111. Chạy ăn từng bữa | 1 |
| `KQ_Có_thế_lực` | Có địa vị, danh tiếng hoặc ảnh hưởng đủ lớn khiến người khác phải coi trọng hoặc bị tác động. | Trạng thái / thuộc tính | 117. Tai to mặt lớn; 118. Có máu mặt | 2 |
| `KQ_Dễ_bị_hại` | Ở vị trí phơi bày trước nguy cơ mà khó tự vệ hoặc chống đỡ. Chưa khẳng định tổn hại thực sự đã xảy ra. | Nguy cơ / triển vọng | 48. Cá nằm trên thớt | 1 |
| `KQ_Đau_khổ` | Trạng thái đau buồn hoặc tổn thương tinh thần sâu sắc; trong bộ này không dùng thay cho đau thể chất. | Trạng thái / thuộc tính | 156. Ngậm đắng nuốt cay; 157. Đau như cắt | 3 |
| `KQ_Đầu_mạnh_cuối_yếu` | Quá trình có khởi đầu nổi bật, mạnh mẽ nhưng kết thúc yếu hoặc nhỏ bé hơn hẳn. Không mặc định hoàn toàn thất bại. | Hệ quả / kết cục | 70. Đầu voi đuôi chuột | 1 |
| `KQ_Đồng_điệu` | Hai người dễ hiểu và hòa hợp với suy nghĩ, cảm nhận của nhau; khác việc chỉ đồng ý về một quyết định cụ thể. | Trạng thái / thuộc tính | 121. Tâm đầu ý hợp | 1 |
| `KQ_Đúng_nhu_cầu` | Điều nhận được phù hợp với yêu cầu thực tế ở đúng hoàn cảnh đang cần, không nhất thiết là một mong ước lâu dài. | Trạng thái / thuộc tính | 163. Buồn ngủ gặp chiếu manh | 1 |
| `KQ_Được_ưu_đãi` | Chủ thể có sẵn điều kiện vật chất hoặc vị thế thuận lợi từ nền tảng xuất thân, thay vì tự đạt được trong việc đang xét. | Trạng thái / thuộc tính | 116. Ngậm thìa vàng | 1 |
| `KQ_Gánh_lỗi_thay` | Một người bị đặt vào vị trí chịu trách nhiệm hoặc hậu quả cho việc sai không do mình gây ra. | Hệ quả / kết cục | 29. Gắp lửa bỏ tay người | 1 |
| `KQ_Gắn_bó` | Quan hệ thân thiết, bền chặt hoặc có sự hiện diện hỗ trợ thường xuyên; không nhất thiết là quan hệ yêu đương. | Trạng thái / thuộc tính | 125. Như hình với bóng; 128. Đồng cam cộng khổ | 3 |
| `KQ_Gây_phiền_toái` | Lời nói hoặc hành vi tạo ra sự khó xử, ngượng ngùng hay rắc rối. Không tự nâng lên mức tai họa nghiêm trọng. | Hệ quả / kết cục | 89. Lỡ mồm lỡ miệng | 1 |
| `KQ_Giàu_có` | Sở hữu nhiều tiền của hoặc tài sản; không tự khẳng định sự giàu có đến từ nỗ lực hay may mắn. | Trạng thái / thuộc tính | 101. Tiền rừng bạc bể | 1 |
| `KQ_Giận_dữ` | Trạng thái tức giận mạnh; chỉ gán HD_Bùng_giận thêm khi câu nhấn mạnh quá trình bùng phát cơn giận. | Trạng thái / thuộc tính | 152. Giận tím mặt; 153. Nổi trận lôi đình | 3 |
| `KQ_Giống_bản_chất` | Nhiều người có cùng kiểu tính cách hoặc đặc điểm bên trong. Không gộp với giống ngoại hình hay chỉ tương hợp trong một quan hệ. | Trạng thái / thuộc tính | 200. Cá mè một lứa | 1 |
| `KQ_Hết_nhẫn_nhịn` | Chủ thể không tiếp tục chịu đựng một cách phục tùng như trước. Trong các dòng dùng nhãn này, hành động phản kháng được ghi riêng ở HD. | Hệ quả / kết cục | 155. Tức nước vỡ bờ | 1 |
| `KQ_Hiển_nhiên` | Thông tin hoặc tình trạng rõ đến mức dễ nhận thấy, ít cần suy đoán để hiểu. | Trạng thái / thuộc tính | 91. Rõ như ban ngày | 1 |
| `KQ_Hiểu_rõ` | Có kiến thức hoặc sự quen thuộc rất sâu đối với nơi chốn, đối tượng hay vấn đề đang nói tới. | Trạng thái / thuộc tính | 90. Thuộc như lòng bàn tay | 1 |
| `KQ_Hòa_hợp_trở_lại` | Quan hệ được khôi phục sự thân thiện hoặc gắn bó sau giai đoạn bất hòa hay chia cách. | Hệ quả / kết cục | 137. Nối lại tình xưa; 138. Gương vỡ lại lành | 2 |
| `KQ_Hoài_nghi` | Chưa tin hoàn toàn và vẫn nghi ngờ điều đang xét. Không đồng nhất với kết luận chắc chắn điều đó sai. | Trạng thái / thuộc tính | 130. Nửa tin nửa ngờ; 186. Bán tín bán nghi | 2 |
| `KQ_Hời_hợt` | Mức tiếp cận mới dừng ở bề mặt, chưa đạt độ hiểu sâu cần thiết; không tự khẳng định toàn bộ nhận định là sai. | Trạng thái / thuộc tính | 69. Cưỡi ngựa xem hoa | 1 |
| `KQ_Hợp_môi_trường` | Môi trường phù hợp với sở trường hoặc thói quen, khiến chủ thể thấy tự nhiên và thoải mái. Không đảm bảo thành công cụ thể. | Trạng thái / thuộc tính | 88. Như cá gặp nước | 1 |
| `KQ_Hứng_chịu_công_kích` | Đứng ở vị trí trực tiếp chịu nguy hiểm hoặc sự chỉ trích. Không tự gán trách nhiệm lãnh đạo. | Trạng thái / thuộc tính | 47. Đầu sóng ngọn gió | 1 |
| `KQ_Khó_khăn_tiếp_diễn` | Sau khi thoát một trở ngại, chủ thể lại gặp trở ngại khác; không mặc định mọi trường hợp trở ngại mới đều nặng hơn. | Hệ quả / kết cục | 42. Tránh vỏ dưa, gặp vỏ dừa | 1 |
| `KQ_Khó_rút_lui` | Việc đã tham gia hoặc cam kết khiến dừng lại, thoát ra hay đảo hướng trở nên khó khăn hoặc nguy hiểm. | Nguy cơ / triển vọng | 54. Cưỡi lên lưng hổ; 79. Đâm lao phải theo lao | 2 |
| `KQ_Khó_thành_công` | Khả năng đạt mục tiêu rất thấp hoặc bị nhiều trở ngại chi phối; đây là triển vọng, không phải kết luận đã thất bại. | Nguy cơ / triển vọng | 55. Châu chấu đá xe; 56. Trứng chọi đá | 4 |
| `KQ_Không_đáng_kể` | Mức đóng góp hoặc tác động quá nhỏ khi so với quy mô nhu cầu hay tổng thể cần giải quyết. | Trạng thái / thuộc tính | 66. Muối bỏ bể | 1 |
| `KQ_Không_đạt_cả_hai` | Không đạt được phương án nào trong hai khả năng đang xét. Không tự thêm động cơ tham lam muốn chiếm cả hai. | Hệ quả / kết cục | 170. Xôi hỏng bỏng không | 1 |
| `KQ_Không_được_trân_trọng` | Điều có giá trị không được người nhận hiểu, thưởng thức hoặc coi trọng. Không đồng nhất với hiểu rõ nhưng không nghe theo chỉ dẫn. | Hệ quả / kết cục | 15. Đàn gảy tai trâu | 1 |
| `KQ_Không_ghi_nhớ` | Nội dung nghe được không được giữ lại hay không được để tâm. Khác với hiểu mà nhất định không làm theo lời khuyên. | Hệ quả / kết cục | 96. Nghe tai này lọt tai kia | 1 |
| `KQ_Không_hiểu` | Không nắm được ý nghĩa của thông tin hoặc lời nói đang tiếp nhận; khác với hiểu nhưng không muốn nghe theo. | Trạng thái / thuộc tính | 92. Như vịt nghe sấm | 1 |
| `KQ_Không_thể_đảo_ngược` | Tình thế đã đi quá xa để có thể trở lại trạng thái trước; mạnh hơn việc chỉ khó rút lui. | Trạng thái / thuộc tính | 174. Ván đã đóng thuyền; 175. Gạo đã nấu thành cơm | 2 |
| `KQ_Không_thỏa_mãn` | Chủ thể không bằng lòng với điều đang có hoặc vẫn cho rằng điều khác đáng muốn hơn. | Trạng thái / thuộc tính | 192. Đứng núi này trông núi nọ | 1 |
| `KQ_Không_thu_được_gì` | Chủ thể không có thành quả, tài sản hoặc lợi ích mong muốn để nhận sau quá trình đã diễn ra. | Hệ quả / kết cục | 112. Trắng tay | 1 |
| `KQ_Không_tiếp_thu` | Lời nói, khuyên bảo hay phê bình không tạo được sự đón nhận hoặc thay đổi tương ứng ở người nghe; không đồng nhất với không hiểu ngôn ngữ. | Hệ quả / kết cục | 16. Nước đổ đầu vịt; 176. Nước đổ lá khoai | 2 |
| `KQ_Không_tiết_lộ` | Thông tin chưa được nói ra hoặc chưa trở thành điều người ngoài biết; không nhất thiết có động cơ xấu. | Hệ quả / kết cục | 10. Ngậm miệng như hến; 11. Kín như bưng | 2 |
| `KQ_Lãng_phí` | Tiền, thời gian hoặc công sức đã bỏ ra không mang lại giá trị tương xứng hoặc bị mất đi vô ích. | Hệ quả / kết cục | 65. Đổ sông đổ bể; 103. Ném tiền qua cửa sổ | 2 |
| `KQ_Lạnh_nhạt` | Thái độ thiếu thân thiện, ít biểu lộ tình cảm hoặc tạo khoảng cách. Không tự khẳng định người đó độc ác hoặc hoàn toàn thiếu lòng trắc ẩn. | Trạng thái / thuộc tính | 184. Lạnh như tiền | 1 |
| `KQ_Lệch_ý` | Các bên giao tiếp không hiểu nhau vì đang nghĩ về vấn đề theo những hướng hoặc nghĩa khác nhau. | Hệ quả / kết cục | 20. Ông nói gà, bà nói vịt | 1 |
| `KQ_Lo_lắng` | Trạng thái bất an, sốt ruột hoặc hồi hộp về điều chưa chắc chắn hay có nguy cơ bất lợi. | Trạng thái / thuộc tính | 145. Ruột gan như lửa đốt; 146. Đứng ngồi không yên | 3 |
| `KQ_Lộ_bản_chất` | Đặc điểm thật hay ý đồ từng được che giấu trở nên có thể nhận ra, thường là mặt xấu trong các dòng sử dụng nhãn này. | Hệ quả / kết cục | 38. Cháy nhà ra mặt chuột; 39. Lòi đuôi cáo | 2 |
| `KQ_Lợi_ích_kép` | Một hành động đem lại hai mục tiêu hay lợi ích khác nhau; không nhất thiết là lợi nhuận tài chính. | Hệ quả / kết cục | 178. Một công đôi việc; 179. Một mũi tên trúng hai đích | 2 |
| `KQ_Lưỡng_nan` | Chủ thể ở giữa những lựa chọn hoặc sức ép đối lập, khó chọn một hướng mà không chịu bất lợi hoặc từ bỏ điều quan trọng. | Trạng thái / thuộc tính | 43. Tiến thoái lưỡng nan | 1 |
| `KQ_Mạnh_bề_ngoài` | Bề ngoài có vẻ mạnh hoặc đáng sợ nhưng thực lực không tương xứng. Không đồng nhất với mạnh thật mà chủ động kiềm chế. | Trạng thái / thuộc tính | 187. Hổ giấy | 1 |
| `KQ_Nắm_lợi_thế` | Chủ thể đang giữ điều kiện quyết định hoặc ưu thế cho phép chi phối diễn biến theo hướng có lợi. | Trạng thái / thuộc tính | 99. Nắm đằng chuôi | 1 |
| `KQ_Ngang_mức` | Hai đối tượng gần ngang nhau về thuộc tính đang so sánh, có thể là năng lực, chất lượng hoặc mức độ. Không chỉ áp dụng cho sức mạnh hay cuộc đua. | Trạng thái / thuộc tính | 199. Kẻ tám lạng, người nửa cân | 1 |
| `KQ_Nghèo_khó` | Thiếu tiền của hoặc điều kiện vật chất để sống thoải mái; không quy kết nguyên nhân nghèo. | Trạng thái / thuộc tính | 108. Nghèo rớt mồng tơi; 109. Khố rách áo ôm | 2 |
| `KQ_Nghiêm_trọng_hóa` | Một việc bị nhìn hoặc trình bày như nghiêm trọng hơn thực tế; đây có thể là hệ quả diễn ngôn, không phải vấn đề thật đã lớn lên. | Hệ quả / kết cục | 8. Chuyện bé xé ra to | 1 |
| `KQ_Nguy_cơ_phản_bội` | Có khả năng người được hỗ trợ hoặc tin cậy quay lại gây hại; không khẳng định sự phản bội đã thực sự xảy ra. | Nguy cơ / triển vọng | 35. Nuôi ong tay áo; 36. Nuôi cáo trong nhà | 2 |
| `KQ_Nhút_nhát` | Đặc điểm dễ sợ hoặc thiếu mạnh dạn được câu mô tả như một trạng thái tính cách, không phải hệ quả của một hành động ngầm định. | Trạng thái / thuộc tính | 181. Nhát như cáy | 1 |
| `KQ_Nợ_nần` | Có nghĩa vụ trả một lượng tiền đáng kể, thường vượt mức dễ dàng thanh toán trong ngữ nghĩa đang xét. | Trạng thái / thuộc tính | 113. Nợ như chúa Chổm | 1 |
| `KQ_Phản_tác_dụng` | Phương án nhằm tác động xấu lên người khác lại gây bất lợi cho chính người đề ra hoặc thực hiện. | Hệ quả / kết cục | 41. Gậy ông đập lưng ông | 1 |
| `KQ_Qua_nguy_hiểm` | Chủ thể đã vượt giai đoạn nguy kịch hoặc phần khó khăn nhất; không đảm bảo mọi rủi ro về sau đều biến mất. | Hệ quả / kết cục | 167. Tai qua nạn khỏi; 168. Chết đi sống lại | 2 |
| `KQ_Quá_tải` | Lượng việc, trách nhiệm hoặc đòi hỏi vượt mức có thể xử lý thoải mái, làm chủ thể thiếu thời gian hoặc kiệt sức. | Trạng thái / thuộc tính | 73. Đầu tắt mặt tối; 74. Tối mặt tối mũi | 2 |
| `KQ_Rất_giống_nhau` | Hai đối tượng có mức tương đồng rất cao ở đặc điểm đang so sánh; không tự mở rộng sang mọi đặc điểm khác. | Trạng thái / thuộc tính | 197. Như hai giọt nước | 1 |
| `KQ_Rất_khác_nhau` | Hai đối tượng có khoảng cách rất lớn về đặc điểm, hoàn cảnh hoặc chất lượng đang được xét. | Trạng thái / thuộc tính | 198. Một trời một vực | 1 |
| `KQ_Rất_khỏe` | Có sức lực thể chất lớn. Không quy đổi thành can đảm, thông minh hay quyền lực xã hội. | Trạng thái / thuộc tính | 82. Khỏe như vâm | 1 |
| `KQ_Rùng_mình` | Phản ứng cơ thể như nổi da gà do sợ, kinh ngạc hoặc xúc động mạnh; không mặc định cảm xúc là tiêu cực. | Trạng thái / thuộc tính | 151. Nổi da gà | 1 |
| `KQ_Sai_lệch_thông_tin` | Nội dung bị biến dạng, gán sai hoặc hiểu sai so với điều ban đầu cần truyền đạt; có thể xảy ra không có chủ ý. | Hệ quả / kết cục | 14. Tam sao thất bản | 1 |
| `KQ_Sai_sự_thật` | Nội dung được phát biểu không phù hợp với thực tế; nhãn này đi cùng HD_Nói_dối khi sự sai lệch là cố ý. | Hệ quả / kết cục | 9. Ăn không nói có | 1 |
| `KQ_Sát_hạn` | Việc hành động bị đẩy đến thời điểm gần hết khoảng thời gian có thể xử lý một cách thuận lợi. | Hệ quả / kết cục | 68. Nước đến chân mới nhảy | 1 |
| `KQ_Sống_còn` | Tình thế được đặt ở mức phải thành công hoặc chịu thất bại toàn diện. Không mặc định chủ thể thực tế sẽ chết nếu thua. | Nguy cơ / triển vọng | 57. Một mất một còn | 1 |
| `KQ_Sợ_hãi` | Trạng thái lo sợ mạnh trước điều đe dọa hoặc đáng kinh hãi, không nhất thiết là đặc điểm tính cách lâu dài. | Trạng thái / thuộc tính | 148. Sợ mất mật; 149. Hồn vía lên mây | 3 |
| `KQ_Sung_túc` | Sống trong điều kiện dư dả, có đủ phương tiện để hưởng sự thoải mái; không tự xác định nguyên nhân do may hay do làm việc. | Trạng thái / thuộc tính | 165. Sống như ông hoàng | 1 |
| `KQ_Sững_sờ` | Bị bất ngờ đến mức tạm thời khó phản ứng hoặc tiếp nhận điều vừa xảy ra. | Trạng thái / thuộc tính | 160. Chết đứng như Từ Hải | 1 |
| `KQ_Tách_rời` | Các bên không còn tiếp tục chung đường hoặc gắn với nhau trong quan hệ, dự án hay tình thế đang xét. | Hệ quả / kết cục | 139. Dứt áo ra đi; 140. Đường ai nấy đi | 2 |
| `KQ_Tai_họa_dồn_dập` | Nhiều điều xấu đến cùng lúc hoặc nối tiếp nhau, thay vì một bất lợi đơn lẻ. Không quy định phải liên quan tiền hay sức khỏe. | Hệ quả / kết cục | 172. Họa vô đơn chí | 1 |
| `KQ_Tái_nhợt` | Sắc mặt trở nên rất nhợt, trong nghĩa đang chọn là phản ứng trước sợ hãi hoặc sốc; không gán chẩn đoán y khoa. | Trạng thái / thuộc tính | 159. Mặt cắt không còn giọt máu | 1 |
| `KQ_Thiếu_hụt` | Nguồn tiền hoặc vật chất không đủ để đáp ứng đồng thời các nhu cầu, có thể chỉ đủ cho sinh hoạt trước mắt. | Trạng thái / thuộc tính | 110. Giật gấu vá vai | 1 |
| `KQ_Thoát_trong_gang_tấc` | Đã tránh được nguy hiểm nhưng chỉ nhờ một khoảng cách, thời gian hoặc cơ hội rất nhỏ. | Hệ quả / kết cục | 166. Thoát chết trong gang tấc | 1 |
| `KQ_Thu_nhập_lớn` | Tiền được thu về với lượng lớn hoặc tốc độ cao; khác KQ_Giàu_có là mức tài sản đã sở hữu. | Hệ quả / kết cục | 102. Tiền vào như nước | 1 |
| `KQ_Thua_lỗ_nặng` | Mất một phần rất lớn hoặc toàn bộ số tiền, vốn hay tài sản đã có hoặc đem vào rủi ro. | Hệ quả / kết cục | 171. Mất cả chì lẫn chài | 1 |
| `KQ_Thuận_lợi` | Quá trình thực hiện tiến triển dễ dàng với ít trở ngại đáng kể; không mặc định kết quả cuối cùng đã đạt. | Trạng thái / thuộc tính | 180. Thuận buồm xuôi gió | 1 |
| `KQ_Thừa_thãi` | Điều được cung cấp hoặc chỉ dẫn không cần thiết vì người nhận hay tình huống đã đáp ứng nhu cầu đó. | Hệ quả / kết cục | 94. Dạy khỉ leo cây | 1 |
| `KQ_Tiến_triển_tốt` | Công việc hoặc vị thế đang phát triển theo chiều tích cực. Không tự gán nguyên nhân là may mắn hay đảm bảo đã giàu có. | Trạng thái / thuộc tính | 114. Ăn nên làm ra; 115. Diều gặp gió | 2 |
| `KQ_Toại_nguyện` | Điều thực tế nhận được phù hợp với điều chủ thể đã mong muốn từ trước. | Hệ quả / kết cục | 161. Cầu được ước thấy | 1 |
| `KQ_Ướt_sũng` | Người hoặc quần áo bị ướt rất nhiều, thường trông nhếch nhác. Không tự suy nguyên nhân là mưa, ngã xuống nước hay bơi. | Trạng thái / thuộc tính | 78. Ướt như chuột lột | 1 |
| `KQ_Vô_cảm` | Thiếu thương xót hoặc không bị lay động trước đau khổ, cảm xúc hay lời cầu xin của người khác. | Trạng thái / thuộc tính | 185. Lòng dạ sắt đá | 1 |
| `KQ_Vô_ích` | Việc làm hoặc công sức không tạo ra tiến bộ hay kết quả hữu ích; khác lãng phí ở chỗ không bắt buộc nhấn mạnh phần nguồn lực bị mất. | Hệ quả / kết cục | 63. Dã tràng xe cát; 64. Công dã tràng | 3 |
| `KQ_Vui_sướng` | Trạng thái hạnh phúc, phấn khởi hoặc thỏa mãn ở mức rất cao. | Trạng thái / thuộc tính | 141. Vui như mở cờ trong bụng; 142. Mừng như bắt được vàng | 3 |
| `KQ_Vượt_khả_năng` | Mức chi hoặc yêu cầu vượt giới hạn nguồn lực có thể đáp ứng; trong bộ hiện tại tập trung vào chi tiêu. | Hệ quả / kết cục | 104. Vung tay quá trán | 1 |
| `KQ_Xung_đột_tăng` | Mức căng thẳng, thù địch hoặc đối đầu giữa các bên trở nên mạnh hơn trước. | Hệ quả / kết cục | 30. Đổ dầu vào lửa | 1 |

### BC — Bối cảnh (28 mã)

| Mã | Nghĩa đầy đủ và giới hạn | Kiểu | Ví dụ | Số dòng |
| --- | --- | --- | --- | ---: |
| `BC_Cảm_xúc` | Trải nghiệm hoặc biểu hiện tình cảm của chủ thể như vui, buồn, sợ, giận; không mặc định nguyên nhân nếu câu không nêu. | Khung ngữ cảnh | 12. Ruột để ngoài da; 141. Vui như mở cờ trong bụng | 19 |
| `BC_Công_việc` | Một nhiệm vụ, kế hoạch hoặc quá trình thực hiện việc cần làm; không giới hạn ở việc làm có trả lương. | Khung ngữ cảnh | 49. Chọc gậy bánh xe; 62. Mò kim đáy bể | 16 |
| `BC_Đánh_giá` | Hoạt động nhận xét chất lượng, động cơ, ưu điểm hoặc khuyết điểm của người hay sự việc. | Khung ngữ cảnh | 60. Bới lông tìm vết; 61. Vạch lá tìm sâu | 2 |
| `BC_Đời_sống` | Điều kiện sinh hoạt và mức hưởng thụ trong cuộc sống thường ngày; không tự quy định nguồn gốc của điều kiện ấy. | Khung ngữ cảnh | 116. Ngậm thìa vàng; 161. Cầu được ước thấy | 5 |
| `BC_Giao_tiếp` | Tình huống nói, nghe hoặc trao đổi giữa người với người; nhãn không hàm ý đã giao tiếp thành công. | Khung ngữ cảnh | 1. Nói toạc móng heo; 2. Thẳng như ruột ngựa | 20 |
| `BC_Không_gian` | Không gian được xét về mức chật, rộng, đông hoặc vắng. Không suy từ chật chội sang tình trạng nghèo khó hay nguy hiểm. | Khung ngữ cảnh | 164. Chật như nêm | 1 |
| `BC_Lợi_ích` | Việc tìm kiếm, bảo vệ hoặc phân chia phần có lợi cho cá nhân hay nhóm; không tự khẳng định hành vi là xấu. | Khung ngữ cảnh | 31. Đục nước béo cò; 32. Thừa nước đục thả câu | 7 |
| `BC_May_rủi` | Yếu tố ngẫu nhiên hoặc điều ngoài khả năng kiểm soát ảnh hưởng đến triển vọng hay kết quả của chủ thể. | Khung ngữ cảnh | 169. Lành ít dữ nhiều; 172. Họa vô đơn chí | 2 |
| `BC_Mua_bán` | Quan hệ cung cấp, chào hàng, mua hàng hoặc trao đổi giá trị giữa bên bán và bên mua. | Khung ngữ cảnh | 23. Treo đầu dê, bán thịt chó; 173. Tiền trao cháo múc | 2 |
| `BC_Năng_lực` | Khả năng thực hiện một việc, mức chuẩn bị hoặc độ phù hợp giữa kỹ năng của chủ thể với hoạt động và môi trường. | Khung ngữ cảnh | 88. Như cá gặp nước; 98. Chưa học bò đã lo học chạy | 2 |
| `BC_Nghịch_cảnh` | Hoàn cảnh đau khổ, bất lợi hoặc khó khăn mà chủ thể phải chịu hay cố gắng vượt qua. | Khung ngữ cảnh | 42. Tránh vỏ dưa, gặp vỏ dừa; 51. Cắn răng chịu đựng | 3 |
| `BC_Ngoại_hình` | Dáng vẻ hoặc tình trạng nhìn thấy ở người, quần áo và đồ vật. Không dùng ngoại hình để suy đoán tính cách hay năng lực. | Khung ngữ cảnh | 78. Ướt như chuột lột | 1 |
| `BC_Nguồn_lực` | Tiền của, thời gian, công sức hoặc phương tiện được xem xét về mức đủ, thiếu, sử dụng hay lãng phí. | Khung ngữ cảnh | 37. Ngồi mát ăn bát vàng; 65. Đổ sông đổ bể | 6 |
| `BC_Nguy_hiểm` | Có khả năng tổn hại đáng kể đối với con người, công việc hoặc lợi ích; không mặc định tai họa đã xảy ra. | Khung ngữ cảnh | 45. Ngàn cân treo sợi tóc; 46. Chỉ mành treo chuông | 10 |
| `BC_Nhận_thức` | Phạm vi hiểu biết, mức hiểu vấn đề hoặc cách nhìn thế giới của chủ thể. | Khung ngữ cảnh | 69. Cưỡi ngựa xem hoa; 90. Thuộc như lòng bàn tay | 6 |
| `BC_Quan_hệ` | Mối liên hệ giữa người với người, gồm tình bạn, gia đình, đồng nghiệp hoặc các quan hệ hỗ trợ và tin cậy. | Khung ngữ cảnh | 27. Đâm sau lưng; 28. Bôi tro trát trấu | 22 |
| `BC_Quyền_lực` | Khả năng ảnh hưởng, kiểm soát, quyết định hoặc buộc người khác phải tuân theo trong một tổ chức hay cộng đồng. | Khung ngữ cảnh | 99. Nắm đằng chuôi; 117. Tai to mặt lớn | 6 |
| `BC_Quyết_định` | Chủ thể cân nhắc, lựa chọn hoặc đã định đoạt một hướng hành động, nhất là khi có hệ quả đáng kể. | Khung ngữ cảnh | 40. Tự đào hố chôn mình; 43. Tiến thoái lưỡng nan | 9 |
| `BC_Rủi_ro` | Chủ thể đứng trước khả năng được hoặc mất đáng kể khi tham gia một việc có kết quả không chắc chắn. | Khung ngữ cảnh | 80. Được ăn cả, ngã về không | 1 |
| `BC_So_sánh` | Đặt hai người hoặc sự vật cạnh nhau để xét mức giống, khác hay tương xứng của họ. | Khung ngữ cảnh | 197. Như hai giọt nước; 198. Một trời một vực | 4 |
| `BC_Sức_khỏe` | Sức lực và tình trạng cơ thể; trong bản này dùng để xét mức khỏe về thể chất, không đưa ra chẩn đoán. | Khung ngữ cảnh | 82. Khỏe như vâm | 1 |
| `BC_Tài_chính` | Thu nhập, tiền bạc, chi tiêu, tài sản hoặc nợ; ưu tiên nhãn này khi nghĩa đang chọn chỉ rõ yếu tố tiền. | Khung ngữ cảnh | 101. Tiền rừng bạc bể; 102. Tiền vào như nước | 13 |
| `BC_Tập_thể` | Nhiều người cùng hành động hoặc có quan hệ về lập trường và mục tiêu trong một nhóm. | Khung ngữ cảnh | 86. A dua a tòng; 122. Đồng tâm hiệp lực | 4 |
| `BC_Thông_tin` | Sự tồn tại, độ đúng, việc truyền đi, che giấu hoặc tiếp nhận tin tức và tri thức. | Khung ngữ cảnh | 10. Ngậm miệng như hến; 11. Kín như bưng | 6 |
| `BC_Tính_cách` | Đặc điểm tương đối ổn định trong cách một người cảm nhận hoặc hành xử; không đồng nhất với cảm xúc nhất thời. | Khung ngữ cảnh | 181. Nhát như cáy; 182. Gan vàng dạ sắt | 7 |
| `BC_Tốc_độ` | Mức nhanh hoặc chậm của chuyển động, phản ứng hay tiến độ thực hiện một việc. | Khung ngữ cảnh | 75. Vắt chân lên cổ; 76. Ba chân bốn cẳng | 4 |
| `BC_Ứng_xử` | Cách một người thể hiện thái độ, xử sự hoặc trình bày bản thân trước người khác. | Khung ngữ cảnh | 21. Khẩu Phật tâm xà; 22. Miệng nam mô, bụng một bồ dao găm | 9 |
| `BC_Xung_đột` | Có sự đối kháng, tranh chấp, tức giận hoặc hành vi gây hại giữa các bên. | Khung ngữ cảnh | 30. Đổ dầu vào lửa; 41. Gậy ông đập lưng ông | 12 |

## 6. Nhật ký thay cặp có vấn đề

Bảng này lưu lý do thay các đối chiếu quan trọng; các chỉnh sửa nhãn còn lại nằm trong CSV và các nhóm ở phần 4. Không giữ lại một cặp chỉ để đủ 200 nếu nét nghĩa chính không khớp.

| Dòng | Cặp ở bản 1.0 | Cặp ở bản 2.0 | Lý do |
| ---: | --- | --- | --- |
| 6 | Ba hoa chích chòe — Talk the hind legs off a donkey | Nói như khướu — Talk the hind legs off a donkey | Bỏ nét khoe khoang không có trong câu Anh; dùng câu Việt thực sự chỉ nói nhiều. |
| 15 | Đàn gảy tai trâu — Fall on deaf ears | Đàn gảy tai trâu — Cast pearls before swine | Phân biệt không có khả năng hiểu hoặc thưởng thức với nghe lời khuyên mà không làm theo. |
| 19 | Đánh trống lảng — Throw someone off the scent | Nói bóng nói gió — Drop hints | Không đồng nhất việc chuyển chủ đề với mọi cách đánh lạc hướng. |
| 25 | Giả nhân giả nghĩa — Shed crocodile tears | Giả câm giả điếc — Play dumb | Giả nhân giả nghĩa rộng hơn giả vờ khóc thương; thay bằng đối chiếu có cùng hành vi. |
| 27 | Ném đá giấu tay — Stab someone in the back | Đâm sau lưng — Stab someone in the back | Ném đá giấu tay không nhất thiết có sự phản bội lòng tin; đổi câu Việt để giữ nét này. |
| 28 | Ngậm máu phun người — Drag someone's name through the mud | Bôi tro trát trấu — Drag someone's name through the mud | Drag someone's name through the mud không nhất thiết là vu khống bằng thông tin sai sự thật. |
| 32 | Mượn gió bẻ măng — Fish in troubled waters | Thừa nước đục thả câu — Fish in troubled waters | Thay câu có phạm vi cơ hội rộng bằng câu trực tiếp nói lợi dụng sự rối ren. |
| 37 | Rước voi về giày mả tổ — Let the fox into the henhouse | Ngồi mát ăn bát vàng — Get a free ride | Bỏ đối chiếu làm mất nét phản bội cộng đồng của câu Việt cũ. |
| 47 | Đứng mũi chịu sào — Bear the brunt | Đầu sóng ngọn gió — In the firing line | Không dùng chịu tác động thay cho nghĩa đứng đầu gánh trách nhiệm. |
| 48 | Dầu sôi lửa bỏng — In the eye of the storm | Cá nằm trên thớt — A sitting duck | Thay cặp chỉ chung nét khủng hoảng bằng đối chiếu cùng nét dễ bị hại và thiếu tự vệ. |
| 51 | Nếm mật nằm gai — Grit one's teeth | Cắn răng chịu đựng — Grit one's teeth | Bỏ nét nuôi chí lớn hoặc phục thù không hiện diện ở câu Anh cũ. |
| 55 | Châu chấu đá xe — David and Goliath | Châu chấu đá xe — Fight a losing battle | Không dùng David and Goliath vì điển tích có thể gợi hy vọng người yếu thắng, trái sắc thái chính của câu Việt. |
| 63 | Dã tràng xe cát — Beat one's head against a brick wall | Dã tràng xe cát — Plough the sand | Chọn thành ngữ trực tiếp chỉ lao động vô ích; không thêm trở ngại cứng đầu hay sự bực bội. |
| 71 | Làm thân trâu ngựa — Work like a dog | Làm như trâu ngựa — Work like a dog | Bỏ nét thân phận nô dịch mà câu Anh không tự khẳng định. |
| 78 | Chân lấm tay bùn — Get one's hands dirty | Ướt như chuột lột — Like a drowned rat | Get one's hands dirty không có nghĩa sống bằng nghề nông như chân lấm tay bùn. |
| 79 | Đâm lao phải theo lao — In for a penny, in for a pound | Đâm lao phải theo lao — Be in too deep | Giữ sự mắc kẹt sau khi đã dấn vào; bỏ sắc thái tự nguyện chơi đến cùng của câu Anh cũ. |
| 80 | Được ăn cả, ngã về không — All or nothing | Được ăn cả, ngã về không — Go for broke | Chọn cách nói trực tiếp có nét đánh cược toàn bộ, thay vì all or nothing còn có thể chỉ một điều kiện đàm phán. |
| 81 | Bắt cá hai tay — Have a foot in both camps | Bắt cá hai tay — Run with the hare and hunt with the hounds | Thay cách nói có thể chỉ liên hệ trung lập với hai nhóm bằng cách nói trực tiếp chỉ theo hai phía đối nghịch. |
| 82 | Cả thèm chóng chán — A passing fancy | Khỏe như vâm — As strong as an ox | Sở thích nhất thời không đủ để biểu đạt tính cả thèm chóng chán; thay cặp. |
| 85 | Theo đóm ăn tàn — Jump on the bandwagon | Mạnh ai nấy lo — Every man for himself | Không đồng nhất việc bám người có lợi thế với tham gia một xu hướng thành công. |
| 88 | Ếch ngồi đáy giếng — Live in a bubble | Như cá gặp nước — Be in one's element | Bỏ cặp chỉ giữ hiểu biết hạn hẹp mà làm mất sự tự cao của ếch ngồi đáy giếng. |
| 89 | Ếch chết tại miệng — Put one's foot in one's mouth | Lỡ mồm lỡ miệng — Put one's foot in one's mouth | Không dùng lỗi nói gây ngượng để đại diện mọi tai họa nghiêm trọng do miệng mà ra. |
| 94 | Suy bụng ta ra bụng người — Measure others by one's own yardstick | Dạy khỉ leo cây — Teach one's grandmother to suck eggs | Thay ánh xạ lẫn giữa suy đoán động cơ và đánh giá bằng chuẩn mực cá nhân. |
| 96 | Lấy râu ông nọ cắm cằm bà kia — Get one's wires crossed | Nghe tai này lọt tai kia — Go in one ear and out the other | Bỏ cặp lẫn thông tin của người này với người kia nhưng câu Anh chỉ nói hiểu nhầm khi giao tiếp. |
| 97 | Ôm rơm rặm bụng — Bite off more than one can chew | Một cổ hai tròng — Between the hammer and the anvil | Ôm rơm rặm bụng không nhất thiết là nhận quá khả năng; thay bằng đối chiếu hai phía gây sức ép. |
| 98 | Cầm đèn chạy trước ô tô — Jump the gun | Chưa học bò đã lo học chạy — Try to run before one can walk | Cầm đèn chạy trước ô tô còn chỉ vượt mặt người giỏi hơn, không chỉ hành động sớm. |
| 120 | Một tay che trời — Be a law unto oneself | Ra oai tác quái — Throw one's weight around | Tự coi mình ngoài quy tắc không đồng nghĩa có quyền lực che lấp mọi việc. |
| 130 | Trên thuận dưới hòa — Sing from the same hymn sheet | Nửa tin nửa ngờ — Take something with a pinch of salt | Không thu hẹp hòa thuận giữa cấp trên và cấp dưới thành cùng phát biểu một quan điểm. |
| 131 | Cơm không lành, canh không ngọt — Be at daggers drawn | Cơm không lành, canh không ngọt — Be at odds | Giảm cường độ thù địch bị thêm vào bởi at daggers drawn. |
| 133 | Bằng mặt không bằng lòng — Keep up appearances | Nói một đằng, làm một nẻo — Say one thing and do another | Không đồng nhất giữ hình ảnh tốt đẹp nói chung với giả vờ hòa thuận trong quan hệ. |
| 136 | Trở mặt như trở bàn tay — Turn on a dime | Thay lòng đổi dạ — Turn one's coat | Turn on a dime chỉ sự đổi hướng nhanh; không có nét bội bạc của câu Việt cũ. |
| 145 | Ruột gan như lửa đốt — Be on tenterhooks | Ruột gan như lửa đốt — Be in a stew | Không tự thêm điều kiện phải chờ kết quả chỉ để ghép với on tenterhooks. |
| 155 | Tức nước vỡ bờ — Reach breaking point | Tức nước vỡ bờ — The worm turns | Reach breaking point chỉ đạt giới hạn, không tự khẳng định phản kháng. |
| 157 | Đau như cắt — Be cut to the quick | Đau như cắt — Have one's heart torn out | Bỏ cách nói thường hàm ý tổn thương vì bị xúc phạm khi câu Việt không có điều kiện ấy. |
| 162 | Chó ngáp phải ruồi — Hit the jackpot | Ngủ như chết — Sleep like a log | Hit the jackpot không mang nét bất tài mà gặp may của câu Việt cũ. |
| 164 | Mèo mù vớ cá rán — Luck out | Chật như nêm — Packed like sardines | Luck out chỉ gặp may, không biểu đạt việc không có khả năng mà vẫn được lợi. |
| 165 | Chuột sa chĩnh gạo — Be in clover | Sống như ông hoàng — Live like a king | Tình trạng sung túc không đồng nghĩa đột nhiên gặp vận may như chuột sa chĩnh gạo. |
| 172 | Tiền mất tật mang — A double whammy | Họa vô đơn chí — It never rains but it pours | Bỏ đối chiếu chỉ giữ hai bất lợi mà mất cấu trúc cụ thể mất tiền và thêm bệnh/hại. |
| 173 | Bút sa gà chết — Sign one's life away | Tiền trao cháo múc — Cash on the barrelhead | Sign one's life away thêm mức nghĩa vụ nặng nề không bắt buộc ở bút sa gà chết. |
| 174 | Ván đã đóng thuyền — A done deal | Ván đã đóng thuyền — What's done is done | A done deal chỉ việc đã chốt; thay bằng cách nói trực tiếp khẳng định không thể làm lại quá khứ. |
| 175 | Gạo đã nấu thành cơm — There is no turning back | Gạo đã nấu thành cơm — What's done is done | Dùng cùng nghĩa và khung với ván đã đóng thuyền; không thêm thái độ khuyên chấp nhận vào MD. |
| 182 | Gan vàng dạ sắt — Have nerves of steel | Gan vàng dạ sắt — As brave as a lion | Phân biệt lòng can đảm với riêng khả năng giữ bình tĩnh của nerves of steel. |
| 183 | Gan lì tướng quân — Have nerves of steel | Gan lì tướng quân — As brave as a lion | Giữ chung lõi can đảm với gan vàng dạ sắt, không gán kết quả bình tĩnh khi chưa đủ căn cứ. |
| 184 | Lòng lang dạ sói — Have a heart of stone | Lạnh như tiền — As cold as ice | Không đánh đồng độc ác với thiếu thương cảm; thay câu Việt và nghĩa đối chiếu. |
| 186 | Bụng dạ hẹp hòi — Bear a grudge | Bán tín bán nghi — Take something with a pinch of salt | Hẹp hòi không chỉ là giữ oán; bỏ ánh xạ quá hẹp và thêm nhóm hoài nghi có nghĩa tương ứng. |
| 187 | Miệng hùm gan sứa — All bark and no bite | Hổ giấy — A paper tiger | Không suy nhát gan từ việc không thực hiện lời đe dọa; thay bằng đối chiếu cùng nét mạnh giả, yếu thật. |
| 194 | Tham bát bỏ mâm — Penny wise and pound foolish | Liệu cơm gắp mắm — Cut one's coat according to one's cloth | Penny wise and pound foolish chỉ một kiểu tính toán tài chính, không bao phủ mọi trường hợp ham lợi nhỏ bỏ lợi lớn. |
| 195 | Há miệng chờ sung — Sit on one's hands | Khoanh tay đứng nhìn — Sit on one's hands | Sit on one's hands không tự có nét chờ lợi tự đến của há miệng chờ sung. |
| 196 | Ăn xổi ở thì — Make a quick buck | Thả con săn sắt, bắt con cá rô — Throw a sprat to catch a mackerel | Kiếm tiền nhanh không đồng nghĩa với toàn bộ lối sống ăn xổi ở thì. |
| 199 | Kẻ tám lạng, người nửa cân — Neck and neck | Kẻ tám lạng, người nửa cân — Be on a par | Không buộc sự ngang nhau phải nằm trong một cuộc đua đang sít sao. |
| 200 | Nồi nào úp vung nấy — Be cut from the same cloth | Cá mè một lứa — Birds of a feather | Hợp nhau không đồng nghĩa giống hệt nhau; thay nồi nào úp vung nấy bằng câu thực sự nói cùng loại. |

## 7. Nguồn và mức kiểm chứng

Khung bốn vai trò lấy cảm hứng từ bài trình bày của Ming Qian: *Automating Idiom Translation with Cross-Lingual Natural Language Generation Grounded in Semantic Analyses Using Large Language Models*, PDF người dùng đã gửi. Bộ cặp và các mã ở đây là biên soạn mới. Không khẳng định đã chạy FrameNet, dùng một ontology chuẩn hay tái tạo kết quả thực nghiệm của tác giả.

Các nguồn dưới đây dùng để đối chiếu chọn mẫu những cách nói cần xác nhận, không phải nguồn chứng thực toàn bộ ánh xạ Anh–Việt hoặc toàn bộ nhãn. Thông tin từ từ điển dùng để kiểm tra nghĩa câu Anh; quyết định ghép cặp và giới hạn nghĩa là quyết định biên soạn riêng.

| Nội dung đối chiếu | Nguồn |
| --- | --- |
| Theo hai phía đối nghịch | [Dictionary.com — run with](https://www.dictionary.com/browse/run-with) |
| Phản kháng sau chịu đựng | [Cambridge — the worm turns](https://dictionary.cambridge.org/dictionary/english/worm-turns) |
| Bỏ lợi nhỏ mong lợi lớn | [Wiktionary — throw a sprat to catch a mackerel](https://en.wiktionary.org/wiki/throw_a_sprat_to_catch_a_mackerel) |
| Đổi lòng trung thành | [Wiktionary — turn one's coat](https://en.wiktionary.org/wiki/turn_one%27s_coat) |
| Công sức vô ích | [Oxford Dictionary of Idioms, bản 2, mục plough the sand](https://ngoaingu.vimaru.edu.vn/wp-content/uploads/documents/Oxford-Dictionary-of-Idioms-1.pdf) |
| Trả tiền ngay | [Dictionary.com — cash on the barrelhead](https://www.dictionary.com/browse/cash-on-the-barrelhead) |
| Đau khổ tinh thần | [Cambridge — tear someone's heart out](https://dictionary.cambridge.org/dictionary/english/tear-heart-out) |
| Lo lắng, bồn chồn | [Oxford Learner's Dictionaries — stew](https://www.oxfordlearnersdictionaries.com/definition/english/stew_1) |
| So sánh lòng can đảm | [Oxford Learner's Dictionaries — brave](https://www.oxfordlearnersdictionaries.com/us/definition/english/brave_1) |
| Nói liên tục, nhiều | [Cambridge Dictionary Blog — how we talk](https://dictionaryblog.cambridge.org/2022/11/23/he-could-talk-the-hind-legs-off-a-donkey-how-we-talk-part-1/) |
| Cung cấp thứ đã có quá nhiều | [Dictionary.com — carry coals to Newcastle](https://www.dictionary.com/browse/carry-coals-to-newcastle) |
| Chặn đường cơ hội người đi sau | [Wiktionary — pull up the ladder](https://en.wiktionary.org/wiki/pull_up_the_ladder) |

Một số cách nói Anh-Anh hoặc văn chương như “plough the sand”, “run with the hare and hunt with the hounds”, “nurse a viper in one's bosom” không phải lựa chọn tự nhiên nhất trong mọi hội thoại đời thường. Cột câu Anh là mục từ để đối chiếu nghĩa; khi dịch câu hoàn chỉnh còn cần biến đổi chủ ngữ, thì, bổ ngữ và sắc thái.

## 8. Dùng trong nghiên cứu

Nếu dùng để huấn luyện hoặc đánh giá mô hình, cần người biết hai ngôn ngữ thẩm định độc lập cả việc ghép cặp lẫn gán vai trò. Giữ nhóm đồng nghĩa và các mục Anh trùng nghĩa trong cùng nhóm khi chia tập để tránh rò rỉ giữa huấn luyện và kiểm thử. Không dùng kết quả kiểm tra số cột hoặc khung trùng làm bằng chứng rằng mọi bản dịch đã đúng.
