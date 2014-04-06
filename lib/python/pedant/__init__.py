import os,json,imp,time,sys

_DATA_STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'web', 'data_storage'))

def put_json_to_file(filepath, data):
	if not os.path.isdir(os.path.dirname(filepath)):
		os.makedirs(os.path.dirname(filepath))
	with open(filepath, 'wb') as data_file:
		json.dump(data, data_file)

def get_json_from_file(json_file):
	with open(json_file) as data_file:
		data = data_file.read()#json.load(data_file)
	return json.loads(data.decode(sys.getfilesystemencoding()))

"""
Create directory by filepath
return string - path
"""
def create_folder_for_file( path ):
	if os.path.isdir(os.path.dirname(path)) == False:
		os.makedirs(os.path.dirname(path), 0777)
	return path

"""
Load and return module from file
"""
def load_module_from_file(filepath):
	name = os.path.basename(os.path.splitext(filepath)[0])
	unique_name = ('%s_%s'%(time.time(),name)).replace('.','_')
	fp, pathname, description = imp.find_module(name, [os.path.dirname(filepath)])
	try:
		#load module
		return imp.load_module(unique_name, fp, filepath, description)
	finally:
		fp.close if fp else None