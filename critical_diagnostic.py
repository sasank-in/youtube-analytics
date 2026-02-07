#!/usr/bin/env python
"""
CRITICAL DIAGNOSTIC - Trace the exact issue with data not appearing
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 100)
print("CRITICAL DIAGNOSTIC - DATABASE DATA FLOW CHECK")
print("=" * 100)

# Step 1: Check database file location
print("\n[STEP 1] Checking database file location...")
from youtube_analytics.config import DB_URL
print(f"  DB_URL from config: {DB_URL}")

import sqlite3
if "sqlite" in DB_URL.lower():
    # Extract path from sqlite URL
    db_path = DB_URL.replace("sqlite:///", "")
    db_path = db_path.replace("sqlite://", "")
    
    # Check if absolute or relative
    if os.path.isabs(db_path):
        print(f"  Path type: ABSOLUTE")
        print(f"  Full path: {db_path}")
    else:
        print(f"  Path type: RELATIVE (This could be a problem!)")
        print(f"  Relative path: {db_path}")
        abs_path = os.path.abspath(db_path)
        print(f"  Resolves to: {abs_path}")
    
    # Check if file exists
    if os.path.exists(db_path):
        print(f"  File exists: YES")
        file_size = os.path.getsize(db_path)
        print(f"  File size: {file_size} bytes")
    elif os.path.exists(abs_path if not os.path.isabs(db_path) else db_path):
        print(f"  File exists: YES (at absolute path)")
    else:
        print(f"  File exists: NOT YET (will be created on first connection)")

# Step 2: Test database connection
print("\n[STEP 2] Testing database connection...")
try:
    from youtube_analytics.database import DatabaseManager
    db = DatabaseManager()
    print(f"  Connection: SUCCESS")
except Exception as e:
    print(f"  Connection: FAILED - {e}")
    sys.exit(1)

# Step 3: Check if tables exist
print("\n[STEP 3] Checking database tables...")
try:
    from youtube_analytics.database import Base, Channel, Video
    
    # List all tables
    inspector = db.engine.inspect
    tables = inspector.get_table_names()
    print(f"  Tables found: {tables}")
    
    if "channels" in tables:
        # Count channels
        session = db.Session()
        channel_count = session.query(Channel).count()
        session.close()
        print(f"  Channels table: EXISTS ({channel_count} rows)")
    else:
        print(f"  Channels table: DOES NOT EXIST")
    
    if "videos" in tables:
        session = db.Session()
        video_count = session.query(Video).count()
        session.close()
        print(f"  Videos table: EXISTS ({video_count} rows)")
    else:
        print(f"  Videos table: DOES NOT EXIST")
        
except Exception as e:
    print(f"  Error checking tables: {e}")
    import traceback
    traceback.print_exc()

# Step 4: Query all channels
print("\n[STEP 4] Querying all channels from database...")
try:
    channels = db.get_all_channels()
    print(f"  Channels returned: {len(channels)}")
    
    if channels:
        print(f"\n  Channel list:")
        for i, ch in enumerate(channels, 1):
            print(f"    {i}. {ch['title']}")
            print(f"       ID: {ch['channel_id']}")
            print(f"       Subscribers: {ch['subscribers']}")
            
            # Query videos for this channel
            videos = db.get_channel_videos(ch['channel_id'])
            print(f"       Videos: {len(videos)}")
    else:
        print(f"  NO CHANNELS FOUND - This is the problem!")
        
except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()

# Step 5: Test data insertion
print("\n[STEP 5] Testing data insertion...")
try:
    test_channel = {
        "channel_id": "TEST_CHANNEL_" + str(os.getpid()),
        "title": "Test Channel",
        "description": "Test Description",
        "custom_url": "test_url",
        "published_at": None,
        "subscribers": "100",
        "total_views": "1000",
        "total_videos": "10",
        "profile_image": "http://example.com/image.jpg",
        "banner_image": "http://example.com/banner.jpg"
    }
    
    print(f"  Inserting test channel: {test_channel['title']}")
    result = db.add_channel(test_channel)
    print(f"  Insert result: {result}")
    
    # Try to retrieve it
    print(f"  Retrieving inserted channel...")
    retrieved = db.get_channel(test_channel['channel_id'])
    if retrieved:
        print(f"  SUCCESS - Channel retrieved: {retrieved['title']}")
    else:
        print(f"  FAILED - Could not retrieve inserted channel!")
        
except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()

# Step 6: Direct SQLite query
print("\n[STEP 6] Direct SQLite query (if using SQLite)...")
if "sqlite" in DB_URL.lower():
    try:
        # Extract db file path
        db_file = DB_URL.replace("sqlite:///", "").replace("sqlite://", "")
        if not os.path.isabs(db_file):
            db_file = os.path.abspath(db_file)
        
        print(f"  Opening SQLite database: {db_file}")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"  Tables: {[t[0] for t in tables]}")
        
        # Count rows
        try:
            cursor.execute("SELECT COUNT(*) FROM channels;")
            channel_count = cursor.fetchone()[0]
            print(f"  Channels (via SQL): {channel_count}")
        except:
            print(f"  Could not query channels table")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM videos;")
            video_count = cursor.fetchone()[0]
            print(f"  Videos (via SQL): {video_count}")
        except:
            print(f"  Could not query videos table")
        
        conn.close()
        
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 100)
print("DIAGNOSTIC COMPLETE")
print("=" * 100)
print("\nSUMMARY:")
print("If you see 0 channels/videos above, data is not being saved properly.")
print("If the database file path is incorrect, that's the issue.")
print("Check Streamlit console output (terminal) for more details.")
print("=" * 100 + "\n")
