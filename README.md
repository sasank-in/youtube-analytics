# YouTube Analytics Platform 📊

A comprehensive Streamlit web application that enables users to efficiently extract, store, and analyze YouTube channel and video data with advanced visualizations and insights.

## 🎯 Features

### Data Extraction
- **Multiple Fetch Methods**: Fetch channels by ID, username, or name search
- **Video Analytics**: Retrieve video data by ID or title
- **Real-time Data**: Access current YouTube statistics via official YouTube Data API v3

### Data Storage
- **SQL Database Integration**: Persistent storage using PostgreSQL and SQLAlchemy
- **Automatic Updates**: Smart save/update mechanism to prevent duplicates
- **Relationships**: Structured data relationships between channels and videos

### Analytics & Visualization
- **Channel Metrics**: Subscribers, total views, video count, engagement rates
- **Video Performance**: Views, likes, comments tracking with top video identification
- **Engagement Analysis**: Like rates, comment rates, and engagement trends
- **Distribution Analysis**: View distribution across all videos
- **Multi-Channel Comparison**: Compare statistics across multiple channels

### Interactive Dashboard
- **Real-time Updates**: Fetch and view data instantly
- **Interactive Charts**: Plotly-powered visualizations with hover details
- **Data Management**: View, update, and delete stored channels
- **Responsive UI**: Works seamlessly on desktop and mobile

## 📋 Project Structure

```
yout-analytics/
├── app.py                 # Main Streamlit application
├── youtube_fetcher.py     # YouTube API wrapper and data fetcher
├── database.py            # SQLAlchemy models and database operations
├── visualizations.py      # Chart and visualization generation
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API key)
└── venv/                  # Virtual environment
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database running
- YouTube Data API v3 credentials

### 1. Clone/Setup Project
```bash
cd yout-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create/Edit `.env` file:
```env
YOUTUBE_API_KEY=your_actual_api_key_here
```

Update `config.py` with your database URL:
```python
DB_URL = "postgresql://username:password@localhost:5432/youtube_db"
```

### 4. Create PostgreSQL Database
```bash
createdb youtube_db
```

### 5. Run the Application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🔑 Getting YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**:
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create credentials (API Key):
   - Click "Create Credentials"
   - Select "API Key"
   - Copy the key to your `.env` file

## 📖 Usage Guide

### Fetching Channel Data

**Method 1: By Channel ID**
```python
from youtube_fetcher import YouTubeFetcher
fetcher = YouTubeFetcher()
data = fetcher.get_channel_by_id("UCkRfArvrzheW2E7b6SVV7vA")
```

**Method 2: By Username**
```python
data = fetcher.get_channel_by_username("GoogleDevelopers")
```

**Method 3: By Channel Name (Search)**
```python
data = fetcher.get_channel_by_name("Google Developers")
```

### Fetching Video Data

**Method 1: By Video ID**
```python
video_data = fetcher.get_video_by_id("dQw4w9WgXcQ")
```

**Method 2: By Title (with optional channel filter)**
```python
# Search all videos
video_data = fetcher.get_video_by_title("Python Tutorial")

# Search within specific channel
video_data = fetcher.get_video_by_title("Python", channel_id="UCkRfArvrzheW2E7b6SVV7vA")
```

### Database Operations

```python
from database import DatabaseManager

db = DatabaseManager()

# Save channel
db.add_channel(channel_data)

# Save video
db.add_video(video_data)

# Retrieve channel
channel = db.get_channel("channel_id")

# Get channel videos
videos = db.get_channel_videos("channel_id")

# Get statistics
stats = db.get_statistics("channel_id")

# Delete channel
db.delete_channel("channel_id")
```

### Creating Visualizations

```python
from visualizations import YouTubeVisualizer

viz = YouTubeVisualizer()

# Video performance chart
fig = viz.create_video_performance_chart("channel_id")

# Engagement analysis
fig = viz.create_engagement_ratio_chart("channel_id")

# Views distribution
fig = viz.create_views_distribution_chart("channel_id")

# Multi-channel comparison
fig = viz.create_comparison_chart(["channel_id_1", "channel_id_2"])
```

## 📊 Available Data Fields

