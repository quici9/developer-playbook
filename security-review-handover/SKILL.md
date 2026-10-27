---
name: security-review-handover
description: >-
  Security review toàn diện trước khi bàn giao hệ thống lên mạng air-gapped: OWASP
  Top 10, authn/authz, hardening container/K8s/VM, network exposure, logging/audit,
  và các kiểm tra đặc thù air-gapped. Use before any handover or production deploy,
  or when the user says "security review", "kiểm tra bảo mật trước bàn giao", "rà soát
  bảo mật", "hardening", "có lỗ hổng không", "pentest checklist", "review bảo mật",
  "an toàn chưa", "OWASP".
---

# Security Review trước bàn giao

Checklist bắt buộc trước khi hệ thống rời tay dev. Sau bàn giao, vá lỗi trên air-gapped chậm và đắt (phải đóng bundle mới, chuyển vật lý) — nên gate này phải chặt. Review theo 6 lớp, báo cáo theo mức HIGH/MED/LOW.

## Lớp 1 — Ứng dụng (OWASP Top 10 rút gọn theo trọng số thực tế)

- [ ] **Access control**: mọi endpoint kiểm tra quyền ở server; user chỉ thấy dữ liệu của mình/vai trò mình; admin route yêu cầu role admin thật sự; ID tham chiếu trực tiếp được kiểm tra ownership (IDOR)
- [ ] **Injection**: parameterized query 100%; không nối chuỗi SQL/shell command từ input; escape output (XSS); không `eval`/`innerHTML` với dữ liệu ngoài
- [ ] **Input hostile**: parser xử lý file/log/pcap/sample từ endpoint được coi là nhận dữ liệu độc — có giới hạn kích thước, timeout, chạy với quyền thấp nhất, lý tưởng là sandbox riêng
- [ ] **Crypto**: password hash bằng argon2/bcrypt; TLS nội bộ cho dữ liệu nhạy cảm; không tự chế crypto; key không nằm trong code
- [ ] **SSRF/path traversal**: URL/path từ user được validate allowlist
- [ ] Upload file: kiểm type thật (magic bytes), giới hạn size, lưu ngoài webroot, không thực thi được

## Lớp 2 — AuthN/AuthZ

- [ ] Session/token: hết hạn hợp lý, revoke được, HttpOnly+Secure cookie hoặc token lưu đúng chỗ
- [ ] Tài khoản mặc định/seeded: KHÔNG có admin/admin — mật khẩu khởi tạo bắt buộc đổi lần đầu
- [ ] Brute-force: rate limit + lockout trên login
- [ ] Tài khoản quản trị có xác thực 2 lớp (TOTP chạy offline được); có đường khôi phục (mã dự phòng / admin reset / CLI trên host) được ghi trong RUNBOOK; đồng hồ máy chủ đồng bộ NTP nội bộ
- [ ] Tích hợp LDAP/AD nội bộ (nếu có): bind an toàn, không lộ credential bind trong config plaintext
- [ ] Phân quyền theo vai trò khớp thực tế đội blue/red: ai thấy gì, ai sửa gì — có ma trận quyền trong docs

## Lớp 3 — Container / K8s / VM

- [ ] Container chạy non-root, `readOnlyRootFilesystem` khi được, drop capabilities không cần
- [ ] Không mount docker.sock, không `privileged` trừ khi bắt buộc (ghi rõ lý do)
- [ ] K8s: NetworkPolicy giới hạn traffic giữa pod; resource limits; secret không nằm trong env của manifest commit vào git
- [ ] VM/systemd: service chạy user riêng, `ProtectSystem=strict`, `NoNewPrivileges=true`; firewall (nftables/firewalld) chỉ mở cổng cần
- [ ] Base image/OS: version còn được vá, đã quét trivy, không package thừa

## Lớp 4 — Network exposure

- [ ] Liệt kê MỌI cổng lắng nghe (`ss -tlnp`) — từng cổng có lý do, bind đúng interface (không 0.0.0.0 bừa)
- [ ] Console quản trị (db admin, message queue UI, metrics endpoint) không mở cho toàn mạng
- [ ] Tài liệu hóa ma trận cổng/giao thức cho đội hạ tầng đặt firewall

## Lớp 5 — Logging & Audit

- [ ] Audit log cho hành động nhạy cảm: login, đổi quyền, xem/xuất dữ liệu case, sửa rule — ai, làm gì, khi nào
- [ ] Log KHÔNG chứa secret/password/token/dữ liệu nhạy cảm nguyên văn
- [ ] Log không sửa/xóa được bởi user thường (append-only hoặc chuyển về log server nội bộ)
- [ ] Thời gian đồng bộ (NTP nội bộ) — log lệch giờ là vô dụng khi điều tra

## Lớp 6 — Đặc thù air-gapped

- [ ] Không phone-home/telemetry/auto-update (xem skill airgap-delivery Phase 3)
- [ ] Secrets: không có secret thật trong bundle/image/git history (xem skill secrets-management)
- [ ] CVE scan + SBOM đã chạy khi còn internet, báo cáo kèm bundle
- [ ] Kế hoạch vá: quy trình đóng bundle vá lỗi khẩn cấp được ghi trong tài liệu bàn giao

## Output Format

```
## 🔒 Security Review — [Hệ thống] v[version] — [ngày]

### Kết luận: ✅ ĐẠT / ❌ CHƯA ĐẠT (bàn giao được không)

### Phát hiện
| # | Mức | Lớp | Vấn đề | Vị trí | Khắc phục |
|---|-----|-----|--------|--------|-----------|
| 1 | HIGH | ... | ... | file:line | ... |

### Đã kiểm tra không thấy vấn đề: [liệt kê lớp]
### Rủi ro chấp nhận (kèm lý do + người quyết)
```

## Rules

- Có finding HIGH chưa xử lý = CHƯA ĐẠT, nói thẳng, không nể nang
- Mỗi finding phải kèm vị trí cụ thể (file:line hoặc config) và cách khắc phục — không phán chung chung
- Review trên code/config thật (đọc code, chạy lệnh kiểm tra), không chỉ hỏi đáp lý thuyết
- Phân biệt "đã kiểm tra và ổn" với "chưa kiểm tra" — không được im lặng bỏ qua lớp nào
