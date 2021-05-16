@echo off

xcopy CelebrityQuotes.txt Release\ /y /i /q /d

cd Release
.\quotes_emoticons_generator.exe

cd ..
xcopy "%USERPROFILE%\Pictures\quotes_emoticons" Release\quotes_emoticons /s /y /i /q /d

pause
