---
name: airgap-delivery
description: >-
  Đóng gói và chuyển giao phần mềm vào mạng air-gapped: vendor toàn bộ dependencies,
  export container images, pin version với checksum manifest, tạo SBOM, quét lỗ hổng
  trước khi đóng gói, và kiểm tra phone-home/telemetry. Use when preparing any deploy
  to the isolated network, or when the user says "đóng gói offline", "chuyển vào mạng
  nội bộ", "air-gapped", "offline bundle", "offline install", "vendor dependencies",
  "mang qua USB", "deploy không có internet", "package for offline". Also trigger
  proactively whenever a project being built is destined for air-gapped deployment.
---

# Air-gapped Delivery

Quy trình chuẩn: dev trên mạng internet → đóng gói offline bundle → chuyển qua phương tiện vật lý → cài đặt và xác minh trên mạng air-gapped. Mọi bước đều phải giả định **target không có bất kỳ kết nối ra ngoài nào**.

Chi tiết vendor theo hệ sinh thái: xem `references/python.md`, `references/go.md`, `references/rust.md`, `references/docker.md`, `references/node.md`.

## Phase 1 — Inventory (trước khi đóng gói)

- [ ] Liệt kê toàn bộ runtime dependencies (trực tiếp + transitive)
- [ ] Liệt kê build dependencies nếu build trên target (tránh nếu được — ưu tiên build sẵn artifact)
- [ ] Liệt kê base images, model weights, dataset, font, GeoIP db... — mọi thứ tải từ internet
- [ ] Xác định target: OS/distro, kernel, arch (x86_64/arm64), phiên bản Docker/K8s, Python/glibc
- [ ] Pin chính xác mọi version — không dùng `latest`, không dùng range (`^`, `~`, `>=`)

## Phase 2 — Vendor & Build

- [ ] Vendor dependencies theo ecosystem (xem references/)
- [ ] Build artifact trên môi trường sạch (container build) để đảm bảo reproducible
- [ ] Ưu tiên static binary (Go, Rust) — giảm phụ thuộc vào target
- [ ] `docker save` mọi image (app + hạ tầng: db, redis, prometheus...) thành tar
- [ ] Với ML: tải sẵn model weights, tokenizer, dataset — cấm mọi lệnh download lúc runtime

## Phase 3 — Offline-cleanliness Check ⭐ BẮT BUỘC

Đây là bước phân biệt bundle đạt/không đạt. Kiểm tra code và config để đảm bảo **không có đường gọi ra ngoài** khi chạy trên air-gapped:

- [ ] Grep telemetry/analytics: `sentry`, `posthog`, `segment`, `google-analytics`, `telemetry`, `crash report`
- [ ] Tắt auto-update, update checker, version check online của mọi tool/framework
- [ ] Không fetch CDN lúc runtime: font, JS/CSS từ CDN, favicon service — tất cả phải bundle local
- [ ] Không gọi API bên ngoài lúc runtime (license check, geolocation, NTP public...) — nếu cần NTP/DNS thì trỏ về server nội bộ, ghi rõ trong tài liệu
- [ ] ML/AI: tắt HuggingFace/torch hub auto-download (`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`)
- [ ] Package manager trên target không được tự gọi registry public (cấu hình pip/npm/go trỏ về vendored/mirror)
- [ ] Test thực tế: chạy toàn bộ stack trong network namespace không có internet (`docker network --internal` hoặc máy ảo cắt mạng) và xác nhận hoạt động đầy đủ

## Phase 4 — Security Gate (trước khi ghi ra media)

- [ ] Quét lỗ hổng dependencies + images khi CÒN internet: `trivy` (image + fs), `pip-audit`/`govulncheck`/`cargo audit`/`npm audit`
- [ ] Vá hoặc ghi nhận rõ mọi CVE HIGH/CRITICAL còn lại kèm lý do chấp nhận
- [ ] Tạo SBOM: `syft <image/dir> -o cyclonedx-json` cho từng thành phần
- [ ] Quét secrets trong bundle: không được có credential dev, `.env` thật, private key thừa
- [ ] Ký hoặc checksum toàn bộ: `sha256sum` từng file → `MANIFEST.sha256`

## Phase 5 — Bundle Layout chuẩn

```
bundle-<system>-<version>-<yyyymmdd>/
├── MANIFEST.sha256          # checksum mọi file trong bundle
├── BUNDLE.md                # nội dung bundle, version, target yêu cầu
├── images/                  # docker save *.tar
├── artifacts/               # binary, wheel, package đã build
├── vendor/                  # dependencies vendored (nếu build trên target)
├── config/                  # config mẫu, .env.example (KHÔNG chứa secret thật)
├── sbom/                    # SBOM + báo cáo quét CVE
├── scripts/
│   ├── install.sh           # cài đặt idempotent, có thể chạy lại
│   ├── verify.sh            # xác minh checksum + smoke test sau cài
│   └── rollback.sh          # quay về phiên bản trước
└── docs/                    # deployment guide, runbook (xem skill handover-docs)
```

## Phase 6 — Transfer & Install trên target

- [ ] Verify checksum sau khi copy qua media: `sha256sum -c MANIFEST.sha256`
- [ ] `docker load` images, tag lại theo registry nội bộ nếu có
- [ ] Chạy `install.sh` — script phải idempotent, không giả định internet, không giả định DNS public
- [ ] Chạy `verify.sh`: service lên, healthcheck pass, smoke test chức năng chính
- [ ] Lưu bundle cũ để rollback được ít nhất 1 phiên bản

## Output Format

Khi hoàn thành đóng gói, xuất báo cáo:

```
## 📦 Air-gapped Bundle — [system] v[version]

### Nội dung
| Thành phần | Version | Kích thước | SHA256 (8 ký tự đầu) |
|---|---|---|---|

### Offline-cleanliness: ✅/❌ (đã test trong môi trường cắt mạng: có/chưa)
### Security gate: CVE HIGH/CRITICAL còn lại: [số lượng + lý do]
### Cài đặt: [lệnh] | Rollback: [lệnh]
```

## Rules

- KHÔNG BAO GIỜ để bước "tải thêm khi cài" lọt vào install script — bundle phải tự đủ 100%
- Mọi version phải pin cứng; bundle phải reproducible từ cùng commit
- Quét CVE và tạo SBOM khi còn internet — trên target không quét được nữa
- Bundle chứa secret thật = FAIL, dừng và cảnh báo ngay
- Nếu chưa test trong môi trường cắt mạng, phải ghi rõ "CHƯA XÁC MINH OFFLINE" trong báo cáo
