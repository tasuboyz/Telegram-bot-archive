import os
from aiogram import types
import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('filemgr.db')
        self.c = self.conn.cursor()
        
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS files
                        (id INTEGER PRIMARY KEY, path TEXT)''')
        self.conn.commit()

    def insert_entry(self, path):
        self.create_table()
        self.c.execute("INSERT OR IGNORE INTO files (path) VALUES (?)", (path,))
        self.conn.commit()
        return self.c.lastrowid
    
    def update_entry(self, Id, new_path):
        self.c.execute("UPDATE files SET path = ? WHERE id = ?", (new_path, Id))
        self.conn.commit() 
    
    def get_entry(self, Id):
        self.create_table()
        self.c.execute('SELECT path FROM files WHERE id = ?', (Id,))
        row = self.c.fetchone()
        self.conn.commit()
        if row is not None:
            return row[0]
        else:
            return False
        
    def get_id(self, path):
        self.create_table()
        self.c.execute('SELECT id FROM files WHERE path = ?', (path,))
        row = self.c.fetchone()
        self.conn.commit()
        if row is not None:
            return row[0]
        else:
            return False

    def delete_entry(self, id):
        self.create_table()
        self.c.execute("DELETE FROM files WHERE id=?", (id,))
        self.conn.commit()

class UserInfo:
    def __init__(self, data):
        if isinstance(data, types.Message):
            user = data.from_user
            self.chat_id = data.chat.id
            self.message_id = data.message_id
            self.data = data.text
        elif isinstance(data, types.CallbackQuery):
            user = data.from_user
            self.chat_id = data.message.chat.id
            self.message_id = data.message.message_id
            self.data = data.data
        else:
            return None

        self.user_id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.language = user.language_code
