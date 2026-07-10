---
name: model-evaluation
description: >-
  Đánh giá model ML nghiêm ngặt và tối ưu hyperparameter: chọn metric đúng cho bài
  toán (đặc biệt imbalanced như detection), cross-validation, so sánh có ý nghĩa
  thống kê, phân tích lỗi, tuning bằng Optuna. Use when the user says "đánh giá model",
  "model performance", "accuracy bao nhiêu", "precision recall", "model có tốt không",
  "tune hyperparameters", "tối ưu model", "Optuna", "grid search", "so sánh hai model",
  "false positive nhiều quá", or after training any model.
---

# Model Evaluation & Tuning

Bài toán điển hình ở đây (detection, phân loại alert, anomaly) hầu như luôn **imbalanced nặng** và **chi phí lỗi bất đối xứng** — một câu "accuracy 99%" thường vô nghĩa. Đánh giá phải trả lời: model này đưa vào vận hành thì đội blue team được gì, chịu gì.

## 1. Chọn metric theo chi phí lỗi thật

- Imbalanced: quên accuracy — dùng precision/recall/F1 theo class, PR-AUC (không phải ROC-AUC, ROC nhìn đẹp giả tạo khi negative áp đảo)
- Dịch metric ra ngôn ngữ vận hành: precision 90% @ 1000 alerts/ngày = **100 false positive/ngày cho analyst xử lý** — con số đó mới là thứ để quyết định
- Chọn ngưỡng (threshold) là quyết định nghiệp vụ: vẽ precision-recall theo threshold, chọn cùng người dùng cuối theo sức chịu FP/FN của họ, ghi lại lý do
- Anomaly detection không nhãn: đánh giá bằng tập nhãn tay nhỏ + review top-K score với analyst — đừng tin silhouette score suông

## 2. Đánh giá đúng cách

- Test set **theo thời gian** (train quá khứ → test tương lai) cho dữ liệu event/log; giữ test set thiêng liêng — chỉ chạm khi kết luận cuối
- Cross-validation: `StratifiedKFold` cho imbalanced, `TimeSeriesSplit` cho temporal; báo mean ± std, không báo một con số
- So sánh 2 model: khác biệt phải lớn hơn std giữa các fold; nếu sát nhau, kiểm định (paired t-test/McNemar) hoặc thừa nhận "tương đương — chọn cái đơn giản hơn"
- **Phân tích lỗi thủ công**: xem 20-50 case sai tệ nhất — thường lộ ra lỗi nhãn, feature leak, hoặc một segment dữ liệu model mù hoàn toàn; đây là bước giá trị nhất và hay bị bỏ qua
- Slice theo segment (nguồn log, loại thiết bị, khoảng thời gian): metric tổng che được model tệ ở một segment quan trọng

## 3. Hyperparameter tuning

- Thứ tự đầu tư: thêm/sửa feature và dữ liệu sạch hơn > đổi model > tune HP — tune chỉ vắt nốt vài % cuối
- Optuna là mặc định (self-hosted, storage sqlite/postgres nội bộ): sampler TPE, pruner Median, `n_trials` 50-200 tùy chi phí train
- Tune trên **validation qua CV**, không tune trên test set; search space log-scale cho learning rate/regularization
- Nghi overfit validation khi tune dài: kiểm tra best trial trên test một lần cuối cùng — chênh nhiều là đã overfit vào validation
- Ghi mọi trial vào MLflow/Optuna storage (xem skill ml-pipeline) — best params kèm bối cảnh dữ liệu nào

## Output Format

```
## 📊 Đánh giá — [model] trên [dataset, khoảng thời gian]

### Bảng metric (mean ± std qua CV, và trên test cuối)
| Model | Precision | Recall | F1 | PR-AUC | FP/ngày ước tính |

### Threshold đề xuất + lý do nghiệp vụ
### Phân tích lỗi: pattern sai chính (kèm ví dụ)
### Slice yếu cần lưu ý
### Kết luận: dùng được chưa / cần gì thêm
```

## Rules

- Không bao giờ báo mỗi accuracy cho bài toán imbalanced — luôn kèm confusion matrix và metric theo class
- Mọi cải thiện phải kiểm chứng trên test set chưa từng chạm, cùng split — so sánh khác split là vô nghĩa
- Kết quả "quá đẹp" (F1 > 0.98) → nghi leak trước khi mừng: kiểm tra feature có chứa thông tin tương lai/nhãn không
- Kết luận phải kèm khuyến nghị vận hành cụ thể (ngưỡng, khối lượng alert dự kiến, dấu hiệu cần retrain)
