import os,sys

cmd_folder = os.path.realpath( __file__ + '/../../lib/python/' )
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

from pedant.cli_app import Application 