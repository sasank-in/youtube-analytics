#!/usr/bin/env python
"""
RESET AND VERIFY DATABASE SCHEMA
Delete all database files and recreate with correct schema
"""

import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 100)
print("DATABASE RESET AND VERIFICATION")
print("=" * 100 + "\n")

# Step 1: Find and delete all database files
print("[STEP 1] Finding and deleting all database files...")

search_patterns = [
    "*.db",
    "*.sqlite",
    "youtube_analytics.db*"
]

deleted_files = []
for pattern in search_patterns:
    for file_path in glob.glob(pattern):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"  ✅ Deleted: {file_path}")
        except Exception as e:
            print(f"  ⚠️ Could not delete {file_path}: {e}")

if not deleted_files:
    print(f"  No database files found to delete")

# Step 2: Check current directory
print(f"\n[STEP 2] Current working directory:")
cwd = os.getcwd()
print(f"  {cwd}")

# Step 3: Verify config settings
print(f"\n[STEP 3] Checking config settings...")
try:
    from youtube_analytics.config import DB_URL, PROJECT_ROOT
    print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"  DB_URL: {DB_URL}")
    
    # Extract file path from URL
    if "sqlite://" in DB_URL:
        db_path = DB_URL.replace("sqlite:///", "")
        db_path = os.path.abspath(db_path)
        print(f"  Absolute DB path: {db_path}")
        
        # Check if it exists
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"  ✅ Deleted absolute path database")
            except Exception as e:
                print(f"  ⚠️ Could not delete: {e}")
except Exception as e:
    print(f"  Error checking config: {e}")

# Step 4: Import models and create fresh database
print(f"\n[STEP 4] Creating fresh database with correct schema...")
try:
    # This will recreate the database with the current models
    from youtube_analytics.database import DatabaseManager, Base, Channel, Video
    
    print(f"  Channel model columns:")
    for col in Channel.__table__.columns:
        print(f"    - {col.name}")
    
    print(f"  Video model columns:")
    for col in Video.__table__.columns:
        print(f"    - {col.name}")
    
    # Initialize database
    db = DatabaseManager()
    
    print(f"\n  ✅ Database created successfully")
    
except Exception as e:
    print(f"  ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Verify schema
print(f"\n[STEP 5] Verifying created schema...")
try:
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    tables = inspector.get_table_names()
    print(f"  Tables: {tables}")
    
    # Check videos table columns
    if "videos" in tables:
        columns = inspector.get_columns("videos")
        print(f"\n  Videos table columns:")
        for col in columns:
            col_name = col['name']
            col_type = col['type']
            nullable = col['nullable']
            print(f"    - {col_name}: {col_type} (nullable={nullable})")
        
        # Check if channel_title exists
        column_names = [c['name'] for c in columns]
        if 'channel_title' in column_names:
            print(f"\n  ✅ channel_title column exists in videos table!")
        else:
            print(f"\n  ❌ channel_title column is MISSING from videos table!")
            print(f"  This is the problem - need to fix the model or database")
    
    # Check channels table
    if "channels" in tables:
        columns = inspector.get_columns("channels")
        print(f"\n  Channels table columns:")
        for col in columns:
            col_name = col['name']
            col_type = col['type']
            nullable = col['nullable']
            print(f"    - {col_name}: {col_type} (nullable={nullable})")
        
except Exception as e:
    print(f"  Error inspecting schema: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 100)
print("DATABASE RESET COMPLETE")
print("=" * 100 + "\n")
