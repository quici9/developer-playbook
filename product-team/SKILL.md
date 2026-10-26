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
4. Thêm vào `CLAUDE.md` của repo một mục ngắn trỏ tới `.claude/team/project.md`. Không chép lại nội dung.
5. Cho người dùng xem tóm tắt cấu hình. Sửa nếu họ yêu cầu.

## Bước 2: một đợt làm việc (round)
1. **Nghiên cứu:** chụp hiện trạng bằng `scripts/capture.mjs`, đọc code và dữ liệu thật mà hệ thống có.
   Không thiết kế thứ dữ liệu không có. Nếu có panel thì hỏi nhu cầu, nhưng **mình là người thiết kế**.
2. **Mockup:** HTML tĩnh trong scratchpad, chụp bằng `scripts/framecap.mjs`, gửi ảnh cho khách.
   Nêu rõ "đây là bản vẽ, chưa phải code".
3. **Khách quyết:** chỉ hỏi các điểm thật sự cần khách quyết (≤ 6). Ghi vào `decisions.md`.
4. **Spec:** viết theo `templates/spec.md` (§0 quy tắc, §n từng phần có chủ, phần nghiệm thu, phân công, thứ tự gộp).
5. **Giao việc:** spawn hoặc gửi tin cho các vai (định nghĩa agent: `dev-backend`, `dev-shell`, `dev-pages`,
   `integrator`, `panel-user`).
   - Mỗi dev: nhánh `<prefix>/<round>-<area>` từ tip đang chạy, worktree riêng trong scratchpad,
     compose project và thư mục log riêng.
   - Brief phải tự đủ: đường dẫn spec, mockup, phần của họ, phụ thuộc, chủ file, "no push, no deploy".
6. **Review từng commit:** xem ảnh chụp thật, so với mockup và §0. Trả lời từng dev ngắn gọn:
   duyệt, hoặc liệt kê lỗi đánh số.
7. **Integrator:** gộp theo thứ tự (backend → shell → pages), chạy `scripts/gate.sh`, chụp bộ ảnh nghiệm thu.
   Integrator thêm gate cho mọi lỗi tìm thấy để lỗi không quay lại.
8. **Trình khách:** gửi ảnh nghiệm thu, kết quả gate, ảnh hưởng khi deploy, cách rollback.
   Push và deploy **chỉ khi khách nói rõ**.
9. **Deploy:** theo quy trình trong `project.md`. Phải backup trước, chạy kiểm tra sau deploy, ghi lại cách rollback.

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
- **Dev chờ notification mà không kiểm log:** nếu lâu không thấy báo cáo thì hỏi trạng thái một lần.
- **Báo khách bằng ngôn ngữ của khách:** chỉ nói thay đổi gì, ảnh hưởng gì, cần quyết gì.
  Không dán log, không nhắc tên hàm nếu không cần.

## Tham chiếu
- `references/intake.md`: câu hỏi intake và cách suy ra mặc định.
- `references/rules-baseline.md`: §0 chung (UI, dữ liệu cũ, số liệu, thời gian, văn phong, air-gapped).
- `references/roles.md`: mẫu brief cho từng vai khi spawn hoặc giao việc.
- `templates/`: project.md, ownership.md, gate.conf, pages.txt, spec.md, decisions.md, report.md.
- `scripts/`:
  - `capture.mjs`: chụp các trang của dev server;
  - `framecap.mjs`: chụp các khung `.frame` trong một mockup HTML;
  - `gate.sh`: gate chung, đọc `.claude/team/gate.conf`;
  - `pages-check.mjs`: không cuộn ngang, không lỗi console, không 404, link cũ chuyển đúng.

  Mọi script dùng Chrome local ở chế độ headless, không cần mạng.
