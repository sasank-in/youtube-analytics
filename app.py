import streamlit as st
from youtube_analytics.fetcher import YouTubeFetcher
from youtube_analytics.database import DatabaseManager
from youtube_analytics.visualizer import YouTubeVisualizer
from datetime import datetime
import pandas as pd
import time
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="YouTube Analytics Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, modern CSS with excellent text visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean light background */
    .stApp {
        background: #f8f9fa;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Hero Header - Gradient with white text */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.25);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: white !important;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: rgba(255, 255, 255, 0.95) !important;
        margin-top: 0.75rem;
        font-weight: 400;
    }
    
    /* White Cards */
    .white-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e8e8;
    }
    
    /* Metric Cards - Gradient with white text */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 1.75rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white !important;
    }
    
    .metric-label {
        font-size: 0.875rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
        color: white !important;
    }
    
    /* Section Title */
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1a1a1a !important;
        margin-bottom: 1.5rem;
    }
    
    /* Input Fields - Dark text on white */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.875rem 1rem;
        font-size: 1rem;
        background: white;
        color: #1a1a1a !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
    }
    
    .stTextInput label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Buttons - Gradient with white text */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Radio Buttons - Dark text */
    .stRadio > label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    .stRadio [role="radiogroup"] label {
        color: #333 !important;
        background: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stRadio [role="radiogroup"] label:hover {
        border-color: #667eea;
        background: #f8f9ff;
    }
    
    /* Checkbox - Dark text */
    .stCheckbox > label {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox - Dark text */
    .stSelectbox > label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        border-radius: 10px;
    }
    
    /* Tabs - Clean design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e8e8;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        color: #666 !important;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f5f5f5;
    }
    
    .stTabs [aria-selected="true"]:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }
    
    /* Data Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e8e8;
    }
    
    /* Success/Error/Info Messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Ensure all text is dark and readable */
    p, span, div, label, li {
        color: #1a1a1a !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    
    .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Metric component */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-size: 1.75rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #666 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #666 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to safely format numbers
def format_number(value):
    """Safely format a number with commas, handling strings and 'Private' values"""
    if value == "Private" or value is None:
        return "Private"
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)

# Initialize components with caching
@st.cache_resource
def init_components():
    return YouTubeFetcher(), DatabaseManager(), YouTubeVisualizer()

fetcher, db, visualizer = init_components()

# Function to refresh database data in Streamlit
def refresh_data():
    """Force refresh of cached data"""
    st.cache_data.clear()
    st.rerun()

# Hero Header
st.markdown("""
<div class='hero-header'>
    <div class='hero-title'>🎯 YouTube Analytics Pro</div>
    <div class='hero-subtitle'>Instant Channel Insights • Auto-Save • Real-Time Analytics</div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Quick Fetch", "📊 Analytics Dashboard", "💾 Saved Channels", "🎬 Video Analytics"])

# ============== TAB 1: QUICK FETCH ==============
with tab1:
    st.markdown("<div class='white-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚡ Quick Fetch & Auto-Save</div>", unsafe_allow_html=True)
    
    # Quick stats
    channels = db.get_all_channels()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Saved Channels</div>
            <div class='metric-value'>{len(channels)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_videos = sum([len(db.get_channel_videos(ch['channel_id'])) for ch in channels])
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Total Videos</div>
            <div class='metric-value'>{total_videos}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Status</div>
            <div class='metric-value'>✓</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch Options
    st.markdown("<div class='white-card'>", unsafe_allow_html=True)
    
    fetch_option = st.radio(
        "Choose fetch method:",
        ["📺 Channel ID", "🎬 Video ID", "🔍 Search by Name"],
        horizontal=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Channel ID Fetch
    if fetch_option == "📺 Channel ID":
        col1, col2 = st.columns([3, 1])
        with col1:
            channel_id = st.text_input(
                "Enter YouTube Channel ID",
                placeholder="UCkRfArvrzheW2E7b6SVV7vA",
                help="Paste the channel ID from YouTube URL"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            fetch_videos = st.checkbox("Fetch Videos", value=True)
        
        if st.button("🚀 Fetch & Save Channel", type="primary"):
            if channel_id:
                with st.spinner("🔄 Fetching channel data..."):
                    channel_data = fetcher.get_channel_by_id(channel_id)
                    
                    if "error" not in channel_data:
                        # Auto-save channel
                        result = db.add_channel(channel_data)
                        print(f"✅ DEBUG: Channel saved with result: {result}")
                        
                        # Display channel info
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if channel_data.get('profile_image'):
                                st.image(channel_data['profile_image'], width=120)
                        with col2:
                            st.markdown(f"### ✅ {channel_data['title']}")
                            st.write(f"**Subscribers:** {format_number(channel_data['subscribers'])}")
                            st.write(f"**Total Views:** {format_number(channel_data['total_views'])}")
                            st.write(f"**Videos:** {channel_data['total_videos']}")
                        
                        st.success(f"✅ Channel saved to database!")
                        
                        # Fetch videos if requested
                        if fetch_videos:
                            with st.spinner("📹 Fetching channel videos..."):
                                videos = fetcher.get_channel_videos(channel_id, max_results=50)
                                
                                if isinstance(videos, list) and len(videos) > 0:
                                    progress_bar = st.progress(0)
                                    saved_count = 0
                                    
                                    for i, video in enumerate(videos):
                                        if "error" not in video:
                                            db.add_video(video)
                                            saved_count += 1
                                        progress_bar.progress((i + 1) / len(videos))
                                    
                                    st.success(f"✅ Saved {saved_count} videos to database!")
                                    print(f"✅ DEBUG: Videos saved, rerunning app to refresh")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.info("📌 No videos found to save, but channel was saved successfully!")
                                    print(f"✅ DEBUG: No videos found, but channel saved - rerunning to refresh")
                                    time.sleep(1)
                                    st.rerun()
                        else:
                            # CRITICAL FIX: Rerun after channel save even if videos not fetched
                            print(f"✅ DEBUG: Channel saved without videos - rerunning to refresh UI")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error(f"❌ {channel_data['error']}")
            else:
                st.warning("⚠️ Please enter a Channel ID")
    
    # Video ID Fetch
    elif fetch_option == "🎬 Video ID":
        col1, col2 = st.columns([3, 1])
        with col1:
            video_id = st.text_input(
                "Enter YouTube Video ID",
                placeholder="dQw4w9WgXcQ",
                help="Paste the video ID from YouTube URL (the part after 'v=')"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            fetch_videos = st.checkbox("Save Analysis", value=True, key="video_save")
        
        if st.button("🎬 Fetch & Analyze Video", type="primary"):
            if video_id:
                with st.spinner("🔄 Fetching video data..."):
                    video_data = fetcher.get_video_by_id(video_id)
                    
                    if "error" not in video_data:
                        # Display video info
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if video_data.get('thumbnail'):
                                st.image(video_data['thumbnail'], width=120)
                        with col2:
                            st.markdown(f"### ✅ {video_data['title']}")
                            st.write(f"**Channel:** {video_data.get('channel_title', 'Unknown')}")
                            st.write(f"**Views:** {format_number(video_data.get('views', 0))}")
                        
                        st.success(f"✅ Video analyzed successfully!")
                        
                        # Save to database if requested
                        if fetch_videos:
                            db.add_video(video_data)
                            st.info("✅ Video saved to database!")
                    else:
                        st.error(f"❌ {video_data['error']}")
            else:
                st.warning("⚠️ Please enter a video ID")
    
    # Search by Name
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            channel_name = st.text_input(
                "Search Channel by Name",
                placeholder="Google Developers",
                help="Search for a channel by name"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            fetch_videos = st.checkbox("Fetch Videos", value=True, key="search_vids")
        
        if st.button("🔍 Search & Save Channel", type="primary"):
            if channel_name:
                with st.spinner("🔍 Searching..."):
                    channel_data = fetcher.get_channel_by_name(channel_name)
                    
                    if "error" not in channel_data:
                        # Auto-save channel
                        result = db.add_channel(channel_data)
                        print(f"✅ DEBUG: Channel saved with result: {result}")
                        
                        # Display channel info
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if channel_data.get('profile_image'):
                                st.image(channel_data['profile_image'], width=120)
                        with col2:
                            st.markdown(f"### ✅ {channel_data['title']}")
                            st.write(f"**Channel ID:** `{channel_data['channel_id']}`")
                            st.write(f"**Subscribers:** {format_number(channel_data['subscribers'])}")
                        
                        st.success(f"✅ Channel saved to database!")
                        
                        # Fetch videos if requested
                        if fetch_videos:
                            with st.spinner("📹 Fetching videos..."):
                                videos = fetcher.get_channel_videos(channel_data['channel_id'], max_results=50)
                                
                                if isinstance(videos, list) and len(videos) > 0:
                                    progress_bar = st.progress(0)
                                    saved_count = 0
                                    
                                    for i, video in enumerate(videos):
                                        if "error" not in video:
                                            db.add_video(video)
                                            saved_count += 1
                                        progress_bar.progress((i + 1) / len(videos))
                                    
                                    st.success(f"✅ Saved {saved_count} videos!")
                                    print(f"✅ DEBUG: Videos saved, rerunning to refresh")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.info("📌 No videos found to save, but channel was saved successfully!")
                                    print(f"✅ DEBUG: No videos found, but channel saved - rerunning to refresh")
                                    time.sleep(1)
                                    st.rerun()
                        else:
                            # CRITICAL FIX: Rerun after channel save even if videos not fetched
                            print(f"✅ DEBUG: Channel saved without videos - rerunning to refresh UI")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error(f"❌ {channel_data['error']}")
            else:
                st.warning("⚠️ Please enter a channel name")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Tips
    st.info("💡 **Pro Tip:** Data is automatically saved to the database when you fetch. No extra clicks needed!")

# ============== TAB 2: ENHANCED ANALYTICS DASHBOARD ==============
with tab2:
    st.markdown("<div class='white-card'><h3 style='color: #1a1a1a;'>📊 Channel Analytics Dashboard</h3></div>", unsafe_allow_html=True)
    
    channels = db.get_all_channels()
    
    # Initialize session state for persistent channel selection
    if 'selected_channel_id' not in st.session_state:
        st.session_state.selected_channel_id = None
    if 'channel_data' not in st.session_state:
        st.session_state.channel_data = None
    
    # Two options: Select from saved or search for new
    analysis_mode = st.radio(
        "Choose analysis method:",
        ["📁 Saved Channels", "🔍 Search New Channel"],
        horizontal=True
    )
    
    selected_channel_id = st.session_state.selected_channel_id
    channel_data = st.session_state.channel_data
    
    if analysis_mode == "📁 Saved Channels":
        if not channels:
            st.markdown("""
            <div class='white-card' style='text-align: center; padding: 4rem;'>
                <h2 style='color: #1a1a1a;'>📊 No Data Yet</h2>
                <p style='font-size: 1.2rem; color: #666;'>Fetch a channel in the Quick Fetch tab to see analytics</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Channel Selector with hover effect
            selected_channel = st.selectbox(
                "Select Channel to Analyze",
                options=[ch['title'] for ch in channels],
                help="Hover to see all saved channels and click to select"
            )
            selected_channel_id = next(ch['channel_id'] for ch in channels if ch['title'] == selected_channel)
            channel_data = db.get_channel(selected_channel_id)
            # Persist in session state
            st.session_state.selected_channel_id = selected_channel_id
            st.session_state.channel_data = channel_data
    
    else:  # Search New Channel
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        search_type = st.radio("Search by:", ["Channel Name", "Channel ID"], horizontal=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if search_type == "Channel Name":
                search_query = st.text_input(
                    "Enter Channel Name",
                    placeholder="e.g., Google Developers",
                    help="Search for a channel by its name"
                )
            else:
                search_query = st.text_input(
                    "Enter Channel ID",
                    placeholder="e.g., UCkRfArvrzheW7b6SVV7vA",
                    help="Paste the channel ID from YouTube URL"
                )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("🔍 Search", type="primary")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if search_btn and search_query:
            with st.spinner("Fetching channel data..."):
                try:
                    if search_type == "Channel ID":
                        channel_data = fetcher.get_channel_by_id(search_query)
                    else:
                        channel_data = fetcher.get_channel_by_name(search_query)
                    
                    if "error" not in channel_data:
                        # Save to database
                        db.add_channel(channel_data)
                        selected_channel_id = channel_data['channel_id']
                        # Persist in session state
                        st.session_state.selected_channel_id = selected_channel_id
                        st.session_state.channel_data = channel_data
                        st.success("✅ Channel fetched and saved!")
                        
                        # Fetch and save videos
                        with st.spinner("📹 Fetching videos..."):
                            videos = fetcher.get_channel_videos(channel_data['channel_id'], max_results=50)
                            
                            if isinstance(videos, list) and len(videos) > 0:
                                saved_count = 0
                                for video in videos:
                                    if "error" not in video:
                                        db.add_video(video)
                                        saved_count += 1
                                st.info(f"✅ Fetched and saved {saved_count} videos")
                                st.rerun()  # Refresh to show new data
                            else:
                                st.info("📌 No videos found for this channel")
                    else:
                        st.error(f"❌ {channel_data['error']}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Display Analytics if channel selected or searched
    if channel_data and selected_channel_id:
        stats = db.get_statistics(selected_channel_id)
        
        # Channel Header with detailed info
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 3, 2])
        with col1:
            if channel_data.get('profile_image'):
                st.image(channel_data['profile_image'], width=150)
        with col2:
            st.markdown(f"## {channel_data['title']}")
            st.write(f"**Channel ID:** `{channel_data['channel_id']}`")
            st.write(f"**Custom URL:** {channel_data.get('custom_url', 'N/A')}")
            st.write(f"**Published:** {channel_data['published_at']}")
        with col3:
            if channel_data.get('description'):
                st.write("**About:**")
                st.write(channel_data['description'][:200] + "..." if len(channel_data.get('description', '')) > 200 else channel_data.get('description', 'No description'))
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Key Metrics
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>👥 Subscribers</div>
                <div class='metric-value'>{format_number(channel_data['subscribers'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>👁️ Total Views</div>
                <div class='metric-value'>{format_number(channel_data['total_views'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🎥 Videos</div>
                <div class='metric-value'>{channel_data['total_videos']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_views = stats['avg_views'] if stats else 0
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>📊 Avg Views</div>
                <div class='metric-value'>{avg_views:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Engagement Metrics
        if stats:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 💬 Engagement Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💖 Total Likes", f"{stats['total_likes']:,}")
            with col2:
                st.metric("💬 Total Comments", f"{stats['total_comments']:,}")
            with col3:
                engagement_rate = (stats['total_likes'] / stats['total_views'] * 100) if stats['total_views'] > 0 else 0
                st.metric("🔥 Like Rate", f"{engagement_rate:.2f}%")
            with col4:
                comment_rate = (stats['total_comments'] / stats['total_views'] * 100) if stats['total_views'] > 0 else 0
                st.metric("💭 Comment Rate", f"{comment_rate:.2f}%")
        
        # Visualizations
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Performance Analytics")
        
        # Get detailed insights
        insights = visualizer.get_content_insights(selected_channel_id)
        
        if insights:
            # Display key insights
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Avg Engagement Rate", f"{insights['avg_engagement_rate']:.2f}%")
            with col2:
                st.metric("👍 Avg Like Rate", f"{insights['avg_like_rate']:.2f}%")
            with col3:
                st.metric("💬 Avg Comment Rate", f"{insights['avg_comment_rate']:.2f}%")
            with col4:
                st.metric("🎯 Total Engagement", f"{insights['total_likes'] + insights['total_comments']:,}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Best performing content
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🏆 **Best Video:** {insights['best_video'][:50]}... ({insights['best_video_views']:,} views)")
            with col2:
                st.success(f"🔥 **Most Engaging:** {insights['most_engaging'][:50]}... ({insights['most_engaging_rate']:.2f}% engagement)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Enhanced Visualizations with better graphs
        st.markdown("### 📊 Detailed Charts & Analytics")
        
        # Engagement Overview Chart
        fig_engagement = visualizer.create_engagement_overview_chart(selected_channel_id)
        if fig_engagement:
            st.plotly_chart(fig_engagement, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = visualizer.create_video_performance_chart(selected_channel_id)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No video data available")
        
        with col2:
            fig2 = visualizer.create_engagement_ratio_chart(selected_channel_id)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No video data available")
        
        # Posting Frequency
        fig_freq = visualizer.create_posting_frequency_chart(selected_channel_id)
        if fig_freq:
            st.plotly_chart(fig_freq, use_container_width=True)
        
        # Performance Heatmap
        fig_heatmap = visualizer.create_performance_heatmap(selected_channel_id)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Views Distribution
        fig3 = visualizer.create_views_distribution_chart(selected_channel_id)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Video List with enhanced analytics
        videos = db.get_channel_videos(selected_channel_id)
        if videos:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='white-card'>", unsafe_allow_html=True)
            st.markdown("### 🎬 Video Performance Table")
            
            videos_df = pd.DataFrame(videos)
            videos_df['views'] = pd.to_numeric(videos_df['views'], errors='coerce').fillna(0)
            videos_df['likes'] = pd.to_numeric(videos_df['likes'], errors='coerce').fillna(0)
            videos_df['comments'] = pd.to_numeric(videos_df['comments'], errors='coerce').fillna(0)
            
            # Calculate engagement metrics
            videos_df['engagement_rate'] = ((videos_df['likes'] + videos_df['comments']) / videos_df['views'] * 100).fillna(0).round(2)
            videos_df['like_rate'] = (videos_df['likes'] / videos_df['views'] * 100).fillna(0).round(2)
            
            # Format numbers
            videos_df['views_formatted'] = videos_df['views'].apply(lambda x: f"{int(x):,}")
            videos_df['likes_formatted'] = videos_df['likes'].apply(lambda x: f"{int(x):,}")
            videos_df['comments_formatted'] = videos_df['comments'].apply(lambda x: f"{int(x):,}")
            
            # Sort by views first, then select columns to display
            videos_df_sorted = videos_df.sort_values('views', ascending=False)
            display_df = videos_df_sorted[['title', 'views_formatted', 'likes_formatted', 'comments_formatted', 'engagement_rate', 'like_rate', 'published_at']].copy()
            display_df.columns = ['Title', 'Views', 'Likes', 'Comments', 'Engagement %', 'Like %', 'Published']
            
            st.dataframe(display_df, use_container_width=True, height=400)
            
            # Download option
            csv = videos_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Data (CSV)",
                data=csv,
                file_name=f"{channel_data['title']}_videos.csv",
                mime="text/csv"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============== TAB 3: SAVED CHANNELS ==============
with tab3:
    channels = db.get_all_channels()
    
    if not channels:
        st.markdown("""
        <div class='white-card' style='text-align: center; padding: 4rem;'>
            <h2 style='color: #1a1a1a;'>💾 No Saved Channels</h2>
            <p style='font-size: 1.2rem; color: #666;'>Fetch your first channel to get started</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='white-card'><h3 style='color: #1a1a1a;'>📁 Saved Channels ({len(channels)})</h3></div>", unsafe_allow_html=True)
        
        for channel in channels:
            videos = db.get_channel_videos(channel['channel_id'])
            
            st.markdown("<div class='white-card'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col1:
                if channel.get('profile_image'):
                    st.image(channel['profile_image'], width=80)
            
            with col2:
                st.markdown(f"### {channel['title']}")
                st.write(f"**Subscribers:** {format_number(channel['subscribers'])} | **Views:** {format_number(channel['total_views'])} | **Videos:** {len(videos)}")
                st.write(f"**Saved:** {channel['fetched_at']}")
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Delete", key=f"del_{channel['channel_id']}"):
                    result = db.delete_channel(channel['channel_id'])
                    if result["success"]:
                        st.success("✅ Deleted!")
                        time.sleep(1)
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============== TAB 4: VIDEO ANALYTICS ==============
with tab4:
    st.markdown("<div class='white-card'><h3 style='color: #1a1a1a;'>🎬 Single Video Analytics</h3></div>", unsafe_allow_html=True)
    st.write("Get detailed analytics for any YouTube video by video ID")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_id = st.text_input(
            "Enter YouTube Video ID",
            placeholder="e.g., dQw4w9WgXcQ",
            help="Paste the video ID from YouTube URL (the part after 'v=')"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🔍 Analyze Video", type="primary")
    
    if analyze_btn:
        if video_id:
            with st.spinner("Fetching video data..."):
                try:
                    # Fetch video data
                    video_data = fetcher.get_video_by_id(video_id)
                    
                    if "error" not in video_data:
                        # Save to database (if channel also saved)
                        channel_id = video_data.get('channel_id')
                        if channel_id:
                            db.add_video(video_data)
                        
                        # Display video details
                        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            if video_data.get('thumbnail'):
                                st.image(video_data['thumbnail'], width=150)
                        
                        with col2:
                            st.markdown(f"### {video_data['title']}", unsafe_allow_html=True)
                            st.write(f"**Channel:** {video_data.get('channel_title', 'Unknown')}")
                            st.write(f"**Video ID:** `{video_data['video_id']}`")
                            st.write(f"**Description:** {video_data.get('description', 'N/A')[:300]}...")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Video metrics
                        st.markdown("<div class='white-card'><h4 style='color: #1a1a1a;'>📊 Video Performance Metrics</h4></div>", unsafe_allow_html=True)
                        
                        metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
                        
                        with metric_col1:
                            views = int(video_data.get('views', 0)) if video_data.get('views', 0) != 'Private' else 0
                            st.metric("Views", format_number(views))
                        
                        with metric_col2:
                            likes = int(video_data.get('likes', 0)) if video_data.get('likes', 0) != 'Private' else 0
                            st.metric("Likes", format_number(likes))
                        
                        with metric_col3:
                            comments = int(video_data.get('comments', 0)) if video_data.get('comments', 0) != 'Private' else 0
                            st.metric("Comments", format_number(comments))
                        
                        with metric_col4:
                            try:
                                views_int = int(video_data.get('views', 1)) if video_data.get('views', 1) != 'Private' else 1
                                likes_int = int(video_data.get('likes', 0)) if video_data.get('likes', 0) != 'Private' else 0
                                engagement = (likes_int / views_int * 100) if views_int > 0 else 0
                                st.metric("Engagement %", f"{engagement:.2f}%")
                            except:
                                st.metric("Engagement %", "N/A")
                        
                        with metric_col5:
                            st.metric("Published", video_data.get('published_at', 'N/A')[:10] if video_data.get('published_at') else 'N/A')
                        
                        # Additional details
                        st.markdown("<div class='white-card'><h4 style='color: #1a1a1a;'>ℹ️ Video Details</h4></div>", unsafe_allow_html=True)
                        
                        detail_col1, detail_col2 = st.columns(2)
                        
                        with detail_col1:
                            st.write(f"**Duration:** {video_data.get('duration', 'N/A')}")
                            st.write(f"**Published At:** {video_data.get('published_at', 'N/A')}")
                        
                        with detail_col2:
                            st.write(f"**Video ID:** `{video_data['video_id']}`")
                            st.write(f"**Channel ID:** `{video_data.get('channel_id', 'N/A')}`")
                        
                        # Engagement chart
                        if video_data.get('views') and video_data.get('likes'):
                            try:
                                views = int(video_data.get('views', 0)) if video_data.get('views', 0) != 'Private' else 0
                                likes = int(video_data.get('likes', 0)) if video_data.get('likes', 0) != 'Private' else 0
                                comments = int(video_data.get('comments', 0)) if video_data.get('comments', 0) != 'Private' else 0
                                
                                if views > 0:
                                    fig = go.Figure(data=[go.Pie(
                                        labels=['Views', 'Likes', 'Comments'],
                                        values=[views, likes, comments],
                                        marker=dict(colors=['#667eea', '#764ba2', '#f093fb'])
                                    )])
                                    fig.update_layout(title='Engagement Distribution', height=400)
                                    st.plotly_chart(fig, use_container_width=True)
                            except:
                                pass
                        
                        st.success("✅ Video analyzed successfully!")
                    else:
                        st.error(f"❌ {video_data['error']}")
                except Exception as e:
                    st.error(f"❌ Error analyzing video: {str(e)}")
                    print(f"Video Analytics Error: {e}")
        else:
            st.warning("⚠️ Please enter a video ID")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class='white-card' style='text-align: center;'>
    <p style='margin: 0; font-size: 1.1rem; font-weight: 600; color: #1a1a1a;'>🎯 YouTube Analytics Pro</p>
    <p style='margin: 0.5rem 0 0 0; color: #666;'>Powered by YouTube Data API v3 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
