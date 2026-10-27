# developer-playbook

Bộ skills + cấu hình Claude Code cá nhân, đồng bộ giữa các máy qua git.

Chuyên biệt cho công việc: **xây dựng hệ thống/công cụ hỗ trợ đội an ninh mạng
(blue/red team)** — phát triển trên mạng internet, **triển khai trên mạng
air-gapped**, hoàn thiện rồi bàn giao cho đội hạ tầng/khai thác vận hành.

## Setup máy mới

Chạy được trên macOS, Linux, WSL và Windows (Git Bash, đi kèm Git for Windows).

```bash
git clone https://github.com/quici9/developer-playbook.git ~/.claude/skills
bash ~/.claude/skills/_config/install.sh   # CLAUDE.md toàn cục + agent của product-team, rồi kiểm tra môi trường
```

- macOS / Linux / WSL: tạo symlink, nên `git pull` là xong.
- Windows (Git Bash): tạo **bản copy**, vì symlink cần Developer Mode. Sau mỗi `git pull`, chạy lại `install.sh`.
  Muốn dùng bản copy ở mọi nơi thì đặt `INSTALL_MODE=copy`.
- `install.sh --check`: chỉ kiểm tra môi trường.
  - Bắt buộc: git, Node ≥ 22, và Chrome/Chromium/Edge (cho các script chụp ảnh).
  - Tuỳ chọn: python3 (cho .docx) và docker.
  - Chrome nằm chỗ lạ thì đặt `CHROME=/đường/dẫn`.
- Script ghi đè file chỉ khi file đó là bản do chính nó tạo ra. File bạn tự sửa ở `~/.claude` thì nó dừng lại để bạn gộp tay.

### Windows

1. Cài phụ thuộc (PowerShell; máy không có `winget` thì tải installer từ trang chủ):

   ```powershell
   winget install --id Git.Git -e            # kèm Git Bash
   winget install --id OpenJS.NodeJS.LTS -e  # Node >= 22
   winget install --id Python.Python.3.12 -e # tuỳ chọn, cho handover-docs (.docx)
   ```

   Edge có sẵn trên Windows nên đủ cho các script chụp ảnh. Mở terminal mới để PATH nhận Git/Node.

2. Clone và cài. Dùng **Git Bash**:

   ```bash
   git clone https://github.com/quici9/developer-playbook.git ~/.claude/skills
   bash ~/.claude/skills/_config/install.sh
   ```

   Hoặc từ **PowerShell** (gọi bash của Git for Windows):

   ```powershell
   git clone https://github.com/quici9/developer-playbook.git "$HOME\.claude\skills"
   & "$env:ProgramFiles\Git\bin\bash.exe" "$HOME/.claude/skills/_config/install.sh"
   ```

3. Cập nhật về sau: `git pull` rồi **chạy lại `install.sh`**, vì `CLAUDE.md` và agent ở `~/.claude` là bản copy.

Lưu ý:
- `install.sh` tự đặt `git config core.fileMode false` cho repo. Filesystem Windows không giữ exec bit, nên thiếu dòng này thì các script `.sh` bị báo là đã sửa và chặn `git pull`.
- Báo `✗ Chrome` dù đã có Edge hoặc Chrome ở chỗ lạ: đặt `CHROME="C:/Program Files/.../msedge.exe"` trước lệnh `install.sh`.
- Báo `· python3` dù đã cài Python: bình thường, vì trên Windows lệnh là `python`.

## Danh sách skills (18)

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

### 👥 Đội agent

| Skill | Nội dung |
|---|---|
| [`product-team`](product-team/SKILL.md) | Đội nhiều agent cho dự án web: lead designer (chính phiên chat) nghiên cứu, vẽ mockup, viết spec, review, chốt FINAL; dev agent code; integrator gộp, chạy gate, chụp ảnh nghiệm thu. Khách (bạn) quyết |

Kích hoạt khi nói "dùng đội ngũ", "lập đội", "audit UI/UX rồi giao dev"… Lần đầu ở mỗi repo, skill chạy **intake**:
hỏi những gì không suy ra được từ code, rồi sinh `.claude/team/` (quy tắc §0, chủ file, cấu hình gate), mục
*Working context* trong `CLAUDE.md` và skill `verify` (chạy test/build với output gọn) vào repo đó.

