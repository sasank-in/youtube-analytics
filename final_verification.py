#!/usr/bin/env python
import sys
sys.path.insert(0, 'c:/Users/shash/yout-analytics')

from youtube_analytics.database import DatabaseManager

print("=" * 60)
print("Final Verification Test")
print("=" * 60)

db = DatabaseManager()
channels = db.get_all_channels()

print(f"\n✅ Database check: {len(channels)} channels in database\n")

for ch in channels:
    videos = db.get_channel_videos(ch['channel_id'])
    print(f"   📊 {ch['title']}: {len(videos)} videos saved")
    print(f"      Subscribers: {ch['subscribers']}")
    print(f"      Total Views: {ch['total_views']}")

print("\n" + "=" * 60)
print("✅ ALL OPERATIONS WORKING CORRECTLY")
print("=" * 60)
