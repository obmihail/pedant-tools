import time,Worker,sys,datetime,json,os,re,glob,threading,ctypes, shutil

class Application:
	
	def __init__(self):	
		#workers list
		self.workers = []
		self.timestamp = ''
		self.lock_file_path = ''
		#browsers configs for scanning
		self.browsers = []
		self.runned = False
		#items list for scanning
		self.items = []
		self.log_file = False
		#prev_mess_len
		self.prev_mess_len = 0

	def configure(self, config, mode, timestamp = False ):
		#current timestamp
		self.timestamp = time.time() if timestamp == False else timestamp
		
		#create working directory if not exists
		os.makedirs( config['data_storage_root'] ) if not os.path.isdir( config['data_storage_root'] ) else None
		
		if ( config.has_key('logging') and config['logging'] is True ):
			#filepath
			self.log_file = os.path.join( config['data_storage_root'] , 'logs' , '%s.log' % str( self.timestamp ) )
			#create dir
			os.makedirs( os.path.dirname( self.log_file ) ) if not os.path.isdir( os.path.dirname( self.log_file ) ) else None

		self.config = config
		self.lock_file_path = os.path.join( config['data_storage_root'] , 'lock.file' )
		browsers = self.reconfigureBrowsers( config['modes'][ mode ] )
		self.items = config['urls']
		
		#optimisation hack. if we have one browser - chunk items for workers and create workers
		if ( len( browsers ) == 1):
			#calculate workers count for items
			workers_cnt = self.calculate_workers_by_items( config['urls'] )
			if workers_cnt > config['max_workers']:
				workers_cnt = config['max_workers']
			items = self.chunkList(config['urls'],workers_cnt)
			self.total_count = len(config['urls'])
			browsers = [ browsers for bro in range(workers_cnt) if True ][0]
			for i in range( workers_cnt ):
				inst = Worker.Worker( browsers[0] , items[i] , self.timestamp , config['data_storage_root'] )
				self.workers.append( inst )

		#else create workers by browsers count
		else:
			#calculate needle workers count
			workers_cnt = len( browsers )
			if workers_cnt > config['max_workers']:
				workers_cnt = config['max_workers']
			browsers = self.chunkList( browsers,workers_cnt )
			self.total_count = workers_cnt * len(config['urls'])
			for i in range( workers_cnt ):
				inst = Worker.Worker( browsers[i][0] , config['urls'], self.timestamp, config['data_storage_root'] )
				self.workers.append( inst )

		return self

	def symlink(self, source, link_name):
		os_symlink = getattr(os, "symlink", None)
		if callable(os_symlink):
			os_symlink(source, link_name)
		else:
			csl = ctypes.windll.kernel32.CreateSymbolicLinkW
			csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
			csl.restype = ctypes.c_ubyte
			flags = 1 if os.path.isdir(source) else 0
			if csl(link_name, source, flags) == 0:
				raise ctypes.WinError( descr='Sorry. Symlink not created. You can find solution in project wiki on github.' )

	def create_symlinks( self, source_dir, prj_root = False ):
		if not prj_root:
			prj_root = self.config['data_storage_root']
		if not os.path.isdir( prj_root ):
			os.makedirs( prj_root, 0777 )
		for filename in ( 'pedant.json', 'urls.json', 'PedantHooks.py' ):
			if os.path.isfile( source_dir + os.sep + filename ):
				if ( os.path.isfile( prj_root + os.sep + filename ) ):
					os.remove( prj_root + os.sep + filename )
				self.symlink( source_dir + os.sep + filename, prj_root + os.sep + filename )

	def reconfigureBrowsers( self, browsers ):
		#set uniq keys
		setted = {}

		for browser in browsers:
			#unid generation
			if setted.has_key( browser[ 'unid' ] ):
				print '>Warn pedant find duplicate browser unid in current configuration. Use last browser: %s ' % unid
			if not browser.has_key( 'info' ):
				browser['info'] = 'no info'
			setted[ browser[ 'unid' ] ] = browser
		return setted.values()

	# make url dicts [ {} , {} ] from list [ 'url1' , 'url2' , 'url3' ]
	def make_urls_from_list( self, urls_list ):
		reconfigured = []
		for url in urls_list:
			name = re.sub('[^0-9a-zA-Z_]+', '_', url)
			reconfigured.append(
					{
						'url' : url,
						'name' : name,
						'unid' : name,
						'scripts' : [],
						'wait_scripts' : [],
					} )
		return reconfigured

	#get list for sources needle scanning
	def find_sources_in_directory( self, search_directory, file_types = ('*.html','*.htm'), mask = '' , prj_name = '' ):
		local_sources_path = os.path.join( search_directory , 'urls.json' )
		sources = []
		#get all sources from file urls.json
		if os.path.isfile(local_sources_path):
			loc_sources = json.load( open( local_sources_path ) )
			sources += self.make_urls_from_list( loc_sources )
		#find all static files in current directory
		files = []
		for file_type in file_types:
			files.extend( glob.glob( os.path.join( search_directory , file_type )) )

		for item in files:
			item_name = os.path.basename(item)
			sources.append(
				{
					'url' : mask.replace( '#ITEM_NAME#', item_name ).replace( '#PRJ_NAME#' , prj_name ),
					'name' : item_name,
					'unid' : item_name,
					'scripts' : [],
					'wait_scripts' : [],
				} )
		return sources

	#get config for project from path
	def get_project_config( self, directory ):
		local_conf_path =  os.path.join( directory,  "pedant.json" )
		local_config = {}
		#read global config
		
		config = self.get_default_config()
		config['urls'] = []
		config['modes'] = {}
		#read local config
		if os.path.isfile( local_conf_path ):
			try:
				local_config = json.load( open( local_conf_path ) )
			except:
				return {}
		#config = dict( config.items() + local_config.items() )
		#normalize config
		for key, value in local_config.iteritems():
			if ( config.has_key(key) ):
				config[ key ] = value
		#your project name. Default - current directory name
		prj_name = os.path.basename( directory )
		if not local_config.has_key("prj_name"):
			config['prj_name'] = prj_name
		else:
			config['prj_name'] = re.sub( '[^0-9a-zA-Z_]+', '_', local_config['prj_name'] )
		return config#self.check_config( config )

	def save_project_config(self, prj_dir, config):
		if not config.has_key('without_urls'):
			urls_file_path = os.path.join( prj_dir , 'urls.json' )
			urls = config['urls']
			del config['urls']
			#save urls to root dir/urls.json
			urls_file_o = open( urls_file_path , 'wb')
			json.dump( urls, urls_file_o )
			urls_file_o.close
		else:
			del config['without_urls']
		
		config_file_path = os.path.join( prj_dir , 'pedant.json' )
		#save config to root dir/pedant.json
		config_file_o = open( config_file_path , 'wb')
		json.dump( config, config_file_o )
		config_file_o.close

		return config

	def log(self, log_str=''):
		if ( self.log_file and log_str ):
			#open file for writing
			log_file_o = open( self.log_file , 'a')
			log_file_o.write( log_str + "\n" )
			log_file_o.close

	def get_timestamp(self):
		return self.timestamp

	#create lock file
	def lock( self ):
		if os.path.isfile( self.lock_file_path ):
			return False
		#create lock file
		with open(self.lock_file_path, 'a'):
			os.utime(self.lock_file_path, None)
		return True

	#remove lock file
	def unlock( self ):
		if os.path.isfile( self.lock_file_path ):
			os.remove( self.lock_file_path )

	def check_config( self, config, ignore_urls = False, ignore_normalizied_prj_name=False ):
		#check modes section exists
		config['error'] = ''
		if ( not config.has_key('urls') or not config.has_key('modes') ):
			config['error'] += 'Modes and URLS missing in config'
			return config
			
		#check modes count
		if ( len( config['modes'] ) < 1 ):
			config['error'] += 'Modes is empty'
			return config

		#check browsers in modes
		for modename,mode in config['modes'].iteritems():
			if ( len(mode) < 1):
				config['error'] += ' Mode ' + modename + ' have not browsers'
				return config
			else:
				for browser in config['modes'][modename]:
					for key in ('unid', 'desired_capabilities', 'type', 'info', 'wd_url'):
						if not browser.has_key( key ):
							config['error'] += ' Pedant can not work with browser without required key - ' + key
							return config
		
		#check default mode exists
		if not config["modes"].has_key("*"):
			config["error"] = "Default mode are missing in config"
			return config
		#check browsers is unique in default mode
		checked = {}
		for browser in config['modes']['*']:
			if checked.has_key( browser['unid'] ):
				config['error'] += ' Browser ' + browser['unid'] + ' not unique'
			checked[ browser['unid'] ] = browser['unid']
		
		#check urls count
		if ( len(config['urls']) < 1 ) and not ignore_urls and not config.has_key('without_urls'):
			config['error'] += ' Urls is empty '

		#check urls format
		url_regex = re.compile(
			r'^(?:http|ftp)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
			r'localhost|' #localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		if not config.has_key('without_urls'):
			for url in config['urls']:
				if ( not url_regex.match( url ) ):
					config['error'] += ' Url ' + url + ' is invalid'
			if not url_regex.match( config['url_mask'] ):
					config['error'] += ' Url mask ' + config['url_mask'] + ' is invalid'
		
		#check project name
		normalized_name = re.sub('[^0-9a-zA-Z_]+', '_', config['prj_name'])
		if ( len(normalized_name) < 1 ):
			config['error'] += ' Project name ' + config['prj_name'] + ' is invalid'
		#
		if ( not ignore_normalizied_prj_name and normalized_name != config['prj_name'] ):
			config['error'] += ' Project name ' + normalized_name + ' is not equal old prj_name:' + config['prj_name']

		config['prj_name'] = normalized_name.encode("utf8")
		
		#check max workers
		max_workers = int(config['max_workers'])
		#TODO: get max value for max_workers from pedant config 
		if ( max_workers < 1 or max_workers > 50 ):
			config['error'] += ' Max workers count: ' + config['max_workers'] + ' is invalid (must be > 0 and < 40 )'

		if( len( config['error'] ) < 1 ):
			del config['error']
		return config

	def get_default_config(self):
		return json.load( open( os.path.join( os.path.dirname(os.path.realpath(__file__)) , "default.conf.json" ) ) )

	def calculate_workers_by_items(self,items):
		#normal items count for one worker.
		items_for_worker = 25
		k = int( round( ( len(items) / items_for_worker ) + 0.5 ) )
		return k

	def chunkList(self,mylist,parts):
		avg = len(mylist) / float(parts)
		out = []
		last = 0.0
		while last < len(mylist):
			out.append(mylist[int(last):int(last + avg)])
			last += avg
		return out

	def access(self):
		return not os.path.isfile( self.lock_file_path ) and os.path.isdir( self.config['data_storage_root'] ) and os.access( self.config['data_storage_root'], os.W_OK )

	"""
	Job. Start all workers, print info and return when it's finished
	"""
	def start(self):

		self.log( " --- Pedant started at %s " % str ( datetime.datetime.fromtimestamp( self.timestamp ).strftime('%d-%m-%Y %H:%M:%S') ) )
		print "Pedant started at %s " % str ( datetime.datetime.fromtimestamp( self.timestamp ).strftime('%d-%m-%Y %H:%M:%S') )
		#start all workers
		for worker_inst in self.workers:
			worker_inst.start()
		finished = {}
		
		self.runned = True

		#wait all workers are finished
		while( self.runned ):
			#write status
			self.print_progress(  '%s / %s finished | Active workers:  %s ' % ( str( len(finished) ) , str( self.total_count ), str(len( self.workers)) ) )
			#check all workers
			log = ''
			for worker_inst in self.workers:
				#calculate problems count
				log += worker_inst.log()
				finished.update( worker_inst.finished_ids )
				#check worker
				if worker_inst.isAlive() == False:
					#worker_inst.browser['instance'].close()
					worker_inst.handled = True
			#write log
			self.log( log )
			# if workers count < 1 then finish
			if len( self.workers ) < 1:
				print
				self.log( " --- Pedant finished at %s " % str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') ) )
				print "Pedant finished at %s" % str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') )
				self.runned = False
				self.stop()
				return True
			#kill finished workers
			self.workers = [t for t in self.workers if t.handled == False]
			#sleep three seconds before next loop
			time.sleep(3)

	def is_runned(self):
		return self.runned

	def start_in_thread(self):
		t = threading.Thread(target=self.start)
		#t.daemon = True
		t.start()
		return t

	def stop(self):
		self.log("Stopping pedant. Report saved in /reports/" + str(self.timestamp) + " directory" )
		for worker_inst in self.workers:
			worker_inst.initStop()
		self.unlock()
	
	def print_progress(self,message):
		sys.stdout.write( "\r" * self.prev_mess_len + message )
		sys.stdout.flush()
		self.prev_mess_len = len(message)

	def approve_image( self, item, browser ):
		pathes = generate_pathes( os.path.dirname( self.config['data_storage_root'] ), os.path.basename( self.config['data_storage_root'] ), self.timestamp, item, browser )
		#backup approved image in report dir
		os.remove( pathes['approved_report_image_bckp'] ) if os.path.isfile( pathes['approved_report_image_bckp'] ) else None
		os.rename( pathes['approved_report_image'], pathes['approved_report_image_bckp'] ) if os.path.isfile( pathes['approved_report_image'] ) else None
		#backup diff image in report dir
		os.remove( pathes['diff_image_bckp'] ) if os.path.isfile( pathes['diff_image_bckp'] ) else None
		os.rename( pathes['diff_image'], pathes['diff_image_bckp'] ) if os.path.isfile( pathes['diff_image'] ) else None
		#backup approved image in approved dir
		os.remove( pathes['approved_image_bckp'] ) if os.path.isfile( pathes['approved_image_bckp'] ) else None
		os.rename( pathes['approved_image'], pathes['approved_image_bckp'] ) if os.path.isfile( pathes['approved_image'] ) else None
		#backup json
		os.remove( pathes['report_json_bckp'] ) if os.path.isfile( pathes['report_json_bckp'] ) else None
		os.rename( pathes['report_json'], pathes['report_json_bckp'] ) if os.path.isfile( pathes['report_json'] ) else None
		#get json data from backuped report
		json_report = json.loads( open( pathes['report_json_bckp'] ).read() )
		
		#create approved folder if it's need
		os.makedirs(os.path.dirname( pathes['approved_image'] )) if not os.path.isdir( os.path.dirname(pathes['approved_image']) ) else None
		#copy actual to approved and report
		shutil.copyfile( pathes['actual_image'], pathes['approved_image'] )
		shutil.copyfile( pathes['actual_image'], pathes['approved_report_image'] )
		
		#update json, save it to file
		json_report['msg'] = "success"
		obj = open( pathes['report_json'] , 'wb')
		json.dump( json_report, obj )
		obj.close

		#images web pathes
		json_report['images'] = {
			'actual': pathes['actual_image_web'] if os.path.isfile( pathes['actual_image'] ) else False,
			'approved': pathes['approved_image_web'] if os.path.isfile( pathes['approved_image'] ) else False,
			'approved_report': pathes['approved_report_image_web'] if os.path.isfile( pathes['approved_report_image'] ) else False,
			'diff': pathes['diff_image_web'] if os.path.isfile( pathes['diff_image'] ) else False,
		}
		return json_report

	def cancel_approve_image( self, item, browser ):
		pathes = generate_pathes( os.path.dirname( self.config['data_storage_root'] ), os.path.basename( self.config['data_storage_root'] ) , self.timestamp, item, browser )
		
		#web imgs pathes
		approved_img_web = False
		approved_report_img_web = False
		diff_img_web = False

		#restore image im approved
		os.remove( pathes['approved_image'] ) if os.path.isfile( pathes['approved_image'] ) else None
		os.rename( pathes['approved_image_bckp'], pathes['approved_image'] ) if os.path.isfile( pathes['approved_image_bckp'] ) else None
		#restore approved image in report
		os.remove( pathes['approved_report_image'] ) if os.path.isfile( pathes['approved_report_image'] ) else None
		os.rename( pathes['approved_report_image_bckp'], pathes['approved_report_image'] ) if os.path.isfile( pathes['approved_report_image_bckp'] ) else None
		#restore diff image
		os.remove( pathes['diff_image'] ) if os.path.isfile( pathes['diff_image'] ) else None
		os.rename( pathes['diff_image_bckp'], pathes['diff_image'] ) if os.path.isfile( pathes['diff_image_bckp'] ) else None
		#restore report.json
		os.remove( pathes['report_json'] ) if os.path.isfile( pathes['report_json'] ) else None
		os.rename( pathes['report_json_bckp'], pathes['report_json'] ) if os.path.isfile( pathes['report_json_bckp'] ) else None
		#read report
		json_report = json.loads( open( pathes['report_json'] ).read() )
		#set images
		json_report['images'] = {
			'actual': pathes['actual_image_web'] if os.path.isfile( pathes['actual_image'] ) else False,
			'approved': pathes['approved_image_web'] if os.path.isfile( pathes['approved_image'] ) else False,
			'approved_report': pathes['approved_report_image_web'] if os.path.isfile( pathes['approved_report_image'] ) else False,
			'diff': pathes['diff_image_web'] if os.path.isfile( pathes['diff_image'] ) else False,
		}
		return json_report

	def get_report(self):
		data = list()
		#print glob.glob( self.config['data_storage_root'] + os.sep + 'reports' + os.sep + self.timestamp + os.sep + '*' + os.sep + '*' + os.sep + 'report.json' )
		for json_path in glob.glob( self.config['data_storage_root'] + os.sep + 'reports' + os.sep + self.timestamp + os.sep + '*' + os.sep + '*' + os.sep + 'report.json' ):
			json_content=open(json_path)
			json_report = json.load(json_content)
			json_content.close()
			pathes = generate_pathes( os.path.dirname( self.config['data_storage_root'] ), os.path.basename( self.config['data_storage_root'] ) , self.timestamp, json_report['item']['unid'], json_report['browser']['unid'] )
			#set images
			json_report['images'] = {
				'actual': pathes['actual_image_web'] if os.path.isfile( pathes['actual_image'] ) else False,
				'approved': pathes['approved_image_web'] if os.path.isfile( pathes['approved_image'] ) else False,
				'approved_report': pathes['approved_report_image_web'] if os.path.isfile( pathes['approved_report_image'] ) else False,
				'diff': pathes['diff_image_web'] if os.path.isfile( pathes['diff_image'] ) else False,
			}
			data.append( json_report )
		return data

	def get_approved_images(self):
		pathes = generate_pathes( os.path.dirname( self.config['data_storage_root'] ), os.path.basename( self.config['data_storage_root'] ) )
		data = list()
		for img in glob.glob( pathes['approved_dir'] + os.sep + '*' + os.sep + '*' + os.sep + 'approved.png' ):
			itemname = os.path.basename( os.path.dirname( os.path.dirname( img ) ) )
			browser = os.path.basename( os.path.dirname( img ) )
			item_pathes = generate_pathes( os.path.dirname( self.config['data_storage_root'] ), os.path.basename( self.config['data_storage_root'] ), '', itemname, browser )
			data.append( 
				{ 'name':itemname,
				'browser':browser,
				'images': { 
					'approved': item_pathes['approved_image_web'] if os.path.isfile( item_pathes['approved_image'] ) else False,
					} 
				})
		return data

#get pathes for items
def generate_pathes( ds_root, prj_name, timestamp = '', item = '', browser = '' ):
	prj_name = prj_name.encode('utf-8')
	item = item.encode('utf-8')
	browser = browser.encode('utf-8')
	timestamp = timestamp.encode('utf-8')
	pathes = {
		'prj_root': os.path.realpath( (ds_root + os.sep + '%s') % (prj_name) ),
		#approved images
		'approved_dir': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'approved') % (prj_name) ),
		'approved_image': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'approved' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'approved.png') % ( prj_name, item, browser ) ),
		'approved_image_bckp': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'approved' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'approved.png.bckp') % ( prj_name, item, browser ) ),
		'approved_image_web':  '/projects/%s/static/approved/%s/%s/approved.png' % ( prj_name, item, browser ),
		#
		'reports_dir': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports') % prj_name ),
		#report
		'approved_report_image': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'approved_report.png' ) % ( prj_name, timestamp, item, browser ) ), 
		'approved_report_image_bckp': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'approved_report.bckp' ) % ( prj_name, timestamp, item, browser ) ), 
		'approved_report_image_web': '/projects/%s/static/reports/%s/%s/%s/approved_report.png' % ( prj_name, timestamp, item, browser ),
		'actual_image': os.path.realpath( ( ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'actual.png' ) % ( prj_name, timestamp, item, browser ) ), 
		'actual_image_web': '/projects/%s/static/reports/%s/%s/%s/actual.png' % ( prj_name, timestamp, item, browser ),
		'diff_image': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'diff.png') % ( prj_name, timestamp, item, browser ) ),
		'diff_image_bckp': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'diff.png.bckp') % ( prj_name, timestamp, item, browser ) ),
		'diff_image_web': '/projects/%s/static/reports/%s/%s/%s/diff.png' % ( prj_name , timestamp, item, browser ),
		'report_json': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'report.json') % ( prj_name, timestamp, item, browser ) ),
		'report_json_bckp': os.path.realpath( (ds_root + os.sep + '%s' + os.sep + 'reports' + os.sep + '%s' + os.sep + '%s' + os.sep + '%s' +  os.sep + 'report.json.bckp') % ( prj_name, timestamp, item, browser ) )
	}
	return pathes