**Quy trình:** lead chọn luồng theo cỡ việc.
- **S** (sửa lỗi, một thay đổi rõ): brief → 1 dev → kiểm → báo.
- **M/L** (màn hình, luồng, API, migration):
  1. nghiên cứu;
  2. mockup (theo `ui-design`);
  3. khách quyết, một lượt;
  4. spec;
  5. mỗi phần một agent mới, **hỏi trước khi code**;
  6. integrator gộp, chạy gate, chụp ảnh;
  7. lead review một lần; có lỗi thì giao brief sửa cho agent mới;
  8. trình khách.
- Push / deploy chỉ khi khách nói rõ.

**Agent** (`_config/agents/`, cài vào `~/.claude/agents/`):

| Agent | Vai |
|---|---|
| `dev-backend` | API, migration, test, tài liệu vận hành |
| `dev-shell` | Router, layout, token, chart và helper dùng chung (chỉ khi đợt đó đổi thứ dùng chung) |
| `dev-pages` | Các trang nghiệp vụ theo spec + mockup |
| `integrator` | Gộp nhánh, gate, gate hồi quy cho mỗi lỗi, ảnh nghiệm thu |
| `panel-user` | Vai người dùng nêu nhu cầu (mặc định tắt) |

Quy tắc rút từ eval 2026-10-27 (4 bài × 3 phương án × 2 lần):
- **Mỗi nhiệm vụ một agent mới**: rẻ hơn khoảng 13 lần so với giữ teammate qua nhiều đợt.
- **Hỏi trước khi code**: bắt được các lỗi spec từng tốn vòng sửa.
- **Dev chỉ chạy kiểm tra hẹp**; gate đầy đủ là việc của integrator.

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
| [`handover-docs`](handover-docs/SKILL.md) | Bộ 4 tài liệu bàn giao (OVERVIEW, DEPLOYMENT, RUNBOOK, TROUBLESHOOTING); xuất .docx theo TT22/2021/TT-BQP + script kiểm thể thức |

## Cách skills hoạt động

- Mỗi skill là một thư mục `<tên-skill>/SKILL.md` với YAML frontmatter
  (`name` + `description`) — Claude Code đọc description để **tự kích hoạt theo
  ngữ cảnh**, trigger phrases viết song ngữ Việt–Anh
- File lớn/chi tiết đặt trong `references/` của skill, chỉ được đọc khi cần
  (tiết kiệm context)
- Skill dùng chung xuyên dự án đặt ở đây; quy trình riêng của một dự án đặt
  trong `.claude/skills/` của dự án đó

## Cấu hình đi kèm

- `_config/CLAUDE.md`: chỉ dẫn toàn cục (ngôn ngữ, bối cảnh air-gapped mặc định, stack, nguyên tắc security-first).
  Cài vào `~/.claude/CLAUDE.md`.
- `_config/agents/`: định nghĩa agent cho `product-team`, cài vào `~/.claude/agents/`.
- `_config/install.sh`: cài hai mục trên (symlink, hoặc bản copy trên Windows), rồi kiểm tra môi trường.
  `--check` chỉ kiểm tra. Chạy lại bao nhiêu lần cũng được.
- `synced/`: skill đồng bộ từ claude.ai, quản lý riêng từng máy, không nằm trong git.

## Duy trì

```bash
# Sau khi sửa skill hoặc agent trên máy bất kỳ: luôn sửa file TRONG repo, không sửa bản ở ~/.claude
cd ~/.claude/skills && git add -A && git commit -m "..." && git push

# Máy khác
cd ~/.claude/skills && git pull
bash _config/install.sh   # bắt buộc trên Windows (bản copy); macOS/Linux chỉ cần khi có agent/file cấu hình mới
```

Thêm skill mới: tạo `<tên-mới>/SKILL.md` đúng format frontmatter, description
phải chứa trigger phrases song ngữ; tránh trùng tên với skill built-in của
Claude Code (`code-review`, `schedule`, `init`...). Cập nhật bảng trong README này.
Thêm agent mới: đặt file vào `_config/agents/` rồi chạy lại `install.sh`.
