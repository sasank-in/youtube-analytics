#!/usr/bin/env python
"""
Database Diagnostic Test Script

This script tests all database integration points and helps diagnose issues.
Run with: python test_database_integration.py
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_analytics.config import YOUTUBE_API_KEY, DB_URL, DB_ECHO
from youtube_analytics.database import DatabaseManager
from youtube_analytics.fetcher import YouTubeFetcher

print("=" * 70)
print("🔍 YOUTUBE ANALYTICS - DATABASE INTEGRATION TEST")
print("=" * 70)

# Test 1: Configuration
print("\n[1/6] Checking Configuration...")
print(f"  API Key: {'✅ Set' if YOUTUBE_API_KEY else '❌ NOT SET'}")
print(f"  Database URL: {DB_URL[:50]}..." if len(DB_URL) > 50 else f"  Database URL: {DB_URL}")
print(f"  Debug Mode: {'✅ Enabled' if DB_ECHO else '⚠️ Disabled (set DB_ECHO=True for SQL logs)'}")

# Test 2: Database Connection
print("\n[2/6] Testing Database Connection...")
try:
    db = DatabaseManager()
    print("  ✅ Database connected successfully!")
except Exception as e:
    print(f"  ❌ Database connection failed: {e}")
    print("\n  💡 SOLUTION:")
    if "postgresql" in str(e).lower():
        print("     - Ensure PostgreSQL is running")
        print("     - Check DATABASE_URL in .env is correct")
        print("     - Or use SQLite (delete/comment DATABASE_URL in .env)")
    else:
        print(f"     - Error: {e}")
    sys.exit(1)

# Test 3: Check Saved Channels
print("\n[3/6] Checking Saved Channels...")
try:
    channels = db.get_all_channels()
    if channels:
        print(f"  ✅ Found {len(channels)} saved channel(s):")
        for i, ch in enumerate(channels, 1):
            videos_list = db.get_channel_videos(ch['channel_id'])
            print(f"     {i}. {ch['title']:40} | {len(videos_list):3} videos | Subscribers: {ch['subscribers']}")
    else:
        print("  ⓘ No channels saved yet (this is normal for first run)")
except Exception as e:
    print(f"  ❌ Error fetching channels: {e}")
    sys.exit(1)

# Test 4: YouTube API Connection
print("\n[4/6] Testing YouTube API Connection...")
if not YOUTUBE_API_KEY:
    print("  ❌ No API key configured")
    print("     - Add YOUTUBE_API_KEY to .env file")
    print("     - Get key from: https://console.cloud.google.com/")
else:
    try:
        fetcher = YouTubeFetcher()
        print("  ✅ YouTube API initialized successfully!")
    except Exception as e:
        print(f"  ❌ API initialization failed: {e}")
        sys.exit(1)

# Test 5: Fetch and Save Test (Optional)
print("\n[5/6] Testing Fetch & Save (Using Google Developers Channel)...")
try:
    # Use a well-known channel
    test_channel_id = "UCBR8-60-B8q_2La_hu5QyAQ"  # Google Developers official channel
    
    channel_data = fetcher.get_channel_by_id(test_channel_id)
    
    if "error" in channel_data:
        print(f"  ⚠️ Could not fetch test channel: {channel_data['error']}")
    else:
        print(f"  ✅ Fetched: {channel_data['title']}")
        
        # Try to save it
        result = db.add_channel(channel_data)
        
        if result["success"]:
            print(f"  ✅ Saved to database successfully!")
            
            # Verify we can retrieve it
            saved = db.get_channel(test_channel_id)
            if saved:
                print(f"  ✅ Retrieved from database: {saved['title']}")
                print(f"     Subscribers: {saved['subscribers']}")
                print(f"     Total Views: {saved['total_views']}")
            else:
                print(f"  ❌ Could not retrieve saved channel!")
        else:
            print(f"  ❌ Save failed: {result['error']}")
            
except Exception as e:
    print(f"  ❌ Test failed: {e}")

# Test 6: Summary
print("\n[6/6] Test Summary")
print("=" * 70)

all_good = True
if not YOUTUBE_API_KEY:
    print("  ⚠️  No YouTube API key set")
    all_good = False
if not channels and all_good:
    print("  ⓘ Database is ready but empty (fetch data to populate)")
else:
    print(f"  ✅ Database has {len(channels)} channel(s)")

if all_good:
    print("\n✅ ALL TESTS PASSED! Your database integration is working.")
    print("\n📝 Next Steps:")
    print("   1. Go to Streamlit app: streamlit run app.py")
    print("   2. Use 'Quick Fetch' tab to fetch YouTube data")
    print("   3. View results in 'Analytics Dashboard' tab")
    print("   4. Manage data in 'Saved Channels' tab")
else:
    print("\n⚠️  Some tests failed. Check the errors above.")

print("\n" + "=" * 70)
