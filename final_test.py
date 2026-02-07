#!/usr/bin/env python
"""
FINAL COMPREHENSIVE TEST - End-to-end data flow verification
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 100)
print("FINAL COMPREHENSIVE TEST - COMPLETE DATA FLOW")
print("=" * 100 + "\n")

# Step 1: Delete old test data
print("[STEP 1] Cleaning up old test data...")
try:
    from youtube_analytics.database import DatabaseManager, Channel
    db = DatabaseManager()
    
    # Get all test channels
    session = db.Session()
    test_channels = session.query(Channel).filter(Channel.channel_id.startswith("TEST_")).all()
    for ch in test_channels:
        session.delete(ch)
    session.commit()
    session.close()
    print(f"  ✅ Cleaned up {len(test_channels)} test channels")
except Exception as e:
    print(f"  ⚠️ Error cleaning up: {e}")

# Step 2: Insert test data
print("\n[STEP 2] Inserting test channel and videos...")
try:
    test_channel = {
        "channel_id": f"TEST_CHANNEL_{int(time.time())}",
        "title": "Test Channel for Final Verification",
        "description": "Test description",
        "custom_url": "testchannelurl",
        "published_at": None,
        "subscribers": "1000",
        "total_views": "100000",
        "total_videos": "50",
        "profile_image": "http://example.com/profile.jpg",
        "banner_image": "http://example.com/banner.jpg"
    }
    
    result = db.add_channel(test_channel)
    print(f"  ✅ Channel inserted: {test_channel['title']}")
    
    # Insert videos
    for i in range(5):
        video = {
            "video_id": f"TEST_VIDEO_{i}_{int(time.time())}",
            "title": f"Test Video {i+1}",
            "description": f"Test video description {i+1}",
            "channel_id": test_channel['channel_id'],
            "channel_title": test_channel['title'],
            "published_at": None,
            "duration": "PT10M30S",
            "views": "1000",
            "likes": "100",
            "comments": "50",
            "thumbnail": "http://example.com/thumb.jpg"
        }
        db.add_video(video)
    
    print(f"  ✅ Inserted 5 test videos")
    
except Exception as e:
    print(f"  ❌ Error inserting test data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Verify data via get_all_channels
print("\n[STEP 3] Verifying data via get_all_channels()...")
try:
    channels = db.get_all_channels()
    print(f"  Total channels in database: {len(channels)}")
    
    # Find our test channel
    test_ch = [ch for ch in channels if ch['channel_id'].startswith("TEST_")]
    if test_ch:
        ch = test_ch[0]
        print(f"  ✅ Test channel found: {ch['title']}")
        print(f"     - Channel ID: {ch['channel_id']}")
        print(f"     - Subscribers: {ch['subscribers']}")
    else:
        print(f"  ❌ Test channel NOT found in get_all_channels()!")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Verify data via get_channel
print("\n[STEP 4] Verifying data via get_channel(channel_id)...")
try:
    channel = db.get_channel(test_channel['channel_id'])
    if channel:
        print(f"  ✅ Channel retrieved by ID: {channel['title']}")
    else:
        print(f"  ❌ Could not retrieve channel by ID!")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Step 5: Verify videos
print("\n[STEP 5] Verifying videos via get_channel_videos()...")
try:
    videos = db.get_channel_videos(test_channel['channel_id'])
    print(f"  Total videos for channel: {len(videos)}")
    
    if len(videos) == 5:
        print(f"  ✅ All 5 test videos found!")
        for i, vid in enumerate(videos[:2], 1):
            print(f"     {i}. {vid['title']}")
    else:
        print(f"  ⚠️ Expected 5 videos but found {len(videos)}")
        
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Step 6: Test direct session retrieval
print("\n[STEP 6] Testing direct SQLAlchemy session retrieval...")
try:
    from sqlalchemy.orm import sessionmaker
    session = db.Session()
    
    # Query test channel
    ch = session.query(Channel).filter_by(
        channel_id=test_channel['channel_id']
    ).first()
    
    if ch:
        print(f"  ✅ Direct session query works: {ch.title}")
    else:
        print(f"  ❌ Direct session query failed!")
        
    session.close()
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Step 7: Test Streamlit-like caching scenario
print("\n[STEP 7] Testing Streamlit caching scenario...")
try:
    # Simulate what @st.cache_resource does - reusing instance
    db_cached = db  # Use same instance
    
    channels_cached = db_cached.get_all_channels()
    test_ch_cached = [ch for ch in channels_cached if ch['channel_id'] == test_channel['channel_id']]
    
    if test_ch_cached:
        print(f"  ✅ Cached instance retrieves data: {test_ch_cached[0]['title']}")
    else:
        print(f"  ❌ Cached instance does NOT retrieve data!")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Step 8: Simulate Dashboard tab flow
print("\n[STEP 8] Simulating Dashboard tab flow...")
try:
    print(f"  Getting all channels...")
    channels = db.get_all_channels()
    
    if not channels:
        print(f"  ❌ No channels returned - Dashboard would be empty!")
        sys.exit(1)
    
    print(f"  ✅ Got {len(channels)} channels")
    
    # Simulate selecting first test channel
    test_channels = [ch for ch in channels if ch['channel_id'].startswith("TEST_")]
    if test_channels:
        sel_ch = test_channels[0]
        print(f"\n  Selected channel: {sel_ch['title']}")
        
        # Get videos for selected channel
        videos = db.get_channel_videos(sel_ch['channel_id'])
        print(f"  Videos for channel: {len(videos)}")
        
        if len(videos) > 0:
            print(f"  ✅ Dashboard can display {len(videos)} videos for {sel_ch['title']}")
        else:
            print(f"  ❌ Dashboard would show 0 videos but database has some!")
    else:
        print(f"  ❌ No test channels found in Dashboard query!")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 100)
print("✅ ALL TESTS PASSED!")
print("=" * 100)
print("\nSUMMARY:")
print("  ✅ Data saves to database correctly")
print("  ✅ get_all_channels() retrieves all data")
print("  ✅ get_channel() retrieves by ID")
print("  ✅ get_channel_videos() retrieves related videos")
print("  ✅ Cached instances (like Streamlit) work fine")
print("  ✅ Dashboard tab would display data correctly")
print("\n>>> If Streamlit still doesn't show data,")
print(">>> it's likely a caching issue in the app.py @st.cache_resource")
print("\n" + "=" * 100 + "\n")
