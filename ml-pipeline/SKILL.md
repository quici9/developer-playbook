---
name: ml-pipeline
description: >-
  Xây pipeline ML/data chạy offline: tiền xử lý dữ liệu (pandas/polars), feature
  engineering, training pipeline tái lập được, experiment tracking bằng MLflow
  self-hosted, đóng gói model để deploy air-gapped không tải gì lúc runtime.
  Use when the user says "ML pipeline", "tiền xử lý dữ liệu", "preprocess", "làm sạch
  data", "feature engineering", "training pipeline", "MLflow", "track experiment",
  "ETL", "data pipeline", "deploy model", or when building ML for detection/analysis tools.
---

# ML Pipeline (offline / self-hosted)

ML trong bối cảnh này thường là: phân loại/scoring trên log, phát hiện bất thường, hỗ trợ triage — dữ liệu nhạy cảm không rời mạng nội bộ, model phải **deploy air-gapped và không tải gì lúc runtime**. Toàn bộ chuỗi: dữ liệu → tiền xử lý → train → track → đóng gói → serve.

## 1. Tiền xử lý dữ liệu

- Khám phá trước khi xử lý: shape, dtypes, missing %, phân bố, cardinality — quyết định dựa trên số liệu in ra, không đoán
- Missing: hiểu **vì sao** thiếu trước khi chọn impute/drop (thiếu do sensor chết khác thiếu ngẫu nhiên); log số dòng bị ảnh hưởng ở từng bước
- Mọi transform (scaler, encoder, vocab) **fit trên train, apply trên test** — leak qua preprocessing là lỗi phổ biến nhất; gói vào `sklearn.Pipeline`/`ColumnTransformer` để serialize cùng model
- Dữ liệu log/security: cẩn thận high-cardinality (IP, hostname, hash) — hashing trick/frequency encoding thay vì one-hot nổ chiều; timestamp tách thành feature chu kỳ (giờ, thứ) khi hành vi theo lịch
- Polars thay pandas khi dữ liệu > vài GB; đọc streaming/chunked, đừng nuốt cả file

## 2. Pipeline train tái lập được

- Cấu trúc: `data/` (raw bất biến → processed) / `src/` (code từng bước) / `configs/` (YAML: params, path, seed) / `artifacts/`
- Mỗi bước là hàm/CLI chạy riêng được: `prepare → featurize → train → evaluate` — orchestrate bằng Makefile/script trước, chỉ lên Airflow/Prefect khi thật sự cần schedule phức tạp
- Seed cố định mọi nguồn ngẫu nhiên; version dữ liệu bằng hash/snapshot path ghi vào run
- Split theo **thời gian** cho dữ liệu event/log (train quá khứ, test tương lai) — random split trên time-series là tự dối mình

## 3. Experiment tracking — MLflow self-hosted

- MLflow server chạy nội bộ (docker, backend postgres + artifact store local/MinIO) — không W&B/SaaS
- Log mỗi run: params (từ config), metrics, artifact (model, confusion matrix, feature list), git commit, hash dữ liệu
- Model registry của MLflow để đánh dấu bản nào đang production; so sánh run trong UI thay vì file Excel

## 4. Đóng gói & serve trên air-gapped

- Model + preprocessing pipeline serialize thành **một** artifact (sklearn Pipeline / `mlflow.pyfunc`) — không tách rời kẻo lệch version transform
- Deploy: FastAPI service đơn giản load model local là đủ cho đa số; batch scoring bằng CLI cho pipeline định kỳ
- `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`; weights/tokenizer bundle sẵn (xem skill airgap-delivery); pin version sklearn/torch — model pickle lệch version là vỡ
- Ghi vào tài liệu bàn giao: input schema, output nghĩa là gì, ngưỡng quyết định, giới hạn đã biết, và **khi nào cần retrain** (dấu hiệu drift: phân bố input lệch, precision giảm trên nhãn mới)

## Rules

- Baseline đơn giản trước (rule/logistic/tree) — deep learning phải thắng baseline rõ ràng mới đáng chi phí vận hành
- Không có bước nào của pipeline được gọi internet lúc chạy trên target
- Mọi kết quả phải kèm: dữ liệu nào (hash/ngày), config nào, commit nào — không tái lập được thì không tin được
- Đo hiệu năng inference (latency, RAM) trên cấu hình tương đương target trước khi hứa
