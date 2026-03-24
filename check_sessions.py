"""
Check practice sessions with dates
"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('speech_therapy.db')
cursor = conn.cursor()

print("=" * 60)
print("PRACTICE SESSIONS WITH DATES")
print("=" * 60)

cursor.execute("""
    SELECT id, user_id, clarity_score, created_at 
    FROM practice_sessions 
    ORDER BY created_at DESC
""")

sessions = cursor.fetchall()

if sessions:
    for session in sessions:
        session_id, user_id, score, created_at = session
        print(f"\nSession ID: {session_id}")
        print(f"  User ID: {user_id}")
        print(f"  Score: {score}%")
        print(f"  Created: {created_at}")
        
        # Parse the date
        try:
            dt = datetime.fromisoformat(created_at.replace(' ', 'T'))
            print(f"  Date only: {dt.date()}")
        except:
            print(f"  Date only: {created_at.split()[0]}")
else:
    print("No sessions found")

# Count unique dates
cursor.execute("""
    SELECT DISTINCT DATE(created_at) as practice_date
    FROM practice_sessions
    ORDER BY practice_date DESC
""")

unique_dates = cursor.fetchall()
print("\n" + "=" * 60)
print(f"UNIQUE PRACTICE DATES: {len(unique_dates)}")
print("=" * 60)
for date in unique_dates:
    print(f"  - {date[0]}")

conn.close()
