---
name: product-team
description: >-
  Dựng và điều phối một đội sản phẩm nhiều agent cho dự án web: lead designer (chính session này)
  nghiên cứu, vẽ mockup, viết spec, review, ra quyết định FINAL; dev-backend / dev-shell / dev-pages
  code trên nhánh + worktree riêng; integrator gộp, chạy gate, chụp ảnh nghiệm thu; panel người dùng
  (tuỳ chọn) nêu nhu cầu. Lần đầu ở một repo: hỏi thông tin dự án rồi sinh .claude/team/ riêng cho dự án.
  Use when the user says "dùng đội ngũ", "lập đội", "product team", "team dev", "đội thiết kế",
  "redesign giao diện với đội", "audit UI/UX rồi giao dev", "/product-team", or wants the
  designer-lead + dev subagents workflow on a new project.
---

# Product team: lead designer + dev subagents

Session này đóng vai **lead designer / điều phối**. Khách hàng là người dùng: họ quyết, mình đề xuất.
**Mình không code sản phẩm.** Mockup HTML và script đo/chụp trong scratchpad là công cụ thiết kế, được phép.
Code sản phẩm do các dev agent viết.

## Bước 0: dự án đã có cấu hình đội chưa?
- Có `.claude/team/project.md` → đọc nó cùng `.claude/team/gate.conf`, rồi sang bước 2.
- Chưa có → bước 1 (intake).

## Bước 1: intake (chỉ lần đầu ở mỗi repo)
1. Tự đọc trước để khỏi hỏi thừa: README, CLAUDE.md, package.json / pyproject / go.mod, docker-compose,
   các file DEPLOYMENT/RUNBOOK, cấu trúc frontend/backend, lệnh build/test sẵn có.
2. Hỏi người dùng **chỉ những gì không suy ra được**, theo `references/intake.md`.
   Dùng AskUserQuestion, mỗi lượt tối đa 4 câu, có đề xuất mặc định.
3. Sinh vào repo, từ `templates/`:
   - `.claude/team/project.md`: §0 quy tắc riêng của dự án (copy `references/rules-baseline.md` rồi điền / thêm theo câu trả lời);
   - `.claude/team/ownership.md`: chủ file theo vai;
   - `.claude/team/gate.conf`: tham số cho `scripts/gate.sh`;
   - `.claude/team/pages.txt`: danh sách trang cho `scripts/pages-check.mjs`;
   - `.claude/team/decisions.md`: sổ quyết định của khách.
4. Thêm vào `CLAUDE.md` của repo mục **Working context** theo `templates/claude-context.md`, tối đa 60 dòng.
   Mục này gồm cấu trúc repo, helper dùng chung, lệnh và quy tắc rút gọn. Mọi agent đều tự nạp `CLAUDE.md`,
   nên đây là context rẻ nhất. Chi tiết vẫn để trong `project.md`, không chép sang.
5. Cài skill `verify` vào repo: copy `templates/verify/` sang `.claude/skills/verify/`. Script đọc `gate.conf`.
   Chạy thử `verify.sh backend` và `verify.sh frontend` một lần để chắc lệnh đúng.
   Dev dùng skill này thay cho lệnh thô, vì output gọn hơn và context không phình.
6. Cho người dùng xem tóm tắt cấu hình. Sửa nếu họ yêu cầu.

## Bước 2: một đợt làm việc (round)

Đầu tiên chọn luồng theo cỡ việc. Đừng chạy luồng lớn cho việc nhỏ.
- **Việc nhỏ (S):** sửa lỗi hoặc một thay đổi rõ ràng, không đổi thiết kế (một hàm, một cột, một câu chữ).
- **Việc vừa/lớn (M/L):** thêm hoặc đổi màn hình, đổi luồng, thêm API, migration, bảo mật.

### Luồng S (4 bước)
1. **Brief:** lead viết brief tự đủ (không cần mockup hay spec riêng). Một dev, không hỏi trước.
2. **Dev:** làm, chạy `verify`, commit, báo cáo.
3. **Kiểm:** đổi giao diện thì integrator chạy gate và chụp đúng các trang bị đổi; chỉ đổi backend thì kết quả
   `verify` đầy đủ của dev là đủ. Lead xem ảnh hoặc diff một lần.
