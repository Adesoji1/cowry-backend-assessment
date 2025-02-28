FROM python:3.11-slim

WORKDIR /usr/src/app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . /usr/src/app/frontend_service

EXPOSE 8001

CMD ["uvicorn", "frontend_service.main:app", "--host", "0.0.0.0", "--port", "8001"]



