import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create Patients table
c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        disease TEXT
    )
''')

# Optional: Create Doctors table now too
c.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        contact TEXT
    )
''')

conn.commit()
conn.close()

print("✅ Tables created successfully!")