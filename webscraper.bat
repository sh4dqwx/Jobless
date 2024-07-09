@echo off
setlocal

set "dir=%~dp0"
call "%dir%webscraper\.venv\Scripts\activate.bat"
pip install -r "%dir%webscraper\requirements.txt"
python "%dir%webscraper\main.py" >> "%dir%logs\webscraper.log" 2>&1
call deactivate

endlocal