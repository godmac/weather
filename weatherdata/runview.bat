@echo on

REM echo ��ǰ�̷���%~d0
REM echo ��ǰ�̷���·����%~dp0
REM echo ��ǰ������ȫ·����%~f0
REM echo ��ǰ�̷���·���Ķ��ļ�����ʽ��%~sdp0
REM echo ��ǰCMDĬ��Ŀ¼��%cd%

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
