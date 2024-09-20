@echo off
REM 檢查是否有拖曳資料夾進來
if "%1"=="" (
    echo 請將資料夾拖曳到此 BAT 檔案上。
    pause
    exit /b
)

REM 設定 Python 腳本的路徑
set SCRIPT_PATH=.\main.py

REM 呼叫 Python 並傳遞資料夾路徑參數
python "%SCRIPT_PATH%" "%~1"

REM 暫停以查看結果
pause