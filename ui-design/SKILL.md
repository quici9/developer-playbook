---
name: ui-design
description: >-
  Thiết kế giao diện dựa trên triết lý thiết kế thay vì quy tắc cứng: hiểu người dùng và
  khoảnh khắc sử dụng, chọn lọc nội dung, một điểm nhấn – phần còn lại lùi lại, sự dịu và
  nhất quán, tôn trọng người đọc — rồi render, nhìn và phán xét như người dùng, lặp lại.
  Không phụ thuộc stack (React/Angular/Vue/HTML), asset offline cho air-gapped. Use when
  the user says "thiết kế giao diện", "design UI", "làm mockup", "vẽ màn hình", "giao diện
  đẹp hơn", "UI xấu quá", "nặng nề quá", "polish UI", "redesign", "landing page",
  "dashboard trông thế nào", "design system", "theme", "dark mode", or before building
  any user-facing screen from scratch. Pairs with web-frontend and product-team.
---

# UI Design

Skill này không phải bộ luật. Nó là **cách nghĩ** của một designer giỏi, kèm vài mặc định
để khởi đầu. Mọi con số, pattern, token trong `references/` đều là *điểm xuất phát*: dùng
khi chưa có lý do làm khác, và bỏ khi có lý do.

Bài học từ việc thua công cụ thiết kế chuyên dụng không nằm ở kỹ thuật. Model biết rất
nhiều, nên có xu hướng **đưa hết vào màn hình** và **không bao giờ nhìn lại kết quả**.
Thiết kế tốt thì ngược lại: biết bỏ, và nhìn bằng mắt người dùng.

## Triết lý

### 1. Thiết kế cho một người, trong một khoảnh khắc
Trước khi vẽ, hình dung một người cụ thể đang ở một tình huống cụ thể. Ví dụ một analyst ở
giờ thứ 10 của ca trực, vừa nhận incident critical. Họ cần biết điều gì đầu tiên? Họ sẽ
làm gì tiếp theo? Họ mệt đến mức nào? Mọi quyết định sau đó đều quy về câu trả lời này.
*Tự hỏi: màn hình này giúp ai, làm gì, ngay lúc nào?*

### 2. Thiết kế là chọn lọc
Thông tin có sẵn luôn nhiều hơn thông tin cần thấy. Giá trị của designer nằm ở chỗ quyết
định **cái gì không xuất hiện**, hoặc chỉ xuất hiện khi được hỏi. Một màn hình đầy đủ mọi
thứ không phải là chu đáo, mà là đẩy việc chọn lọc sang người dùng.
*Tự hỏi: bỏ chi tiết này đi thì người dùng mất gì? Nếu câu trả lời là "không mất gì đáng
kể", bỏ nó.*

Nhưng chọn lọc là tìm cho ra **vừa đủ**, không phải cắt càng nhiều càng tốt. Thừa thì nặng.
Thiếu thì người dùng phải click liên tục, mất ngữ cảnh, và cảm thấy màn hình "chưa xong"
hoặc không đáng tin. Mức "đủ" do công việc của người dùng quyết định. Người phân tích cần
đủ ngữ cảnh để ra quyết định ngay tại chỗ; người chỉ lướt qua để biết tình hình thì cần ít
hơn nhiều.
*Tự hỏi thêm: với những gì đang hiện, người dùng đã đủ tự tin để hành động chưa?*

### 3. Một giọng nói chính, phần còn lại lùi lại
Sự chú ý có hạn. Mỗi màn hình có một điều quan trọng nhất, và nó phải được nói rõ nhất.
Mọi thứ khác hạ giọng: nhỏ hơn, nhạt hơn, ít màu hơn. Khi nhiều thứ cùng nói to (màu, khung,
badge, chữ đậm), người xem không nghe được gì, và cảm thấy *nặng*.
*Tự hỏi: nheo mắt nhìn, mắt rơi vào đâu đầu tiên? Có đúng là thứ quan trọng nhất không?*

