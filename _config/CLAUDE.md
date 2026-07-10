# Chỉ dẫn toàn cục

## Ngôn ngữ
- Trao đổi bằng tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh
- Code, comment, commit message: tiếng Anh

## Bối cảnh mặc định
- Tôi là kỹ sư an ninh mạng: xây dựng hệ thống/công cụ hỗ trợ đội blue/red team,
  hoàn thiện rồi bàn giao cho đội hạ tầng/khai thác vận hành
- Dev trên mạng internet, DEPLOY TRÊN MẠNG AIR-GAPPED (bundle chuyển qua phương tiện
  vật lý). Trừ khi nói khác đi, mọi thiết kế và dependency mới phải sống được offline:
  vendor được, pin version, không phone-home/telemetry, không asset từ CDN
- Stack chính: Python, Go, Rust/C/C++; frontend Angular/React/Vue + TypeScript;
  hạ tầng Docker/K8s on-prem và VM/systemd; PostgreSQL; toàn bộ self-hosted — không
  đề xuất SaaS hay cloud managed service (AWS/GCP/Datadog...)

## Nguyên tắc làm việc
- Security-first: dữ liệu từ endpoint/log/sample là hostile by default; không hardcode
  secret; hành động nhạy cảm phải có audit log
- Mọi hệ thống hướng đến bàn giao: thay đổi ảnh hưởng vận hành thì cập nhật luôn
  tài liệu (DEPLOYMENT/RUNBOOK) trong cùng thay đổi
- Ưu tiên giải pháp đơn giản mà đội khai thác vận hành nổi trên air-gapped,
  hơn là giải pháp "chuẩn cloud" phức tạp
