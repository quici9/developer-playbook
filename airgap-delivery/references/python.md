# Python — vendor & offline install

## Vendor dependencies (trên máy có internet)

```bash
# Pin toàn bộ (kể cả transitive) trước
pip freeze > requirements.lock          # hoặc: uv pip compile pyproject.toml -o requirements.lock

# Tải wheel cho ĐÚNG platform/python của target (quan trọng!)
pip download -r requirements.lock -d vendor/wheels/ \
  --platform manylinux2014_x86_64 --python-version 3.11 --only-binary=:all:
```

- Nếu có package chỉ có sdist (phải build): build wheel sẵn trên máy dev cùng arch/glibc, hoặc dùng container giống target để build.
- `uv` nhanh hơn và lock tốt hơn pip — nếu dự án dùng uv: `uv export --frozen -o requirements.lock`.

## Cài trên target (không internet)

```bash
pip install --no-index --find-links=vendor/wheels/ -r requirements.lock
```

Cấu hình chặn pip gọi ra ngoài (đặt trong install.sh hoặc pip.conf trên target):

```ini
# /etc/pip.conf
[global]
no-index = true
find-links = /opt/bundle/vendor/wheels
```

## Bẫy thường gặp

- Wheel sai platform/glibc → lỗi lúc cài trên target. Luôn chỉ định `--platform` + `--python-version`.
- Package có C extension (numpy, cryptography, psycopg2): bắt buộc `--only-binary=:all:` hoặc build sẵn.
- ML: `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`; tải model bằng `huggingface-cli download` khi còn internet, bundle vào `artifacts/models/`.
- Đơn giản nhất khi có thể: đóng app vào Docker image — mọi deps nằm trong image, không cần vendor wheels.
