@echo off

copy CelebrityQuotes.txt Release

cd Release
.\quotes_emoticons_generator.exe

cd ..
xcopy "%USERPROFILE%\Pictures\quotes_emoticons" quotes_emoticons /s /y /i /q
xcopy quotes_emoticons Release\quotes_emoticons /s /y /i /q

del Release\quotes_emoticons_generator.7z
"C:\Program Files\7-Zip\7z.exe" a quotes_emoticons_generator.7z Release
move /y quotes_emoticons_generator.7z Release\quotes_emoticons_generator.7z

pause
