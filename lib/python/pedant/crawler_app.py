import time,sys,datetime,json,Queue,CheckableQueue,grabber,os
import parser

class Application:

	config = {}
	grabbers = []
	parsers = []
	#urls for scanning
	#content queue
	content_queue = Queue.Queue()
	#urls queue
	urls_queue = Queue.Queue()
	#visited urls queue
	visited_queue = CheckableQueue.CheckableQueue()
	#visited_cnt
	#prev_mess_len
	prev_mess_len = 0
	tmp_file_mask = os.getcwd() + os.sep + 'tmp_report_#NUM#.json'

	def __init__(self,config):
		self.urls_queue.put( config['base_url'] )
		self.workers_cnt = config['workers_cnt']
		#current timestamp
		timestamp = time.time()
		for i in range( config['workers_cnt'] ):
			#create grabber
			grabber_inst = grabber.pedant_grabber( 
					config['timeout'],
					self.urls_queue, 
					self.content_queue, 
					self.tmp_file_mask.replace( '#NUM#',str(i) ) )
			#grabber_inst.setDaemon(True) 
			self.grabbers.append( grabber_inst )
			#create parser
			parser_inst = parser.pedant_parser(
					config['base_url'],
					config['timeout'],
					self.urls_queue, 
					self.content_queue,
					self.visited_queue, 
					config['blacklist'] )
			#parser_inst.setDaemon(True) 
			self.parsers.append( parser_inst )

		print "Pedant-crawler started at " + str ( datetime.datetime.fromtimestamp( timestamp ).strftime('%d-%m-%Y %H:%M:%S') )


	"""
	Job. Start all workers, print info and return when it's finished
	"""
	def start(self):
		#start grabbers
		for grabber in self.grabbers:
			grabber.start()
		
		#start parsers
		for parser in self.parsers:
			parser.start()
		#wait all workers are finished
		#need_work = True
		while( True ):
			#write status
			self.print_progress( 
				' Founded:' + str( self.visited_queue._qsize() ) + ' | Grabbers: ' + str(len( self.grabbers)) + ' | Parsers: ' + str( len( self.parsers ) ) )
			#kill finished threads
			for g in self.grabbers:
				if not g.isAlive(): 
					g.handled = True
			for p in self.parsers:
				if not p.isAlive(): 
					p.handled = True
			#kill finished grabbers\parsers
			self.grabbers = [ g for g in self.grabbers if not g.handled ]
			self.parsers = [ p for p in self.parsers if not p.handled ]

			#finish work
			if len( self.grabbers ) < 1 and len( self.parsers ) < 1:
				print
				print "Pedant finished at " + str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') )
				break
			#sleep
			time.sleep(5)
		urls_list = []
		errors_list = []
		for i in range(self.workers_cnt):
			filename = self.tmp_file_mask.replace( '#NUM#',str(i) )
			if os.path.isfile( filename ):
				#read json and calculate summary results
				data = json.load( open( filename ) )
				os.remove( filename )
				urls_list = urls_list + data['success']
				errors_list = errors_list + data['errors']
		#write sum result
		with open('urls.json', 'w') as outfile: json.dump(urls_list, outfile)
		with open('errors.json', 'w') as outfile: json.dump(errors_list, outfile)

	def print_progress(self,message):
		sys.stdout.write( "\r" * self.prev_mess_len + message )
		sys.stdout.flush()
		self.prev_mess_len = len(message)