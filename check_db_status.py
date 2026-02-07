#!/usr/bin/env python
"""
Quick Database Status Check - See what's currently saved
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_analytics.database import DatabaseManager

print("=" * 80)
print("📊 DATABASE CURRENT STATUS")
print("=" * 80)

try:
    db = DatabaseManager()
    print("✅ Database connected\n")
    
    # Check channels
    channels = db.get_all_channels()
    print(f"Saved Channels: {len(channels)}")
    
    if channels:
        for i, ch in enumerate(channels, 1):
            print(f"\n  {i}. {ch['title']}")
            print(f"     Channel ID: {ch['channel_id']}")
            print(f"     Subscribers: {ch['subscribers']}")
            print(f"     Total Views: {ch['total_views']}")
            print(f"     Saved at: {ch['fetched_at']}")
            
            # Get videos for this channel
            videos = db.get_channel_videos(ch['channel_id'])
            print(f"     Videos in DB: {len(videos)}")
            
            if videos:
                print(f"\n     Video samples:")
                for v in videos[:3]:
                    print(f"       - {v['title'][:50]}... ({v['views']} views)")
    else:
        print("  ⚠️ No channels saved yet")
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
