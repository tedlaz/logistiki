pyinstaller -F glog.py
copy .\dist\glog.exe .\venv\Scripts\.
rd /S /Q dist
rd /S /Q build
