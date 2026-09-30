FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pycryptodome
COPY plonk_engine.py hw_model.cpython-311-x86_64-linux-gnu.so hsm_main.py /app/
EXPOSE 1337
CMD ["python", "hsm_main.py"]
