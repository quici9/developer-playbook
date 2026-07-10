---
name: threat-modeling
description: >-
  Threat modeling cho hệ thống đang thiết kế hoặc đã có: xác định tài sản, vẽ luồng
  dữ liệu và trust boundaries, liệt kê mối đe dọa theo STRIDE, đánh giá rủi ro và
  đề xuất biện pháp giảm thiểu. Use when designing any new system/feature, or when
  the user says "threat model", "mô hình hóa mối đe dọa", "phân tích rủi ro bảo mật",
  "attack surface", "bề mặt tấn công", "STRIDE", "ai có thể tấn công hệ thống này",
  "kịch bản tấn công". Also trigger during system-proposal for security-sensitive systems.
---

# Threat Modeling

Phân tích mối đe dọa có cấu trúc, chạy ở **giai đoạn thiết kế** (rẻ nhất để sửa) hoặc trước bàn giao. Bối cảnh mặc định: hệ thống chạy trong mạng nội bộ air-gapped phục vụ đội an ninh mạng — kẻ tấn công đáng quan tâm nhất thường là **insider, lateral movement từ máy đã bị chiếm trong mạng nội bộ, và supply chain qua bundle đưa vào**.

## Quy trình 4 bước

### Bước 1 — Xác định phạm vi & tài sản
- Hệ thống làm gì, dữ liệu gì đi qua? Phân loại: dữ liệu điều tra/case, credential, log thu thập, cấu hình hạ tầng, model/rule detection
- Tài sản nào mất/lộ/sửa thì thiệt hại nhất? (với hệ thống blue team: integrity của log/alert thường quan trọng hơn confidentiality)
- Ai dùng hệ thống, với vai trò gì?

### Bước 2 — Vẽ luồng dữ liệu & trust boundaries
- Sơ đồ DFD (Mermaid): external entities → processes → data stores, đánh dấu trust boundary
- Trust boundaries điển hình trong môi trường này: user ↔ hệ thống, hệ thống ↔ nguồn dữ liệu thu thập (endpoint/sensor — **dữ liệu từ máy có thể đã bị chiếm**), admin ↔ user thường, bundle từ ngoài ↔ mạng air-gapped, giữa các segment mạng nội bộ

### Bước 3 — Liệt kê mối đe dọa theo STRIDE
Với từng thành phần/luồng cắt qua trust boundary:

| STRIDE | Câu hỏi | Ví dụ trong bối cảnh này |
|---|---|---|
| **S**poofing | Giả mạo danh tính được không? | Sensor giả gửi log giả, giả mạo user nội bộ |
| **T**ampering | Sửa dữ liệu/code được không? | Sửa log để xóa dấu vết, sửa rule detection, thay file trong bundle USB |
| **R**epudiation | Chối hành động được không? | Không có audit log ai đã xem case, ai sửa rule |
| **I**nfo disclosure | Lộ dữ liệu được không? | Lộ credential trong log, dữ liệu case cho user sai phân quyền |
| **D**oS | Đánh sập được không? | Sensor flood dữ liệu độc làm sập pipeline xử lý |
| **E**levation | Leo thang đặc quyền? | User thường → admin, container escape, RCE qua dữ liệu thu thập |

Chú ý đặc thù: **dữ liệu đầu vào từ endpoint/malware sample là hostile by default** — parser xử lý nó là bề mặt tấn công số một (RCE qua file độc là kịch bản kinh điển với tool blue team).

### Bước 4 — Đánh giá & biện pháp
- Chấm mỗi threat: Khả năng (Cao/TB/Thấp) × Thiệt hại (Cao/TB/Thấp) → ưu tiên
- Với mỗi threat ưu tiên cao: biện pháp cụ thể (mitigate/eliminate/accept), map vào backlog
- Threat chấp nhận rủi ro phải ghi rõ lý do + người quyết định

## Output Format

```
## 🛡️ Threat Model — [Hệ thống] v[phiên bản thiết kế]

### Tài sản & phân loại
### Sơ đồ DFD + trust boundaries (Mermaid)
### Bảng threats
| # | Thành phần | STRIDE | Mô tả threat | Khả năng | Thiệt hại | Ưu tiên | Biện pháp |
### Threats chấp nhận rủi ro (kèm lý do)
### Việc cần đưa vào backlog
```

## Rules

- Không bỏ qua threat nội bộ — "trong mạng air-gapped nên an toàn" là giả định SAI, air-gap chỉ chặn exfiltration trực tiếp
- Luôn xét bề mặt "dữ liệu hostile đi vào parser" với tool xử lý log/sample/pcap
- Threat không có biện pháp hoặc quyết định chấp nhận = chưa xong threat model
- Cập nhật threat model khi kiến trúc đổi, không làm một lần rồi bỏ
