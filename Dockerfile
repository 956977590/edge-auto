FROM python:3.9-slim-buster 
 
WORKDIR /app 
 
COPY . .
 
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*
 
# 安装Python依赖 
RUN pip install --no-cache-dir selenium 
 
# 设置驱动权限 
RUN chmod +x /app/msedgedriver 
 
CMD ["python", "main.py"]
