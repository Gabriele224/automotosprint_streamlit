FROM python:3.10-slim

WORKDIR  /app

RUN apt-get update && apt-get install -y \
build-essential \
curl \
software-properties-common \
git \
&& rm -rf /var/lib/apt/lists/*

RUN git clone
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit","run","main.py"]