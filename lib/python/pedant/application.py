import os,sys,json,shutil,threading,inspect,re,glob,time,traceback,hashlib,imp,pedant,datetime
from time import gmtime, strftime
from collections import Counter
from Queue import Queue
import threading, thread
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os,sys,json,hashlib,time,uuid,urllib2,shutil
from pedant.errors import PedantError, Skip, Fail
from pedant import get_json_from_file,put_json_to_file,load_module_from_file
from pedant.errors import PedantError


class PedantApplication:
	
	_RUNNED = 'RUNNED'
	_FINISHED = 'FINISHED'
	_WAITING = 'WAITING'

	def __init__(self, project, verbose=False, logging=True):
		#workers list
		self.stat = {}
		self.status = PedantApplication._WAITING
		self.log_file = False
		self.log_str = ''
		self.exception = Exception('')
		#items list for scanning
		self.logging = logging
		self.project = project
		self.verbose = verbose
		self.expectation_workers_list = []
		self.active_workers = []
		self.threads_limit = project.get_threads_count()
		self.timestamp = time.time()
		self.statistic = { 'TOTAL': Queue(), 'PASSED':Queue(),'FAILED':Queue(),'FINISHED':Queue(),'SKIPPED':Queue()}
		self.log_file_o = False

	def log(self, log_line='', print_headers=True, level='INFO'):
		log_line = log_line
		if print_headers:
			log_line = "%s [%s] %s \n" % ( strftime("%Y-%m-%d %H:%M:%S", gmtime()) , level , log_line)
		self.log_str = self.log_str + log_line
		if (self.log_file and not self.log_file_o):
			#open file for writing
			self.log_file_o = open(self.log_file, 'a')
		if (self.log_file_o):
			self.log_file_o.write("%s\n"%log_line)
		if self.verbose:
			print  "%s\n"%log_line
		return self

	def get_current_log(self):
		return self.log_str

	def get_timestamp(self):
		return self.timestamp

	def get_exception(self):
		return self.exception

	def chunk_list(self,items_list,count):
		return [items_list[x:x+count] for x in xrange(0, len(items_list), count)]
		#avg = len(mylist)/float(parts)
		#out = []
		#last = 0.0
		#while last<len(mylist):
		#	out.append(mylist[int(last):int(last + avg)])
		#	last += avg
		#return out

	def get_statistic(self):
		stat = dict( [ ( key , list(self.statistic[key].queue) ) for key in self.statistic.keys() ] )
		return stat


	def get_status(self):
		return self.status

	"""
	Job. Start all workers, print info and return when it's finished
	"""
	def start(self):
		self.project.lock()
		#previous message length ( for live output )
		self.prev_mess_len = 0
		self.status = PedantApplication._RUNNED
		#
		self.log( " --- Pedant started at %s " % str ( datetime.datetime.fromtimestamp( self.timestamp ).strftime('%d-%m-%Y %H:%M:%S') ) )
		self.progress_pattern = '%d'+' / %d finished | Expectation workers: '%self.statistic['TOTAL'].qsize() + ' %d | Active workers: %d | Passed: %d | Failed: %d | Skipped: %d'
		while(True):
			#add new workers from expectation list
			if len(self.active_workers) < self.threads_limit:
				for i in range(self.threads_limit - len(self.active_workers)):
					try:
						worker = self.expectation_workers_list.pop()
						worker.start()
						self.active_workers.append(worker)
					except IndexError:
						pass
					except Exception as e:
						print "WORKER START ERROR %s"%str(e)
						self.log('ERROR IN WORKER STARTING: %s ' %str(e))
			self.print_progress()
			#write workers log
			for worker in self.active_workers:
				self.log( worker.log(), False )
			# if all workers are finished - finish work
			if len(self.active_workers)<1 and len(self.expectation_workers_list)<1:
				self.print_progress()
				print
				self.log( " --- Pedant finished at %s " % str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') ) )
				#print "Pedant finished at %s" % str ( datetime.datetime.fromtimestamp( time.time() ).strftime('%d-%m-%Y %H:%M:%S') )
				self.status = PedantApplication._FINISHED
				self.stop()
				self.project.unlock()
				return self

			#print self.active_workers
			#kill finished workers
			self.active_workers = [w for w in self.active_workers if w.isAlive()]
			#sleep one second 
			if len(self.active_workers) or len(self.expectation_workers_list):
				time.sleep(1)

	"""
	need for catch exception when application run in thread
	"""
	def quiet_start(self):
		try:
			self.start()
		except Exception as e:
			print e
			self.exception = e

	"""
	start stop procedure
	"""
	def stop(self):
		self.log("Pedant stopped. Report saved in %s directory. Report name: %s"%(self.reports_dir,str(self.timestamp)))
		[ worker.stop() for worker in self.active_workers ]
		[ worker.stop() for worker in self.expectation_workers_list ]
		return self

	def print_progress(self):
		message = self.progress_pattern%(self.statistic['FINISHED'].qsize(), len(self.expectation_workers_list) ,len(self.active_workers),self.statistic['PASSED'].qsize(),self.statistic['FAILED'].qsize(),self.statistic['SKIPPED'].qsize())
		sys.stdout.write( "\r" * self.prev_mess_len + message )
		sys.stdout.flush()
		self.prev_mess_len = len(message)

	"""
	RESULTS METHODS
	"""
	def get_reports(self):
		path = os.path.join(self.reports_dir, '[0-9]*.[0-9]*')+os.sep
		return map(
				lambda x: {
						'pretty': datetime.datetime.fromtimestamp( float( os.path.basename( os.path.dirname(x) ) ) ).strftime('%Y-%m-%d %H:%M:%S.%f') ,
						'timestamp': os.path.basename(os.path.dirname(x))}, 
					glob.glob(path))

	def delete_report(self,timestamp):
		path = os.path.join(self.reports_dir, timestamp)
		if os.path.isdir(path):
			shutil.rmtree(path)
		else:
			raise PedantError('Report not exists')
	

	"""
	Get launch log by timestamp
	"""
	def get_log(self, timestamp):
		log_file_path = os.path.join(self.reports_dir, timestamp, 'log.txt')
		if os.path.isfile(log_file_path):
			with open(log_file_path, 'r') as log_file:
				content = log_file.read()
			return content
		raise PedantError('Log file with timestamp %s not found'%timestamp)

class PedantWorker(threading.Thread):

	_PASSED = 'passed'
	_SKIPPED = 'skipped'
	_FAILED = 'failed'

	def __init__(self, report_dir):
		super(PedantWorker, self).__init__()
		self.log_str = ''
		self._stopped = False
		#super(Worker, self).__init__()
		self.report_dir = report_dir

	def set_queues(self,finished, skipped, passed, failed):
		self._FINISHED_QUEUE = finished
		self._SKIPPED_QUEUE = skipped
		self._PASSED_QUEUE = passed
		self._FAILED_QUEUE = failed

	def stop(self):
		self._stopped = True

	def log(self, line = False, level="INFO"):
		if (line):
			self.log_str += "%s [%s] %s \n" % ( strftime("%Y-%m-%d %H:%M:%S", gmtime()) , level , line )
		else:
			log = self.log_str
			#clear and return log
			self.log_str = ''
			return log

	"""
	init browser
	"""
	def init_browser(self, browser):
		#launch browser
		#caps
		caps = getattr( DesiredCapabilities , browser['type'].upper() ) if hasattr(DesiredCapabilities , browser['type'].upper()) else {}
		if browser.has_key('desired_capabilities'):
			caps = dict( caps.items() + browser['desired_capabilities'].items() )
		#print caps
		try:
			browser['instance'] = webdriver.Remote(
					command_executor=str(browser['wd_url']),
					desired_capabilities=caps,
					keep_alive=False )
			self.log("Connected to browser: %s"%str(browser))
		except Exception as e:
			browser['instance'] = False
			err_text = "Can not connect to browser: %s"%str(browser)
			self.log(err_text, "ERROR")
			raise PedantError(err_text)
		try:
			browser['instance'].set_window_size(browser['window_size'][0],browser['window_size'][1])
		except Exception, e:
			self.log("Cacthed error in set_window_size, maybe its mobile browser? Error: %s"%str(e), "INFO")
			#Window handling not supported on Android
		return browser

	def stop_browser(self, browser):
		if browser['instance']:
			browser['instance'].close()
		self.log("Disconnect from selenium browser with id %s"%browser['id'])