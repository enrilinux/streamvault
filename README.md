# Streamvault

Streamvault is a Docker app that uses **yt-dlp** for download videos from YouTube and many other platforms.

## How to install:

Use Docker run:

```bash
docker run -d \
  --name streamvault \
  -p 8000:8000 \
  -v ./downloads:/app/downloads \
  enrilinux/streamvault:latest
```

or use Docker Compose:
```yaml
services:
  streamvault:
    image: enrilinux/streamvault:latest
    ports:
      - 8000:8000
    volumes:
      - ./downloads:/app/downloads
```
## Access the Web Interface:
```
http://localhost:8000
```

