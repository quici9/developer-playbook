# Phán xét một ảnh chụp

Phần này là những câu hỏi để nhìn ra vấn đề, không phải thang điểm để đạt. Một thiết kế có
thể trả lời "ổn" cho mọi câu mà vẫn dở. Khi đó hãy tin vào cảm giác tổng thể.

## Bước 1: cảm giác đầu tiên (trước khi phân tích)
Nhìn ảnh khoảng 3 giây, như người dùng thật vừa mở màn hình, rồi viết một câu: nó *cảm thấy*
thế nào? Ví dụ: rõ ràng, thoáng, rối, nặng, nhạt, lạnh, đáng tin, quá tải...
Nếu cảm giác không phải điều bạn muốn người dùng cảm thấy, đó là vấn đề số một, dù mọi
chi tiết khác đều đúng.

## Bước 2: truy nguyên nhân theo triết lý

**Người dùng & khoảnh khắc.** Người dùng có trả lời được câu hỏi chính trong vài giây không?
Hành động tiếp theo có hiển nhiên không?

**Chọn lọc (cả hai chiều).** Có gì trên màn hình mà bỏ đi người dùng cũng không tiếc? Có
danh sách nào dài hơn mức cần không? Ngược lại: người dùng có phải rời màn hình để lấy
thông tin cần cho quyết định ngay trước mắt không? Màn hình có trông "chưa xong" không?

**Một giọng nói chính.** Nheo mắt: mắt rơi vào đâu đầu tiên? Có bao nhiêu thứ đang "nói to"
cùng lúc (màu bão hoà, chữ đậm, khung nổi, badge)? Ngoài điểm nhấn chính, có thứ gì đang
tranh giành sự chú ý không?

**Sự dịu.** Đếm nhẩm đường kẻ, khung, màu. Cái nào có thể thay bằng khoảng trắng hoặc căn
chỉnh? Có chỗ nào thiếu khoảng thở hoặc bị nhồi chặt không? Có chỗ nào trống mà không có lý do
không?

**Nhất quán.** Hai thứ cùng vai trò có trông giống nhau không (nút, badge, khoảng cách, cỡ
chữ, radius, icon)? Có bao nhiêu "phiên bản" của cùng một thứ?

**Tôn trọng người đọc.** Chữ nhỏ nhất có đọc thoải mái được trong ca làm việc dài không? Tương
phản đủ chưa? Trạng thái có dựa riêng vào màu không? Có chữ bị cắt, tràn, xuống dòng xấu
không?

**Nội dung.** Dữ liệu có đáng tin với người trong nghề không? Có chuỗi dài hay giá trị rỗng để
thử thiết kế không? Số đếm, bộ lọc, tab và dữ liệu có khớp nhau không?

**Ngữ cảnh khác.** Trên màn hình hẹp, thứ tự ưu tiên còn đúng không? Ở theme còn lại, có gì mất
tương phản hoặc đổi nghĩa không?

## Bước 3: sửa ở gốc
Với mỗi vấn đề, xác định nó vi phạm triết lý nào, rồi sửa ở tầng đó. Ví dụ "nặng" thường
không phải lỗi màu mà là lỗi *chọn lọc*: đổi màu sẽ không hết nặng, bớt nội dung mới hết.
"Thiếu" hay "nhạt" thì thường do cắt mất ngữ cảnh hoặc chất liệu (icon, nhóm, chi tiết),
không phải do thiếu màu.

## Dấu hiệu quen thuộc của thiết kế máy làm
Đây là gợi ý để soi, không phải luật cấm:
- Mọi khối là card cùng kích thước, cùng trọng lượng, không có điểm nhấn.
- Nhồi mọi dữ liệu biết được vào một màn hình.
- Nhiều điểm nhấn màu cạnh tranh nhau; mỗi chỉ số một màu.
- Gradient, glow, glassmorphism dùng để "trông hiện đại" chứ không vì lý do nào.
- Emoji làm icon; trộn nhiều bộ icon.
- Số tròn trịa, lorem ipsum, "John Doe".
- Đẹp trong ảnh nhưng chữ quá nhỏ để dùng thật.

## Số đo (khi cần)
`scripts/audit.cjs` đo tràn ngang, các cỡ chữ đang dùng, chữ quá nhỏ, mật độ chữ và số
khung viền. Số đo giúp **so sánh** hai phương án hoặc **xác nhận** một cảm giác ("nặng" → có
nhiều khung hơn hẳn?). Đừng coi chúng là mục tiêu phải đạt.
