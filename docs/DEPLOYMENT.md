# Deployment Guide

## Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Click "New app"
4. Select repository, branch, and `app.py`
5. Add secrets:
   ```
   YOUTUBE_API_KEY = "your_key"
   DATABASE_URL = "your_database_url"
   ```
6. Deploy

## Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t youtube-analytics .
docker run -p 8501:8501 youtube-analytics
```

## Heroku Deployment

Create `Procfile`:
```
web: streamlit run app.py --logger.level=error
```

Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku config:set YOUTUBE_API_KEY=your_key
```

## Other Options

- AWS EC2 / Elastic Beanstalk
- Google Cloud Run / App Engine
- DigitalOcean App Platform
- Self-hosted VPS

See documentation for detailed steps.
