---
name: handover-docs
description: >-
  Soạn gói tài liệu bàn giao hệ thống cho đội hạ tầng/khai thác: deployment guide,
  runbook vận hành, troubleshooting, sơ đồ kiến trúc. Use when a system is ready to
  hand over, or when the user says "tài liệu bàn giao", "viết runbook", "deployment
  guide", "tài liệu vận hành", "bàn giao cho đội hạ tầng", "đội khai thác",
  "handover", "operations manual", "hướng dẫn triển khai".
---

# Handover Docs

Gói tài liệu bàn giao chuẩn cho đội hạ tầng/khai thác — những người **không tham gia phát triển** và vận hành hệ thống trên **mạng air-gapped không có người dev bên cạnh**. Tài liệu phải đủ để họ tự deploy, tự xử lý sự cố thường gặp, và biết khi nào phải gọi ai.

## Bộ tài liệu chuẩn (4 file)

### 1. OVERVIEW.md — Tổng quan hệ thống
- Hệ thống làm gì, cho ai, tại sao tồn tại (3-5 câu)
- Sơ đồ kiến trúc (Mermaid hoặc ASCII): thành phần, luồng dữ liệu, cổng/giao thức giữa các thành phần
- Bảng thành phần: tên, công nghệ, version, vai trò, tài nguyên yêu cầu (CPU/RAM/disk)
- Phụ thuộc bên ngoài trong mạng nội bộ: DNS, NTP, LDAP/AD, registry, database dùng chung

### 2. DEPLOYMENT.md — Hướng dẫn triển khai
- Yêu cầu target: OS, arch, Docker/K8s version, tài nguyên tối thiểu, cổng cần mở
- Các bước cài từ bundle: verify checksum → load images → cấu hình → install.sh → verify.sh
- Bảng toàn bộ biến cấu hình: tên, ý nghĩa, giá trị mặc định, bắt buộc hay không
- Cách nâng cấp phiên bản và cách **rollback** (bước cụ thể, không chỉ "chạy rollback.sh")
- Checklist sau triển khai: service nào phải chạy, healthcheck URL, log ở đâu

### 3. RUNBOOK.md — Vận hành hàng ngày
- Start/stop/restart từng service (lệnh chính xác)
- Kiểm tra sức khỏe định kỳ: cái gì cần xem mỗi ngày/tuần, ngưỡng bình thường
- Backup & restore: cái gì cần backup, tần suất, lệnh backup, **quy trình restore đã được test**
- Quản lý log: vị trí, rotation, log nào quan trọng
- Quản lý dung lượng: cái gì phình ra theo thời gian, dọn thế nào
- Bảng alert (nếu có monitoring): alert nào → nghĩa là gì → làm gì

### 4. TROUBLESHOOTING.md — Xử lý sự cố
- Bảng triệu chứng → nguyên nhân khả dĩ → cách xử lý, cho các sự cố lường trước được
- Cách thu thập thông tin chẩn đoán (bundle log + config gửi cho dev khi bí)
- Giới hạn đã biết (known issues) và cách né
- Ma trận liên hệ: sự cố loại nào → gọi ai, mức độ nào thì escalate

## Nguyên tắc viết

- Viết cho người vận hành, không phải người dev: mọi lệnh copy-paste chạy được ngay, không "xem code để hiểu"
- Không giả định target có internet: không link đến docs online như cách giải quyết duy nhất — kiến thức cần thiết phải nằm trong tài liệu
- Mọi quy trình quan trọng (restore, rollback) phải được **thực hành ít nhất một lần** trước khi bàn giao — chưa test thì ghi rõ
- Version tài liệu khớp version hệ thống, để trong `docs/` của bundle
- Song ngữ nếu đội khai thác cần: ưu tiên tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh

## Rules

- Bắt đầu bằng cách hỏi/xác định: ai vận hành, trình độ của họ, họ được phép làm gì (có quyền root? được sửa config?)
- Sinh đủ 4 file theo cấu trúc trên; nội dung lấy từ code/config thật của dự án, không viết chung chung
- Bảng biến cấu hình và bảng cổng/giao thức là bắt buộc — đây là 2 thứ đội hạ tầng cần nhất
- Nếu thiếu thông tin (ví dụ chưa rõ quy trình backup), đánh dấu `⚠️ TODO` rõ ràng thay vì bịa
