# QUICK START GUIDE

## 🚀 5-Minute Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Setup API Key
- Get key from: https://console.cloud.google.com/
- Add to `.env`:
```
YOUTUBE_API_KEY=your_key_here
```

### 3. Setup Database
```bash
# Create database
createdb youtube_db

# Update config.py with your credentials:
DB_URL = "postgresql://postgres:password@localhost:5432/youtube_db"
```

### 4. Run Application
```bash
streamlit run app.py
```

### 5. Start Using!
- Open http://localhost:8501
- Go to "Fetch Data" tab
- Enter a channel ID or name
- View analytics in "Dashboard" tab

---

## 📱 Tab Guide

### 📥 Fetch Data
- Fetch channels by ID, username, or name
- Fetch videos by ID or title
- Save data to database

### 📊 Dashboard
- View channel statistics
- See video performance charts
- View engagement metrics
- Track channel growth

### 📈 Analysis
- Single channel detailed analysis
- Multi-channel comparison
- Engagement rates breakdown
- Video performance table

### 💾 Manage Data
- View all stored channels
- See video counts
- Delete channels
- Manage database

### ❓ Guide
- In-app help and documentation
- API key setup instructions
- Database configuration guide

---

## 💡 Pro Tips

1. **Find Channel ID**: Go to channel → Share → Copy URL → Extract ID
   - URL format: youtube.com/channel/CHANNEL_ID

2. **API Key Limits**: 10,000 requests/day (free tier)

3. **Database Tips**:
   - Backup data regularly
   - Use indexes for faster queries

4. **Performance**:
   - Cache results locally
   - Batch multiple requests
   - Use pagination for large datasets

---

## 🔗 Useful Links

- [YouTube Data API v3 Docs](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Plotly Charts](https://plotly.com/python/)

---

## 🆘 Common Issues

### "YOUTUBE_API_KEY not found"
→ Add YOUTUBE_API_KEY to .env file

### "could not connect to server"
→ PostgreSQL not running. Start it:
- Windows: `pg_ctl start`
- Mac: `brew services start postgresql`
- Linux: `sudo systemctl start postgresql`

### "Address already in use"
→ Use different port:
```bash
streamlit run app.py --server.port 8502
```

### "Module not found"
→ Install requirements:
```bash
pip install -r requirements.txt
```

---

## 📊 Example API Calls

### Fetch Channel
```python
from youtube_fetcher import YouTubeFetcher
fetcher = YouTubeFetcher()

# By ID
data = fetcher.get_channel_by_id("UCkRfArvrzheW2E7b6SVV7vA")

# By username
data = fetcher.get_channel_by_username("GoogleDevelopers")

# By name
data = fetcher.get_channel_by_name("Google Developers")
```

### Fetch Video
```python
# By ID
video = fetcher.get_video_by_id("dQw4w9WgXcQ")

# By title
video = fetcher.get_video_by_title("Python Tutorial")

# By title in channel
video = fetcher.get_video_by_title("Python", channel_id="UCkRfArvrzheW2E7b6SVV7vA")
```

### Database Operations
```python
from database import DatabaseManager
db = DatabaseManager()

# Save
db.add_channel(channel_data)
db.add_video(video_data)

# Retrieve
channel = db.get_channel("channel_id")
videos = db.get_channel_videos("channel_id")
stats = db.get_statistics("channel_id")

# Delete
db.delete_channel("channel_id")
```

---

## 📈 Features at a Glance

✅ Fetch YouTube data in real-time
✅ Store data in PostgreSQL database
✅ Interactive Streamlit dashboard
✅ Advanced visualizations with Plotly
✅ Multi-channel comparison
✅ Engagement analytics
✅ Video performance tracking
✅ Data management interface
✅ Comprehensive documentation
✅ Easy setup and deployment

---

**Questions?** Check README.md or INSTALLATION.md for detailed information.
