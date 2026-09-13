FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY company_v2 ./company_v2
COPY config ./config
COPY scripts ./scripts
RUN pip install --no-cache-dir .
RUN mkdir -p /app/var
CMD ["python", "scripts/run_api.py"]
