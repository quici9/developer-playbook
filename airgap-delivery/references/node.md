# Node.js / Frontend (Angular, React, Vue) — offline delivery

## Nguyên tắc vàng cho frontend

**Build khi còn internet, chỉ chuyển sản phẩm build** (`dist/`, `build/`, `.next/standalone`). KHÔNG BAO GIỜ `npm install` trên air-gapped. Static bundle (Angular/React/Vue SPA) chỉ là file tĩnh — copy + serve bằng nginx là xong.

```bash
npm ci && npm run build        # build từ lockfile, reproducible
# bundle: dist/ + nginx.conf, hoặc đóng vào image nginx:alpine
```

## Offline-cleanliness — frontend hay dính nhất

- [ ] Fonts: không dùng Google Fonts CDN — self-host bằng `@fontsource/*` hoặc file woff2 local
- [ ] Không có `<script src="https://cdn...">`, không icon/analytics từ CDN (grep `https://` trong dist/)
- [ ] Map tiles, chart lib assets: bundle local
- [ ] API base URL cấu hình được lúc deploy (env/config.json), không hardcode domain internet
- [ ] Angular: tắt CLI analytics (`ng analytics off`); source map upload (Sentry...) loại khỏi build prod

## Backend Node (nếu có) — vendor node_modules

Cách 1 (ưu tiên): đóng Docker image, deps nằm trong image.

Cách 2: bundle cache npm offline:

```bash
npm ci                                     # trên máy internet
tar czf vendor/npm-cache.tgz ~/.npm        # hoặc dùng npm pack cho từng deps
# Trên target:
npm ci --offline --cache ./npm-cache
```

Cách 3: bundler (esbuild/webpack) gộp server thành 1 file JS → chỉ cần Node runtime trên target.

## Bẫy thường gặp

- `postinstall` script tải binary (esbuild, sharp, puppeteer, node-sass): phải có sẵn trong cache đúng platform target, hoặc loại bỏ deps đó.
- `npm audit` + `npx license-checker` khi còn internet.
- Node version trên target phải khớp — ghi vào BUNDLE.md, hoặc bundle luôn Node tarball chính thức.
