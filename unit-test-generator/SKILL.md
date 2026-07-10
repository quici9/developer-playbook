---
name: unit-test-generator
description: >-
  Sinh unit test đầy đủ happy path, edge case và error case cho Python (pytest),
  Go (testing), Rust (cargo test), TypeScript (vitest/jest) — chú trọng test parser
  và code xử lý input hostile. Use when the user says "viết test", "thêm test",
  "generate tests", "test hàm này", "coverage", "test case nào cần có", "viết unit
  test", or after implementing new logic that lacks tests.
---

# Unit Test Generator

Test tốt kiểm tra **hành vi qua public API**, không kiểm tra chi tiết cài đặt. Mỗi test một hành vi, tên test đọc lên hiểu ngay hành vi gì đang được đảm bảo.

## Quy trình

1. Đọc hàm/module → xác định contract: input hợp lệ là gì, output cam kết gì, lỗi nào được ném ra
2. Lập danh sách case theo 3 nhóm trước khi viết code test:
   - **Happy path**: 1-2 case tiêu biểu
   - **Edge**: rỗng, null/None/nil, 0, âm, giá trị biên (min/max), unicode, trùng lặp, đã tồn tại
   - **Error**: input sai kiểu/sai format, dependency fail (IO, network, db), timeout
3. Code xử lý dữ liệu ngoài (parser log/file/network) thêm nhóm **hostile**: input cắt cụt, header giả, size khai láo, đệ quy sâu, bytes rác — parser phải trả lỗi sạch, không crash/treo
4. Viết test theo Arrange-Act-Assert, mỗi test độc lập, không phụ thuộc thứ tự chạy

## Theo ngôn ngữ

**Python (pytest)**: `@pytest.mark.parametrize` cho bảng case; `pytest.raises(SpecificError)` — không bắt `Exception` trần; fixture cho setup lặp lại; mock ở ranh giới IO (`monkeypatch`, `unittest.mock`) — không mock hàm nội bộ của chính module đang test.

**Go**: table-driven test là mặc định; `t.Run(tc.name, ...)` cho subtests; `t.Parallel()` khi độc lập; kiểm tra error bằng `errors.Is/As`, không so sánh string; fuzz test (`go test -fuzz`) cho parser.

**Rust**: `#[cfg(test)] mod tests` cùng file; `#[should_panic(expected=...)]` dùng dè — ưu tiên assert trên `Result`; proptest/quickcheck cho hàm thuần túy; test `unsafe` code với Miri nếu có.

**TypeScript (vitest/jest)**: `test.each` cho bảng case; test async bằng `await expect(...).rejects.toThrow(...)`; mock module ranh giới (`vi.mock`) — tối thiểu hóa mock.

## Output Format

Trước khi viết code test, liệt kê bảng case:

```
| # | Nhóm | Case | Kỳ vọng |
|---|------|------|---------|
```

Sau đó code test hoàn chỉnh chạy được ngay + lệnh chạy (`pytest path -v`, `go test ./... -run X`).

## Rules

- Test phải chạy được ngay — đúng import, đúng đường dẫn, đúng framework dự án đang dùng (kiểm tra trước)
- Không viết test khẳng định điều vô nghĩa (assert mock được gọi mà không kiểm tra hành vi)
- Mock tối thiểu, chỉ ở ranh giới IO; test cần db/service thật thì nói rõ đó là integration test
- Nếu code khó test (hàm làm quá nhiều việc, IO trộn logic) → đề xuất tách nhỏ trước, kèm cách tách
- Chạy được test thì chạy và báo kết quả thật, không chỉ đưa code
