from PedantStandartHandlers import PedantStandartHandlers

class PedantHandlers(PedantStandartHandlers):

	"""
	@param item - dict. { 'url' , 'unid', 'wait_js':[ {'timeout_ms','js', 'condition'} ] }
	@param browser - dict { 'unid', 'config', 'instance'} - current browser. 'Instance' -
selenium webdriver instance
	"""
	
	#self.log( "string", level='INFO' ) - write something to pedant log

	def before_screenshot(self,item, browser):
		#self.wait_js( "return document.readyState != 'complete'", 5000 )
		pass

	"""
	@param browser - dict { 'unid', 'config', 'instance'} - current browser. 'Instance' -
selenium wd instance - 
	@param item - dict. { 'url' , 'unid', 'wait_js':[ {'timeout_ms','js', 'condition'} ] }
	@param screenshot - base_64 string of taken screenshot. Important!! Its a link for var. You can change it

	"""
	def after_screenshot( self,item, screenshot ):
		#self.log( "Screenshot taken.Save copy to" , "screenshot_base_64" )
		pass