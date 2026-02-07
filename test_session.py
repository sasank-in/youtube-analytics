#!/usr/bin/env python
"""
Test if the issue is with session caching in Streamlit
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 80)
print("SESSION CACHING TEST - Fresh session query")
print("=" * 80 + "\n")

from youtube_analytics.database import DatabaseManager, Channel
from youtube_analytics.config import DB_URL

print(f"Database URL: {DB_URL}")

# Test 1: Direct query without DatabaseManager
print("\n[TEST 1] Direct SQLAlchemy query...")
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    channels = session.query(Channel).all()
    print(f"  Channels found: {len(channels)}")
    for ch in channels:
        print(f"    - {ch.title} (ID: {ch.channel_id})")
    
    session.close()
except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Via DatabaseManager fresh instance
print("\n[TEST 2] Via DatabaseManager fresh instance...")
try:
    db = DatabaseManager()
    channels = db.get_all_channels()
    print(f"  Channels found: {len(channels)}")
    for ch in channels:
        print(f"    - {ch['title']} (ID: {ch['channel_id']})")
except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check Channel model
print("\n[TEST 3] Checking Channel model...")
try:
    from youtube_analytics.database import Channel
    print(f"  Channel model: {Channel}")
    print(f"  Channel table name: {Channel.__tablename__}")
    print(f"  Columns: {[col.name for col in Channel.__table__.columns]}")
except Exception as e:
    print(f"  Error: {e}")

# Test 4: Raw SQL execution
print("\n[TEST 4] Raw SQL execution on same connection...")
try:
    from sqlalchemy import text
    engine = create_engine(DB_URL)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) as cnt FROM channels"))
        count = result.fetchone()[0]
        print(f"  Raw SQL COUNT: {count}")
        
        result = conn.execute(text("SELECT channel_id, title FROM channels LIMIT 5"))
        for row in result:
            print(f"    - {row[1]} (ID: {row[0]})")
except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("SESSION TEST COMPLETE")
print("=" * 80 + "\n")
