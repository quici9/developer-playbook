---
name: api-design
description: >-
  Thiết kế REST API nhất quán: resource modeling, versioning, phân trang, error
  format chuẩn RFC 9457, authn/authz, và sinh OpenAPI 3 spec làm hợp đồng giữa
  các hệ thống nội bộ. Use when the user says "thiết kế API", "design API",
  "endpoint nên đặt thế nào", "OpenAPI", "swagger", "API spec", "chuẩn hóa response",
  "error format", "REST", or when building a new service that exposes an API.
---

# API Design

API nội bộ giữa các hệ thống của đội blue/red team vẫn cần hợp đồng chặt — vì hệ thống bàn giao xong sẽ có người khác tích hợp mà không hỏi được dev. **OpenAPI spec là sản phẩm bàn giao**, không phải tài liệu phụ.

## Quy ước resource & URL

- Danh từ số nhiều, phân cấp nông: `/cases/{id}/artifacts`, không quá 2 cấp lồng
- Hành động không phải CRUD → sub-resource động từ có giới hạn: `POST /scans/{id}/cancel`
- Filter/sort/search qua query param: `GET /alerts?severity=high&since=...&sort=-created_at`
- Versioning: `/api/v1/` ngay từ đầu — nội bộ càng cần vì không ép client update được

## Chuẩn response

- Phân trang mặc định cho mọi list — cursor-based cho dữ liệu lớn/ghi nhiều (log, events), page-based đủ cho dữ liệu nhỏ; response kèm `next_cursor`/`total`
- Timestamp: ISO 8601 UTC ở mọi nơi, không epoch lẫn ISO lộn xộn
- ID: dùng UUID/ULID, không lộ auto-increment ID ra ngoài (đếm được, IDOR dễ hơn)
- Error format thống nhất theo RFC 9457 (Problem Details):

```json
{ "type": "/errors/validation", "title": "Validation failed", "status": 422,
  "detail": "field 'severity' must be one of ...", "instance": "/api/v1/alerts",
  "errors": [{"field": "severity", "message": "..."}] }
```

- Status code đúng nghĩa: 400 sai cú pháp / 401 chưa authn / 403 không có quyền / 404 / 409 xung đột / 422 sai ngữ nghĩa / 429 rate limit / 500 — error message KHÔNG lộ stack trace, query, đường dẫn nội bộ

## Security mặc định

- AuthN: token (JWT ngắn hạn + refresh, hoặc API key cho service-to-service) — kể cả trong mạng nội bộ
- AuthZ kiểm tra ở từng endpoint theo resource ownership/role — xem skill security-review-handover
- Input validation ở server bằng schema (pydantic / zod / validator theo stack); giới hạn size request body
- Rate limit các endpoint đắt (search, export, upload)
- Endpoint mutation: idempotency key cho client retry an toàn khi mạng nội bộ chập chờn

## OpenAPI spec

- Code-first (FastAPI, NestJS tự sinh) hay spec-first đều được — nhưng spec phải **khớp thực tế** và nằm trong repo, version cùng code
- Mỗi endpoint: mô tả, request/response schema đầy đủ kèm example, error responses liệt kê rõ
- Bundle kèm Swagger UI/Redoc self-hosted (asset local, không CDN) để đội tích hợp đọc trên air-gapped

## Rules

- Breaking change (đổi field, đổi nghĩa, bỏ endpoint) → bump version, giữ version cũ một thời gian chuyển tiếp có ghi trong docs
- Thiết kế xong liệt kê luôn bảng endpoint: method, path, quyền yêu cầu, mô tả 1 dòng — bảng này đi vào tài liệu bàn giao
- Đừng thiết kế generic quá mức (GraphQL-hóa, HATEOAS đầy đủ) cho API nội bộ — nhất quán và dễ đoán quan trọng hơn thanh lịch
