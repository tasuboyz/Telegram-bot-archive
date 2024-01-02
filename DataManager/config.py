import logging

bot_token = '6260189061:AAGfrCYpQMhBrwVV5riAyH8ESYV5Q0fz4Kw' #token of test

#bot_token = '6067993693:AAFXGtO7iXsjxJK0dBv8YuT-zgNcpQTU06g'

admin_id = 1026795763

api_base_url = 'http://localhost:8081'  

log_file_path = 'log.txt'  

use_local_api = False  # Imposta su False se l'API non è in locale

log_level = logging.INFO  # Livello di logging desiderato


class FileExtensions:
    def __init__(self):
        self.folders = {
            '.jpg': 'foto',
            '.png': 'foto',
            '.pdf': 'pdf',
            '.xls': 'excel',
            '.xlsx': 'excel',
            '.zip' : 'Zip',
            '.html': 'Note',
            '.txt': 'Note'
            # Aggiungi qui altri tipi di file se necessario
        }

    def get_folder(self, extension):
        return self.folders.get(extension)