### 4. Sự dịu đến từ việc bớt đi, không từ việc tô thêm
Một giao diện yên tĩnh có ít đường kẻ, ít khung, ít màu, và nhiều khoảng thở. Cấu trúc được
tạo bằng khoảng trắng và căn chỉnh trước, rồi mới đến đường kẻ hay hộp. Màu dành cho
ý nghĩa (trạng thái, hành động), không dành cho trang trí. Mỗi phần tử thị giác thêm vào
đều có giá: nó lấy đi một ít sự chú ý của những thứ khác.
*Tự hỏi: khung, viền, màu này đang phân tách hay mang nghĩa gì? Khoảng trắng có làm được
việc đó không?*

Dịu không có nghĩa là trống hay nhạt. Một giao diện dịu vẫn có kết cấu: icon giúp nhận diện
nhanh, nhóm thông tin rõ ràng, chi tiết được chăm chút. Những thứ này làm màn hình có sức
sống và trông hoàn thiện, miễn là chúng *phục vụ việc đọc* chứ không tranh giành sự chú ý.
Hãy bớt *tiếng ồn*, đừng bớt *chất liệu*.

### 5. Nhất quán tạo ra sự tin cậy
Khi cùng một thứ luôn trông giống nhau (cùng kiểu nút, cùng khoảng cách, cùng cách thể hiện
trạng thái), người dùng ngừng phải suy nghĩ về giao diện và tập trung vào công việc. Sự
nhất quán là thứ người ta cảm nhận là "chuyên nghiệp", dù không gọi tên được. Vì vậy hãy
định nghĩa hệ thống (thang khoảng cách, cỡ chữ, màu theo vai trò) trước, rồi mới dựng từng
phần.
*Tự hỏi: hai thứ cùng vai trò ở hai chỗ có trông giống nhau không?*

### 6. Tôn trọng người đọc
Đẹp mà không đọc được, không thao tác được thì không phải là đẹp. Chữ phải đủ lớn và đủ
tương phản cho người dùng thật trong điều kiện thật. Mọi control phải dùng được bằng bàn
phím. Trạng thái không được chỉ dựa vào màu. Đừng đổi sự gọn gàng lấy chữ tí hon: hãy giảm
*số lượng* thứ hiển thị, đừng giảm *kích thước* của chúng.

### 7. Nội dung thật làm nên thiết kế thật
Thiết kế được kiểm chứng bằng nội dung. Dữ liệu giả phải đúng với lĩnh vực, có chuỗi dài,
có giá trị rỗng, có cả trường hợp xấu. Lorem ipsum và số tròn trịa che giấu đúng những
chỗ thiết kế sẽ vỡ. Thiết kế cả lúc không có dữ liệu, đang tải, và bị lỗi.

Màn hình cũng phải kể **một câu chuyện nhất quán**. Số đếm, bộ lọc đang áp dụng, tab đang
chọn và dữ liệu hiển thị phải khớp nhau. Lọc "Critical" mà vẫn hiện alert Low, hay tab
"Chưa giao" mà có dòng đã giao, là những lỗi người dùng nhận ra ngay. Khi đó họ thôi tin
vào giao diện.

### 8. Nhìn, rồi phán xét như người dùng
Code đúng không có nghĩa là trông đúng. Hãy render, nhìn ảnh, và đọc nó như người dùng ở
nguyên tắc 1 sẽ đọc, không như người vừa viết ra nó. Cảm giác đầu tiên ("rối", "nặng",
"không biết nhìn đâu") là dữ liệu quan trọng nhất. Checklist và số đo chỉ giúp tìm *nguyên
nhân* của cảm giác đó, không thay thế được nó.

Cảm giác có hai chiều. "Nặng" và "rối" nghĩa là thừa. "Thiếu", "nhạt", "chưa xong" nghĩa
là cắt quá tay. Sửa một chiều thì phải để ý đừng rơi sang chiều kia.

