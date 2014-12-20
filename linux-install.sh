#!/bin/sh
CWD=$(pwd)
#install selenium
pip install selenium -t $CWD/lib/python
#install bottle
pip install bottle -t $CWD/lib/python/bottle
#i don't know why bottle __init__.py is missing
if [ ! -f lib/python/bottle/__init__.py ]; then
    touch lib/python/bottle/__init__.py
fi

#create aliases
echo "alias pedant-screens='python $CWD/bin/pedant-screens'" >> ~/.bashrc
echo "alias pedant-crawler='python $CWD/bin/pedant-crawler'" >> ~/.bashrc
echo "alias pedant-server='python $CWD/bin/pedant-server'" >> ~/.bashrc
bash