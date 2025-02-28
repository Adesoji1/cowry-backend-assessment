FROM python:3.11-slim

WORKDIR /usr/src/app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY  root.crt /usr/src/app/certs/root.crt


COPY . /usr/src/app/admin_service



EXPOSE 8000


CMD ["uvicorn", "admin_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
