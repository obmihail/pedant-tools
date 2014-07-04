from PedantStandartHandlers import PedantStandartHandlers

class PedantHandlers(PedantStandartHandlers):

	def before_screenshot(self,item):
		self.wait_js( "return document.readyState != 'complete'", 5000 )
		#print self.run_js( "return document.readyState == 'complete'" )