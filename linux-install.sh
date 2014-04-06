#!/bin/sh
CWD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
 
#check system packages installed

#check os
os=$(uname)
echo
if [ "$os" = "Linux" ]; then
	echo "works with linux os"
	INSTALLED=$(dpkg -l \grep python python-dev python-pip)
fi
if [ "$os" = "Darwin" ]; then
	echo "works with mac os"
	INSTALLED="uzbagoysya"
fi

if [ "$INSTALLED" != "" ]; then
	echo "Required packages installed. Continue"
else
	echo "Required packages (python,python-dev) not found. Install its first."
	exit
fi

#install selenium
pip install selenium -t lib/python

#create dir for bottle
[ -d lib/python/bottle ] || mkdir lib/python/bottle

#install bottle
pip install bottle -t lib/python/bottle

#install behave
pip install behave -t lib/python/

#i don't know why bottle __init__.py is missing
[ -f lib/python/bottle/__init__.py ] || touch lib/python/bottle/__init__.py

#pil install
pip install Pillow -t lib/python/

bash