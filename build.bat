@echo off
rd /s /q Release
md Release

copy SourceHanSerif-Bold.ttc Release
copy CelebrityQuotes.txt     Release

pyinstaller  -F -i quotes_emoticons_generator.ico quotes_emoticons_generator.py
move /y dist\quotes_emoticons_generator.exe Release\quotes_emoticons_generator.exe

::pyinstaller  -F -w -i quotes_emoticons_generator.ico quotes_emoticons_generator.py
::move /y dist\quotes_emoticons_generator.exe Release\quotes_emoticons_generator.exe

echo "********************built********************"

::clean
echo "********************cleaning temp files********************"
rd /s /q build
rd /s /q __pycache__
del /q quotes_emoticons_generator.spec
rd /s /q dist


echo "********************succeed********************"

pause
