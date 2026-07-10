---
name: web-frontend
description: >-
  Xây dựng frontend cho hệ thống nội bộ với Angular, React hoặc Vue + TypeScript:
  component, quản lý state, form, bảng dữ liệu lớn, hiệu năng và accessibility cơ
  bản — self-host toàn bộ asset cho air-gapped. Use when the user says "tạo component",
  "viết UI", "build dashboard", "màn hình này", "form", "bảng dữ liệu", "quản lý state",
  "React", "Angular", "Vue", "web chậm", "re-render", or shares a UI mockup/wireframe.
---

# Web Frontend (Angular / React / Vue)

UI cho tool nội bộ của đội blue/red team: **mật độ thông tin cao, thao tác nhanh, chạy offline hoàn toàn**. Ưu tiên rõ ràng và bền hơn là hào nhoáng.

## Nguyên tắc chung (mọi framework)

- TypeScript strict; props/API response có type đầy đủ — không `any`
- Component một trách nhiệm; tách container (data) khỏi presentational khi component phình
- Mọi trạng thái async có đủ 3 mặt: loading / error (hiển thị được, retry được) / empty — tool nội bộ hay quên error state nhất
- Dữ liệu render từ nguồn ngoài phải escape (framework tự lo nếu không dùng `innerHTML`/`v-html`/`bypassSecurityTrust*` — thấy các hàm này là red flag review)
- **Air-gapped**: không CDN — fonts (`@fontsource`), icon, map tiles, mọi asset đều bundle local; API URL đọc từ config lúc deploy, không hardcode

## Quản lý state — chọn theo nhu cầu thật

| Nhu cầu | React | Vue | Angular |
|---|---|---|---|
| Server data (fetch/cache/refetch) | TanStack Query | TanStack Query / Pinia Colada | Service + signal, HttpClient |
| Client state cục bộ | useState/useReducer | ref/reactive | signal trong component |
| Client state toàn cục (ít) | Zustand / Context | Pinia | Service singleton + signals |

- Phần lớn "state toàn cục" thật ra là server cache — dùng query lib trước khi nghĩ đến store
- Không thêm Redux/NgRx trừ khi app đã lớn và nhiều người cùng sửa — mặc định là không

## Pattern hay gặp ở tool nội bộ

- **Bảng dữ liệu lớn** (alerts, logs): phân trang server-side là mặc định; virtualize khi phải cuộn dài (TanStack Virtual, cdk-virtual-scroll); filter/sort đẩy về server, giữ trạng thái filter trên URL để share được link
- **Form phức tạp**: schema validation (zod + react-hook-form / vee-validate / Angular reactive forms) — thông báo lỗi theo field, disable submit khi đang gửi
- **Realtime nhẹ** (dashboard SOC): polling có backoff là đủ và dễ vận hành hơn WebSocket — chỉ nâng cấp khi độ trễ thật sự quan trọng
- **Auth**: token trong memory + refresh, interceptor gắn header, redirect login khi 401 — logic authz thật nằm ở server, UI ẩn nút chỉ là UX

## Hiệu năng & A11y (mức tối thiểu bắt buộc)

- Đo trước khi tối ưu (React DevTools Profiler / Vue devtools / Angular profiler); nghi phạm quen: re-render cả list vì thiếu key ổn định, object/handler tạo mới mỗi render truyền xuống sâu, bundle to vì import cả thư viện (`import { x }` thay vì import default lodash...)
- Lazy load theo route; build production kiểm tra source map không lộ, analytics tắt
- A11y tối thiểu: element đúng ngữ nghĩa (button là `<button>`), form có label, thao tác được bằng bàn phím, focus nhìn thấy được, contrast đủ đọc — tool nội bộ dùng 8h/ngày càng cần

## Rules

- Hỏi/nhìn framework dự án đang dùng trước khi viết — không trộn pattern framework này sang framework kia
- Component mới phải khớp cấu trúc, naming, styling hiện có của repo
- Không thêm UI library/dependency mới khi codebase đã có cái tương đương
- Ra component kèm luôn kiểu dữ liệu props/API và ví dụ sử dụng
