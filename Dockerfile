FROM ghcr.io/astral-sh/uv:latest AS builder

FROM ghcr.io/osgeo/gdal:ubuntu-small-latest
COPY --from=builder /uv /uvx /bin/

ARG ENV=dev
ARG OTEL_ENDPOINT="http://localhost/:4317"
ARG OTEL_KEY="foo-bar"

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV DEBIAN_FRONTEND=noninteractive

ADD . /app
WORKDIR /app
RUN uv sync --locked --no-install-project --dev
RUN uv run opentelemetry-bootstrap --action=install

ENV OTEL_RESOURCE_ATTRIBUTES=service.name=stand-metrics-${ENV}
ENV OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_ENDPOINT}
ENV OTEL_EXPORTER_OTLP_HEADERS=signoz-ingestion-key=${OTEL_KEY}
ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc

EXPOSE 8000
CMD ["uv", "run", "opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "120", "--workers", "2"]
