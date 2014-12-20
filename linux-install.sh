#!/bin/sh
CWD=$(pwd)
#install selenium
pip install selenium -t $CWD/lib/python
#create aliases
echo "alias pedant-screens='python $CWD/bin/pedant-screens'" >> ~/.bashrc
echo "alias pedant-crawler='python $CWD/bin/pedant-crawler'" >> ~/.bashrc
echo "alias pedant-server='python $CWD/bin/pedant-server'" >> ~/.bashrc
bash