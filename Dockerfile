FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg curl

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

RUN curl -fsSL https://deno.land/install.sh | sh \
    && mv /root/.deno/bin/deno /usr/local/bin/deno

COPY app ./app
RUN mkdir downloads

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
