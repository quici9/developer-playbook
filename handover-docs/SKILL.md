---
name: handover-docs
description: >-
  Soạn gói tài liệu bàn giao hệ thống cho đội hạ tầng/khai thác: deployment guide,
  runbook vận hành, troubleshooting, sơ đồ kiến trúc; và soạn tài liệu hướng dẫn sử
  dụng. Bao gồm xuất bản Word (.docx) theo chuẩn trình bày văn bản hành chính Bộ Quốc
  phòng (Thông tư 22/2021/TT-BQP, Nghị định 30/2020/NĐ-CP) với văn phong mệnh lệnh.
  Use when a system is ready to hand over, or when the user says "tài liệu bàn giao",
  "viết runbook", "deployment guide", "tài liệu vận hành", "hướng dẫn sử dụng",
  "bàn giao cho đội hạ tầng", "đội khai thác", "handover", "operations manual",
  "hướng dẫn triển khai", "xuất Word", "file docx", "văn bản hành chính", "chuẩn Bộ
  Quốc phòng", "Nghị định 30", "Thông tư 22".
---

# Handover Docs

Gói tài liệu bàn giao chuẩn cho đội hạ tầng/khai thác — những người **không tham gia phát triển** và vận hành hệ thống trên **mạng air-gapped không có người dev bên cạnh**. Tài liệu phải đủ để họ tự deploy, tự xử lý sự cố thường gặp, và biết khi nào phải gọi ai.

## Bộ tài liệu chuẩn (4 file)

### 1. OVERVIEW.md — Tổng quan hệ thống
- Hệ thống làm gì, cho ai, tại sao tồn tại (3-5 câu)
- Sơ đồ kiến trúc (Mermaid hoặc ASCII): thành phần, luồng dữ liệu, cổng/giao thức giữa các thành phần
- Bảng thành phần: tên, công nghệ, version, vai trò, tài nguyên yêu cầu (CPU/RAM/disk)
- Phụ thuộc bên ngoài trong mạng nội bộ: DNS, NTP, LDAP/AD, registry, database dùng chung

### 2. DEPLOYMENT.md — Hướng dẫn triển khai
- Yêu cầu target: OS, arch, Docker/K8s version, tài nguyên tối thiểu, cổng cần mở
- Các bước cài từ bundle: verify checksum → load images → cấu hình → install.sh → verify.sh
- Bảng toàn bộ biến cấu hình: tên, ý nghĩa, giá trị mặc định, bắt buộc hay không
- Cách nâng cấp phiên bản và cách **rollback** (bước cụ thể, không chỉ "chạy rollback.sh")
- Checklist sau triển khai: service nào phải chạy, healthcheck URL, log ở đâu

### 3. RUNBOOK.md — Vận hành hàng ngày
- Start/stop/restart từng service (lệnh chính xác)
- Kiểm tra sức khỏe định kỳ: cái gì cần xem mỗi ngày/tuần, ngưỡng bình thường
- Backup & restore: cái gì cần backup, tần suất, lệnh backup, **quy trình restore đã được test**
- Quản lý log: vị trí, rotation, log nào quan trọng
- Quản lý dung lượng: cái gì phình ra theo thời gian, dọn thế nào
- Bảng alert (nếu có monitoring): alert nào → nghĩa là gì → làm gì

### 4. TROUBLESHOOTING.md — Xử lý sự cố
- Bảng triệu chứng → nguyên nhân khả dĩ → cách xử lý, cho các sự cố lường trước được
- Cách thu thập thông tin chẩn đoán (bundle log + config gửi cho dev khi bí)
- Giới hạn đã biết (known issues) và cách né
- Ma trận liên hệ: sự cố loại nào → gọi ai, mức độ nào thì escalate

## Nguyên tắc viết

- Viết cho người vận hành, không phải người dev: mọi lệnh copy-paste chạy được ngay, không "xem code để hiểu"
- Không giả định target có internet: không link đến docs online như cách giải quyết duy nhất — kiến thức cần thiết phải nằm trong tài liệu
- Mọi quy trình quan trọng (restore, rollback) phải được **thực hành ít nhất một lần** trước khi bàn giao — chưa test thì ghi rõ
- Version tài liệu khớp version hệ thống, để trong `docs/` của bundle
- Song ngữ nếu đội khai thác cần: ưu tiên tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh

## Xuất bản Word (.docx) — kỹ thuật trình bày theo Thông tư 22/2021/TT-BQP

**Căn cứ đúng là Thông tư số 22/2021/TT-BQP ngày 06/02/2021** (Quy chế công tác văn thư trong
Bộ Quốc phòng). *Không có Thông tư 52/2021/TT-BQP về văn thư* — nếu người dùng nhắc số hiệu đó,
hỏi lại.

