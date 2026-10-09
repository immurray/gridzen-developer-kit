FROM python:3.12-slim@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f
WORKDIR /srv
COPY pyproject.toml README.md LICENSE NOTICE.md ./
COPY skills ./skills
COPY src ./src
RUN pip install --no-cache-dir '.[server]' && useradd --uid 10001 --no-create-home developer && mkdir /metrics && chown 10001:10001 /metrics
USER 10001
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/srv/src
CMD ["uvicorn","gridzen_developer.server:app","--host","0.0.0.0","--port","8030","--no-access-log"]
