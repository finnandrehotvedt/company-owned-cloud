FROM python:3.13.7-slim-bookworm@sha256:adafcc17694d715c905b4c7bebd96907a1fd5cf183395f0ebc4d3428bd22d92d

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH=/opt/venv/bin:$PATH

RUN python -m venv /opt/venv
WORKDIR /app
COPY app/requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir --require-hashes -r /app/requirements.lock

RUN useradd --create-home --uid 10001 cloudlab
COPY app/src /app/src
COPY app/entrypoint.sh /app/entrypoint.sh
RUN chmod 0755 /app/entrypoint.sh && mkdir -p /var/log/company-owned-cloud && chown -R cloudlab:cloudlab /app /var/log/company-owned-cloud

USER cloudlab
EXPOSE 8080
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "cloud_demo.main:app", "--host", "0.0.0.0", "--port", "8080", "--no-access-log"]
