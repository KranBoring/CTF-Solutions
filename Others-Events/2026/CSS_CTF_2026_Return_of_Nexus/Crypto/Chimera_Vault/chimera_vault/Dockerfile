FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pycryptodome

RUN useradd -m -u 1001 -s /bin/bash ctfuser
WORKDIR /home/ctfuser

COPY server.py /home/ctfuser/server.py
RUN chmod 755 /home/ctfuser/server.py

USER ctfuser
EXPOSE 7867

CMD ["socat", "-T45", "TCP-LISTEN:7867,reuseaddr,fork", "EXEC:python3 -u /home/ctfuser/server.py,stderr"]