### Channel Data
- `channel_id`: Unique YouTube channel identifier
- `title`: Channel name
- `description`: Channel description
- `custom_url`: Custom URL (if available)
- `published_at`: Channel creation date
- `subscribers`: Subscriber count
- `total_views`: Total channel views
- `total_videos`: Total video count
- `profile_image`: Channel thumbnail URL
- `banner_image`: Channel banner URL
- `fetched_at`: Last update timestamp

### Video Data
- `video_id`: Unique video identifier
- `channel_id`: Associated channel ID
- `title`: Video title
- `description`: Video description
- `published_at`: Video publication date
- `duration`: Video duration (ISO 8601 format)
- `views`: View count
- `likes`: Like count
- `comments`: Comment count
- `thumbnail`: Thumbnail image URL
- `fetched_at`: Last update timestamp

## 📈 Analytics Features

### Dashboard Features
- **Channel Overview**: Quick metrics for subscribers, views, and videos
- **Performance Charts**: Top 10 videos by views
- **Engagement Metrics**: Like and comment rates visualization
- **View Distribution**: Histogram of video views

### Analysis Features
- **Single Channel Analysis**: Detailed statistics and video breakdown
- **Multi-Channel Comparison**: Side-by-side channel metrics
- **Engagement Rates**: Calculate and visualize engagement percentages
- **Video Performance Table**: Sortable table of all videos

## 🔒 Security Considerations

1. **API Key**: Never commit `.env` file with real API key
2. **Database Credentials**: Store database credentials securely
3. **Rate Limiting**: Respects YouTube API rate limits
4. **Data Privacy**: Respects YouTube's terms of service

## ⚙️ Configuration

### config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DB_URL = "postgresql://username:password@localhost:5432/youtube_db"
```

### .env
```env
YOUTUBE_API_KEY=your_api_key_here
```

## 📊 Database Schema

### channels table
```sql
CREATE TABLE channels (
    channel_id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    custom_url VARCHAR(255),
    published_at DATETIME,
    subscribers VARCHAR(50),
    total_views VARCHAR(50),
    total_videos VARCHAR(50),
    profile_image VARCHAR(500),
    banner_image VARCHAR(500),
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### videos table
```sql
CREATE TABLE videos (
    video_id VARCHAR(100) PRIMARY KEY,
    channel_id VARCHAR(100) NOT NULL FOREIGN KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    published_at DATETIME,
    duration VARCHAR(50),
    views VARCHAR(50),
    likes VARCHAR(50),
    comments VARCHAR(50),
    thumbnail VARCHAR(500),
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing

### Manual Testing
1. Run the Streamlit app
2. Test each tab functionality
3. Verify data is saved to database
4. Check visualizations load correctly

### API Testing
```bash
python api_key_test.py
```

## 🐛 Troubleshooting

### API Key Errors
- Verify API key is enabled for YouTube Data API v3
- Check `.env` file has correct key
- Ensure key has no extra spaces

### Database Errors
- Verify PostgreSQL is running
- Check database credentials in config.py
- Ensure database exists: `createdb youtube_db`

### Streamlit Issues
- Clear cache: `streamlit cache clear`
- Restart server: `Ctrl+C` then `streamlit run app.py`

## 📚 Technologies Used

- **Streamlit**: Web application framework
- **YouTube Data API v3**: Official YouTube data source
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Data storage
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Google API Client**: YouTube API wrapper

## 🎯 Use Cases

1. **Content Creators**: Track channel growth and video performance
2. **Marketers**: Analyze competitor channels and engagement strategies
3. **Analysts**: Generate insights and reports on YouTube trends
4. **Researchers**: Collect data for academic studies
5. **Agencies**: Manage multiple client channels

## 📈 Future Enhancements

- [ ] Playlist analytics
- [ ] Comment sentiment analysis
- [ ] Subscriber growth trending
- [ ] Video recommendation engine
- [ ] Automated report generation
- [ ] Email notifications
- [ ] Advanced ML predictions
- [ ] Real-time data sync

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues or questions:
1. Check the User Guide in the app
2. Review this documentation
3. Check YouTube API documentation
4. Report bugs with detailed description

## 🙏 Acknowledgments

- YouTube Data API v3 documentation
- Streamlit community
- SQLAlchemy ORM framework
- Plotly visualization library

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Active Development
# youtube-analytics
