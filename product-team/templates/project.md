# <Tên dự án>: cấu hình đội sản phẩm

Sinh bởi skill `product-team` ngày <YYYY-MM-DD>. Sửa trực tiếp file này khi quy tắc thay đổi.

## Sản phẩm
- Người dùng và nhiệm vụ: <…>
- Thiết bị và độ rộng màn hình: <desktop 1280–2560 | …>
- Phong cách: <triết lý, hình mẫu>; theme mặc định: <tối | sáng>
- Quyền của hệ thống: <chỉ quan sát | được ra lệnh …>

## §0 Quy tắc (bắt buộc mọi đợt)
<copy từ references/rules-baseline.md, chỉnh theo dự án>
- Từ cấm: <…>
- Thuật ngữ thống nhất: <…>

## Lệnh
- Dev server: `<cmd>` (cổng <port>); dữ liệu giả lập: <cách bật>
- Build: `<cmd>`; check frontend: `<cmd>`; test backend: `<cmd>` (compose project riêng: `-p <proj>-<area>`)

## Vận hành
- Môi trường: <host>; giao code bằng: <git bundle | registry | …>
- Deploy: <các bước>; backup trước deploy: <lệnh>; kiểm tra sau deploy: <lệnh>; rollback: <lệnh>
- Ai duyệt push / deploy: <khách hàng, nói rõ trong chat>
- Vùng cấm: <repo / server không được ghi>
- Tiền tố nhánh: `<prefix>/`

## Đội
- Panel: <không | danh sách persona>
- Phân vùng chủ code: xem `ownership.md`
