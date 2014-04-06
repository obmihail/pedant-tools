import os,sys,json,pedant,re,hashlib,glob,shutil
from pedant import _DATA_STORAGE_DIR,get_json_from_file,put_json_to_file
from errors import PedantError

"""
Get existing project from ds dir
"""
def get_project(name,init=True):
	if init:
		return Project().load(name=name)#.decode('utf8'))
	return Project().init_pathes(name)

def get_empty_project():
	prj = Project()	
	prj.set_config(prj.get_default_config())
	return prj

"""
Create new project in ds dir
"""
def create_project(config, urls):
	#check project folder not exists
	prj = Project().set_config(config).set_urls(urls)
	if os.path.isdir( os.path.join( _DATA_STORAGE_DIR, prj.get_name() ) ):
		raise PedantError('Project with name %s already exists' % prj.get_name() )
	return prj.save()

"""
Linking project to sources_directory
pedant.json - required in sources_directory
"""
def register_project_dir(sources_directory):
	sources_directory = sources_directory.decode(sys.getfilesystemencoding())
	if not os.path.isdir(sources_directory):
		raise PedantError('Directory %s not exists'%sources_directory) 
	config_file = os.path.join(sources_directory,'pedant.json')
	#read config from file
	if os.path.isfile(config_file):
		#try reading
		with open (config_file, "r") as config_file_o:
			config_data=config_file_o.read().replace('\n', '')
		if len(config_data) > 1:
			try:
				config = get_json_from_file(config_file)
			except Exception as e:
				raise PedantError('Broken json config. Error %s'%str(e))
		else:
			config = {}
	else:
		raise PedantError('Project config (pedant.json) not found in directory %s'%sources_directory)
	config['name'] = config['name'] if config.has_key('name') else os.path.basename(sources_directory)
	prj = get_empty_project()
	#normalize config
	config = prj.validate_config(config)
	#check project already exists
	#
	path_for_prj = os.path.join(_DATA_STORAGE_DIR, config['name'])
	link_file_path = os.path.join(path_for_prj,'pedant.link.json')
	#check project with name already exists
	if os.path.isdir(path_for_prj):
		#check link file exists for project
		if os.path.isfile(link_file_path):
			#check link content
			try:
				link_content = get_json_from_file(link_file_path)
			except:
				link_content = {}
			if link_content.has_key('sources_directory') and os.path.isdir(link_content['sources_directory']) and link_content['sources_directory'] != sources_directory:
				raise PedantError('Project with name %s already registered in pedant. Change name or remove project'%config['name'])
		else:
			#raise project exists
			raise PedantError('Project with name %s already registered in pedant. Change name or remove project'%config['name'])
	#recreate link project
	#save normal config
	put_json_to_file(config_file,config)
	os.remove(link_file_path) if os.path.isfile(link_file_path) else None
	if not _DATA_STORAGE_DIR in sources_directory:
		put_json_to_file(link_file_path, {"sources_directory": sources_directory})
	return get_project(config['name']).save()

"""
	else:
		raise PedantError('Can not find config file in %s' % sources_directory)
	#validate config
	name = Project().set_config(config).get_name()
	link_file = os.path.join(_DATA_STORAGE_DIR, name, 'pedant.link.json')
	#try find existing link file for this directory
	for p_link_file in glob.glob(os.path.join(_DATA_STORAGE_DIR, '*', 'pedant.link.json')):
		prj_real_path = get_json_from_file(p_link_file)
		#link file for this dir already exists
		if prj_real_path["sources_directory"] == sources_directory.decode("utf-8"):
			return get_project(os.path.basename(os.path.dirname(p_link_file.decode("utf-8")))).set_config(config).save()
	#recreate link file
	os.remove(link_file) if os.path.isfile(link_file) else None
	put_json_to_file(link_file, {"sources_directory": sources_directory.decode('utf-8')})
	#resave normalized config for created project
	return get_project(name).save()
"""

"""
Get list of existing projects
returns list of projects: [ {'name':'blablabla', 'edit':True} ]
"""
def get_projects():
	return map(lambda name: {
	'name': os.path.basename( os.path.dirname(name) ),
	'id': os.path.basename( os.path.dirname(name) )
	},
	glob.glob( os.path.join( _DATA_STORAGE_DIR.decode('utf8') , '*' ,'' ) ) )

def delete_project(name):
	prj_dir = os.path.join(_DATA_STORAGE_DIR.decode('utf8'), name)
	if os.path.isdir(prj_dir):
		shutil.rmtree(prj_dir)
	else:
		raise PedantError("Project %s not found"%name)



