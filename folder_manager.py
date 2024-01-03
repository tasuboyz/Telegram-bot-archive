import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import shutil
import sqlite3
import requests
from aiohttp import client
import concurrent.futures
import time
import json
from DataManager import config

class FolderManager:
    def __init__(self, base_path, bot, db):
        self.base_path = base_path
        self.current_path = base_path
        self.conn = sqlite3.connect('filemgr.db')
        self.c = self.conn.cursor()
        self.bot = bot
        self.db = db

    def list_entries(self, filter_text, page):
        items_per_page = 25
        entries = os.listdir(self.current_path)
        entries = [entry for entry in entries if not filter_text or filter_text in entry]

        start_index = page * items_per_page
        end_index = start_index + items_per_page
        buttons = []
    
        keyboard_buttons = []

        for entry in entries[start_index:end_index]:
            entry_path = os.path.join(self.current_path, entry)
            p = self.db.insert_entry(entry_path)  # Insert the entry into the database and get its unique ID
            i = self.db.get_id(entry_path)
            callback_data = f"folder_entry:{i}" if os.path.isdir(entry_path) else f"file_action:{i}"
            button_text = f"📁 {entry}, {i}" if os.path.isdir(entry_path) else f"📄 {entry}"
        
            if os.path.isdir(entry_path):
                keyboard_buttons.append([InlineKeyboardButton(text=f"📁 {entry}", callback_data=f"folder_entry:{i}"),
                                         InlineKeyboardButton(text=f"🔍 {entry}", callback_data=f"folder_action:{i}")])
            else:
                keyboard_buttons.append([InlineKeyboardButton(text=f"📄 {entry}", callback_data=f"file_action:{i}")])

        if page > 0:
            keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Previus", callback_data=f"prev_page:{page-1}")])

        if end_index < len(entries):
            keyboard_buttons.append([InlineKeyboardButton(text="Next ➡️", callback_data=f"next_page:{page+1}")])

        if self.current_path != self.base_path:
            keyboard_buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back")])

        keyboard_buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard

    async def ReciveImage(self, message):
        chat_id = message.chat.id
        try:           
            loading_message = await self.bot.send_message(chat_id, "File upload in progress...")
            if message.document or message.photo or message.animation:
                file = message.document or message.photo[-1] or message.animation
                file_info = await self.bot.get_file(file.file_id)
                file_path = file_info.file_path                
                original_file_name = file.file_name if hasattr(file, 'file_name') else file_path.split("/")[-1]

                # Ottieni il percorso della directory del tuo script
                script_dir = os.path.dirname(os.path.realpath(__file__))

                # Crea il percorso completo dove salvare il file
                save_path = os.path.join(script_dir, original_file_name)

                # start_time = time.time()
                if config.use_local_api == False:
                    await self.bot.download_file(file_path, save_path)
                else:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        executor.submit(shutil.move, file_path, save_path)
                
                file_size = os.path.getsize(save_path) / (1024 * 1024)  # Dimensione del file in MB
        
                return save_path, original_file_name
            return None
        finally:
            await self.bot.delete_message(chat_id, message.message_id)   
            await self.bot.delete_message(chat_id, loading_message.message_id)
     
    def list_folders(self):
        entries = os.listdir(self.current_path)
        folders = []
        buttons = []

        for entry in entries:
            entry_path = os.path.join(self.current_path, entry)
            if os.path.isdir(entry_path):
                unique_id = self.db.get_id(entry_path)  # get the id from the database or insert if not exists
                folders.append((entry, unique_id))  # store the folder name and its unique id

        keyboard_buttons = []

        for folder in folders:
            folder_name, folder_id = folder
            keyboard_buttons.append([
                InlineKeyboardButton(text=f"📁 {folder_name}, {folder_id}", callback_data=f"enter_folder:{folder_id}"),
                InlineKeyboardButton(text=f"✅ {folder_name}, {folder_id}", callback_data=f"move_to_folder:{folder_id}")
            ])

        # Aggiungi bottoni di cancellazione e indietro
        if self.current_path != self.base_path:
            keyboard_buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back")])

        keyboard_buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        return keyboard

    def handle_callback(self, callback):
        if callback.startswith("move:"):
            folder_id = int(callback.split(":")[-1])
            folder_name = self.get_entry(folder_id)
            if folder_name:
                self.change_folder(folder_name)

    def file_actions(self, file_id):
        buttons = []
        buttons.append(
        [
            InlineKeyboardButton(text="📥 Upload", callback_data=f"get:{file_id}"),
            InlineKeyboardButton(text="✏️ Rename", callback_data=f"rename:{file_id}")
        ])
        buttons.append(
        [
            InlineKeyboardButton(text="📂 Move", callback_data=f"move:{file_id}"),
            InlineKeyboardButton(text="🗑️ Delate", callback_data=f"delete:{file_id}")
        ])
        buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back")])
        buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")])        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    def folder_actions(self, folder_id):
        buttons = []
        buttons.append(
        [
            InlineKeyboardButton(text="📥 Upload", callback_data=f"get:{folder_id}"),
            InlineKeyboardButton(text="✏️ Rename", callback_data=f"rename:{folder_id}")
        ])
        buttons.append(
        [
            InlineKeyboardButton(text="📂 Move", callback_data=f"move:{folder_id}"),
            InlineKeyboardButton(text="🗑️ Delate", callback_data=f"delete:{folder_id}")
        ])        
        buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back")])
        buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    def change_folder(self, folder_name):
        new_path = os.path.join(self.current_path, folder_name)
        if os.path.isdir(new_path):
            self.current_path = new_path
            return True
        else:
            return False

    def go_back(self):
        if self.current_path != self.base_path:
            self.current_path = os.path.dirname(self.current_path)
            return True
        else:
            return False

    def save_file(self, file_path, base_dir):
        # Ottieni l'estensione del file
        _, extension = os.path.splitext(file_path)

        file_extensions = config.FileExtensions()
        folder = file_extensions.get_folder(extension)

        if folder:
            dest_dir = os.path.join(base_dir, folder)
            os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            shutil.move(file_path, dest_path)
        else:
            _, file_name = os.path.split(file_path)

            existing_file_path = self.file_exists_in_subfolders(base_dir, file_name)

            if existing_file_path:
                # Se il file esiste già, rimuovilo
                os.remove(existing_file_path)
                # Sposta il nuovo file nella posizione del vecchio
                shutil.move(file_path, existing_file_path)
        
    def file_exists_in_subfolders(self, base_dir, file_name):
        for root, dirs, files in os.walk(base_dir):
            if file_name in files:
                return os.path.join(root, file_name)
        return None


