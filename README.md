pedant-tool
==========

## [UBUNTU-Install]

### install pip,git
sudo apt-get install python-pip python-dev build-essential git

### clone this repository in your home directory, for example, ~/pedant-tool/
mkdir pedant-tool && git clone git@github.com:obmihail/pedant-tool.git ~/pedant-tool/

### install selenium for python
pip install --install-option="--install-purelib=~/pedant-tool/lib/python" -U selenium

### create aliases for checking
1. For creating temp aliases: type in your command line

- alias pedant='python ~/pedant-tool/bin/pedant.py'

- alias pedant-server='python ~/pedant-tool/bin/pedant-server.py'

2. For persistant aliases put this strings in your ~/.bashrc file

- alias pedant='python ~/pedant-tool/bin/pedant.py'

- alias pedant-server='python ~/pedant-tool/bin/pedant-server.py'


Wonderfull! Now you can use pedant!

## [Ubuntu-usage]

Try run pedant web-server
Now let's try start pedant-server
run "pedant-server" command
You should see this message:

"""
Bottle v0.13-dev server starting up (using WSGIRefServer())...
Listening on http://localhost:8081/
Hit Ctrl-C to quit.
"""

If you open http://localhost:8081/ in your browser you should see pedant main page and projects list


Now let's try tun cli-script:
- download and run [[phantomjs_run]] on localhost:4445

1. run this command: "cd ~/pedant_install_dir/test_project/ && pedant"
2. when you see "Pedant finished at".open page "http://localhost:8081/test_project/reports/last" in browser, you should see report for last scanning