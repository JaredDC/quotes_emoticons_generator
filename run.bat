@echo off

::copy SourceHanSerif-Bold.ttc Release

cd Release
.\quotes_emoticons_generator.exe

xcopy "%USERPROFILE%\Pictures\quotes_emoticons" ..\quotes_emoticons /s /y /i /q
xcopy ..\quotes_emoticons quotes_emoticons /s /y /i /q

cd ..
"C:\Program Files\7-Zip\7z.exe" a quotes_emoticons_generator.7z Release
move /y quotes_emoticons_generator.7z Release\quotes_emoticons_generator.7z

pause
