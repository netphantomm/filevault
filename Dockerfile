FROM python:3.14-slim
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py test_filevault.py ./
COPY public/readme.txt ./public/
COPY private/demo-secret.txt ./private/

CMD ["python", "test_filevault.py"]
