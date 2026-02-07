#!/usr/bin/env python
"""
Data Flow Diagnostic Script - Trace what happens during fetch and save
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_analytics.fetcher import YouTubeFetcher
from youtube_analytics.database import DatabaseManager

print("=" * 80)
print("🔍 DATA FLOW DIAGNOSTIC - TRACING FETCH & SAVE")
print("=" * 80)

# Initialize
db = DatabaseManager()
fetcher = YouTubeFetcher()

# Use a test channel ID (Google Developers)
test_channel_id = "UCBR8-60-B8q_2La_hu5QyAQ"

print("\n[STEP 1] Fetching channel data...")
print(f"  Channel ID: {test_channel_id}")

channel_data = fetcher.get_channel_by_id(test_channel_id)

print(f"\n[STEP 2] Checking channel fetch result...")
if "error" in channel_data:
    print(f"  ❌ Error: {channel_data['error']}")
    sys.exit(1)
else:
    print(f"  ✅ Channel fetched successfully")
    print(f"  Title: {channel_data['title']}")
    print(f"  Fields returned: {list(channel_data.keys())}")

print(f"\n[STEP 3] Saving channel to database...")
result = db.add_channel(channel_data)
if result["success"]:
    print(f"  ✅ Channel saved: {result['message']}")
else:
    print(f"  ❌ Save failed: {result['error']}")
    sys.exit(1)

print(f"\n[STEP 4] Verifying channel in database...")
saved_channel = db.get_channel(test_channel_id)
if saved_channel:
    print(f"  ✅ Channel retrieved from database")
    print(f"  Title: {saved_channel['title']}")
    print(f"  Subscribers: {saved_channel['subscribers']}")
    print(f"  Total Views: {saved_channel['total_views']}")
else:
    print(f"  ❌ Could not retrieve channel")
    sys.exit(1)

print(f"\n[STEP 5] Fetching videos for this channel...")
videos = fetcher.get_channel_videos(test_channel_id, max_results=10)

if isinstance(videos, dict) and "error" in videos:
    print(f"  ❌ Error fetching videos: {videos['error']}")
    sys.exit(1)
elif isinstance(videos, list):
    print(f"  ✅ Videos fetched: {len(videos)} videos")
    if len(videos) > 0:
        print(f"\n  First video sample:")
        print(f"    Fields: {list(videos[0].keys())}")
        print(f"    Video ID: {videos[0].get('video_id')}")
        print(f"    Title: {videos[0].get('title', 'N/A')[:50]}...")
        print(f"    Channel ID: {videos[0].get('channel_id')}")
        print(f"    Views: {videos[0].get('views')}")
        print(f"    Likes: {videos[0].get('likes')}")
else:
    print(f"  ❌ Unexpected response type: {type(videos)}")
    sys.exit(1)

print(f"\n[STEP 6] Saving videos to database...")
saved_count = 0
failed_count = 0
failed_videos = []

for i, video in enumerate(videos[:5]):  # Test with first 5
    if isinstance(video, dict) and "error" not in video:
        result = db.add_video(video)
        if result.get("success"):
            saved_count += 1
        else:
            failed_count += 1
            failed_videos.append((video.get('title'), result.get('error')))
    else:
        failed_count += 1
        failed_videos.append((video.get('title', 'Unknown'), 'Error in video data'))

print(f"  Attempted: 5 videos")
print(f"  ✅ Saved: {saved_count}")
print(f"  ❌ Failed: {failed_count}")

if failed_videos:
    print(f"\n  Failed videos:")
    for title, error in failed_videos:
        print(f"    - {title}: {error}")

print(f"\n[STEP 7] Verifying videos in database...")
db_videos = db.get_channel_videos(test_channel_id)
print(f"  Videos in database: {len(db_videos)}")

if len(db_videos) > 0:
    print(f"  ✅ Videos successfully saved!")
    print(f"\n  Sample video from database:")
    print(f"    Title: {db_videos[0].get('title', 'N/A')[:50]}...")
    print(f"    Views: {db_videos[0].get('views')}")
    print(f"    Saved at: {db_videos[0].get('fetched_at')}")
else:
    print(f"  ❌ No videos found in database!")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC COMPLETE")
print("=" * 80)
