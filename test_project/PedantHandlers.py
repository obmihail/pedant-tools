from PedantStandartHandlers import PedantStandartHandlers

class PedantHandlers(PedantStandartHandlers):

	"""
	@param item - dict. { 'url' , 'unid', 'wait_js':[ {'timeout_ms','js', 'condition'} ] }
	@param browser - dict { 'unid', 'config', 'instance'} - current browser. 'Instance' -
selenium webdriver instance
	"""
	
	#self.log( "string", level='INFO' ) - write something to pedant log

	def before_screenshot(self, item, browser ):
		#self.wait_js( "return document.readyState != 'complete'", 5000 )
		pass