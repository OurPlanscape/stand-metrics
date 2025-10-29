FROM ghcr.io/astral-sh/uv:latest AS builder

FROM ghcr.io/osgeo/gdal:ubuntu-small-latest
COPY --from=builder /uv /uvx /bin/

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV DEBIAN_FRONTEND=noninteractive

ADD . /app
WORKDIR /app
RUN uv sync --locked --no-install-project --dev


EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "--host", "0.0.0.0", "--timeout-keep-alive", "120"]

# TAG = "gcr.io/planscape-23d66/stand-metrics-test"