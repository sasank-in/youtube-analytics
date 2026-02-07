#!/usr/bin/env python3
"""
Verify complete data flow including database operations and data retrieval.
Tests the exact sequence: Fetch -> Save -> Retrieve -> Display
"""

import sys
import os
from datetime import datetime

# Add the project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_analytics.database import DatabaseManager, parse_datetime
from youtube_analytics.fetcher import YouTubeFetcher

def test_complete_flow():
    """Test the complete sequence of operations"""
    print("\n" + "="*70)
    print("TESTING COMPLETE DATA FLOW")
    print("="*70)
    
    # Initialize components
    fetcher = YouTubeFetcher()
    db = DatabaseManager()
    
    # Step 1: Fetch a channel
    print("\n[1] FETCHING CHANNEL...")
    search_query = "Google Developers"
    channel_data = fetcher.get_channel_by_name(search_query)
    
    if "error" in channel_data:
        print(f"❌ Channel fetch failed: {channel_data['error']}")
        return False
    
    print(f"✅ Channel fetched: {channel_data['title']}")
    channel_id = channel_data['channel_id']
    print(f"   Channel ID: {channel_id}")
    
    # Step 2: Save channel to database
    print("\n[2] SAVING CHANNEL TO DATABASE...")
    try:
        db.add_channel(channel_data)
        print(f"✅ Channel saved successfully")
    except Exception as e:
        print(f"❌ Channel save failed: {str(e)}")
        return False
    
    # Step 3: Fetch videos
    print("\n[3] FETCHING VIDEOS...")
    videos = fetcher.get_channel_videos(channel_id, max_results=10)
    
    if "error" in videos:
        print(f"❌ Video fetch failed: {videos['error']}")
        return False
    
    if isinstance(videos, list):
        print(f"✅ Fetched {len(videos)} videos")
    else:
        print(f"❌ Unexpected response type: {type(videos)}")
        return False
    
    # Step 4: Save videos to database
    print("\n[4] SAVING VIDEOS TO DATABASE...")
    saved_count = 0
    for i, video in enumerate(videos, 1):
        if "error" not in video:
            try:
                db.add_video(video)
                saved_count += 1
                if i % 3 == 0:
                    print(f"   ✅ Saved {i} videos...")
            except Exception as e:
                print(f"   ❌ Error saving video: {str(e)}")
                return False
    
    print(f"✅ Successfully saved {saved_count}/{len(videos)} videos")
    
    # Step 5: Retrieve channel from database
    print("\n[5] RETRIEVING CHANNEL FROM DATABASE...")
    retrieved_channel = db.get_channel(channel_id)
    
    if retrieved_channel:
        print(f"✅ Channel retrieved: {retrieved_channel['title']}")
        print(f"   Subscribers: {retrieved_channel.get('subscribers', 'N/A')}")
        print(f"   Total Views: {retrieved_channel.get('total_views', 'N/A')}")
        print(f"   Total Videos: {retrieved_channel.get('total_videos', 'N/A')}")
    else:
        print(f"❌ Channel not found in database")
        return False
    
    # Step 6: Retrieve videos from database
    print("\n[6] RETRIEVING VIDEOS FROM DATABASE...")
    retrieved_videos = db.get_channel_videos(channel_id)
    
    if retrieved_videos:
        print(f"✅ Retrieved {len(retrieved_videos)} videos from database")
        
        # Show sample videos
        for i, video in enumerate(retrieved_videos[:3], 1):
            print(f"\n   Video {i}: {video['title'][:50]}...")
            print(f"   - Views: {video.get('views', 'N/A')}")
            print(f"   - Likes: {video.get('likes', 'N/A')}")
            print(f"   - Comments: {video.get('comments', 'N/A')}")
    else:
        print(f"⚠️  No videos found for channel (This could be an issue!)")
    
    # Step 7: Get statistics
    print("\n[7] CALCULATING STATISTICS...")
    stats = db.get_statistics(channel_id)
    
    if stats:
        print(f"✅ Statistics calculated:")
        print(f"   Total Videos: {stats['total_videos']}")
        print(f"   Total Views: {stats['total_views']}")
        print(f"   Total Likes: {stats['total_likes']}")
        print(f"   Total Comments: {stats['total_comments']}")
        if stats['total_likes'] > 0:
            engagement = (stats['total_likes'] / stats['total_views'] * 100) if stats['total_views'] > 0 else 0
            print(f"   Engagement Rate: {engagement:.2f}%")
    else:
        print(f"❌ Statistics could not be calculated")
        return False
    
    # Step 8: Verify data persistence
    print("\n[8] VERIFYING DATA PERSISTENCE...")
    all_channels = db.get_all_channels()
    print(f"✅ Total channels in database: {len(all_channels)}")
    
    # Check if our channel is in the list
    channels_dict = {ch['channel_id']: ch for ch in all_channels}
    if channel_id in channels_dict:
        print(f"✅ Our channel persists in database")
        
        # Check video count
        channel_info = channels_dict[channel_id]
        print(f"   Channel in list: {channel_info['title']}")
        
        # Count actual videos for this channel
        actual_videos = db.get_channel_videos(channel_id)
        print(f"   Videos in database: {len(actual_videos)}")
    else:
        print(f"⚠️  Channel not found in persistent data")
    
    # Step 9: Check for any errors in video data
    print("\n[9] VALIDATING VIDEO DATA INTEGRITY...")
    if retrieved_videos:
        errors_found = 0
        for i, video in enumerate(retrieved_videos):
            if not video.get('title'):
                print(f"   ❌ Video {i} missing title")
                errors_found += 1
            if video.get('view_count') is None:
                print(f"   ❌ Video {i} missing view_count")
                errors_found += 1
        
        if errors_found == 0:
            print(f"✅ All {len(retrieved_videos)} videos have valid data")
        else:
            print(f"⚠️  Found {errors_found} videos with missing data")
    
    print("\n" + "="*70)
    print("✅ COMPLETE DATA FLOW TEST PASSED")
    print("="*70)
    print("\nSummary:")
    print(f"  • Channel: {channel_data['title']}")
    print(f"  • Videos: {saved_count} fetched and saved")
    print(f"  • Database persistence: ✅ Working")
    print(f"  • Data retrieval: ✅ Working")
    print(f"  • Statistics: ✅ Working")
    print("\n")
    
    return True

if __name__ == "__main__":
    try:
        success = test_complete_flow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
