"""Database Module

Provides SQLAlchemy ORM models and database operations for
managing YouTube channel and video data in PostgreSQL.
"""

from sqlalchemy import create_engine, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from youtube_analytics.config import DB_URL
from datetime import datetime

Base = declarative_base()


class Channel(Base):
    """Channel database model"""
    __tablename__ = "channels"
    
    channel_id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    custom_url = Column(String(255))
    published_at = Column(DateTime)
    subscribers = Column(String(50))
    total_views = Column(String(50))
    total_videos = Column(String(50))
    profile_image = Column(String(500))
    banner_image = Column(String(500))
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "custom_url": self.custom_url,
            "published_at": self.published_at,
            "subscribers": self.subscribers,
            "total_views": self.total_views,
            "total_videos": self.total_videos,
            "fetched_at": self.fetched_at
        }


class Video(Base):
    """Video database model"""
    __tablename__ = "videos"
    
    video_id = Column(String(100), primary_key=True)
    channel_id = Column(String(100), ForeignKey("channels.channel_id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    published_at = Column(DateTime)
    duration = Column(String(50))
    views = Column(String(50))
    likes = Column(String(50))
    comments = Column(String(50))
    thumbnail = Column(String(500))
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    channel = relationship("Channel", back_populates="videos")
    
    def to_dict(self):
        return {
            "video_id": self.video_id,
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "published_at": self.published_at,
            "duration": self.duration,
            "views": self.views,
            "likes": self.likes,
            "comments": self.comments,
            "fetched_at": self.fetched_at
        }


class DatabaseManager:
    """Manages database operations for channels and videos"""
    
    def __init__(self):
        self.engine = create_engine(DB_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_channel(self, channel_data):
        """Add or update channel data"""
        session = self.Session()
        try:
            channel = session.query(Channel).filter_by(channel_id=channel_data["channel_id"]).first()
            
            if channel:
                for key, value in channel_data.items():
                    setattr(channel, key, value)
            else:
                channel = Channel(**channel_data)
                session.add(channel)
            
            session.commit()
            return {"success": True, "message": f"Channel '{channel_data['title']}' saved/updated"}
        except Exception as e:
            session.rollback()
            return {"success": False, "error": str(e)}
        finally:
            session.close()
    
    def add_video(self, video_data):
        """Add or update video data"""
        session = self.Session()
        try:
            video = session.query(Video).filter_by(video_id=video_data["video_id"]).first()
            
            if video:
                for key, value in video_data.items():
                    setattr(video, key, value)
            else:
                video = Video(**video_data)
                session.add(video)
            
            session.commit()
            return {"success": True, "message": f"Video '{video_data['title']}' saved/updated"}
        except Exception as e:
            session.rollback()
            return {"success": False, "error": str(e)}
        finally:
            session.close()
    
    def get_channel(self, channel_id):
        """Get channel by ID"""
        session = self.Session()
        try:
            channel = session.query(Channel).filter_by(channel_id=channel_id).first()
            return channel.to_dict() if channel else None
        finally:
            session.close()
    
    def get_all_channels(self):
        """Get all channels"""
        session = self.Session()
        try:
            channels = session.query(Channel).all()
            return [channel.to_dict() for channel in channels]
        finally:
            session.close()
    
    def get_channel_videos(self, channel_id):
        """Get all videos of a channel"""
        session = self.Session()
        try:
            videos = session.query(Video).filter_by(channel_id=channel_id).all()
            return [video.to_dict() for video in videos]
        finally:
            session.close()
    
    def delete_channel(self, channel_id):
        """Delete channel and its videos"""
        session = self.Session()
        try:
            session.query(Video).filter_by(channel_id=channel_id).delete()
            session.query(Channel).filter_by(channel_id=channel_id).delete()
            session.commit()
            return {"success": True, "message": "Channel deleted"}
        except Exception as e:
            session.rollback()
            return {"success": False, "error": str(e)}
        finally:
            session.close()
    
    def get_statistics(self, channel_id):
        """Get aggregated statistics for a channel"""
        session = self.Session()
        try:
            videos = session.query(Video).filter_by(channel_id=channel_id).all()
            
            if not videos:
                return None
            
            total_views = sum([int(v.views) if v.views != "Private" else 0 for v in videos])
            total_likes = sum([int(v.likes) if v.likes != "Private" else 0 for v in videos])
            total_comments = sum([int(v.comments) if v.comments != "Private" else 0 for v in videos])
            
            return {
                "total_videos": len(videos),
                "total_views": total_views,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "avg_views": total_views // len(videos) if videos else 0,
                "avg_likes": total_likes // len(videos) if videos else 0,
                "avg_comments": total_comments // len(videos) if videos else 0
            }
        finally:
            session.close()
