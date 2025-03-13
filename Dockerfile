# 基础镜像  
FROM python:3.9-slim  
# 工作目录  
WORKDIR /app  
# 复制文件  
COPY . .  
# 安装Edge浏览器  
RUN apt update && apt install -y wget gnupg  
RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | apt-key add -  
RUN echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list  
RUN apt update && apt install -y microsoft-edge-stable  
# 安装依赖  
RUN pip install msedge-selenium-tools selenium==4.9.0  
# 给驱动文件权限  
RUN chmod +x /app/msedgedriver  
# 启动命令  
CMD ["python", "main.py"]