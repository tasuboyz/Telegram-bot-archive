REM Questo è un file batch per creare e attivare un ambiente virtuale Python
python -m venv env
call env\Scripts\activate
call pip install -r requirements.txt
call python main.py
