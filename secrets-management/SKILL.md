---
name: secrets-management
description: >-
  Quản lý và phát hiện secrets cho hệ thống self-hosted/air-gapped: quét secret lộ
  trong code/git history/image, pre-commit hook, lưu trữ secret đúng cách (Vault
  self-hosted, SOPS/age, K8s secrets), rotation và cấp phát khi deploy offline.
  Use when the user says "quản lý secret", "lộ API key", "quét secret", "hardcoded
  password", "vault", "lưu mật khẩu ở đâu", "secret trong git", ".env", "SOPS",
  "credential", or when setting up a new project/deploy pipeline.
---

# Secrets Management (self-hosted / air-gapped)

Nguyên tắc: **secret của môi trường air-gapped không bao giờ tồn tại ở môi trường dev có internet** — sinh và cấp phát ngay trên target lúc triển khai. Không cloud KMS; mọi giải pháp phải self-hosted.

## 1. Phát hiện secret lộ

```bash
# Quét toàn bộ repo + lịch sử git
gitleaks detect --source . -v
trufflehog git file://. --only-verified

# Quét image trước khi bundle
trivy image --scanners secret <image>
```

- [ ] Quét cả **git history**, không chỉ HEAD — secret đã commit rồi xóa vẫn nằm trong history
- [ ] Secret đã lộ trong history: coi như đã bị lộ → **rotate ngay**, việc xóa history (`git filter-repo`) chỉ là dọn dẹp sau
- [ ] Pre-commit hook cho mọi repo mới: `gitleaks protect --staged` trong `.pre-commit-config.yaml`
- [ ] Vị trí hay quên: docker-compose.yml, K8s manifest, script deploy, notebook, file test, log mẫu trong docs

## 2. Lưu trữ theo quy mô

| Bối cảnh | Giải pháp | Ghi chú |
|---|---|---|
| App đơn lẻ trên VM | File env `chmod 600` root-owned + systemd `EnvironmentFile=` | Đơn giản, đủ dùng; KHÔNG commit |
| Config cần versioning | **SOPS + age** — encrypt secret trong file config, commit bản mã hóa | Key age nằm ngoài repo; hợp air-gapped vì không cần server |
| Nhiều app, nhiều team | **Vault self-hosted** (hoặc OpenBao) trong mạng nội bộ | Có audit log, rotation, lease; đáng đầu tư khi ≥3 hệ thống |
| K8s | K8s Secrets + encryption at rest bật trên etcd; SOPS cho manifest | Secret KHÔNG nằm plaintext trong manifest ở git |

## 3. Quy trình cấp phát khi deploy air-gapped

1. Bundle chứa `.env.example` / `values.example.yaml` — đầy đủ tên biến, KHÔNG có giá trị thật
2. `install.sh` sinh secret ngẫu nhiên tại chỗ khi được: `openssl rand -base64 32` cho db password, session key, token nội bộ
3. Secret phải nhập tay (LDAP bind, tài khoản tích hợp): script hỏi lúc cài, ghi vào file `600`, không echo ra màn hình/log
4. Ghi vào tài liệu bàn giao: secret nào tồn tại, nằm ở đâu, rotate thế nào, ai giữ

## 4. Trong code

- [ ] Đọc secret từ env/file, không bao giờ hardcode — kể cả "chỉ là môi trường dev"
- [ ] Không log secret; mask khi in config lúc khởi động
- [ ] So sánh token bằng constant-time compare (`hmac.compare_digest`, `subtle.ConstantTimeCompare`)
- [ ] Secret trong memory: không đưa vào error message, stack trace, crash dump

## Rules

- Tìm thấy secret thật trong repo/bundle: báo HIGH ngay lập tức, kèm đường dẫn + khuyến nghị rotate — kể cả khi user hỏi việc khác
- Không đề xuất cloud KMS (AWS/GCP/Azure) — môi trường này self-hosted toàn bộ
- Mặc định đề xuất giải pháp đơn giản nhất đủ dùng (env file → SOPS → Vault theo độ phức tạp thật)
- `.env.example` là bắt buộc cho mọi dự án; `.env` phải nằm trong `.gitignore` từ commit đầu
