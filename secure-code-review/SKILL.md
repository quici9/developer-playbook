---
name: secure-code-review
description: >-
  Code review với lăng kính security-first cho Python, Go, Rust, C/C++, TypeScript:
  logic, xử lý input hostile, memory safety, concurrency, hiệu năng, maintainability.
  Use when the user says "review code này", "kiểm tra code", "xem lại code", "check
  logic", "có vấn đề gì không", "có lỗi gì không", "xem diff này", or shares code/diff
  asking for feedback. (Đây là review thủ công theo checklist riêng — built-in
  /code-review dùng cho review cả branch/PR.)
---

# Secure Code Review

Review theo thứ tự ưu tiên dưới đây. Bối cảnh mặc định: code sẽ chạy trong hệ thống phục vụ đội an ninh mạng, thường xuyên **xử lý dữ liệu hostile** (log từ máy nhiễm, sample, pcap, input từ mạng) — nên security và robustness xếp trên style.

## Checklist theo thứ tự

### 1. Hiểu ngữ cảnh trước khi phán
- Ngôn ngữ, framework, mục đích của đoạn code; input/output contract
- Dữ liệu đi vào từ đâu — nguồn nào là untrusted?

### 2. Đúng logic
- Edge cases: null/None/nil, rỗng, 0, số âm, unicode, quá dài
- Điều kiện biên vòng lặp, off-by-one
- Async/concurrency: race condition, deadlock, promise/goroutine leak, dùng chung state không lock
- Error handling: lỗi bị nuốt? error path có cleanup tài nguyên (defer/finally/context manager)?

### 3. Security (trọng số cao nhất)
- Input untrusted đi thẳng vào: SQL/command/path/regex (ReDoS)/deserialize? → HIGH
- Parser dữ liệu ngoài: giới hạn size, độ sâu đệ quy, timeout? Zip bomb, XML bomb, path traversal trong archive?
- AuthZ: endpoint/handler mới có kiểm tra quyền không, hay chỉ authn?
- Secret hardcode, log ra secret/PII
- **C/C++**: buffer bound, integer overflow trước khi malloc/index, use-after-free, format string
- **Rust**: block `unsafe` có invariant ghi rõ không; `unwrap()`/`expect()` trên input ngoài
- **Go**: lỗi bị bỏ qua (`_ = err`), goroutine không có cách dừng, `defer` trong vòng lặp
- **Python**: `pickle`/`yaml.load` trên dữ liệu ngoài, `shell=True`, mutable default arg
- **TS/JS**: `any` che lỗi, prototype pollution, thiếu validate ở server (chỉ validate client)

### 4. Hiệu năng
- N+1 query, IO trong vòng lặp, đọc cả file lớn vào RAM khi có thể stream
- Cấu trúc dữ liệu sai (list scan thay vì set/map), regex compile trong loop
- Với tool xử lý dữ liệu lớn (log/pcap): độ phức tạp thuật toán theo kích thước input là bao nhiêu?

### 5. Maintainability
- Tên rõ nghĩa, hàm một việc, không lặp code đã có sẵn trong codebase
- Magic number/string cần đặt tên; comment giải thích "tại sao" chứ không "cái gì"

## Output Format

```
## 🔍 Code Review — [file/diff]

### ⚠️ Phát hiện
1. **[HIGH] Security** — mô tả vấn đề (file:line)
   → Cách sửa cụ thể (kèm code nếu ngắn)
2. **[MED] Logic** — ...
3. **[LOW] Style** — ...

### ✅ Điểm tốt (ngắn gọn, thật sự đáng khen mới ghi)
### 📋 Kết luận: [Merge được / Sửa HIGH trước / Cần bàn thêm]
```

## Rules

- Mỗi finding phải chỉ đúng file:line và kèm cách sửa — không phán chung chung
- Code tốt thì nói thẳng "không có vấn đề HIGH/MED" — không bới lông tìm vết cho có
- Không đề xuất refactor lớn ngoài phạm vi diff trừ khi thấy lỗi nghiêm trọng
- Nghi ngờ có lỗ hổng nhưng chưa chắc: ghi rõ là "nghi ngờ, cần xác minh" kèm cách xác minh
