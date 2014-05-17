#!/bin/sh
CWD=$(pwd)
#install selenium
pip install --install-option="--install-purelib=$CWD/lib/python" -U selenium
#create aliases
echo "alias pedant-screens='python $CWD/bin/pedant-screens'" >> ~/.bashrc
echo "alias pedant-crawler='python $CWD/bin/pedant-crawler'" >> ~/.bashrc
echo "alias pedant-server='python $CWD/bin/pedant-server'" >> ~/.bashrc
bash