class Project:

	url_regex = re.compile(
			r'^(?:http|ftp)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
			r'localhost|' #localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE )

	def __init__(self):
		self.config = {}
		self.urls = []
		self.name = False
		self.old_root_dir = False
		self.root_dir = ''
		self.sources_dir = ''
		pass

	def init_pathes(self, name):
		self.root_dir = os.path.join(pedant._DATA_STORAGE_DIR.decode('utf8'), name)
		self.link_file = os.path.join(self.root_dir, 'pedant.link.json')
		
		self.lock_file_path = os.path.join(self.root_dir , 'lock.file' )
		#sources location
		#print self.sources_dir, self.link_file
		if not len(self.sources_dir):
			if os.path.isfile(self.link_file):
				sources_dir = get_json_from_file(self.link_file)['sources_directory']
				if os.path.isdir(sources_dir):
					self.sources_dir = sources_dir
				else:
					raise PedantError('Sources directory %s not exists'%sources_dir)
			else:
				self.sources_dir = self.root_dir
		self.config_path = os.path.join(self.sources_dir , 'pedant.json')
		self.urls_path = os.path.join(self.sources_dir , 'urls.json')
		return self

	def get_root_dir(self):
		return self.root_dir

	def get_sources_dir(self):
		return self.sources_dir

	def get_pathes(self):
		return self.pathes

	def get_threads_count(self):
		return self.config['threads']

	def set_threads_count(self,value):
		self.config['threads'] = self.validate_threads(value)
		return self

	"""
	Load project sources by project name
	"""
	def load(self, name):
		self.init_pathes(name)
		#config
		if not os.path.isdir(self.root_dir):
			raise PedantError("Project '%s' not exists"%name)
		if os.path.isfile(self.config_path):
			self.old_root_dir = self.root_dir
			self.set_config(get_json_from_file(self.config_path))
		else:
			raise PedantError("Configuration file %s not found" % self.config_path )
		#urls
		self.set_urls(self.find_urls_in_directory(self.sources_dir))
		return self

	"""
	Set configuration for current project
	"""
	def set_config(self, config):
		self.config = self.validate_config(config)
		#store previously name for correct renaming
		self.name = self.config['name']
		self.init_pathes(self.name)
		return self

	def get_mode_params(self,modename):
		if self.config['modes'].has_key(modename):
			return (self.config['modes'][modename]['browsers'],self.config['modes'][modename]['states'])
		else:
			raise PedantError('Mode %s is unknown. Known modes: %s'%(modename,str(self.config['modes'].keys())))

	"""
	Set urls for current project
	"""
	def set_urls(self, urls):
		self.urls = self.validate_urls(urls)
		return self
	
	"""
	Get current project name
	"""	
	def get_name(self):
		return self.name

	def get_config(self):
		return self.config

	def get_urls(self):
		return self.urls

	def get_browsers(self):
		return self.config['browsers']

	def set_browsers(self, browsers):
		self.config['browsers'] = self.validate_browsers(browsers)
		return self

	def get_browsers_by_mode(self,mode):
		if self.config['modes'].has_key(mode):
			return self.get_browsers_by_ids( [ browser['id'] for browser in self.config['browsers'] if browser['id'] in self.config['modes'][mode]['browsers'] ] )
		raise PedantError("Mode %s not found in project configuration"%mode)

	def filter_browsers(self,ids):
		bro_list = []
		ids = list(ids)
		existing = [ browser['id'] for browser in self.config['browsers'] ]
		unknown = []
		for browser_id in list(ids):
			if browser_id not in existing:
				unknown.extend(browser_id)
			bro_list.extend( [ browser for browser in self.config['browsers'] if browser['id'] == browser_id ] )
		
		if unknown:
			raise PedantError("Browsers %s not found in %s. Check your configuration"%(unknown,str(self.config['browsers'])))
		#set browsers
		self.config['browsers'] = bro_list
		return self

	def validate_browsers(self,browsers):
		#check all browsers
		if not browsers:
			raise PedantError("Browsers is empty")
		checked = {}
		for browser in browsers:
			if checked.has_key(browser['id']):
				raise PedantError('Browser %s not unique '%browser['id'] )
			checked[ browser['id'] ] = browser['id']
			for key in ('id', 'desired_capabilities', 'type', 'description', 'wd_url'):
				if not browser.has_key(key):
					raise PedantError("Browser %s have not required key %s" %(str(browser), key))
		return browsers

	def update_config(self, config_part_dict):
		new_config = self.config.copy()
		new_config.update(config_part_dict)
		self.config = self.validate_config(new_config)
		return self

	def get_diffs_saving_value(self):
		return self.config['diffs_saving']

	"""
	Config validator
	"""
	def validate_config(self, config):
		corrected_config = self.get_default_config()
		corrected_config.update(config)
		corrected_config['browsers'] = self.validate_browsers(corrected_config['browsers'])
		#check modes not empty and has existing browsers
		for modename,mode in corrected_config['modes'].iteritems():
			if not mode.has_key('browsers'):
				mode['browsers'] = []
			for browser in mode['browsers']:
				if [bro for bro in corrected_config['browsers'] if bro['id'] == browser]:
					pass
				else:
					raise PedantError("Unknown browser (%s) in mode (%s)"%(browser,mode))
			if not mode.has_key('states'):
				mode['states'] = []

		#check project name
		normalized_name = re.sub('[\[\]/\;,><&*:%=+@!#^()|?^\s]', '_', corrected_config['name'])
		if (len(normalized_name) < 1):
			raise PedantError('Project name %s is invalid'%corrected_config['name'])
		corrected_config['name'] = normalized_name
		#check threads value
		corrected_config['threads'] = self.validate_threads(corrected_config['threads'])
		#check base url
		if not self.url_regex.match(corrected_config['base_url']):
			raise PedantError( 'Base url (%s) is invalid' %corrected_config['base_url'] )
		return corrected_config

	def validate_threads(self,value):
		value = int(value)
		return 1 if value < 1 else value

	def make_full_url(self,url):
		if not self.url_regex.match(url):
			if url.startswith('/') and self.config['base_url'].endswith('/'):
				return self.config['base_url'] + url[1:]
			else:
				return self.config['base_url'] + url
		else:
			return url

	"""
	Urls validator
	"""
	def validate_urls(self, urls):
		#check urls format
		for url in urls:
			if not self.url_regex.match(url):
				#make abs url
				url = self.make_full_url(url)
				#validate abs url
				if not self.url_regex.match(url):
					raise PedantError( ' Url (%s) is invalid' % url )
		return urls

	""" 
	Make items dicts [ {url:'','id':''},{url:'','id':''} ] from list [ 'url1' , 'url2' , 'url3' ]
	"""
	def convert_urls_to_items(self, urls_list):
		items = []
		for url in urls_list:
			if not len(url):
				continue
			id = hashlib.sha1(url).hexdigest()
			#full url
			items.append( { 'url' : self.make_full_url(url), 'id' : id, 'description': '' } )
		return items

	"""
	Get list of urls. Urls forming from file urls.json and static htm, html files
	"""
	def find_urls_in_directory( self, search_directory ):
		local_sources_path = os.path.join( search_directory , 'urls.json' )
		urls = []
		#get all sources from file urls.json
		if os.path.isfile(local_sources_path):
			urls = get_json_from_file( local_sources_path )
		#find all static files in search_directory
		"""
		files = []
		for file_type in ('*.html','*.htm'):
			files.extend( glob.glob( os.path.join( search_directory , file_type )) )
		for item in files:
			item_name = os.path.basename(item)
			urls.append( self.config['url_mask'].replace( '#ITEM_NAME#', item_name ).replace( '#PRJ_ID#' , self.config['name'] ))
		"""
		#validate all urls
		self.validate_urls(urls)
		#return checking items
		return urls

	"""
	Get all items for this project
	"""
	def get_items_for_scanning(self):
		return self.convert_urls_to_items(self.urls)

	"""
	Save config to pedant.json file
	"""
	def save_config(self):
		#rename folder if project name changed
		#print self.root_dir,self.old_root_dir
		if self.root_dir != self.old_root_dir and self.old_root_dir != False:
			#rename folder
			if os.path.isdir(self.root_dir):
				raise PedantError("Project with this name (%s) already exists"%self.name)
			os.rename(self.old_root_dir, self.root_dir)
		put_json_to_file(self.config_path, self.config)
		return self

	"""
	Save urls to urls.json file
	"""
	def save_urls(self):
		put_json_to_file(self.urls_path, self.urls)
		return self

	"""
	Save urls and config
	"""
	def save(self):
		self.save_config()
		self.save_urls()
		return self

	"""
	Remove current project
	"""
	def remove(self):
		if os.path.isdir(self.root_dir):
			shutil.rmtree(self.root_dir)
		else:
			raise PedantError('Project directory %s not found' %self.root_dir )
		return True

	"""
	Lock project
	"""
	#create lock file
	def lock(self):
		if os.path.isfile(self.lock_file_path):
			raise PedantError('Project locked. Lock file: %s'%self.lock_file_path)
		#create lock file
		with open(self.lock_file_path, 'a'):
			os.utime(self.lock_file_path, None)
		return self

	"""
	Unlock project
	"""
	def unlock(self):
		if os.path.isfile( self.lock_file_path ):
			os.remove( self.lock_file_path )
		return self

	"""
	Project access to write and other operations
	"""
	def access(self):
		return not os.path.isfile( self.lock_file_path ) and os.path.isdir(self.root_dir) and os.access(self.root_dir, os.W_OK)

	def get_default_config(self):
		return get_json_from_file( os.path.join( os.path.dirname(os.path.realpath(__file__)) , "default.conf.json" ) )