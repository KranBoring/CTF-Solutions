FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && pip install --no-cache-dir pycryptodome \
    && git clone https://github.com/awnonbhowmik/Dragon-Crypto.git /opt/dragon-crypto \
    && cd /opt/dragon-crypto \
    && git checkout 046ad8d \
    && rm -rf /var/lib/apt/lists/*

COPY patch.py /tmp/patch.py
RUN python /tmp/patch.py

WORKDIR /app
COPY chall.py .

CMD ["python", "chall.py"]
