---
name: system-proposal
description: >-
  Biến ý tưởng hoặc bản thiết kế chung chung thành đề xuất hệ thống cụ thể: làm rõ
  yêu cầu, so sánh phương án kỹ thuật, chốt kiến trúc, phạm vi MVP, rủi ro và kế
  hoạch triển khai — kèm ADR cho các quyết định quan trọng. Use when the user says
  "đề xuất hệ thống", "thiết kế hệ thống này", "nhận được bản thiết kế chung chung",
  "nên dùng công nghệ gì", "phương án nào tốt hơn", "A hay B", "đánh giá giải pháp",
  "kiến trúc thế nào", "viết proposal", "ADR", "scope MVP", or when starting any
  new system from a vague requirement.
---

# System Proposal

Từ "đội blue team cần một cái để X" → tài liệu đề xuất mà cấp trên duyệt được và dev (chính mình) build được. Ràng buộc mặc định của mọi thiết kế: **deploy air-gapped, self-hosted toàn bộ, đội khai thác vận hành sau bàn giao, nguồn lực dev hạn chế**.

## Bước 1 — Làm rõ yêu cầu (trước khi nghĩ giải pháp)

- Ai dùng, giải quyết nỗi đau nào, hiện tại họ đang làm thủ công ra sao?
- Dữ liệu: nguồn nào, khối lượng/tốc độ bao nhiêu (con số thật: GB/ngày, events/giây, số user), giữ bao lâu?
- Ràng buộc cứng: mạng nào, tài nguyên phần cứng có gì, tích hợp với hệ thống nội bộ nào (LDAP, SIEM...), deadline?
- Tiêu chí thành công đo được: "giảm thời gian triage từ X còn Y" chứ không phải "tiện hơn"
- Bản thiết kế chung chung nhận được: liệt kê các điểm mơ hồ thành câu hỏi cụ thể gửi lại người giao — đừng tự đoán yêu cầu quan trọng

## Bước 2 — So sánh phương án

Với mỗi quyết định lớn (build vs dùng open source có sẵn, ngôn ngữ, kiến trúc, storage):

| Tiêu chí | Phương án A | Phương án B | Phương án C |
|---|---|---|---|
| Đáp ứng yêu cầu chính | | | |
| Vận hành trên air-gapped (deps, update, license) | | | |
| Công sức build + duy trì | | | |
| Đội khai thác vận hành nổi không | | | |
| Rủi ro chính | | | |

- Luôn xét phương án "dùng/ghép tool open source có sẵn" trước khi build mới — build là phương án đắt nhất
- Open source: check license, còn maintain không, chạy offline được không, cộng đồng đủ lớn để tự vá
- Chấm điểm xong phải **chọn** — bảng so sánh không có kết luận là chưa xong

## Bước 3 — Kiến trúc & phạm vi

- Sơ đồ kiến trúc (Mermaid): thành phần, luồng dữ liệu, ranh giới mạng/trust boundary
- Chạy threat-modeling cho thiết kế nếu hệ thống chạm dữ liệu nhạy cảm (mặc định là có)
- MVP: lát cắt mỏng nhất chứng minh giá trị end-to-end — liệt kê rõ **những gì KHÔNG làm** ở phase 1
- Roadmap phase 2+ ngắn gọn, tránh thiết kế trước cho tương lai chưa chắc đến

## Bước 4 — ADR cho quyết định quan trọng

Mỗi quyết định khó đảo ngược (chọn DB, message queue, ngôn ngữ, mô hình deploy) một ADR ngắn:

```
# ADR-NNN: [Quyết định]
Ngày | Trạng thái: Đề xuất/Đã duyệt
## Bối cảnh: (vấn đề + ràng buộc dẫn đến quyết định)
## Quyết định: (chọn gì)
## Lý do & phương án đã loại: (tại sao, loại gì, vì sao loại)
## Hệ quả: (được gì, chịu gì, lối thoát nếu sai)
```

## Output Format

Tài liệu proposal: Tóm tắt 1 đoạn → Vấn đề & yêu cầu → Phương án & lựa chọn (bảng + kết luận) → Kiến trúc (sơ đồ) → Phạm vi MVP & không-làm → Rủi ro chính & giảm thiểu → Nguồn lực & timeline ước lượng → ADRs đính kèm.

## Rules

- Không có con số (khối lượng dữ liệu, số user, tài nguyên) thì hỏi hoặc ghi rõ giả định — thiết kế không số liệu là thiết kế mò
- Mọi đề xuất phải sống được trên air-gapped: hỏi ngay từ đầu "cái này update/license/deps thế nào khi không có internet"
- Ước lượng công sức thành khoảng (2-4 tuần) kèm điều kiện, không hứa điểm chết
- Khuyến nghị dứt khoát một phương án — trình bày trade-off xong phải chốt, không đẩy quyết định ngược lại người hỏi
