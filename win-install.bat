set OLDDIR=%CD%

pip install selenium -t lib\python


:: create dir for bottle

pip install bottle -t lib\python\bottle

:: install behave

pip install behave -t lib\python\

:: i don't know why bottle __init__.py is missing

if exist lib\python\bottle\__init__.py goto _nocreate

:: Create the zero-byte file

type nul>lib\python\bottle\__init__.py

:_nocreate

:: pillow install

pip install Pillow -t lib\python\

pause