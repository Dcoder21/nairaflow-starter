# Deliberately naive. Project 1 task: harden like the API image.
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "worker.py"]
