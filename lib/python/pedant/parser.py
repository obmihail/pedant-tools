import threading,os,sys,urllib2,re,httplib,time
import lxml.html
from urlparse import urlparse

class pedant_parser(threading.Thread):

	handled = False 

	def __init__(self, base_url, timeout, urls_queue, content_queue, visited_queue, blacklist = [] ):

		super(pedant_parser, self).__init__()
		self.timeout = timeout
		self.urls_queue = urls_queue
		self.content_queue = content_queue
		#parser = PedantHTMLParser()
		self.blacklist = blacklist
		self.HREF_LEN_LIMIT = 414
		parsed_url = urlparse( base_url )
		self.base_url = parsed_url.scheme + '://' + parsed_url.netloc #base url
		self.visited_queue = visited_queue
		#self.parser = parser

	def getLinks( self, html_str ):
		html = lxml.html.fromstring(html_str)
		hrefs = html.xpath('//a/@href')
		links = []
		for value in hrefs:
			url = ''
			for regex in self.blacklist:
				if ( regex.match( value ) ):
					value = ''
			if ( len( value ) > self.HREF_LEN_LIMIT ):
				print '\n is skipped by len ' + value
			#href is abs link
			if ( value[0:4] == 'http'):
				parsed = urlparse( value )
				if ( parsed.scheme + '://' + parsed.netloc == self.base_url ):
					url = value
			#href is related link
			elif( value[0:1] == '/' ):
				url = self.base_url + value
			#href is bad http link ( it can be static from current, mailto: , js function)
			else:
				errors = ' check this url: ' + self.base_url
			if ( url != "" and url not in self.visited_queue ):
				self.visited_queue.put( url )
				links.append( url )
		return links

	"""
	run this thread
	@return void
	"""
	def run(self):
		while True:
			timeout = 0
			#check contents count and wait timeout
			while self.content_queue._qsize() < 1:
				time.sleep(0.2)
				timeout = timeout + 0.2	
				#exit by timeout
				if timeout > self.timeout:
					return
			data = self.content_queue.get()
			links = self.getLinks(data)
			#links = self.parser.feed( data ):
			for link in links:
				self.urls_queue.put(link)
			self.content_queue.task_done()
			#sleep