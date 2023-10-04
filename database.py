import sqlite3
import pickle
from tkinter import simpledialog, messagebox
from constants import DATABASE_FILE, SECURITY_CODE

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, encoding TEXT)''')

    conn.commit()
    conn.close()

def load_known_users():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM users")
    rows = cursor.fetchall()
    known_names = []
    known_encodings = []

    for row in rows:
        name, encoding_blob = row
        encoding_bytes = bytes(encoding_blob)
        encodings = pickle.loads(encoding_bytes)
        known_names.append(name)
        known_encodings.extend(encodings)

    conn.close()
    return known_names, known_encodings

def insert_user(name, encodings):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    encoding_bytes = pickle.dumps(encodings)
    cursor.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (name, sqlite3.Binary(encoding_bytes)))

    conn.commit()
    conn.close()

def reset_database():
    security_code = simpledialog.askstring("Security Code", "Enter the security code to reset the database:")
    if security_code == SECURITY_CODE:
        confirm_reset = messagebox.askyesno("Reset Database", "Are you sure you want to reset the database?")
        if confirm_reset:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM users")
            conn.commit()
            conn.close()
            messagebox.showinfo("Database Reset", "Database reset completed.")
        else:
            messagebox.showinfo("Database Reset", "Database reset canceled.")
    else:
        messagebox.showwarning("Database Reset", "Database reset canceled.")
