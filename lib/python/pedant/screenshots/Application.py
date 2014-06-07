import time,Worker,sys,datetime

class Application:
	
	#workers list
	workers = []

	#browsers configs for scanning
	browsers = []

	#items list for scanning
	items = []

	#prev_mess_len
	prev_mess_len = 0

	def __init__(self,config):
		
		#current timestamp
		timestamp = time.time()
		self.items = config['items']
		print "Pedant started at " + str ( datetime.datetime.fromtimestamp( timestamp ).strftime('%d-%m-%Y %H:%M:%S') )

		#optimisation hack. if we have one browser - chunk items for workers and create workers
		if ( len( config['browsers'] ) == 1):
			#calculate workers count for items
			workers_cnt = self.calculate_workers_by_items( config['items'] )
			if workers_cnt > config['max_workers']:
				workers_cnt = config['max_workers']
			items = self.chunkList(config['items'],workers_cnt)
			browsers = [ config['browsers'] for bro in range(workers_cnt) if True ]
			# for i in range( workers_cnt ):
			# 	inst = screen_worker.screen_worker( config['browsers'][0] , items[i] , timestamp , config['data_storage_root'] )
			# 	self.workers.append( inst )
		#else create normal workers
		else:	
			#calculate needle workers count
			workers_cnt = len( config['browsers'] )
			if workers_cnt > config['max_workers']:
				workers_cnt = config['max_workers']
			browsers = self.chunkList( config['browsers'],workers_cnt )
		for i in range( workers_cnt ):

			inst = Worker.Worker( browsers[i][0] , config['items'], timestamp, config['data_storage_root'] )
			self.workers.append( inst )

	def calculate_workers_by_items(self,items):
		#normal items count for one for worker. Calculated on core i7, ssd and 8gb ram in ubuntu 12.10 ;)
		items_for_worker = 50
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
		#start all workers
		for worker_inst in self.workers:
			worker_inst.start()
		need_work = True
		finished = {} 
		#wait all workers are finished
		while( need_work ):
			#write status
			self.print_progress( str( len(finished) ) + ' / ' + str(len( self.items )) + ' finished | Active workers: ' + str(len( self.workers)) )
			#check all workers
			for worker_inst in self.workers:
				#calculate problems count 
				finished.update( worker_inst.finished_ids )
				#check worker
				if worker_inst.isAlive() == False:
					#worker_inst.browser['instance'].close()
					worker_inst.handled = True
			if len( self.workers ) < 1:
				print
				#print "Done " + str( len(finished) ) + " items from " + str(len( self.items ))
				print "Pedant finished at " + str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') )
				return True
			#kill finished workers
			self.workers = [t for t in self.workers if t.handled == False]
			#sleep three seconds
			time.sleep(3)
	
	def print_progress(self,message):
		sys.stdout.write( "\r" * self.prev_mess_len + message )
		sys.stdout.flush()
		self.prev_mess_len = len(message)