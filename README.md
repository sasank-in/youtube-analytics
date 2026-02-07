# YouTube Analytics Pro

Professional FastAPI backend with a corporate-style frontend for YouTube channel and video analytics. Data is stored locally (SQLite by default) and visualized with Chart.js.

## Features

- Channel search (ID or name) with automatic DB persistence
- Video search by ID with local-first retrieval
- Background video fetching for channels
- Corporate-style charts and benchmarks
- RPM-based earnings estimate per channel (stored in DB)
- Settings: delete channels/videos from DB

## Tech Stack

- FastAPI + Uvicorn
- SQLAlchemy + SQLite (default) or PostgreSQL
- YouTube Data API v3
- Vanilla JS + Chart.js frontend

## Project Structure

```
yout-analytics/
├── main_api.py                 # FastAPI app entrypoint
├── youtube_analytics/          # Backend modules (fetcher, db, config)
├── static/                     # Frontend JS/CSS
├── templates/                  # HTML templates
├── youtube_analytics.db        # SQLite DB (default)
├── .env                        # API key + optional DB URL
└── requirements.txt
```

## Getting Started

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment

Create `.env`:

```env
YOUTUBE_API_KEY=your_api_key_here
# Optional: Use PostgreSQL instead of SQLite
# DATABASE_URL=postgresql://user:pass@localhost:5432/youtube_db
```

### 3) Run the backend

```bash
python main_api.py 3000
```

Open `http://127.0.0.1:3000` in the browser.  
The frontend and API share the same origin (no CORS issues).

## API Endpoints (Core)

- `POST /api/channel/search` (body: `{query, search_type}`)
- `GET /api/channels`
- `GET /api/channel/{channel_id}`
- `POST /api/channel/{channel_id}/videos/fetch`
- `GET /api/channel/{channel_id}/videos`
- `GET /api/video/{video_id}`
- `GET /api/video/search?q=VIDEO_ID`
- `DELETE /api/channel/{channel_id}`
- `DELETE /api/video/{video_id}`
- `GET /api/channel/{channel_id}/rpm`
- `PUT /api/channel/{channel_id}/rpm` (body: `{rpm}`)

## Notes

- SQLite is used by default at `youtube_analytics.db`.
- RPM is stored per channel and used for earnings estimates.
- Recent channels are sorted by `last_searched_at`.

## Troubleshooting

- **Port already in use**: run `python main_api.py 3001` and open `http://127.0.0.1:3001`.
- **API key errors**: verify `YOUTUBE_API_KEY` in `.env`.

## License

Provided as-is for educational and commercial use.
