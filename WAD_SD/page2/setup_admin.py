import sqlite3
import hashlib

def setup_admin_database():
    """
    Initializes the CozMoz database and registers the default administrator.
    """
    # Connect to the local CozMoz database file
    conn = sqlite3.connect('cozmoz_system.db')
    cursor = conn.cursor()

    # 1. Create the Users Table
    # This stores the credentials for the CozMoz management system.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # 2. Define Default Admin Credentials
    # These match the requested 'admin' and 'admin123' logic.
    DEFAULT_ADMIN_USER = "admin"
    DEFAULT_ADMIN_PASS = "admin123"
    
    # We use a simple role assignment for system-wide access[cite: 1].
    ADMIN_ROLE = "administrator"

    try:
        # Check if the admin already exists to prevent duplicate entries[cite: 1]
        cursor.execute("SELECT * FROM users WHERE username = ?", (DEFAULT_ADMIN_USER,))
        
        if not cursor.fetchone():
            # Insert the revised admin details into the database[cite: 1]
            cursor.execute('''
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', (DEFAULT_ADMIN_USER, DEFAULT_ADMIN_PASS, ADMIN_ROLE))
            
            conn.commit()
            print("-" * 30)
            print("COZMOZ SYSTEM INITIALIZATION")
            print("-" * 30)
            print(f"Success: Admin account '{DEFAULT_ADMIN_USER}' created.")
            print("Status: Database is ready for campus event management.")
        else:
            print("System Note: Admin account already exists. No changes made.")

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_admin_database()