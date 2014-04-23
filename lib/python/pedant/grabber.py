import threading,os,sys,urllib2,re,httplib,time,json
from urlparse import urlparse

class pedant_grabber(threading.Thread):

	handled = False

	allowed_content_types = [ 'text/html' ]

	def __init__(self, timeout, urls_queue, content_queue, tmp_file_path ):

		super(pedant_grabber, self).__init__()
		self.timeout = timeout
		self.urls_queue = urls_queue
		self.content_queue = content_queue
		self.result_file = tmp_file_path

	"""
	run this thread
	@return void
	"""
	def run(self):
		result = { 'success':[] , 'errors':[] }
		#
		while True:	
			#reset timeout
			timeout = 0
			#check urls count and wait timeout
			while self.urls_queue._qsize() < 1:
				time.sleep(0.2)
				timeout = timeout + 0.2	
				#exit by timeout
				if timeout > self.timeout:
					return

			next_url = self.urls_queue.get()
			html = ''
			try:
				response = urllib2.urlopen( next_url )
				if ( response.info().gettype() in self.allowed_content_types ):
					result['success'].append( next_url )
					html = response.read()
				response.close()
				#get
			except urllib2.HTTPError, e:
				result['errors'].append( next_url + ' - ' + str( e.getcode() ) )
			#put results to file
			with open( self.result_file, 'w') as outfile:
				json.dump(result, outfile)
			#wait queue
			while self.content_queue.full():
				pass
			if html != '':
				self.content_queue.put(html)
			self.urls_queue.task_done()
		return