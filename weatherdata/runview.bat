@echo on

REM echo 当前盘符：%~d0
REM echo 当前盘符和路径：%~dp0
REM echo 当前批处理全路径：%~f0
REM echo 当前盘符和路径的短文件名格式：%~sdp0
REM echo 当前CMD默认目录：%cd%

set TARGETDISK=%~d0

set WEATHER_HOME=%~dp0

echo TARGETDISK:%TARGETDISK%

echo WEATHER_HOME=%WEATHER_HOME%


echo %CURRENTDIR%\runbase.bat

call %WEATHER_HOME%\runbase.bat



%TARGETDISK%



cd %WEATHER_HOME%

start %PYTHON_HOME%\python.exe main.py




pause