### Ranh giới áp dụng — đọc trước khi làm

Tài liệu hướng dẫn sử dụng phần mềm **không phải văn bản hành chính** (không nằm trong 29 tên
loại của Nghị định 30/2020). Vì vậy:

- **ÁP DỤNG** phần *kỹ thuật trình bày*: khổ giấy, lề, phông, cỡ chữ, giãn dòng, số trang,
  cách đánh số đề mục.
- **KHÔNG nhồi** các *thành phần thể thức* của văn bản hành chính vào thân tài liệu: Quốc hiệu –
  Tiêu ngữ, số/ký hiệu, địa danh ngày tháng, nơi nhận, khối chữ ký, dấu `./.`. Những thành phần
  đó thuộc về **quyết định ban hành** tài liệu. Nhồi Quốc hiệu vào đầu một cuốn hướng dẫn 40
  trang rồi kết thúc bằng `./.` là dùng sai mẫu.
- Nếu tài liệu ban hành kèm quyết định, thêm dòng *(Ban hành kèm theo Quyết định số … ngày …
  của …)* in nghiêng, canh giữa, dưới tên tài liệu trên trang bìa.

### Quy cách bắt buộc (moddoc.py đã cài sẵn)

| Chỉ tiêu | Giá trị | Căn cứ |
|---|---|---|
| Khổ giấy | A4 | NĐ30 PL I |
| Lề trên / dưới | 20–25 mm | NĐ30 PL I |
| Lề trái | 30–35 mm | NĐ30 PL I |
| Lề phải | 15–20 mm | NĐ30 PL I |
| Phông chữ | Times New Roman | TT22 PL I |
| Cỡ chữ nội dung | **14** | TT22 |
| Căn lề nội dung | **đều hai biên** | TT22 |
| Lùi đầu dòng | **1,27 cm (1 tab)** — không phải 1 cm | TT22 |
| Cách đoạn | tối thiểu **6 pt** | TT22 |
| Giãn dòng | tối đa **1,5 lines** | TT22 |
| Số trang | chữ số Ả Rập, **cỡ 14**, đứng, canh giữa, **cách mép trên 1 cm** trong lề trên, **không hiện ở trang 1** | TT22 |
| Cỡ chữ bảng, chú thích hình | 13 | quy ước |

NĐ30 dùng cho khổ giấy và định lề vì bản hướng dẫn TT22 không nêu hai chỉ tiêu này.

### Đánh số đề mục — bố cục "phần, mục, khoản, điểm" (TT22)

| Cấp | Ký hiệu | Trình bày |
|---|---|---|
| Mục | `I.` `II.` | **IN HOA, cỡ 14, đứng, ĐẬM**, căn trái |
| Khoản | `1.` `2.` | in thường, cỡ 14, đứng, **không đậm** |
| Điểm | `a)` `b)` | in thường, cỡ 14, đứng |
| Tiết / tiểu tiết | `-` rồi `+` | in thường, cỡ 14, đứng |

Trong Markdown (pandoc): `#` = Mục, `##` = Khoản, cấp `a)` viết thành đoạn thường — **không**
dùng `###`. Với `moddoc`: `h1("I", ...)`, `h2("1", ...)`, `para("a) ...")`.

### Cách sinh

Dùng `assets/moddoc.py` (lớp `MoDDoc`, dựa trên `python-docx`) trong venv riêng:
`python3 -m venv .docvenv && .docvenv/bin/pip install python-docx`. **Không** dùng
`--break-system-packages`.

Viết một script sinh riêng (`scripts/gen_*_docx.py`) gọi API `MoDDoc`; script đó là nguồn chuẩn
của bản Word, `.md` chỉ là bản đọc. **Không convert thẳng Markdown → docx cho bản chính thức**:
văn xuôi mô tả sẽ không thành "Bước 1/2/3" và mất văn phong mệnh lệnh.

Nếu dự án đã dùng pandoc + reference doc thay vì moddoc (ví dụ PT186S), quy cách phải khớp từng
con số với bảng trên — xem `socp/scripts/make-docx-reference.py`.

**TUYỆT ĐỐI KHÔNG sửa tay tệp .docx** — lần sinh lại sau là mất. Nếu người dùng đã lỡ sửa tay,
trích khác biệt ra rồi chuyển ngược vào mã nguồn trước khi sinh lại.

### Kiểm tra bắt buộc sau khi sinh

```bash
python3 ~/.claude/skills/handover-docs/assets/check_thethuc.py <tệp1.docx> [<tệp2.docx> ...]
```

Truyền nhiều tệp thì nó còn **đối chiếu chéo**: mọi tài liệu bàn giao phải cho cùng một kết quả
trên từng chỉ tiêu. Đây là thứ chặn việc hai tài liệu của hai dự án lệch thể thức nhau.

