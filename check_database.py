"""
Quick script to check if database tables exist and show data
"""
import sqlite3

# Connect to database
conn = sqlite3.connect('speech_therapy.db')
cursor = conn.cursor()

print("=" * 60)
print("DATABASE CHECK")
print("=" * 60)

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\n📊 Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check users
print("\n👥 Users:")
cursor.execute("SELECT id, username, email FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")

# Check practice sessions
print("\n🎤 Practice Sessions:")
try:
    cursor.execute("SELECT id, user_id, clarity_score, pronunciation, created_at FROM practice_sessions")
    sessions = cursor.fetchall()
    if sessions:
        for session in sessions:
            print(f"  Session ID: {session[0]}, User ID: {session[1]}, Score: {session[2]}, Rating: {session[3]}, Date: {session[4]}")
    else:
        print("  No practice sessions found yet.")
except sqlite3.OperationalError as e:
    print(f"  ⚠️  Error: {e}")
    print("  The practice_sessions table might not exist yet.")

conn.close()

print("\n" + "=" * 60)
print("✅ Database check complete!")
print("=" * 60)
