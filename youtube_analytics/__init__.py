"""Creatorscope — self-hosted YouTube analytics platform."""

from youtube_analytics.database import DatabaseManager
from youtube_analytics.fetcher import YouTubeFetcher

__version__ = "2.0.0"

__all__ = [
    "DatabaseManager",
    "YouTubeFetcher",
]
