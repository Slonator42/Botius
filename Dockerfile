FROM python:3.12-slim

RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYDEVD_DISABLE_FILE_VALIDATION=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY ./src /app/src

EXPOSE 8000

CMD ["python", "src/main.py"]