# 使用官方 Python 基礎映像
FROM python:3.11.2

# 設置工作目錄
WORKDIR /app

# 將當前目錄下的文件添加到工作目錄
ADD . /app

# 安裝 C++ 編譯環境
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential g++

# 安裝 Python 依賴
RUN pip install -r requirements.txt

# 設置容器啟動時執行的命令
CMD ["python", "server.py"]