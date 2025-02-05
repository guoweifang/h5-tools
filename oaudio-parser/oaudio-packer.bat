REM 設定 Python 腳本的路徑
set SCRIPT_PATH=.\oaudio.py

REM 呼叫 Python 並傳遞資料夾路徑參數
python "%SCRIPT_PATH%" "%~1"

REM 暫停以查看結果
pause