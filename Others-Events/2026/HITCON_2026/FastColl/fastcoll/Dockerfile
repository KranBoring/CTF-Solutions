FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && useradd --uid 10001 --create-home --shell /usr/sbin/nologin fastcoll

COPY app.py runner.py /app/
COPY templates /app/templates
COPY static /app/static

USER 10001:10001
EXPOSE 8080
CMD ["gunicorn", "--workers", "1", "--threads", "8", "--timeout", "0", "--bind", "0.0.0.0:8080", "app:app"]