4. **Trình khách** theo `templates/report.md`.

### Luồng M/L (8 bước)
1. **Nghiên cứu:** chụp hiện trạng bằng `scripts/capture.mjs`, đọc code và dữ liệu thật mà hệ thống có.
   Không thiết kế thứ dữ liệu không có. Panel người dùng mặc định tắt; chỉ dùng khi khách muốn nghe một vai cụ thể.
   **Mình là người thiết kế.**
2. **Mockup:** thiết kế theo skill `ui-design`, đi đủ 7 bước của nó.
   - Token lấy từ design system của dự án; dự án chưa có thì dùng `ui-design/references/tokens.css`.
   - Mockup là HTML tĩnh trong scratchpad, chụp bằng `scripts/framecap.mjs` ở các độ rộng dự án cam kết.
   - Tự phán xét bằng `ui-design/references/critique.md` trước khi gửi khách.
   - Gửi kèm câu "đây là bản vẽ, chưa phải code".
   - Việc không đổi giao diện (API, migration, bảo mật) thì thay mockup bằng phương án ngắn: luồng, dữ liệu, rủi ro.
3. **Khách quyết:** chỉ hỏi các điểm thật sự cần khách quyết (≤ 6), gộp vào **một** lượt hỏi cùng mockup.
   Ghi vào `decisions.md`.
4. **Spec:** viết theo `templates/spec.md` (§0, §n từng phần có chủ, nghiệm thu, phân công, thứ tự gộp).
5. **Giao việc:** mỗi phần một agent mới, brief có "ask first" (mẫu trong `references/roles.md`).
   - **dev-shell chỉ khi đợt này đổi thứ dùng chung** (layout, token, chart, helper); không thì dev-pages tự làm.
   - **Hỏi trước:** dev trả về câu hỏi chặn (≤ 5) hoặc READY. Lead trả lời **một lần**, đánh dấu FINAL. Điểm nào
     thuộc quyền khách thì hỏi khách, rồi trả lời dev. Không ai code trước khi có câu trả lời.
   - Các dev chạy song song. Backend gửi shape API cho pages bằng SendMessage ngay khi commit.
6. **Integrator:** gộp theo thứ tự backend → shell → pages, chạy `scripts/gate.sh`, chụp bộ ảnh nghiệm thu.
   Mỗi lỗi tìm thấy thành một gate mới. Đợt chỉ có một nhánh dev thì không cần gộp: chạy gate và chụp ảnh trên
   chính nhánh đó.
7. **Lead review một lần, trên ảnh nghiệm thu và diff.** Phán xét bằng `ui-design/references/critique.md`: cảm giác
   đầu tiên trước, nguyên nhân theo triết lý sau. Sửa ở gốc, đừng vá đúng chỗ bị chỉ.
   - Đạt: sang bước 8.
   - Có lỗi: gom **tất cả** lỗi thành một danh sách đánh số, mỗi dev một **brief sửa** cho một agent mới, rồi quay
     lại bước 6. Không review lẻ từng commit giữa chừng.
8. **Trình khách:** ảnh nghiệm thu, kết quả gate, ảnh hưởng khi deploy, cách rollback (`templates/report.md`).
   Push và deploy **chỉ khi khách nói rõ**. Deploy theo `project.md`: backup trước, kiểm tra sau, ghi cách rollback.

### Chung cho cả hai luồng
- **Mỗi nhiệm vụ một agent mới; agent xong việc thì kết thúc.** Không giữ teammate qua nhiều nhiệm vụ hay đợt.
  Context phình làm mỗi lần gọi đắt dần. Eval 2026-10-27: teammate sống lâu tốn 8,8M token cho một bài mà
  agent mới chỉ tốn 0,4–0,7M. Trạng thái giữa các nhiệm vụ nằm trong spec, `decisions.md` và commit.
