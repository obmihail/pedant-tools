#!/bin/sh
CWD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
 
#install selenium
pip install selenium -t lib/python

#create dir for bottle
[ -d lib/python/bottle ] || mkdir lib/python/bottle

#install bottle
pip install bottle -t lib/python/bottle >> /dev/null

#i don't know why bottle __init__.py is missing
[ -f lib/python/bottle/__init__.py ] || touch lib/python/bottle/__init__.py

#create aliases
echo "alias pedant-screens='python \"$CWD/bin/pedant-screens\"'" >> ~/.bashrc
echo "alias pedant-crawler='python \"$CWD/bin/pedant-crawler\"'" >> ~/.bashrc
echo "alias pedant-server='python \"$CWD/bin/pedant-server\"'" >> ~/.bashrc
bash