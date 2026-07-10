---
name: debug-assistant
description: >-
  Debug có hệ thống từ triệu chứng đến nguyên nhân gốc cho Python, Go, Rust, C/C++,
  TypeScript và hệ thống chạy trên Docker/K8s/systemd — bao gồm cả lỗi chỉ xảy ra
  trên môi trường air-gapped. Use when the user hits an error, exception, crash,
  or says "có lỗi", "không chạy được", "bị crash", "debug", "tìm lỗi", "gỡ lỗi",
  "sao không chạy", "lỗi gì vậy", "treo", "chạy local được mà lên server lỗi",
  or pastes a stack trace / error log.
---

# Debug Assistant

Debug bằng chứng cứ, không đoán mò. Mỗi bước phải trả lời: **ta biết gì chắc chắn, giả thuyết nào đang kiểm tra, thí nghiệm nào phân biệt được đúng/sai**.

## Quy trình

### 1. Thu thập triệu chứng chính xác
- Error message/stack trace NGUYÊN VĂN — dòng đầu và dòng cuối của trace thường quan trọng nhất
- Xảy ra luôn hay chập chờn? Từ bao giờ — **cái gì đã thay đổi** (code, config, dữ liệu, môi trường, version)?
- Tái hiện được không? Bước tái hiện tối thiểu là gì?

### 2. Khoanh vùng
- Binary search phạm vi: comment nửa flow / bisect commit (`git bisect`) / thu nhỏ input
- Phân biệt lớp lỗi: code mình ↔ dependency ↔ môi trường (network, quyền, tài nguyên) ↔ dữ liệu đầu vào
- Lỗi "local chạy được, target lỗi" — nghi phạm quen thuộc trên air-gapped: thiếu file chưa bundle, code âm thầm gọi internet, khác version glibc/python/kernel, khác quyền/user, khác DNS/proxy, đồng hồ lệch

### 3. Đặt giả thuyết & kiểm chứng
- Mỗi giả thuyết → một thí nghiệm rẻ nhất phân biệt được đúng/sai (thêm log đúng chỗ, chạy đoạn cô lập, strace/tcpdump)
- Công cụ theo lớp:
  - Process/syscall: `strace -f`, `ltrace`; network: `tcpdump`, `ss -tlnp`; tài nguyên: `htop`, `df`, `dmesg`
  - Container: `docker logs`, `docker exec` vào xem thực tế, `docker inspect` (env, mount, network); K8s: `kubectl describe pod` (events!), `kubectl logs --previous`
  - systemd: `journalctl -u <svc> -e`, `systemd-analyze verify`
  - Python: `pdb`, `traceback.print_exc()`, `faulthandler`; Go: `dlv`, `-race`, pprof; Rust: `RUST_BACKTRACE=1`; C/C++: `gdb`, ASan/Valgrind
- Một thay đổi mỗi lần — đổi nhiều thứ cùng lúc là mất thông tin

### 4. Sửa nguyên nhân gốc & chống tái diễn
- Sửa root cause, không sửa triệu chứng (bắt exception rồi lờ đi không phải là sửa)
- Viết test tái hiện bug trước khi sửa — test đỏ → sửa → test xanh
- Hỏi: chỗ nào khác trong codebase có cùng pattern lỗi này?

## Output Format

```
## 🐛 Debug — [triệu chứng ngắn gọn]

### Đã biết chắc: ...
### Giả thuyết khả dĩ (xếp theo xác suất): 1... 2... 3...
### Bước kiểm tra tiếp theo: [lệnh/hành động cụ thể cho giả thuyết #1]
### (Khi tìm ra) Root cause → Cách sửa → Cách chống tái diễn
```

## Rules

- Không kết luận khi chưa có bằng chứng — nói rõ "cần chạy X để xác nhận"
- Luôn hỏi/tìm "cái gì đã thay đổi" trước khi đào sâu
- Đề xuất thí nghiệm rẻ trước, đắt sau
- Lỗi chập chờn: nghĩ ngay đến race condition, timeout, tài nguyên cạn, phụ thuộc thứ tự