## Cách làm

1. **Hiểu**: viết vài dòng về người dùng, khoảnh khắc sử dụng, câu hỏi chính và hành động
   chính của màn hình (nguyên tắc 1).
2. **Chọn lọc**: liệt kê mọi thứ *có thể* hiện, rồi quyết định cái gì lên màn hình, cái gì
   nằm sau một cú click, cái gì bỏ hẳn (nguyên tắc 2). Xác định điểm nhấn duy nhất (nguyên
   tắc 3).
3. **Hệ thống**: project đã có design system thì dùng nó. Chưa có thì khởi đầu từ
   `references/tokens.css` và điều chỉnh theo tính cách sản phẩm (nguyên tắc 5).
4. **Dựng**: theo stack của project (`references/stacks.md`). Giá trị lấy từ token, asset
   chạy offline.
5. **Nhìn & phán xét**: render rồi Read ảnh (`scripts/shot.sh`). Ghi lại cảm giác đầu tiên,
   rồi mới phân tích nguyên nhân theo các câu hỏi trong `references/critique.md`. Khi cần số
   đo để soi (tràn ngang, cỡ chữ, mật độ), dùng `scripts/audit.cjs`.
6. **Lặp**: sửa nguyên nhân gốc, không vá triệu chứng. Thường cần 2–3 vòng. Mỗi vòng hướng về
   mức *vừa đủ*: bớt tiếng ồn, giữ chất liệu.
7. **Báo cáo**: kết quả, ảnh, các lựa chọn chính và lý do, những gì đã cố ý bỏ.

Khi người dùng nhận xét về thiết kế ("nặng", "rối", "nhạt"), hãy truy về triết lý nào đang
bị vi phạm, rồi sửa ở tầng đó. Đừng chỉ sửa đúng chỗ họ chỉ vào.

## Trong đội agent (skill `product-team`)
Triết lý và cách làm ở trên giữ nguyên. Chỉ phân vai:
- **Lead designer** đi đủ 7 bước khi làm mockup, và dùng `references/critique.md` khi review ảnh nghiệm thu.
  Kết quả phán xét chuyển thành danh sách lỗi đánh số trong brief sửa.
- **dev-shell** dựng token: design system của dự án được ưu tiên; dự án chưa có thì khởi đầu từ `references/tokens.css`.
- **dev-pages** không thiết kế lại. Chỗ spec bỏ ngỏ thì quyết theo triết lý này, rồi liệt kê các quyết định đó trong
  báo cáo. Nhìn trang của mình một lần bằng bước 1–2 của `critique.md`.
- **Chụp ảnh trong đội** dùng script của `product-team` (Chrome local, độ rộng và theme trong `.claude/team/gate.conf`).
  Không dùng `scripts/shot.sh`: mặc định 1440/390 của nó không phải độ rộng dự án cam kết, và nó cần Playwright.
  `scripts/audit.cjs` vẫn dùng được để đo.

## Ràng buộc air-gapped
Không dùng font, icon hay ảnh từ CDN trong sản phẩm. Font dùng system stack hoặc vendor
woff2 vào repo; icon dùng package local hoặc inline SVG. Các script trong `scripts/` là
công cụ lúc dev, không nằm trong bundle triển khai.

## Tài liệu tham khảo (mặc định, không phải luật)
| File | Nội dung |
|---|---|
| `references/defaults.md` | Mặc định cụ thể (spacing, chữ, màu, layout) và các bẫy CSS đã gặp |
| `references/tokens.css` | Bộ token khởi đầu, light + dark, đã kiểm contrast |
| `references/patterns.md` | Câu hỏi chính và cách tiếp cận cho các loại màn hình hay gặp |
| `references/critique.md` | Câu hỏi để phán xét một ảnh chụp |
| `references/stacks.md` | Áp token và component vào từng stack |
