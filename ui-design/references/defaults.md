# Mặc định tham khảo

Đây là các giá trị khởi đầu hợp lý khi chưa có lý do làm khác. Chúng phục vụ triết lý
trong `SKILL.md`, không thay thế nó. Nếu bối cảnh cần khác (sản phẩm tiêu dùng, màn hình
treo tường, thiết bị cảm ứng, brand riêng...) thì cứ phá, miễn là giải thích được vì sao.
Project đã có design system thì design system đó đứng trước file này.

## 1. Spacing

- Thang 4px: `4 8 12 16 20 24 32 40 48 64 80`. Không dùng 5, 7, 10, 15, 18…
- **Trong một nhóm** < **giữa các nhóm** < **giữa các vùng**. Ví dụ compact:
  label↔value 4, item↔item 8–12, nhóm↔nhóm 24, vùng↔vùng 32.
- Padding card/panel: 16 (compact) – 24 (comfortable). Padding ngang ≥ padding dọc.
- Gutter giữa panel cùng hàng = khoảng cách giữa các hàng panel (thường 16 hoặc 24).
- Lề trang: 24–32 desktop, 16 mobile.

## 2. Typography

- **Tối đa 2 họ chữ**: một sans cho UI, một mono cho dữ liệu kỹ thuật (IP, hash, log, ID).
- **Tối đa 5–6 cỡ chữ trên một màn hình.** Thang gợi ý (px): `12 13 14 16 18 22 28 36`.
  Body compact 13–14, comfortable 15–16.
- Line-height: body 1.5; heading 1.2–1.3; số lớn 1.1.
- Weight: 400 body, 500 nhấn nhẹ / label, 600 heading & số KPI. Tránh 700+ cho UI dày.
- Chữ ≥ 24px: letter-spacing −0.01 đến −0.02em. Chữ in hoa nhỏ (eyebrow/label nhóm):
  11–12px, +0.04–0.06em, weight 500–600, mực secondary.
- 3 cấp mực: primary (nội dung), secondary (label, meta), tertiary (gợi ý, timestamp phụ).
  Phân cấp bằng mực **trước** khi tăng cỡ chữ.
- Số: `font-variant-numeric: tabular-nums` trong bảng, KPI, trục; căn phải trong cột số.
- Độ dài dòng văn bản 60–80 ký tự (`max-width: 70ch`).

## 3. Màu

- Xây theo **vai trò**, không theo tên màu: `bg`, `surface`, `surface-raised`, `border`,
  `text`, `text-secondary`, `text-tertiary`, `accent`, `accent-soft`, `status-*`.
- Neutral hơi ngả lạnh (xanh xám) cho tool kỹ thuật; ngả ấm cho sản phẩm tiêu dùng/biên tập.
- **Một accent.** Dùng cho: nút chính, link, trạng thái chọn/active, focus ring. Không dùng
  cho tiêu đề hay trang trí.
- Màu trạng thái: critical (đỏ) · high (cam) · medium (vàng hổ phách) · low/neutral (xám)
  · ok (xanh lá) · info (xanh dương = accent hoặc riêng). Hiển thị dạng **soft**: nền nhạt
  10–15% + chữ đậm cùng họ + icon. Chỉ critical đang cần hành động mới được nền đặc.
- Contrast: chữ thường ≥ 4.5:1 (kể cả chữ trắng trên nút accent), chữ ≥ 18px/600 và icon
  ≥ 3:1. Viền là thứ duy nhất nhận diện control (input, checkbox) → ≥ 3:1 (`--border-input`);
  viền trang trí của card/panel thì được mờ.
- Không dựa vào màu đơn thuần: kèm icon hình dạng khác nhau, chữ, hoặc vị trí.

### Dark mode — không phải đảo màu
- Nền không đen tuyệt đối: `#0b0d12`–`#111318`. Bề mặt nâng lên **sáng hơn** nền 3–6%
  (dark dùng độ sáng để thể hiện elevation, không dùng shadow).
- Chữ không trắng tuyệt đối: `#e8eaee` cho primary.
- Màu bão hoà phải giảm độ đậm/tăng độ sáng so với light mode để không chói.
- Viền mảnh `rgba(255,255,255,0.06–0.10)` thay cho shadow.

## 4. Bố cục

- Lưới 12 cột hoặc layout flex có tỷ lệ rõ (2:1, 3:1). Tránh chia đều mọi thứ.
- **Căn mép**: mọi phần tử trong một cột phải chung mép trái; số liệu chung mép phải.
- Một vùng nhấn chính trên màn hình (P1) — lớn hơn hoặc ở góc trên trái (đọc F-pattern).
- Header trang: tiêu đề + meta + hành động chính phía phải, cùng một baseline.
- Responsive: ≤ 768px các cột xếp chồng theo thứ tự ưu tiên P1→P3, bảng rộng cuộn ngang
  trong khung riêng, toolbar wrap. Không bao giờ để trang cuộn ngang.

