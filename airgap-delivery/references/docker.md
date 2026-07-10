# Docker / K8s — export & offline load

## Export images (máy có internet)

```bash
# Pin digest, không dùng :latest
docker pull postgres:16.3-alpine
docker save -o images/postgres-16.3-alpine.tar postgres:16.3-alpine

# Nhiều image vào 1 tar cũng được, nhưng tách file dễ checksum/rollback từng phần
```

Multi-arch: `docker pull --platform linux/amd64` đúng arch của target — `docker save` chỉ lưu arch đang pull.

## Load trên target

```bash
docker load -i images/postgres-16.3-alpine.tar
# Nếu có registry nội bộ trong air-gapped:
docker tag postgres:16.3-alpine registry.internal:5000/postgres:16.3-alpine
docker push registry.internal:5000/postgres:16.3-alpine
```

## Chặn Docker/K8s gọi ra ngoài

- Compose/manifest chỉ tham chiếu image local hoặc registry nội bộ — không có tên image trần (docker.io mặc định).
- `imagePullPolicy: IfNotPresent` (K8s) — `Always` sẽ fail hoặc treo trên air-gapped.
- Kiểm tra base image của chính app: `FROM` phải là image đã bundle.
- Helm chart: `helm pull` chart tar về bundle, values trỏ image về registry nội bộ; cấm `helm repo add` trên target.

## Quét trước khi bundle

```bash
trivy image --severity HIGH,CRITICAL postgres:16.3-alpine
syft postgres:16.3-alpine -o cyclonedx-json > sbom/postgres.json
```

Trivy trên target không có DB — nếu cần quét định kỳ trong air-gapped, bundle luôn DB offline: `trivy image --download-db-only` rồi copy `~/.cache/trivy` vào bundle.