- SendMessage chỉ để phối hợp **trong lúc** một nhiệm vụ đang chạy.
- Mỗi dev: nhánh `<prefix>/<round>-<area>` từ tip đang chạy, worktree riêng, compose project và log riêng.
  Brief ghi sẵn tên compose project.
- Lead tự theo dõi việc dài bằng Monitor (xem luật điều phối).

## Luật điều phối (rút từ kinh nghiệm, không bỏ qua)
- **Một quyết định chỉ chốt một lần, đánh dấu FINAL.** Không đảo quyết định khi tin nhắn còn đang đi:
  agent làm theo tin trước rồi mới đọc tin sau, gây commit/revert qua lại.
  Nếu dev đã lỡ làm thứ ngoài phạm vi: nhận hoặc từ chối trong **một** tin.
- **Không reset / rewrite một nhánh mà người khác có thể đã merge.** Muốn bỏ một commit thì revert, hoặc merge
  `-s ours` rồi xoá tường minh. Integrator phải grep cây gộp cuối để chắc thứ đã bỏ không quay lại.
- **Mỗi thao tác quản trị đặt ở nơi người dùng quản lý đối tượng đó** (vd. xoá NPS nằm ở trang License, không chỉ ở
  cuối trang chi tiết). Khi bị chặn, hiện lý do kèm nút bước tiếp theo, không chỉ disable.
- **Mỗi file một chủ.** Đụng file người khác thì phải hỏi. Thứ dùng chung (component, helper, query key)
  thì một người làm, những người khác dùng lại.
- **Một nguồn sự thật:** một từ cho một khái niệm, một định dạng giờ, một ngăn chi tiết,
  một helper đếm số liệu dùng chung cho mọi trang.
- **Tin nhắn chéo:** khi dev báo việc đã làm theo một tin cũ, kiểm tra tip thực tế trước khi giao việc mới.
- **Tin idle của dev:** chỉ tóm tắt cho người dùng khi có thông tin mới. Nếu không có, trả lời một câu.
- **Không tin "xong" khi chưa có bằng chứng:** cần hash commit, kết quả gate và ảnh chụp.
- **Lead tự theo dõi, không chờ thụ động:** sau khi giao việc dài (gate, suite, chụp ảnh, build), tự Monitor log
  và tip nhánh của agent. Log đã báo xong mà agent chưa báo cáo thì đọc kết quả rồi nhắc ngay. Khách không được
  là người phát hiện đội đang đứng.
- **Dev chỉ chạy kiểm tra hẹp** (check của file mình, build, một ảnh trang mình). Gate đầy đủ và ảnh nghiệm thu
  là việc của integrator. Eval: dev tự chạy gate đầy đủ làm một bài Radar mất 49–79 phút thay vì 13.
- **Agent bị từ chối một lệnh** thì phải thử lại bằng lệnh đơn, không được kết luận "Bash bị khoá". Báo cáo nói
  "chưa test" thì không được coi là xong.
- **Báo khách bằng ngôn ngữ của khách:** chỉ nói thay đổi gì, ảnh hưởng gì, cần quyết gì.
  Không dán log, không nhắc tên hàm nếu không cần.

## Tham chiếu
- `references/intake.md`: câu hỏi intake và cách suy ra mặc định.
- `references/rules-baseline.md`: §0 chung (UI, dữ liệu cũ, số liệu, thời gian, văn phong, air-gapped).
- `references/roles.md`: mẫu brief cho từng vai khi spawn hoặc giao việc.
- `templates/`: project.md, ownership.md, gate.conf, pages.txt, spec.md, decisions.md, report.md,
  claude-context.md (mục Working context cho CLAUDE.md của repo), verify/ (skill verify cho repo).
- `scripts/`:
  - `capture.mjs`: chụp các trang của dev server;
  - `framecap.mjs`: chụp các khung `.frame` trong một mockup HTML;
  - `gate.sh`: gate chung, đọc `.claude/team/gate.conf`;
  - `pages-check.mjs`: không cuộn ngang, không lỗi console, không 404, link cũ chuyển đúng.

  Mọi script dùng Chrome local ở chế độ headless, không cần mạng.
