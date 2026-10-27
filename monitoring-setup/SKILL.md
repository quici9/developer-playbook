---
name: monitoring-setup
description: >-
  Thiết kế observability self-hosted cho hệ thống trong mạng nội bộ: Prometheus,
  Grafana, Loki, Alertmanager, structured logging, healthcheck, alert gắn với runbook
  — toàn bộ chạy offline, không SaaS. Use when the user says "setup monitoring",
  "thêm logging", "giám sát hệ thống", "cấu hình alert", "theo dõi production",
  "metrics", "Grafana dashboard", "Prometheus", "Grafana", "Loki", "log tập trung",
  or when preparing a system for handover to operations.
---

# Monitoring Setup (self-hosted, air-gapped)

Stack chuẩn: **Prometheus + Alertmanager (metrics/alert) + Loki + Promtail (log) + Grafana (dashboard)** — tất cả self-hosted, images bundle theo hệ thống. Không Datadog/CloudWatch/Sentry SaaS. Monitoring là một phần của gói bàn giao: đội khai thác vận hành bằng dashboard và alert, không phải bằng cách đọc code.

## 1. Structured logging trong app (làm trước tiên)

- JSON logs ra stdout/stderr — container runtime/promtail lo phần còn lại, app không tự quản lý file log
- Trường bắt buộc: `ts` (ISO8601), `level`, `msg`, `service`, và context (`request_id`, `user`, `case_id`...)
- Mức dùng đúng: ERROR = cần người xử lý; WARN = bất thường tự phục hồi; INFO = sự kiện nghiệp vụ; DEBUG = tắt ở prod, bật được qua env không cần rebuild
- KHÔNG log secret/token/password; audit log (ai làm gì) tách stream riêng với log kỹ thuật

## 2. Metrics trong app

- Expose `/metrics` Prometheus format (client lib chính chủ cho Python/Go/Rust)
- Bộ tối thiểu cho service: request rate, error rate, duration histogram (RED); với worker/pipeline: items processed, queue depth, lag, last success timestamp
- Metric nghiệp vụ đáng giá hơn metric máy: "phút từ lần ingest log cuối" báo sensor chết sớm hơn CPU%
- Label cardinality thấp — không đưa user_id/IP vào label

## 3. Stack triển khai

- Compose/manifest cho: prometheus (retention rõ ràng, ví dụ `--storage.tsdb.retention.time=30d` + tính disk), alertmanager, loki (retention + compactor), promtail, grafana, node_exporter (mỗi VM), cadvisor (nếu Docker)
- Grafana: provisioning bằng file (datasource + dashboard JSON trong git) — không cấu hình tay qua UI, để tái tạo được trên target
- Grafana đổi mật khẩu admin lúc cài, bind interface nội bộ đúng; toàn bộ images vào bundle air-gapped
- Alert notification trong air-gapped: email server nội bộ / webhook sang hệ thống trực nội bộ — xác nhận kênh nào tồn tại trước khi cấu hình

## 4. Alert rules

- Mỗi alert phải: (1) actionable — có việc cụ thể để làm, (2) trỏ tới mục tương ứng trong RUNBOOK.md, (3) có ngưỡng giải thích được
- Bộ khởi điểm: service down (`up == 0`), error rate > ngưỡng 5 phút, disk > 80% (dự báo đầy), certificate/license hết hạn, pipeline không có dữ liệu mới sau X phút, backup thất bại
- Tránh alert fatigue: ít alert đúng hơn nhiều alert nhiễu — alert mà đội khai thác học cách lờ đi là alert độc hại

## Output Format

Khi setup xong: bảng metric/alert (tên → ý nghĩa → ngưỡng → hành động runbook), file cấu hình đầy đủ, và ghi chú dung lượng disk dự kiến cho retention đã chọn.

## Rules

- Mọi thành phần phải chạy offline — kiểm tra Grafana plugins không tự tải, không phone-home (`analytics_enabled = false`)
- Retention và dung lượng disk phải tính và ghi rõ — target không co giãn được như cloud
- Alert không gắn runbook = chưa xong
- Đề xuất mức tối thiểu đủ dùng trước (1 VM đơn có thể chỉ cần node_exporter + healthcheck script + logrotate), đừng ép full stack cho hệ thống nhỏ
