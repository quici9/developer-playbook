# developer-playbook

Bộ skills + cấu hình Claude Code cá nhân, đồng bộ giữa các máy qua git.

Chuyên biệt cho công việc: **xây dựng hệ thống/công cụ hỗ trợ đội an ninh mạng
(blue/red team)** — phát triển trên mạng internet, **triển khai trên mạng
air-gapped**, hoàn thiện rồi bàn giao cho đội hạ tầng/khai thác vận hành.

## Setup máy mới

```bash
git clone https://github.com/quici9/developer-playbook.git ~/.claude/skills
bash ~/.claude/skills/_config/install.sh   # symlink CLAUDE.md toàn cục
```

Xong — Claude Code tự quét `~/.claude/skills/` mỗi phiên, không cần cấu hình thêm.

## Danh sách skills (17)

Tổ chức theo vòng đời dự án: *đề xuất → thiết kế → xây dựng → đóng gói →
triển khai air-gapped → bàn giao*.

### 📋 Đề xuất & thiết kế

| Skill | Nội dung |
|---|---|
| [`system-proposal`](system-proposal/SKILL.md) | Từ ý tưởng/thiết kế chung chung → proposal: so sánh phương án, kiến trúc, MVP scope, ADR |
| [`threat-modeling`](threat-modeling/SKILL.md) | STRIDE, trust boundaries, DFD — chú trọng insider và dữ liệu hostile từ endpoint |
| [`api-design`](api-design/SKILL.md) | REST API + OpenAPI spec, error format RFC 9457, versioning, phân trang |
| [`database-schema`](database-schema/SKILL.md) | Schema PostgreSQL, index, migration an toàn, partition/retention cho dữ liệu log lớn |

### 🔨 Xây dựng

| Skill | Nội dung |
|---|---|
| [`secure-code-review`](secure-code-review/SKILL.md) | Review security-first cho Python/Go/Rust/C++/TS, chú trọng parser xử lý input hostile |
| [`debug-assistant`](debug-assistant/SKILL.md) | Debug có hệ thống, gồm cả lỗi "local chạy được, lên air-gapped thì không" |
| [`unit-test-generator`](unit-test-generator/SKILL.md) | Test pytest / go test / cargo test / vitest — happy, edge, error, hostile cases |
| [`ui-design`](ui-design/SKILL.md) | Thiết kế giao diện từ triết lý (người dùng & khoảnh khắc, chọn lọc, một điểm nhấn, sự dịu, nhất quán, tôn trọng người đọc) + vòng render → nhìn → phán xét; mọi stack, asset offline |
| [`web-frontend`](web-frontend/SKILL.md) | Angular/React/Vue cho tool nội bộ: state, bảng dữ liệu lớn, form, asset self-host |
| [`ml-pipeline`](ml-pipeline/SKILL.md) | Pipeline ML offline: tiền xử lý, training tái lập được, MLflow self-hosted |
| [`model-evaluation`](model-evaluation/SKILL.md) | Đánh giá model detection/imbalanced: PR-AUC, threshold theo chi phí FP/FN, Optuna |

### 📦 Đóng gói & triển khai air-gapped

| Skill | Nội dung |
|---|---|
| [`airgap-delivery`](airgap-delivery/SKILL.md) | Offline bundle: vendor deps, docker save, SBOM, offline-cleanliness check, manifest checksum. Kèm references chi tiết cho [Python](airgap-delivery/references/python.md) · [Go](airgap-delivery/references/go.md) · [Rust/C/C++](airgap-delivery/references/rust.md) · [Docker/K8s](airgap-delivery/references/docker.md) · [Node/FE](airgap-delivery/references/node.md) |
| [`container-build`](container-build/SKILL.md) | Dockerfile multi-stage, distroless, non-root, pin version, compose dev/prod |
| [`monitoring-setup`](monitoring-setup/SKILL.md) | Prometheus + Grafana + Loki self-hosted, structured logging, alert gắn runbook |

### 🤝 Bảo mật & bàn giao

| Skill | Nội dung |
|---|---|
| [`security-review-handover`](security-review-handover/SKILL.md) | Gate 6 lớp trước bàn giao: OWASP, authn/z, hardening, network, audit log, air-gapped |
| [`secrets-management`](secrets-management/SKILL.md) | Quét secret lộ (cả git history), SOPS/age, Vault self-hosted, cấp phát khi deploy offline |
| [`handover-docs`](handover-docs/SKILL.md) | Bộ 4 tài liệu bàn giao: OVERVIEW, DEPLOYMENT, RUNBOOK, TROUBLESHOOTING |

## Cách skills hoạt động

- Mỗi skill là một thư mục `<tên-skill>/SKILL.md` với YAML frontmatter
  (`name` + `description`) — Claude Code đọc description để **tự kích hoạt theo
  ngữ cảnh**, trigger phrases viết song ngữ Việt–Anh
- File lớn/chi tiết đặt trong `references/` của skill, chỉ được đọc khi cần
  (tiết kiệm context)
- Skill dùng chung xuyên dự án đặt ở đây; quy trình riêng của một dự án đặt
  trong `.claude/skills/` của dự án đó

## Cấu hình đi kèm

- `_config/CLAUDE.md` — chỉ dẫn toàn cục (ngôn ngữ, bối cảnh air-gapped mặc định,
  stack, nguyên tắc security-first), symlink về `~/.claude/CLAUDE.md`
- `_config/install.sh` — tạo symlink trên máy mới

## Duy trì

```bash
# Sau khi sửa skill trên máy bất kỳ
cd ~/.claude/skills && git add -A && git commit -m "..." && git push

# Máy khác
cd ~/.claude/skills && git pull
```

Thêm skill mới: tạo `<tên-mới>/SKILL.md` đúng format frontmatter, description
phải chứa trigger phrases song ngữ; tránh trùng tên với skill built-in của
Claude Code (`code-review`, `schedule`, `init`...). Cập nhật bảng trong README này.