### Placeholder

Nếu không rõ cơ quan/đơn vị/địa danh: để `[TÊN CƠ QUAN CHỦ QUẢN]`, `[TÊN ĐƠN VỊ BAN HÀNH]`,
`[ĐỊA DANH]`, `[____]` (số máy trực ban) và **báo rõ** cho người dùng điền.
Che thông tin nhạy cảm trong ảnh chụp (mật khẩu, khóa) trước khi nhúng.

## Bộ tài liệu bàn giao theo Nghị định 73/2019/NĐ-CP

Với hệ thống đầu tư bằng ngân sách nhà nước, **Điều 35 khoản 4** buộc nhà thầu bàn giao, với
phần mềm nội bộ:

a) Tài liệu của từng giai đoạn theo hợp đồng; b) bộ chương trình cài đặt; c) mã nguồn (nếu có);
d) **tài liệu hướng dẫn sử dụng, quản trị, vận hành; tài liệu phục vụ đào tạo; tài liệu quy
trình bảo trì; hướng dẫn về kỹ thuật và tiêu chuẩn, quy chuẩn**; đ) tài liệu kỹ thuật phục vụ
kết nối.

Điều 35 khoản 2: *"Các tài liệu này phải được xác định rõ trong hợp đồng và là một phần trong
hồ sơ hoàn thành của dự án."*

Nghị định 73 **không quy định gì về thể thức trình bày** và không dẫn chiếu tiêu chuẩn nào cho
việc lập tài liệu — nên không xung đột với TT22.

Tham chiếu quốc tế cho *nội dung và cấu trúc* tài liệu người dùng: **ISO/IEC/IEEE 26514**
(và 26511/26512/26513 cho quản lý, mua sắm, kiểm thử tài liệu). Chưa có TCVN chuyển dịch 26514.

## Văn phong hành chính quân sự (bắt buộc cho tài liệu hướng dẫn/bàn giao)

1. **Mệnh lệnh, dứt khoát, chuẩn hóa thao tác.** Câu chủ động, ngắn gọn, chỉ rõ hành động. Chia thao tác thành **Bước 1, Bước 2, Bước 3...**. Không viết mềm ("bạn có thể bấm..."); viết dứt khoát: *"Nhấn nút **Lưu** (hoặc **Ctrl + S**). Hệ thống báo thành công mới chuyển bước tiếp theo."*
2. **Thuật ngữ chuẩn mực, đồng nhất.**
   - Danh xưng: **Người dùng, Cán bộ quản trị, Cán bộ tác nghiệp, Chỉ huy đơn vị** — không dùng "khách hàng/bạn".
   - Tên giao diện (nút, trường, menu) đặt **in đậm/ngoặc** và **khớp 100%** chữ trên màn hình.
   - Viết hoa đúng danh từ riêng, phiên hiệu, chức vụ, tên hệ thống.
3. **Kỷ luật an toàn thông tin & xử lý lỗi.**
   - Dùng hộp cảnh báo **CHÚ Ý:** / **LƯU Ý QUAN TRỌNG:** (`MoDDoc.box`).
   - Nêu rõ hành vi bị cấm (không chia sẻ tài khoản/chứng thư số; không xuất dữ liệu ra thiết bị ngoài khi chưa được Chỉ huy đơn vị phê duyệt).
   - Xử lý sự cố phải có **đầu mối cụ thể**: *"Trường hợp lỗi ..., cán bộ không tự ý can thiệp mã nguồn mà báo ngay Trực ban Kỹ thuật/Cán bộ quản trị mạng qua số máy quân sự [____]."*

> Bố cục tài liệu hướng dẫn sử dụng theo mục hành chính (I, II, ...; 1, 2, ...; a), b)):
> Quy định chung (mục đích/phạm vi, đối tượng, **an toàn thông tin**, khái niệm) → các chức năng
> theo use case → quy trình nghiệp vụ (đại diện nếu nhiều mục tương tự) → danh mục đầy đủ →
> xử lý sự cố → thuật ngữ → khối ký.

## Rules

- Bắt đầu bằng cách hỏi/xác định: ai vận hành, trình độ của họ, họ được phép làm gì (có quyền root? được sửa config?)
- Tài liệu Word bàn giao dùng `assets/moddoc.py` theo chuẩn BQP ở trên; tài liệu nội bộ/nháp có thể để Markdown
- Sinh đủ 4 file theo cấu trúc trên; nội dung lấy từ code/config thật của dự án, không viết chung chung
- Bảng biến cấu hình và bảng cổng/giao thức là bắt buộc — đây là 2 thứ đội hạ tầng cần nhất
- Nếu thiếu thông tin (ví dụ chưa rõ quy trình backup), đánh dấu `⚠️ TODO` rõ ràng thay vì bịa
