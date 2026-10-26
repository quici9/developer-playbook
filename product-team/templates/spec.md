# <Round>: <tên> (designer spec; khách duyệt <ngày> "<nguyên văn>")

- Mockup: <path>; ảnh chụp: <path>
- Base: `<branch>` @ <hash>. Nhánh tích hợp: `<prefix>/<round>`. Nhánh của dev: `<prefix>/<round>-<area>`.
- **No push. No deploy** cho tới khi khách duyệt.

## Vì sao (vấn đề hiện tại)
1. <…>

## §0 Quy tắc
Theo `.claude/team/project.md` §0, cộng thêm các quy tắc riêng của đợt này:
- <…>

## §1 <Phần> (chủ: <vai>)
- <bố cục, nội dung, trạng thái: bình thường / rỗng / lỗi / dữ liệu cũ, ngân sách chữ>

## §n Backend (chủ: dev-backend, làm trước)
- `<METHOD /path>` → shape; kiểm tra phạm vi; test; tài liệu.

## Nghiệm thu (integrator)
- Mọi gate cũ vẫn xanh, cộng các gate mới: <…>
- Ảnh chụp: <trạng thái × độ rộng × theme>

## Phân công và thứ tự gộp
- dev-backend: §… · dev-shell: §… · dev-pages: §… · integrator: nhánh, gate, ảnh.
- Thứ tự gộp: backend → shell → pages.
