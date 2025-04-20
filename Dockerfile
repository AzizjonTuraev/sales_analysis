FROM python:3.11.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY server/ ./server/
COPY model/products_df ./model/products_df

RUN pip install --no-cache-dir -r server/requirements.txt
EXPOSE 8000
CMD ["python", "server/server_api.py"]
# CMD ["uvicorn", "server.server_api:app", "--host", "0.0.0.0", "--port", "8000"]

### docker execution
# docker build -t sales_project .
# docker run -p 8000:8000 sales_project