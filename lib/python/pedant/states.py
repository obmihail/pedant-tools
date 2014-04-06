from time import sleep
from pedant.errors import PedantError
import re

def description( *values ):
	def mark_function(cls):
		cls._description = values[0]
		return cls
	return mark_function

def urls_regex( *expressions ):
	def mark_function(cls):
		cls._urls_expression = re.compile(expressions[0])
		return cls
	return mark_function

def browsers_regex( *expressions ):
	def mark_function(cls):
		cls._browsers_expression = re.compile(expressions[0])
		return cls
	return mark_function

def event( *decorators ):
	def set_hook(func):
		#print func
		func._decorators=decorators
		return func
	return set_hook

class Default:

	_urls_expression = re.compile('.*')
	_browsers_expression = re.compile('.*')
	_description = ''

	def __init__(self):
		self.fs_by_decos = {}
		pedant_decos = ('before_all', 'before_one', 'before_screenshot', 'after_one', 'after_all')
		#make dict by decorators and functions
		for deco in ( pedant_decos ):
			self.fs_by_decos[deco] = [ getattr(self, method) for method in dir(self) if callable(getattr(self, method)) and hasattr( getattr(self, method), '_decorators' ) and deco in getattr( getattr(self, method), '_decorators' ) ]

	def get_urls_regexp(self):
		return self._urls_expression.pattern

	def get_browsers_regexp(self):
		return self._browsers_expression.pattern

	def get_methods_names_list_by_event(self,event_name):
		functions = [ func.__name__ for func in self.fs_by_decos[event_name] ]
		return functions

	def get_id(self):
		return self.__class__.__name__.lower()

	def get_description(self):
		return self._description

	def set_browser(self, browser):
		self.browser = browser

	def filter_browsers(self, browsers):
		filtered = []
		for browser in browsers:
			if self._browsers_expression.match(browser['id']):
				filtered.append(browser)
		return filtered

	def filter_items(self, items):
		filtered = []
		for item in items:
			if self._urls_expression.match( item['url'] ):
				filtered.append( item )
		return filtered

	def call_by_event(self, *kwargs):
		errors = ''
		for func in self.fs_by_decos[ kwargs[0] ]:
			self.log( 'Try call function %s on event %s with args: %s'%(func.__name__, str(kwargs[0]), str(kwargs[1:])))
			try:
				func(*kwargs[1:])
				self.log('Function %s call in hook %s is ok'%(func.__name__, str(kwargs[0])))
			except Exception as e:
				errors += "\nException in %s. Arguments: %s. Exception: %s " % (func.__name__, str(kwargs[1:]), str(e))
				self.log('Pedant handle exception in %s. Arguments: %s. Exception: %s '%(func.__name__, str(kwargs[1:]), str(e)), level="ERROR")
		if errors:
			raise PedantError(errors)
		return

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

class ExampleState(Default):

	@event('before_all')
	def before_all_one(self):
		#self.browser - instance of webdriver
		return

	@event('before_all')
	def before_all_two(self):
		#self.browser - instance of webdriver
		return

	@event('before_one')
	def before_one(self, item):
		#self.browser - instance of webdriver
		return

	@event('before_screenshot')
	def before_screenshot(self, item):
		#self.browser - instance of webdriver
		return

	@event('after_one')
	def after_one(self, item):
		#self.browser - instance of webdriver
		return

	@event('after_all')
	def after_all(self):
		#self.browser - instance of webdriver
		return