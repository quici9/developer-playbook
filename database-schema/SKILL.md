---
name: database-schema
description: >-
  Thiết kế schema cơ sở dữ liệu: mô hình hóa quan hệ, chọn kiểu dữ liệu, index,
  constraint, migration an toàn, và các pattern cho dữ liệu khối lượng lớn
  (log/event time-series, partition, retention). Use when the user says "thiết kế
  schema", "database schema", "thiết kế bảng", "nên đánh index gì", "migration",
  "chuẩn hóa dữ liệu", "PostgreSQL", "query chậm do thiếu index", or when a new
  system needs its data model designed.
---

# Database Schema

Mặc định PostgreSQL (self-hosted, chạy tốt air-gapped, đủ cho hầu hết nhu cầu kể cả JSONB, full-text search). Schema thiết kế sai là món nợ đắt nhất — migration dữ liệu trên air-gapped sau bàn giao rất phiền.

## Quy trình thiết kế

1. Liệt kê entity + quan hệ từ nghiệp vụ trước, vẽ ERD (Mermaid) — chưa nghĩ đến bảng
2. Chuẩn hóa đến 3NF rồi mới cân nhắc denormalize có chủ đích (ghi lý do)
3. Với từng bảng, quyết định: khóa chính, kiểu dữ liệu, nullable, default, constraint
4. Viết migration + seed mẫu, kèm rollback

## Quy ước

- Tên bảng số nhiều snake_case (`alerts`, `case_artifacts`); PK là `id` UUID (`gen_random_uuid()`) — tránh lộ số đếm qua API
- Mọi bảng có `created_at`, `updated_at` (`timestamptz`, không bao giờ `timestamp` không zone)
- FK luôn khai báo constraint thật + quyết định `ON DELETE` có chủ đích (CASCADE/RESTRICT/SET NULL — nghĩ theo nghiệp vụ)
- Enum nghiệp vụ (`severity`, `status`): dùng `CHECK` constraint hoặc bảng lookup — Postgres native enum khó sửa
- `NOT NULL` là mặc định, nullable phải có lý do
- Soft delete (`deleted_at`) chỉ khi nghiệp vụ cần khôi phục/audit — nhớ partial index `WHERE deleted_at IS NULL`

## Index

- FK columns, cột trong WHERE/ORDER BY thường xuyên; composite index theo thứ tự equality → range
- Partial index cho query trên tập con (`WHERE status = 'open'`); GIN cho JSONB/full-text
- Đừng index mò trước — thiết kế từ query thực tế dự kiến, kiểm chứng bằng `EXPLAIN ANALYZE`
- Mỗi index làm chậm write — bảng ingest nặng (events/log) giữ index tối thiểu

## Dữ liệu lớn dạng log/event (đặc thù hệ thống blue team)

- Time-series append-only: partition theo thời gian (`PARTITION BY RANGE (created_at)`, partition tháng/tuần theo khối lượng)
- Retention = drop partition (tức thì, không bloat) thay vì `DELETE` hàng loạt
- Tính trước dung lượng: rows/ngày × size ước lượng × retention — ghi vào proposal/tài liệu bàn giao vì disk trên target là hữu hạn
- Cân nhắc BRIN index cho cột thời gian trên bảng rất lớn

## Migration an toàn

- Công cụ theo stack (alembic / golang-migrate / sqlx / prisma migrate) — mọi thay đổi schema qua migration file trong git, không sửa tay
- Trên bảng lớn đang chạy: `CREATE INDEX CONCURRENTLY`; thêm cột NOT NULL theo 3 bước (thêm nullable + default → backfill → set NOT NULL)
- Migration phải chạy được offline trong install/upgrade script của bundle; test upgrade từ phiên bản cũ với dữ liệu thật trước khi đóng bundle

## Rules

- Ra schema luôn kèm: ERD + DDL đầy đủ chạy được + giải thích quyết định không hiển nhiên
- Hỏi khối lượng dữ liệu dự kiến trước khi thiết kế bảng ingest — bảng 10K rows và 1B rows là hai bài toán khác nhau
- Không đề xuất thêm hệ CSDL thứ hai (Elastic, Click house, Mongo...) khi Postgres còn gánh được — mỗi hệ thêm là gánh nặng vận hành trên air-gapped
