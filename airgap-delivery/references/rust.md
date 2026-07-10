# Rust / C / C++ — vendor & offline build

## Rust: ưu tiên static binary (musl)

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

Binary musl static chạy trên mọi distro Linux — không lo glibc version trên target.

## Nếu phải build trên target: cargo vendor

```bash
cargo vendor vendor/ > .cargo/config.toml.snippet
# nội dung snippet đưa vào .cargo/config.toml:
# [source.crates-io]
# replace-with = "vendored-sources"
# [source.vendored-sources]
# directory = "vendor"
cargo build --release --offline
```

`--offline` đảm bảo build FAIL thay vì gọi crates.io.

## Kiểm tra

- `cargo audit` (CVE) và `cargo deny check` (license + source) khi còn internet.
- Crate có build.rs tải file từ internet (hiếm nhưng có) — grep `build.rs` cho `http`, `download` trước khi tin vào vendor.

## C/C++

- Vendor source của third-party libs vào repo (submodule pin commit) hoặc bundle tarball + checksum.
- Build trong container cùng distro/glibc với target; ưu tiên link static (`-static` hoặc static libs) khi được.
- Ghi rõ toolchain version (gcc/clang, cmake) vào BUNDLE.md — target phải có sẵn hoặc bundle theo.
