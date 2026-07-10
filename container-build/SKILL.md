---
name: container-build
description: >-
  Xây Dockerfile và compose stack tối ưu, an toàn cho Python, Go, Rust, Node —
  multi-stage build, distroless/scratch, non-root, image nhỏ, sẵn sàng cho registry
  nội bộ và deploy air-gapped. Use when the user says "dockerize", "viết Dockerfile",
  "docker compose", "container hóa", "image quá to", "tối ưu image", "docker build
  lỗi", "container không chạy", or when a project needs containerization.
---

# Container Build

Mục tiêu: image **nhỏ, ít bề mặt tấn công, pin cứng version**, chạy được trên registry nội bộ air-gapped. Compose cho dev local phải tiện; image production phải chặt.

## Dockerfile chuẩn theo ngôn ngữ

**Go / Rust** — build static, chạy trên scratch/distroless:

```dockerfile
FROM golang:1.23.4-alpine AS build          # luôn pin version đầy đủ
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download                          # layer cache deps riêng
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /app ./cmd/app

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /app /app
USER nonroot
ENTRYPOINT ["/app"]
```

**Python** — slim + venv copy, không build tool trong image cuối:

```dockerfile
FROM python:3.12-slim AS build
WORKDIR /src
COPY requirements.lock .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.lock
COPY . .

FROM python:3.12-slim
RUN useradd -r -u 10001 app
COPY --from=build /venv /venv
COPY --from=build /src /srv
USER app
WORKDIR /srv
ENTRYPOINT ["/venv/bin/python", "-m", "app"]
```

**Frontend (Angular/React/Vue)**: stage build node → copy `dist/` sang `nginx:alpine` (pin version), nginx.conf tự viết, không dùng default.

## Checklist bắt buộc

- [ ] Pin version đầy đủ mọi `FROM` (kể cả stage build) — không `latest`, không tag ngắn kiểu `3`
- [ ] Non-root user; `USER` đặt trước ENTRYPOINT
- [ ] `.dockerignore`: `.git`, `.env`, node_modules, __pycache__, test data — vừa nhanh vừa tránh lộ secret
- [ ] Không secret trong image (ARG/ENV build-time cũng lộ qua `docker history`) — secret inject lúc runtime
- [ ] `HEALTHCHECK` hoặc healthcheck trong compose/K8s manifest
- [ ] Layer cache đúng thứ tự: deps trước, source sau
- [ ] Quét trước khi bundle: `trivy image <img>` — HIGH/CRITICAL phải xử lý
- [ ] Air-gapped: mọi image tham chiếu được `docker save` vào bundle (xem skill airgap-delivery)

## Compose: tách dev và prod

- `docker-compose.yml` (dev): bind mount source, hot reload, port mở localhost, secret dev đơn giản
- `docker-compose.prod.yml` (target): image từ registry nội bộ/đã load, không bind mount source, `restart: unless-stopped`, `env_file` trỏ file secret do install.sh sinh, network `internal: true` cho service không cần expose
- Volume có tên (named volume) cho dữ liệu — ghi rõ trong tài liệu bàn giao volume nào cần backup

## Rules

- Image cuối không có shell/package manager khi tránh được (distroless) — trừ khi đội vận hành cần exec vào debug, khi đó ghi rõ trade-off
- `privileged`, mount docker.sock, `network_mode: host` — chỉ khi thật sự cần (tool capture mạng...) và phải ghi lý do ngay trong file
- Compose prod không được tham chiếu image chưa có trong bundle
- Build phải reproducible: cùng commit + cùng lockfile → cùng image
