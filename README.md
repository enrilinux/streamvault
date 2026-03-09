# Streamvault

Streamvault is a Docker app that uses **yt-dlp** for download videos from **YouTube** and **many other platforms**.

## How to install:

Use Docker run:

```bash
docker run -d \
  --name webdlp \
  -p 8000:8000 \
  -v ./downloads:/app/downloads \
  enrilinux/webdlp:latest
```

or use Docker Compose:
```yaml
services:
  webdlp:
    image: enrilinux/webdlp:latest
    ports:
      - 8000:8000
    volumes:
      - ./downloads:/app/downloads
```
## Access the Web Interface:
```
http://localhost:8000
```

