ECHO OFF 
::CMD will no longer show us what command its executing(cleaner)
ECHO Pedant for windows
:: SET PATH=%PATH%;%~dp0\..\..\Portable_Python_2.7.6.1\
SET PATH=%PATH%;%~dp0\..\Portable_Python_2.7.6.1_Windows\
%~dp0\..\Portable_Python_2.7.6.1_Windows\Python-Portable.exe %~dp0\pedant-server
PAUSE 
