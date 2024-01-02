from aiogram.filters.state import State, StatesGroup

class MoveFileState(StatesGroup):
    current_path = State()
    file_name = State()
    folder_name = State()
    destination_path = State()

class CreateFolderState(StatesGroup):
    name = State()
    
class RenameState(StatesGroup):
    rename = State()

class DeleteState(StatesGroup):
    current_path = State()




