import threading,os,sys,urllib2,re,httplib
from urlparse import urlparse

class crawler_worker(threading.Thread):
	#max href len
	HREF_LEN_LIMIT  = 414
	is_finished = False
	url = False
	content_type_search_regex = re.compile('Content-type:\s(.*)\\n')
	allowed_content_types = [ 'text/html' ]

	def __init__(self, base_url, results, get_job, urls_list, blacklist = [] ):

		super(crawler_worker, self).__init__()
		self.url = base_url
		self.results = results
		#get new job
		self.get_job = get_job
		self.urls_list = urls_list
		self.blacklist = blacklist
		parsed = urlparse( base_url )
		self.base_url = parsed.scheme + '://' + parsed.netloc #base url

	#job is done
	def done_job(self,results):
		self.job_is_done = True
		self.urls_list = self.urls_list + results['captured']
		self.results['errors'] = self.results['errors'] + results['errors']
		self.results['not_allowed'] = self.results['not_allowed'] + results['not_allowed']
		self.url = self.get_job()

	def parse_content( self, html, result ):
		#find all hrefs
		links = re.findall('href[^\'"]["|\']([^\'"#]*).*[#|"|\']*', html)
		links = filter(None, links)
		page_results = []
		#print links
		for link in links:
			link = link.strip().lower()

			#if href in blacklist - skip it
			for regex in self.blacklist:
				regex.match( link ) 
				if ( regex.match( link ) ):
					#print "skipped url:" + link
					link = ''
			if ( len( link ) > self.HREF_LEN_LIMIT ):
				link + ' is skipped by len'
				link = ''
			#if href is abs link
			if ( link[0:4] == 'http'):
				parsed = urlparse( link )
				if ( parsed.scheme + '://' + parsed.netloc == self.base_url ):
					url = link
			#if href is related link
			elif( link[0:1] == '/' ):
				url = self.base_url + link
			#if href is mailto
			elif ( link[0:7] == 'mailto:' or link == '' ):
				url = ""
			#href is from current page
			else:
				url = self.url + '../' + link
			if ( url != "" and ( url not in self.results['visited'] ) and self.is_allowed( url ) ):
				page_results.append( url )
		result[ 'captured' ] = page_results


	"""
	run this thread
	@return void
	"""
	def run(self):
		while self.url:
			result = { 'captured':[] , 'errors':[], 'not_allowed':[] }
			# get content with headers
			try:
				response = urllib2.urlopen( self.url )
				if ( response.info().gettype() in self.allowed_content_types ):
					html = response.read()
					self.parse_content( html , result )
				else:
					result['not_allowed'].append( self.url + " - " + response.info().gettype() )
				response.close()
				#get
			except urllib2.HTTPError, e:
				result['errors'].append( self.url + ' - ' + str( e.getcode() ) )
			self.url = False
			self.done_job( result )
		return

	def is_allowed( self, url ):
		try:
			response = urllib2.urlopen( url )
			content_type = response.info().gettype()
			response.close()
			if ( content_type in self.allowed_content_types ):
				return True
			else:
				return False
			#get
		except urllib2.HTTPError, e:
			return False