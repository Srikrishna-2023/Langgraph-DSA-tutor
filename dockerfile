FROM python:3.11-slim
WORKDIR /app
COPY agents/tempcode.py /app/tempcode.py
CMD ["python", "tempcode.py"]