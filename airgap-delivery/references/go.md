# Go — vendor & offline build

## Cách ưu tiên: build static binary trước, chỉ chuyển binary

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -trimpath \
  -ldflags="-s -w -X main.version=$(git describe --tags)" -o dist/app ./cmd/app
```

Static binary không phụ thuộc glibc/libs trên target — đây là lợi thế lớn nhất của Go cho air-gapped. Chỉ cần copy binary + config.

## Nếu phải build trên target: vendor modules

```bash
go mod tidy && go mod vendor      # tạo thư mục vendor/ chứa toàn bộ source deps
# build trên target:
GOFLAGS=-mod=vendor GOPROXY=off go build ./...
```

`GOPROXY=off` đảm bảo build FAIL thay vì âm thầm gọi proxy.golang.org.

## Kiểm tra & bẫy thường gặp

- `govulncheck ./...` — quét CVE khi còn internet.
- CGO: nếu dùng sqlite3, pcap... (`CGO_ENABLED=1`) thì binary phụ thuộc glibc target — build trong container cùng distro với target, hoặc dùng bản thay thế pure-Go (modernc.org/sqlite).
- Timestamp/version check: một số lib tự gọi API check update — grep trước khi bundle.
- Cross-compile arm64 cho thiết bị edge: `GOARCH=arm64`, nhớ test trên đúng arch.
