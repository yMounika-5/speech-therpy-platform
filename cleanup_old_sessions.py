"""
Clean up old test sessions
"""
import sqlite3
from datetime import datetime, date

conn = sqlite3.connect('speech_therapy.db')
cursor = conn.cursor()

print("=" * 60)
print("CLEANUP OLD SESSIONS")
print("=" * 60)

# Show current sessions
cursor.execute("""
    SELECT id, user_id, clarity_score, created_at 
    FROM practice_sessions 
    ORDER BY created_at DESC
""")

sessions = cursor.fetchall()
print(f"\nTotal sessions: {len(sessions)}")

today = date.today()
print(f"Today's date: {today}")

# Ask which sessions to keep
print("\nSessions:")
for session in sessions:
    session_id, user_id, score, created_at = session
    session_date = created_at.split()[0]
    print(f"  [{session_id}] Date: {session_date}, Score: {score}%")

print("\nOptions:")
print("1. Keep only today's sessions")
print("2. Keep all sessions")
print("3. Delete specific session by ID")

choice = input("\nEnter your choice (1/2/3): ").strip()

if choice == "1":
    # Delete sessions not from today
    cursor.execute("""
        DELETE FROM practice_sessions 
        WHERE DATE(created_at) != ?
    """, (str(today),))
    deleted = cursor.rowcount
    conn.commit()
    print(f"\n✅ Deleted {deleted} old session(s)")
    print(f"✅ Kept only today's sessions")
    
elif choice == "2":
    print("\n✅ No changes made")
    
elif choice == "3":
    session_id = input("Enter session ID to delete: ").strip()
    cursor.execute("DELETE FROM practice_sessions WHERE id = ?", (session_id,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"\n✅ Deleted session {session_id}")
    else:
        print(f"\n❌ Session {session_id} not found")
else:
    print("\n❌ Invalid choice")

conn.close()
print("\n" + "=" * 60)