## 5. Bề mặt, viền, bóng, radius

- Phân tách theo thứ tự ưu tiên: **khoảng trắng → đường kẻ mảnh → nền khác tông → card
  có viền → shadow**. Dùng mức thấp nhất đủ hiệu quả.
- Radius nhất quán theo cấp: control 6, card/panel 10, modal 14, pill 999. Phần tử lồng
  trong: radius trong = radius ngoài − padding (tối thiểu 4).
- Shadow (light mode): chỉ cho lớp nổi thật (dropdown, modal, toast). Card thường dùng viền.

## 6. Control & tương tác

- Chiều cao control thống nhất trên một hàng: 28 (dense) / 32 (compact) / 36–40 (comfortable).
- Nút: 1 primary (accent đặc) mỗi vùng; còn lại secondary (viền) hoặc ghost. Nút nguy hiểm
  dùng đỏ, đặt tách khỏi primary.
- Mọi control có: hover (đổi nền 4–8%), focus-visible (ring 2px accent, offset 2px),
  active, disabled (opacity 0.5 + `cursor: not-allowed`).
- Icon: một bộ duy nhất, stroke 1.5–2, cỡ 16 (inline với chữ 13–14) / 20 (nút lớn).
  Icon-only button phải có `aria-label` và tooltip.
- Motion: 120–200ms, ease-out; chỉ cho phản hồi tương tác, không animate trang trí.

## 7. Bẫy kỹ thuật đã gặp (CSS)

- **Flex container `flex-wrap: wrap` xếp dọc trên mobile** → mỗi "dòng" rộng bằng max-content
  của item (bảng 760px kéo cả trang tràn). Khi chuyển sang cột: `flex-wrap: nowrap`, và đặt
  `min-width: 0` cho panel/card là flex item.
- **Định danh có gạch nối** (`ws-ketoan-114`, `dc-ad-01`) bị trình duyệt ngắt ngay dấu `-`
  → bọc `white-space: nowrap`; chỉ chuỗi dài thật (command line, path) mới cho
  `overflow-wrap: anywhere`.
- **Dấu phân cách "·" / "•" dạng phần tử riêng** trôi lẻ loi đầu dòng khi wrap → dùng `gap`
  thay cho phần tử phân cách, hoặc gắn dấu vào cùng item bằng nowrap.
- **Thứ tự ưu tiên trên mobile** khác thứ tự 2 cột desktop → `display: contents` cho 2 cột
  rồi `order` từng panel theo P1→P3.
- **Khối "đã xảy ra" vs "chưa"**: kiểm tra ở *cả hai theme* — nền `surface-raised` trùng màu
  panel ở light mode làm đảo nghĩa. Phân biệt bằng viền/ký hiệu, không chỉ bằng tông nền.

## 8. Dữ liệu dày (tool chuyên gia)

- Bảng: hàng 32–36 (compact) / 44 (comfortable); header sticky; zebra **hoặc** đường kẻ,
  không cả hai; cột text căn trái, số căn phải, trạng thái dạng badge; hover hàng.
- Giá trị dài (hash, path, message): mono, truncate giữa với hash (`a3f9…77c1`), cuối với
  path; tooltip/copy button bên cạnh.
- Timestamp: tương đối cho gần ("4 phút trước") + tuyệt đối trong tooltip; tuyệt đối với
  múi giờ khi cần đối chiếu điều tra.
- Badge/tag: cao 20–22, padding ngang 6–8, chữ 11–12/500, radius 4–6 hoặc pill — một kiểu
  thống nhất.

## 9. Biểu đồ trong UI

- Biểu đồ phục vụ câu hỏi, không lấp chỗ trống. KPI đơn → số lớn (+ sparkline tuỳ chọn),
  không cần chart.
- Gridline mảnh, mờ; không viền khung; trục tối giản; legend khi ≥ 2 series.
- Màu series lấy từ palette categorical cố định, tách biệt với màu trạng thái — trừ khi
  series *chính là* mức độ nghiêm trọng.
- Tooltip khi hover; đánh dấu điểm bất thường bằng annotation có chữ.
- Có skill `dataviz` thì đọc nó cho phần chart.

## 10. Copy (chữ trên giao diện)

- Ngắn, động từ trước cho hành động ("Tạo rule", không phải "Rule mới").
- Nhất quán thuật ngữ trên toàn sản phẩm; giữ thuật ngữ kỹ thuật gốc (alert, host, rule).
- Empty state = giải thích + hành động tiếp theo, không chỉ "Không có dữ liệu".
- Lỗi = chuyện gì xảy ra + làm gì tiếp.
