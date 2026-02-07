#!/usr/bin/env python
import sys
sys.path.insert(0, 'c:/Users/shash/yout-analytics')

print("Testing app imports and basic functionality...")

try:
    print("1. Testing imports...")
    import streamlit as st
    from youtube_analytics.fetcher import YouTubeFetcher
    from youtube_analytics.database import DatabaseManager
    from youtube_analytics.visualizer import YouTubeVisualizer
    import pandas as pd
    print("   ✅ All imports successful")
    
    print("\n2. Testing component initialization...")
    fetcher = YouTubeFetcher()
    db = DatabaseManager()
    visualizer = YouTubeVisualizer()
    print("   ✅ Components initialized")
    
    print("\n3. Testing database connection...")
    channels = db.get_all_channels()
    print(f"   ✅ Database OK - Found {len(channels)} channels")
    
    print("\n4. Testing video DataFrame operations...")
    # Create a test DataFrame like the app would
    test_data = {
        'title': ['Video 1', 'Video 2'],
        'views': [1000, 2000],
        'likes': [100, 200],
        'comments': [10, 20],
        'published_at': ['2025-01-01', '2025-01-02']
    }
    test_df = pd.DataFrame(test_data)
    
    # Test the operations from app.py
    test_df['views'] = pd.to_numeric(test_df['views'], errors='coerce').fillna(0)
    test_df['likes'] = pd.to_numeric(test_df['likes'], errors='coerce').fillna(0)
    test_df['comments'] = pd.to_numeric(test_df['comments'], errors='coerce').fillna(0)
    
    test_df['engagement_rate'] = ((test_df['likes'] + test_df['comments']) / test_df['views'] * 100).fillna(0).round(2)
    test_df['like_rate'] = (test_df['likes'] / test_df['views'] * 100).fillna(0).round(2)
    
    test_df['views_formatted'] = test_df['views'].apply(lambda x: f"{int(x):,}")
    test_df['likes_formatted'] = test_df['likes'].apply(lambda x: f"{int(x):,}")
    test_df['comments_formatted'] = test_df['comments'].apply(lambda x: f"{int(x):,}")
    
    # This is the fixed version
    test_df_sorted = test_df.sort_values('views', ascending=False)
    display_df = test_df_sorted[['title', 'views_formatted', 'likes_formatted', 'comments_formatted', 'engagement_rate', 'like_rate', 'published_at']].copy()
    display_df.columns = ['Title', 'Views', 'Likes', 'Comments', 'Engagement %', 'Like %', 'Published']
    
    print("   ✅ DataFrame operations OK")
    print(f"   Display DataFrame:\n{display_df}")
    
    print("\n✅ ALL TESTS PASSED!")
    print("\nThe app should run without errors.")
    
except Exception as e:
    print(f"\n❌ ERROR DETECTED:")
    print(f"   Type: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    import traceback
    print("\nFull Traceback:")
    traceback.print_exc()
    sys.exit(1)
