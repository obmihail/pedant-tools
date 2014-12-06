import time,Worker,sys,datetime,json,os,re,glob,threading

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

	def configure(self, config, mode):
		#current timestamp
		self.timestamp = time.time()

		#create working directory if not exists
		if ( not os.path.isdir( config['data_storage_root'] ) ):
			os.makedirs( config['data_storage_root'] )

		if ( config.has_key('logging') and config['logging'] is True ):
			#filepath
			self.log_file = config['data_storage_root'] + os.sep + 'logs' + os.sep + str( self.timestamp ) + '.log'
			#create dir
			if ( not os.path.isdir( os.path.dirname( self.log_file ) ) ):
				os.makedirs( os.path.dirname( self.log_file ) )

		self.lock_file_path = config['data_storage_root'] + os.sep + 'lock.file'
		browsers = self.reconfigureBrowsers( config['modes'][ mode ] )
		self.items = config['urls']
		
		#optimisation hack. if we have one browser - chunk items for workers and create workers
		if ( len( browsers ) == 1):
			#calculate workers count for items
			workers_cnt = self.calculate_workers_by_items( config['urls'] )
			if workers_cnt > config['max_workers']:
				workers_cnt = config['max_workers']
			items = self.chunkList(config['urls'],workers_cnt)
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
			for i in range( workers_cnt ):
				inst = Worker.Worker( browsers[i][0] , config['urls'], self.timestamp, config['data_storage_root'] )
				self.workers.append( inst )
		return self

	def reconfigureBrowsers( self, browsers ):
		#set uniq keys
		setted = {}

		for browser in browsers:
			#unid generation
			if setted.has_key( browser[ 'unid' ] ):
				print '>Warn pedant find duplicate browser unid in current configuration. Use last browser: ' + unid
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
		local_src_list = search_directory + os.sep + 'urls.json'
		sources = []
		#get all sources from file urls.json
		if os.path.isfile(local_src_list):
			loc_sources = json.load( open( local_src_list ) )
			sources += self.make_urls_from_list( loc_sources )
		#find all static files in current directory
		files = []
		for file_type in file_types:
			files.extend( glob.glob( search_directory + os.sep + file_type) )

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
		local_conf_file =  directory + os.sep + "pedant.json"
		local_config = {}
		#read global config
		
		config = self.get_default_config()
		config['urls'] = []
		#read local config
		if os.path.isfile( local_conf_file ):
			local_config = json.load( open( local_conf_file ) )
		#config = dict( config.items() + local_config.items() )
		config = dict( config.items() + local_config.items() )

		#your project name. Default - current directory name
		prj_name = os.path.basename( directory )
		if not config.has_key("prj_name"):
			config['prj_name'] = prj_name

		return config#self.check_config( config )

	def save_project_config(self, prj_dir, config):
		urls = config['urls']
		del config['urls']
		config_file = prj_dir + os.sep + 'pedant.json'
		urls_file = prj_dir + os.sep + 'urls.json'

		#save config to root dir/pedant.json
		obj = open( config_file , 'wb')
		json.dump( config, obj )
		obj.close

		#save urls to root dir/urls.json
		obj = open( urls_file , 'wb')
		json.dump( urls, obj )
		obj.close

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

	def check_config( self, config, ignore_urls = False ):

		#check modes section exists
		config['error'] = ''
		if ( not config.has_key('urls') or not config.has_key('modes') ):
			config['error'] += 'Modes and URLS missing in config'
			return config
			
		#check modes count
		if ( len( config['modes'] ) < 1 ):
			config['error'] += 'Modes is empty'
			return config

		#check browsers count in modes
		for modename,mode in config['modes'].iteritems():
			if ( len(mode) < 1):
				config['error'] += ' Mode ' + modename + ' have not browsers'
				return config

		#check browsers is unique in full mode
		checked = {}
		for browser in config['modes']['full']:
			if checked.has_key( browser['unid'] ):
				config['error'] += ' Browser ' + browser['unid'] + ' not unique'
			checked[ browser['unid'] ] = browser['unid']
		
		#check urls count
		if ( len(config['urls']) < 1 ) and not ignore_urls :
			config['error'] += ' Urls is empty '

		#check urls format
		regex = re.compile(
			r'^(?:http|ftp)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
			r'localhost|' #localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		for url in config['urls']:
			if ( not regex.match( url ) ):
				config['error'] += ' Url ' + url + ' is invalid'
		
		#check project name
		normalized_name = re.sub('[^0-9a-zA-Z_]+', '_', config['prj_name'])
		if ( len(normalized_name) < 1):
			config['error'] += ' Project name ' + config['prj_name'] + ' is invalid'
		config['prj_name'] = normalized_name
		
		#check max workers
		max_workers = int(config['max_workers'])
		if ( max_workers < 1 or max_workers > 39 ):
			config['error'] += ' Max workers count: ' + config['max_workers'] + ' is invalid (must be > 0 and < 40 )'

		if( len( config['error'] ) < 1 ):
			del config['error']
		return config

	def get_default_config(self):
		return json.load( open( os.path.dirname(os.path.realpath(__file__)) + os.sep + "default.conf.json" ) )

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

	"""
	Job. Start all workers, print info and return when it's finished
	"""
	def start(self):

		self.log( " --- Pedant started at " + str ( datetime.datetime.fromtimestamp( self.timestamp ).strftime('%d-%m-%Y %H:%M:%S') ) )
		print "Pedant started at " + str ( datetime.datetime.fromtimestamp( self.timestamp ).strftime('%d-%m-%Y %H:%M:%S') )
		#start all workers
		for worker_inst in self.workers:
			worker_inst.start()
		finished = {}
		
		self.runned = True

		#wait all workers are finished
		while( self.runned ):
			#write status
			self.print_progress( str( len(finished) ) + ' / ' + str(len( self.items )) + ' finished | Active workers: ' + str(len( self.workers)) )
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
				self.log( " --- Pedant finished at " + str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') ) )
				print "Pedant finished at " + str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') )
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