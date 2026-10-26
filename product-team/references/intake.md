# Intake: thông tin dự án

Tự suy ra trước từ repo. Chỉ hỏi câu nào không suy ra được. Mỗi câu kèm mặc định đề xuất.

## A. Sản phẩm (luôn hỏi nếu README không nói)
1. Ai dùng, làm nhiệm vụ gì hằng ngày, ra quyết định gì từ màn hình này?
2. Thiết bị: desktop-only (dải độ rộng?) hay cả mobile?
3. Triết lý / phong cách thiết kế mong muốn, có hình mẫu không (vd. Datadog, CrowdStrike, Linear)?
   Nền tối hay sáng mặc định?
4. Hệ thống chỉ quan sát hay được ra lệnh / thay đổi hệ thống khác?

## B. Ngôn ngữ và văn phong
5. Ngôn ngữ giao diện. Văn phong (quân sự / doanh nghiệp / kỹ thuật).
   Từ cấm (vd. "tạm", "ước tính", "hôm nay"…), thuật ngữ thống nhất.
6. Quy tắc ghi giờ / ngày / số (dấu phân cách, múi giờ, giờ chốt số liệu nếu có).

## C. Kỹ thuật (thường suy ra được từ repo)
7. Lệnh: chạy dev server (cổng), build, check / test frontend, test backend
   (có cần compose project riêng không), dữ liệu giả lập (fixture / mock) bật thế nào.
8. Air-gapped? Nếu có: không CDN, vendor dependency, pin phiên bản.

## D. Vận hành và an toàn
9. Môi trường deploy (host, cách giao code, lệnh deploy, kiểm tra sau deploy, backup, rollback).
   Deploy cần ai duyệt?
10. Vùng cấm: repo / server không được ghi; hành động cần hỏi (push, deploy, xoá).
    Tiền tố nhánh (vd. `quici9/`).

## E. Đội
11. Có dùng panel người dùng không, gồm những vai nào (vd. người trực, cán bộ kỹ thuật, chỉ huy)?
12. Phân vùng code cho 3 dev, đề xuất từ cấu trúc repo:
    - backend: `backend/`;
    - shell: layout, theme, router, primitive dùng chung;
    - pages: các trang nghiệp vụ.

Ghi câu trả lời vào `.claude/team/project.md` (§0 và mục Vận hành) và `gate.conf`.
Câu nào chưa trả lời thì ghi "chưa chốt", không tự bịa.
