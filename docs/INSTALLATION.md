# Installation & Setup Guide

## Requirements
- Python 3.8+
- PostgreSQL 10+
- 2GB RAM, 1GB disk space

## Step-by-Step Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable YouTube Data API v3
4. Create API Key credentials
5. Copy key to `.env` file

### 3. Configure Database
```bash
# Create database
createdb youtube_db

# Edit youtube_analytics/config.py with your credentials
DB_URL = "postgresql://username:password@localhost:5432/youtube_db"
```

### 4. Create .env File
```
YOUTUBE_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/youtube_db
```

### 5. Run Application
```bash
streamlit run app.py
```

## Troubleshooting

**API Key Error**  
→ Check `.env` file exists and has correct key

**Database Connection Error**  
→ Verify PostgreSQL running: `psql -U postgres`

**Module Not Found**  
→ Install requirements: `pip install -r requirements.txt`

**Port Already in Use**  
→ Use different port: `streamlit run app.py --server.port 8502`
