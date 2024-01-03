import logging

bot_token = 'YOUR-TOKEN' #token of test

#bot_token = 'YOUR-TOKEN' #token of production

admin_id = 'YOUR-CHAT_ID'

api_base_url = 'http://localhost:8081'  

log_file_path = 'log.txt'  

use_local_api = False   # Set to False if the API is not in local

log_level = logging.INFO  # Desired logging level, INFO, ERROR OR DEBUG


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
            # Add other file types here if needed
            # here is where the files are saved in the folders listed
        }

    def get_folder(self, extension):
        return self.folders.get(extension)
