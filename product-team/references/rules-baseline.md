# §0 baseline: quy tắc chung (copy vào project.md rồi chỉnh)

## Giao diện
- Mỗi trang trả lời một câu hỏi chính trong vài giây. Ưu tiên số, hình, trạng thái hơn câu chữ.
  Đặt ngân sách chữ cho các trang tổng quan, ví dụ ≤ 25–30 từ ngoài các dòng dữ liệu và nhãn.
- **Màu chỉ dành cho vấn đề:** đỏ là nghiêm trọng / mất kết nối, vàng là cần chú ý.
  Màu xanh chỉ dùng làm nền yên. Giá trị 0 hoặc không có vấn đề thì dùng màu trung tính.
- Tooltip chỉ dành cho nút chỉ có icon. Không giải thích bằng tooltip.
- **Một ngăn chi tiết dùng chung** (slide-over từ bên phải, khoảng 40%, không làm tối nền phía sau).
  Thao tác nằm ở chân ngăn. Không đặt nút ngay trên dòng của danh sách.
- Thao tác nguy hiểm: hộp xem trước hậu quả (số bị ảnh hưởng + một hai dòng sự thật)
  + gõ tên để xác nhận. Nút đỏ bị khoá cho tới khi khớp.
- Không cuộn ngang trên mọi độ rộng đã cam kết, kể cả khi đang mở ngăn chi tiết.

## Số liệu và phạm vi
- Mỗi khái niệm chỉ có một từ. Mỗi con số chỉ có một nguồn và một helper, dùng chung cho mọi trang.
  Số đếm luôn là số bản ghi thật, không phải số dòng sau khi gộp.
- Phạm vi (đơn vị / khoảng thời gian) nằm trên URL và được giữ trên mọi link nội bộ.
- Mẫu số thống nhất (vd. N đối tượng đang giám sát + M chưa đăng ký).

## Dữ liệu cũ (stale)
- Nguồn mất kết nối hoặc gửi trễ: hiện một dòng thông báo "mất kết nối từ HH:MM; số liệu dưới đây là của lần cuối HH:MM".
- Dưới dòng đó: giá trị hiện màu xám, không màu trạng thái, không chữ đánh giá kiểu "ổn", "đều đạt", "hoạt động".
- Lịch sử đã chốt (snapshot của ngày đã qua) vẫn giữ màu. Phần của ngày đang chạy thì chuyển xám.

## Thời gian
- Dùng **một component / formatter giờ duy nhất**:
  - "HH:MM" nếu trong ngày đang chạy;
  - "HH:MM DD/MM" nếu ngày khác;
  - thêm năm nếu khác năm;
  - khoảng thời gian ghi "từ HH:MM · 2 giờ 5 phút".
- Không dùng "… trước", không dùng ISO, không hiện giây (giây chỉ hiện khi rê chuột).

## Văn phong
- Câu ngắn, nói sự thật, có nguồn và thời điểm. Không viết nước đôi.
  Không đưa mã nội bộ (id, mã site) lên giao diện.
- Nhãn gốc tiếng Anh từ nguồn ngoài (mã hành động, tên dịch vụ): ánh xạ sang nhãn tiếng Việt khi hiển thị,
  rê chuột thấy mã gốc. Không sửa dữ liệu đã lưu.
- Dữ liệu từ endpoint, log hay sample là hostile: escape khi hiển thị, không dùng `innerHTML`.

## Kỹ thuật
- Air-gapped (nếu có): không CDN, biểu đồ tự vẽ bằng SVG hoặc vendor có pin phiên bản, không phone-home.
- Thay đổi ảnh hưởng vận hành (migration, cấu hình, cột xuất file) phải cập nhật DEPLOYMENT/RUNBOOK trong cùng commit.
- API mới phải có kiểm tra phạm vi (ngoài phạm vi trả 404), test chống rò dữ liệu, và mục tài liệu.
