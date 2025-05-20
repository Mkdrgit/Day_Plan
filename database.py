import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('planner.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Günlük kayıtları tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS diary_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Etkinlikler tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def add_diary_entry(self, date, content):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO diary_entries (date, content, created_at)
            VALUES (?, ?, ?)
        ''', (date, content, created_at))
        self.conn.commit()
    
    def get_diary_entry(self, date):
        self.cursor.execute('''
            SELECT content FROM diary_entries
            WHERE date = ?
        ''', (date,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def add_event(self, date, title, description=""):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO events (date, title, description, created_at, is_done)
            VALUES (?, ?, ?, ?, 0)
        ''', (date, title, description, created_at))
        self.conn.commit()
    
    def get_events(self, date):
        self.cursor.execute('''
            SELECT id, title, description, is_done FROM events
            WHERE date = ?
        ''', (date,))
        return self.cursor.fetchall()
    
    def get_all_diary_entries(self):
        self.cursor.execute('''
            SELECT date, content FROM diary_entries
            ORDER BY date DESC
        ''')
        return self.cursor.fetchall()
    
    def mark_event_done(self, event_id):
        self.cursor.execute('''
            UPDATE events SET is_done = 1 WHERE id = ?
        ''', (event_id,))
        self.conn.commit()
    
    def delete_event(self, event_id):
        self.cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
        self.conn.commit()
    
    def delete_diary_entry(self, date):
        self.cursor.execute('DELETE FROM diary_entries WHERE date = ?', (date,))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close() 