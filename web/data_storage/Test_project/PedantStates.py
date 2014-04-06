# -*- coding: utf-8 -*-
from pedant.states import *
import behave

@description('Auth user')
@urls_regex('.*\?test')
class AuthState(Default):

	@event('before_all')
	def set_cookie(self):
		#raise Exception('Before items')
		return

	@event('before_one')
	def hide_ads(self, item):
		#raise Exception('Before item')
		return

@description('Просто открытые страницы')
class DefaultState(Default):

	@event('after_all')
	def my_after_all_method(self):
		pass