"""
Database migration script to add new columns
"""
import sqlite3

def migrate_database():
    conn = sqlite3.connect('speech_therapy.db')
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    try:
        # Add audio_file_path column to practice_sessions
        cursor.execute("""
            ALTER TABLE practice_sessions 
            ADD COLUMN audio_file_path TEXT
        """)
        print("✅ Added audio_file_path column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("⚠️  audio_file_path column already exists")
        else:
            print(f"❌ Error adding audio_file_path: {e}")
    
    try:
        # Add notes column to practice_sessions
        cursor.execute("""
            ALTER TABLE practice_sessions 
            ADD COLUMN notes TEXT
        """)
        print("✅ Added notes column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("⚠️  notes column already exists")
        else:
            print(f"❌ Error adding notes: {e}")
    
    try:
        # Create user_goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_type TEXT NOT NULL,
                target_sessions INTEGER NOT NULL,
                current_progress INTEGER DEFAULT 0,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("✅ Created user_goals table")
    except sqlite3.OperationalError as e:
        print(f"⚠️  user_goals table: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database migration completed successfully!")
    print("You can now restart the backend server.")

if __name__ == "__main__":
    migrate_database()
