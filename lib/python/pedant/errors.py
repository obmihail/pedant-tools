
class PedantError(Exception):
	pass

class Skip(PedantError):
	pass

class Fail(PedantError):
	pass

class BeforeScenarioError(PedantError):
	def __init__(self, message, scenario):
		super(BeforeScenarioError, self).__init__(message)
		self.scenario = scenario

class AfterScenarioError(PedantError):
	def __init__(self, message, scenario):
		super(AfterScenarioError, self).__init__(message)
		self.scenario = scenario

class BeforeStepError(PedantError):
	def __init__(self, message, step):
		super(BeforeStepError, self).__init__(message)
		self.step = step

class AfterStepError(PedantError):
	def __init__(self, message, step):
		super(AfterStepError, self).__init__(message)
		self.step = step