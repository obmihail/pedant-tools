# import sys
# sys.path.insert(0, '/home/mihailob/projects/pedant-tools/lib/python/pedant/screenshots/' )
from PedantStandartHooks import PedantHooks
from PedantStandartHooks import hook


class Hooks(PedantHooks):

	"""
	PARENT VARS
	self.browser - dict of current browser. self.browser['instance'] - current webdriver instance.


	PARENT FUNCTIONS
	self.log( "log message", level='INFO' ) - write something to pedant log with level 'INFO'
	self.log( "log message", level='WARN' ) - write something to pedant log with level 'WARN'
	self.log( "log message", level='BLABLABLA' ) - write something to pedant running log with level 'BLABLABLA'
	self.wait_js( "return document.readyState != 'complete'", 5000 ) - wait js condition 5000 miliseconds

	HOOKS
	@hook( 'before_items' ) - function run before start items iterating. If you raise exception - pedant skip all items and mark report as failed
	@hook( 'before_item' ) - function run before url opening in browser. If you raise exception - pedant skip current item
	@hook( 'before_screenshot' ) - function run after url opening in browser and before screenshot capture. If you raise exception - pedant skip current item
	@hook( 'after_item' ) - function run after screenshot checking and before report save. If you raise exception - pedant do nothind
	@hook( 'after_items' ) - function run after all items iterate. If you raise exception - pedant do nothing
	"""


	@hook( 'before_items' )
	def log_my_items( self, items ):
		#self.log( "Before all items hook" )
		#self.browser['instance'].implicitly_wait(1)# set implicitly_wait for current browser
		pass


	@hook( 'before_item' )
	def before_item(self, item ):
		#example: self.wait_js( "return document.readyState != 'complete'", 5000 )
		#example: self.log( 'Log message before item ' + item['unid'] )
		pass


	@hook( 'before_screenshot' )
	def my_method( self, item ):
		#element = self.browser['instance'].find_element_by_class_name('input__control')
		pass


	@hook( 'after_item' )
	def after_item( self, item, result ):
		#print "after item hook for: ", item, result
		pass


	@hook( 'after_items' )
	def after_items( self, items ):
		#print "after all items:", items
		pass