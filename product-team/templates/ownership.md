# Chủ file theo vai (một file, một chủ; đụng file người khác phải hỏi)

| Vai | Sở hữu |
|---|---|
| dev-backend | `backend/**`, migrations, tài liệu API (WEB-ADMIN / API.md), RUNBOOK phần backend, <các trang admin / báo cáo nếu giao> |
| dev-shell | router/App, layout/shell, theme tokens, `components/charts*`, helper dùng chung (scope, time, link), <…> |
| dev-pages | <các trang nghiệp vụ>, ngăn chi tiết dùng chung, <…> |
| integrator | nhánh tích hợp, script gate trong scratchpad; không sửa code sản phẩm |

Thứ dùng chung (một chủ, người khác dùng lại): <drawer>, <formatter giờ>, <helper đếm số>, <link giữ phạm vi>.
