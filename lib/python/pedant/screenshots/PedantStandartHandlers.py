from time import sleep

class PedantStandartHandlers:
	
	browser = False

	def __init__(self,browser):
		self.browser = browser

	def before_screenshot(self,item,browser):
		pass

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

	def run_js(self, js):
		return self.browser['instance'].execute_script( js )
