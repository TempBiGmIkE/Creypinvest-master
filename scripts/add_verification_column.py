import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info('users_profile')")
        cols = [row[1] for row in cur.fetchall()]
        if 'verification_level' in cols:
            print('Column "verification_level" already exists in users_profile')
            return
        # Add the column with default 0
        cur.execute("ALTER TABLE users_profile ADD COLUMN verification_level integer NOT NULL DEFAULT 0;")
        conn.commit()
        print('Added column verification_level to users_profile')
    except Exception as e:
        print('Error updating database:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
