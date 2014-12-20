from time import sleep

def hook( *decorators ):
	#print 'LALALA'
	def register_wrapper(func):
		#print func
		for deco in decorators[::-1]:
			#func=deco(func)
			func._decorators=decorators
		return func
	return register_wrapper

pedant_decos = ( 'before_items', 'before_item', 'before_screenshot', 'after_screenshot', 'after_item', 'after_items' )

class PedantHooks:

	def __init__(self, browser ):
		self.browser = browser
		self.fs_by_decos = {}
		#make dict by decorators and functions
		for deco in ( pedant_decos ):
			self.fs_by_decos[deco] = [ getattr(self, method) for method in dir(self) if callable(getattr(self, method)) and hasattr( getattr(self, method), '_decorators' ) and deco in getattr( getattr(self, method), '_decorators' ) ]

	def call_by_event(self, *kwargs):
		res = True
		for func in self.fs_by_decos[ kwargs[0] ]:
			try: 
				func( *kwargs[1:] )
			except Exception as e:
				res = False
				self.log( 'Pedant handler exception in method %s with arguments: %s . Exception: %s ' % ( func.__name__ , str(kwargs[1:]) , str(e) ), level="ERROR" )
		return res

	"""
	@param js - javascript code with return bool value
	@param timeout - miliseconds timeout while pedant wait true from js
	@param period - miliseconds period while pedant check js
	"""
	def wait_js(self,js,timeout = 300, period = 500):
		timeout_s = timeout / 1000
		time = timeout
		while True:
			if time >= timeout:
				return False
			if self.browser['instance'].execute_script( js ) == True:
				return True
			sleep( timeout_s )
			time = time + timeout_s