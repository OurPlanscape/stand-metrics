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
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "120", "--workers", "2"]
