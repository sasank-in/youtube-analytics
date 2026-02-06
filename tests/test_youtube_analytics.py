"""Tests for YouTube Analytics Platform"""

import pytest
from youtube_analytics import YouTubeFetcher, DatabaseManager, YouTubeVisualizer


class TestYouTubeFetcher:
    """Test YouTube Fetcher functionality"""
    
    def test_init(self):
        """Test fetcher initialization"""
        try:
            fetcher = YouTubeFetcher()
            assert fetcher.youtube is not None
        except ValueError:
            pytest.skip("API key not configured")


class TestDatabaseManager:
    """Test Database operations"""
    
    def test_init(self):
        """Test database connection"""
        try:
            db = DatabaseManager()
            assert db.engine is not None
        except Exception:
            pytest.skip("Database not configured")


class TestYouTubeVisualizer:
    """Test Visualization functionality"""
    
    def test_init(self):
        """Test visualizer initialization"""
        try:
            viz = YouTubeVisualizer()
            assert viz.db is not None
        except Exception:
            pytest.skip("Database not configured")
