# Áp dụng vào từng stack

Nguyên tắc: **CSS custom properties là ngôn ngữ chung.** Token sống ở một file CSS
(`tokens.css`), mọi stack tham chiếu tới biến — đổi theme/brand chỉ sửa một chỗ.

Luôn kiểm tra project trước: đã có component library / theme thì dùng nó, map token của
skill vào token của nó thay vì chồng thêm một hệ thứ hai.

## HTML/CSS thuần (mockup, prototype, trang tĩnh)
- Một file HTML, `<style>` nhúng `tokens.css` + CSS component theo class ngữ nghĩa
  (`.panel`, `.badge--critical`, `.kv`). Không inline style rải rác.
- Tương tác nhẹ: vanilla JS hoặc không JS. Đây là định dạng tốt nhất để thử thiết kế nhanh
  và chụp bằng `shot.sh`.

## React
- **Tailwind**: map token vào `theme.extend` (`colors: { surface: 'var(--surface)', ... }`,
  `spacing` giữ thang mặc định — đã là 4px). Tailwind v4: khai báo trong `@theme`.
- Component: **shadcn/ui** (code copy vào repo, dựa trên Radix — vendor tự nhiên, hợp
  air-gapped) hoặc Radix primitives + CSS riêng. shadcn dùng biến CSS — map sang token.
- Icon: `lucide-react`. Chart: Recharts / ECharts (`echarts-for-react`) / uPlot (log lớn).
- Bảng lớn: TanStack Table + TanStack Virtual.

## Angular
- Angular Material 3: map token qua `mat.theme` + override CSS variables (`--mat-sys-*`)
  bằng token của skill; hoặc dùng **Angular CDK** (overlay, a11y, virtual scroll) + CSS
  riêng khi muốn thoát "vẻ Material".
- PrimeNG (theme bằng design tokens, chế độ unstyled) là lựa chọn khi cần nhiều component
  dữ liệu (table, tree) nhanh.
- Icon: `lucide-angular` hoặc SVG sprite local. Chart: ECharts (`ngx-echarts`).
- Style: token toàn cục trong `styles.scss`; component dùng `var(--token)`, không hardcode.

## Vue
- PrimeVue (unstyled/preset), Naive UI, hoặc Radix Vue / Reka UI + CSS riêng.
- Tailwind dùng giống React. Icon: `lucide-vue-next`. Chart: ECharts (`vue-echarts`).

## Svelte / khác
- Cùng nguyên tắc: token CSS toàn cục, component đọc biến; Bits UI / Melt UI cho primitive.

## Font offline
- System stack (mặc định trong `tokens.css`) — luôn an toàn.
- Muốn Inter/JetBrains Mono: `npm i @fontsource-variable/inter` rồi import trong entry —
  font được bundle, không gọi mạng. Kiểm tra bundle không còn `fonts.googleapis.com`.

## Kiểm tra offline sau khi dựng
```bash
grep -rnE "https?://(fonts\.googleapis|fonts\.gstatic|cdn\.|unpkg|cdnjs|esm\.sh|images\.unsplash)" src/ dist/ 2>/dev/null
```
Kết quả phải rỗng. Chi tiết đóng gói: skill `airgap-delivery`.
