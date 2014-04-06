import os,sys,json,shutil,threading,inspect,re,glob,time,traceback,hashlib,imp,pedant,datetime,thread 
#import hashlib,Image,ImageChops,ImageDraw,uuid,urllib2,random
import hashlib,uuid,urllib2,random
from PIL import Image,ImageChops,ImageDraw
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pedant import get_json_from_file, put_json_to_file, load_module_from_file, create_folder_for_file
from pedant.errors import PedantError, Skip, Fail
from pedant.application import PedantApplication, PedantWorker
from states import Default

class Application(PedantApplication):
	
	def __init__(self, project, verbose=False, logging=True):
		#workers list
		PedantApplication.__init__(self,project,verbose,logging)
		#pathes for images
		rand = random.random()
		self.approved_dir = os.path.join(project.get_sources_dir(), 'pedant_data' ,'screens', 'approved')
		self.reports_dir = os.path.join(project.get_sources_dir(), 'pedant_data', 'screens', 'reports')
		self.pathes_skeletons = {
			'approved_image': os.path.join(self.approved_dir, '{1}', '{2}', '{3}','approved.png'),
			'approved_image_bckp': os.path.join(self.approved_dir, '{1}', '{2}','{3}','approved.png.bckp' ),
			'approved_image_thumb': os.path.join(self.approved_dir, '{1}', '{2}','{3}','approved.thumbnail.png'),
			'approved_info': os.path.join(self.approved_dir, '{1}', '{2}', '{3}','info.json'),
			'approved_info_bckp': os.path.join(self.approved_dir, '{1}', '{2}', '{3}','info.json.bckp'),
			'actual_image': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','actual.png'),
			'actual_image_thumb': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','actual.thumbnail.png'),
			'approved_report_image': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','approved_report.png'),
			'approved_report_image_bckp': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','approved_report.png.bckp' ),
			'approved_report_image_thumb': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','approved_report.thumbnail.png'),
			'diff_image': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','diff.png'),
			'diff_image_thumb': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','diff.thumbnail.png'),
			'diff_image_bckp': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','diff.png.bckp'),
			'report_json': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','report.json'),
			'report_json_bckp': os.path.join(self.reports_dir, '{0}', '{1}', '{2}','{3}','report.json.bckp'),
			'actual_image_web': '/projects/%s/static/pedant_data/screens/reports/{0}/{1}/{2}/{3}/actual.png?%s'%(project.get_name(),rand),
			'actual_image_web_thumb': '/projects/%s/thumbnail/pedant_data/screens/reports/{0}/{1}/{2}/{3}/actual.png?%s'%(project.get_name(),rand),
			'approved_image_web': '/projects/%s/static/pedant_data/screens/approved/{1}/{2}/{3}/approved.png?%s'%(project.get_name(),rand),
			'approved_image_web_thumb': '/projects/%s/thumbnail/pedant_data/screens/approved/{1}/{2}/{3}/approved.png?%s'%(project.get_name(),rand),
			'approved_report_image_web': '/projects/%s/static/pedant_data/screens/reports/{0}/{1}/{2}/{3}/approved_report.png?%s'%(project.get_name(),rand),
			'approved_report_image_web_thumb': '/projects/%s/thumbnail/pedant_data/screens/reports/{0}/{1}/{2}/{3}/approved_report.png?%s'%(project.get_name(),rand),
			'diff_image_web': '/projects/%s/static/pedant_data/screens/reports/{0}/{1}/{2}/{3}/diff.png?%s'%(project.get_name(),rand),
			'diff_image_web_thumb': '/projects/%s/thumbnail/pedant_data/screens/reports/{0}/{1}/{2}/{3}/diff.png?%s'%(project.get_name(),rand),
		}
		#default states
		self.states_classes = [Default]
		#states
		self.import_states_from_dir(project.get_sources_dir())

	def build(self, mode=None, states_ids=[]):
		#current timestamp
		self.timestamp = time.time()
		report_dir = os.path.join(self.reports_dir, str(self.timestamp))
		self.threads_limit = self.project.get_threads_count()
		if self.logging:
			self.log_file = os.path.join(report_dir, 'log.txt')
			os.makedirs(os.path.dirname(self.log_file)) if not os.path.isdir(os.path.dirname(self.log_file)) else None
		if mode:
			browsers_ids,mode_states_ids = self.project.get_mode_params(mode)
			if not states_ids:
				states_ids = mode_states_ids
			states = self.get_states_instances_by_ids(states_ids)
			self.project.filter_browsers(browsers_ids)
		else:
			states = self.get_states_instances_by_ids(states_ids)
		browsers = self.project.get_browsers()
		items = self.project.get_items_for_scanning()
		if not items:
			raise PedantError('Urls is empty')
		save_diffs = self.project.get_diffs_saving_value()
		for state in states:
			filtered_items = state.filter_items(items)
			if len(filtered_items) < 1:
				self.log('Skipe state %s. Can not found urls for scanning'%state.get_id())
				continue
			filtered_browsers = state.filter_browsers(browsers)
			if len(filtered_browsers) < 1:
				self.log('Skip state %s. Browsers is empty'%state.get_id())
				continue
				#raise PedantError('Browsers not found for state %s ')
			#make workers by browsers count
			for browser in filtered_browsers:
				count_for_one_worker = (len(filtered_items)/self.threads_limit) if (len(filtered_items)/self.threads_limit)>0 else 1
				chunked_items = [filtered_items[x:x+count_for_one_worker] for x in xrange(0, len(filtered_items), count_for_one_worker)]
				for items_part in chunked_items:
					[self.statistic['TOTAL'].put(item) for item in items_part]
					self.expectation_workers_list.append(Worker(state, browser, items_part, report_dir, self.statistic, save_diffs=save_diffs))
		return self

	def get_pathes(self, timestamp='', item='', state='', browser=''):
		timestamp = str(timestamp)
		return {k: v.format( *[ timestamp, item, state, browser  ] ) for k, v in self.pathes_skeletons.items()}

	"""
	Find hook file in directory and load it
	"""
	def import_states_from_dir(self,search_directory):
		#try find hooks
		state_file = os.path.join( search_directory , 'PedantStates.py' )
		if os.path.isfile(state_file):
			try:
				state_module = load_module_from_file(state_file)
			except Exception as e:
				#get only last error
				pattern = re.compile("\sFile.*return\ imp\.load_module\(unique\_name\,\ fp\,\ filepath\,\ description\)",re.MULTILINE|re.DOTALL)
				tb = pattern.sub("", str(traceback.format_exc()))
				raise PedantError( 'Project state load exception. %s' % tb )
			states_classes = [cls[1] for cls in inspect.getmembers(state_module, inspect.isclass) if 'Default' in str(cls[1].__bases__) ]
			if len( states_classes ) < 1:
				raise PedantError( 'State load error. Class with parent PedantState not found in %s' %state_file )
			self.states_classes = states_classes
		return self

	def get_states_instances_by_mode(self, mode_name):
		prj_config = self.project.get_config()
		if mode_name and prj_config['modes'].has_key(mode_name):
			return self.get_states_instances_by_ids(prj_config['modes'][mode_name]['states'])
		elif mode_name:
			raise PedantError('Unknown mode %s'%mode_name)
		else:
			return self.get_all_states_instances()

	def get_states_instances_by_ids(self, ids_list=[]):
		if ids_list:
			ids_list = [id.lower() for id in ids_list]
			#check ids_list contains real states ids
			unknown_states = list(ids_list)
			[unknown_states.remove(state.__name__.lower()) for state in self.states_classes if state.__name__.lower() in ids_list ]
			if unknown_states:
				raise PedantError("Unknown states: %s"%unknown_states)
		#return filtered states by ids_list
		return [state() for state in self.states_classes if state.__name__.lower() in ids_list or len(ids_list)<1 ]

	def get_all_states_instances(self):
		return [state() for state in self.states_classes]

	"""
	Approve action
	"""
	def approve_image(self, timestamp, item, state, browser):
		if not self.project.access():
			raise PedantError("Have not access to project %s, can not approve image" % project.get_root_dir())
		pathes = self.get_pathes(timestamp, item, state, browser)
		#raise exception if actual image not found
		if not os.path.isfile(pathes['actual_image']):
			raise PedantError("Actual image not found. Filepath: %s"%pathes['actual_image'])
		#clear thumbnails
		os.remove(pathes['diff_image_thumb']) if os.path.isfile(pathes['diff_image_thumb']) else None
		os.remove(pathes['approved_report_image_thumb'] ) if os.path.isfile(pathes['approved_report_image_thumb']) else None
		os.remove(pathes['approved_image_thumb']) if os.path.isfile(pathes['approved_image_thumb']) else None
		os.remove(pathes['diff_image_thumb']) if os.path.isfile(pathes['diff_image_thumb']) else None
		#backup approved image in report dir
		os.remove( pathes['approved_report_image_bckp'] ) if os.path.isfile( pathes['approved_report_image_bckp'] ) else None
		os.rename( pathes['approved_report_image'], pathes['approved_report_image_bckp'] ) if os.path.isfile( pathes['approved_report_image'] ) else None
		#backup diff image in report dir
		os.remove( pathes['diff_image_bckp'] ) if os.path.isfile( pathes['diff_image_bckp'] ) else None
		os.rename( pathes['diff_image'], pathes['diff_image_bckp'] ) if os.path.isfile( pathes['diff_image'] ) else None
		#backup approved image in approved dir
		os.remove( pathes['approved_image_bckp'] ) if os.path.isfile( pathes['approved_image_bckp'] ) else None
		os.rename( pathes['approved_image'], pathes['approved_image_bckp'] ) if os.path.isfile( pathes['approved_image'] ) else None
		#backup json
		os.remove( pathes['report_json_bckp'] ) if os.path.isfile(pathes['report_json_bckp']) else None
		os.rename( pathes['report_json'], pathes['report_json_bckp'] ) if os.path.isfile( pathes['report_json'] ) else None
		#get json data from backuped report
		json_report = get_json_from_file(pathes['report_json_bckp'])
		#create approved folder if it's need
		os.makedirs(os.path.dirname( pathes['approved_image'] )) if not os.path.isdir( os.path.dirname(pathes['approved_image']) ) else None
		#put info to approved image dir if not exists
		image_info = { 
					'item': {'url': json_report['item']['url'], 'id': json_report['item']['id']}, 
					'browser': json_report['browser'], 
					'state': json_report['state'],
					'report': timestamp }
		os.remove(pathes['approved_info_bckp']) if os.path.isfile(pathes['approved_info_bckp']) else None
		os.rename(pathes['approved_info'], pathes['approved_info_bckp']) if os.path.isfile(pathes['approved_info']) else None 
		put_json_to_file(pathes['approved_info'], image_info)

		#copy actual to approved and report
		shutil.copyfile( pathes['actual_image'], pathes['approved_image'] )
		shutil.copyfile( pathes['actual_image'], pathes['approved_report_image'] )
		
		#update json, save it to file
		json_report['status'] = PedantWorker._PASSED
		put_json_to_file(pathes['report_json'], json_report)

		#images web pathes
		json_report['images'] = {
			'actual': pathes['actual_image_web'] if os.path.isfile( pathes['actual_image'] ) else False,
			'actual_thumbnail': pathes['actual_image_web_thumb'] if os.path.isfile( pathes['actual_image'] ) else False,
			'approved': pathes['approved_image_web'] if os.path.isfile( pathes['approved_image'] ) else False,
			'approved_thumbnail': pathes['approved_image_web_thumb'] if os.path.isfile( pathes['approved_image'] ) else False,
			'approved_report': pathes['approved_report_image_web'] if os.path.isfile( pathes['approved_report_image'] ) else False,
			'approved_report_thumbnail': pathes['approved_report_image_web_thumb'] if os.path.isfile( pathes['approved_report_image'] ) else False,
			'diff': pathes['diff_image_web'] if os.path.isfile( pathes['diff_image'] ) else False,
			'diff_thumbnail': pathes['diff_image_web_thumb'] if os.path.isfile( pathes['diff_image'] ) else False,
		}
		return json_report

	def cancel_approve_image(self, timestamp, item, state, browser):
		if not self.project.access():
			raise PedantError("Have not access to project %s, can not cancel approve image" % self.project.get_root_dir())
		pathes = self.get_pathes(timestamp, item, state, browser)
		#clear thumbnails
		os.remove(pathes['diff_image_thumb']) if os.path.isfile(pathes['diff_image_thumb']) else None
		os.remove(pathes['approved_report_image_thumb'] ) if os.path.isfile(pathes['approved_report_image_thumb']) else None
		os.remove(pathes['approved_image_thumb']) if os.path.isfile(pathes['approved_image_thumb']) else None
		os.remove(pathes['diff_image_thumb']) if os.path.isfile(pathes['diff_image_thumb']) else None
		#restore image in approved
		os.remove( pathes['approved_image'] ) if os.path.isfile( pathes['approved_image'] ) else None
		os.rename( pathes['approved_image_bckp'], pathes['approved_image'] ) if os.path.isfile( pathes['approved_image_bckp'] ) else None
		#restore approved image in report
		os.remove( pathes['approved_report_image'] ) if os.path.isfile( pathes['approved_report_image'] ) else None
		os.rename( pathes['approved_report_image_bckp'], pathes['approved_report_image'] ) if os.path.isfile( pathes['approved_report_image_bckp'] ) else None
		#restore diff image
		os.remove( pathes['diff_image'] ) if os.path.isfile( pathes['diff_image'] ) else None
		os.rename( pathes['diff_image_bckp'], pathes['diff_image'] ) if os.path.isfile( pathes['diff_image_bckp'] ) else None
		#restore report.json if backup exists
		os.remove( pathes['report_json'] ) if os.path.isfile(pathes['report_json']) and os.path.isfile(pathes['report_json_bckp']) else None
		os.rename( pathes['report_json_bckp'], pathes['report_json'] ) if os.path.isfile( pathes['report_json_bckp'] ) else None
		#restore approved info file
		os.remove(pathes['approved_info']) if os.path.isfile(pathes['approved_info']) else None 
		os.rename(pathes['approved_info_bckp'],pathes['approved_info']) if os.path.isfile(pathes['approved_info_bckp']) else None 
		#read report
		json_report = get_json_from_file(pathes['report_json'])
		#set images
		json_report['images'] = {
			'actual': pathes['actual_image_web'] if os.path.isfile( pathes['actual_image'] ) else False,
			'actual_thumbnail': pathes['actual_image_web_thumb'] if os.path.isfile( pathes['actual_image'] ) else False,
			'approved': pathes['approved_image_web'] if os.path.isfile( pathes['approved_image'] ) else False,
			'approved_thumbnail': pathes['approved_image_web_thumb'] if os.path.isfile( pathes['approved_image'] ) else False,
			'approved_report': pathes['approved_report_image_web'] if os.path.isfile( pathes['approved_report_image'] ) else False,
			'approved_report_thumbnail': pathes['approved_report_image_web_thumb'] if os.path.isfile( pathes['approved_report_image'] ) else False,
			'diff': pathes['diff_image_web'] if os.path.isfile( pathes['diff_image'] ) else False,
			'diff_thumbnail': pathes['diff_image_web_thumb'] if os.path.isfile( pathes['diff_image'] ) else False,
		}
		return json_report

	def get_report(self, timestamp):
		data = list()
		for json_file in glob.glob(os.path.join(self.reports_dir, timestamp, '*', '*', '*', 'report.json')):
			json_report = get_json_from_file(json_file)
			json_report['item'] = self.rename_key(json_report['item'],'unid','id')
			json_report['state'] = self.rename_key(json_report['state'],'unid','id')
			json_report['browser'] = self.rename_key(json_report['browser'],'unid','id')
			pathes = self.get_pathes(timestamp, json_report['item']['id'], json_report['state']['id'], json_report['browser']['id'])
			#set images
			json_report['images'] = {
				'actual': pathes['actual_image_web'] if os.path.isfile( pathes['actual_image'] ) else False,
				'actual_thumbnail': pathes['actual_image_web_thumb'] if os.path.isfile( pathes['actual_image'] ) else False,
				'approved': pathes['approved_image_web'] if os.path.isfile( pathes['approved_image'] ) else False,
				'approved_thumbnail': pathes['approved_image_web_thumb'] if os.path.isfile( pathes['approved_image'] ) else False,
				'approved_report': pathes['approved_report_image_web'] if os.path.isfile( pathes['approved_report_image'] ) else False,
				'approved_report_thumbnail': pathes['approved_report_image_web_thumb'] if os.path.isfile( pathes['approved_report_image'] ) else False,
				'diff': pathes['diff_image_web'] if os.path.isfile( pathes['diff_image'] ) else False,
				'diff_thumbnail': pathes['diff_image_web_thumb'] if os.path.isfile( pathes['diff_image'] ) else False,
			}
			data.append(json_report)
		return data

	def rename_key(self,dict_to_rename,old,new):
		if dict_to_rename.has_key(old):
			val = dict_to_rename[old]
			del dict_to_rename[old]
			dict_to_rename[new] = val
		return dict_to_rename

	def get_approved_images(self):
		pathes = self.get_pathes( '','','' )
		data = list()
		for img_path in glob.glob( os.path.join( self.approved_dir, '*', '*', '*', 'approved.png' ) ):
			info_path = img_path.replace('approved.png','info.json')
			if not os.path.isfile(info_path):
				continue
			info = get_json_from_file(info_path)
			#correct for old reports
			info['item'] = self.rename_key(info['item'],'unid','id')
			info['browser'] = self.rename_key(info['browser'],'unid','id')
			info['state'] = self.rename_key(info['state'],'unid','id')
			item_pathes = self.get_pathes('', info['item']['id'], info['state']['id'], info['browser']['id'])
			#print item_pathes['approved_image']
			info['images'] = {
				'approved': item_pathes['approved_image_web'] if os.path.isfile(item_pathes['approved_image']) else False,
				'approved_thumbnail': item_pathes['approved_image_web_thumb'] if os.path.isfile(item_pathes['approved_image']) else False
				}
			data.append(info)
		return data

	def delete_approved_image(self, item, state, browser):
		folder_path = os.path.join(self.approved_dir, item, state, browser)
		if os.path.isdir(folder_path):
			shutil.rmtree(folder_path)
		return 'removed' if os.path.isdir(folder_path) else 'can not remove folder %s' % folder_path

"""
Screens worker
"""

class Worker(PedantWorker):

	def __init__(self, state, browser, items, report_dir, queues, save_diffs=True ):
		PedantWorker.__init__(self, report_dir)
		#browser dict may be using in another worker, need copy
		self.set_queues( finished=queues['FINISHED'],skipped=queues['SKIPPED'],failed=queues['FAILED'],passed=queues['PASSED'] )
		self.browser_config = browser.copy()
		self.browser = None
		self.state = state
		self.save_diffs = save_diffs
		self.items = list(items)
		suffix = os.path.join( '%s', self.state.get_id(), self.browser_config['id']).encode('utf-8')
		#set pathes skeletons
		self.path_skeletons = {
			'approved': os.path.join( os.path.dirname(os.path.dirname(self.report_dir)), 'approved' , suffix, 'approved.png'),
			'actual_report': os.path.join(self.report_dir, suffix, 'actual.png'),
			'approved_report': os.path.join(self.report_dir, suffix, 'approved_report.png'),
			'diff_report': os.path.join(self.report_dir, suffix, 'diff.png'),
			'report_json': os.path.join(self.report_dir, suffix, 'report.json')
		}

	"""
	run thread
	@return void
	"""
	def run(self):
		#init browser and state
		try:
			self.browser = self.init_browser(self.browser_config)
			self.state.set_browser(self.browser)
			self.state.log = self.log
			self.state.call_by_event('before_all')
		except Exception as e:
			self.log("Urls been skipped. Cause: %s"%str(e), level="ERROR")
			self.browser = self.browser_config
			self.browser['instance'] = False
			[self.save_result(item, {'status':PedantWorker._FAILED, 'exceptions':[str(e)]}) for item in self.items]
			thread.exit()
		#items
		for item in self.items:
			if (self._stopped):
				self.log("Skip url: %s. Cause: Worker got a stop signal"%item['url'])
				self.save_result(item, {'status':PedantWorker._SKIPPED, 'exceptions':['Worker got a stop signal']})
				continue
			self.log("Start checking url: %s in state: %s(%s)"%(item['url'].decode('utf-8'),self.state.get_description().decode('utf-8'),self.state.get_id()))
			try:
				#before item event
				self.state.call_by_event('before_one', item)
				#open url
				start_time = time.time()
				self.browser['instance'].get(item['url'])
				item['load_time'] = round(time.time()-start_time, 2)
				#before_screenshot event
				self.state.call_by_event('before_screenshot', item)
				comp_res = self.screen_processing(item)
				#after one event
				self.state.call_by_event('after_one', item)
				self.save_result(item, {'status': comp_res[1], 'comparison_result': comp_res[0] })
			except Skip as e:
				self.log("Worker got Skip exception for item: %s. Exception: %s"%(str(item), str(e)), level="INFO")
				self.save_result(item, {'status': PedantWorker._SKIPPED, 'exceptions': [ str(e) ]})
			except Fail as e:
				self.log("Worker got Fail exception for item: %s. Exception: %s"%(str(item), str(e)), level="INFO")
				self.save_result(item, {'status': PedantWorker._FAILED, 'exceptions': [ str(e) ]})
			except Exception as e:
				self.log("Worker got exception for item: %s. Exception: %s"%(str(item), str(e)), level="ERROR")
				self.save_result(item, {'status': PedantWorker._FAILED, 'exceptions': [ str(e) ]})
			self.log("Finish checking url %s"%item['url'])
		#after_all event
		try:
			self.state.call_by_event('after_all')
		except Exception as e:
			self.log( "Exception in after_all event: %s"%str(e), level='ERROR')
			self.save_result(item, {'status': PedantWorker._FAILED, 'exceptions': [str(e)]})
		self.browser['instance'].close()
		self._stopped = True
		self.log("Disconnect from selenium browser with id %s"%self.browser['id'])
		return

	"""
	This function do work with taked screenshot
	@param item - dict with info about scanning item
	@param screenshot - png in string. Taked screenshot 
	"""
	def screen_processing(self, item ):
		#generate pathes for item
		pathes = self.get_pathes_for_item(item)
		if not self.save_diffs:
			pathes['diff_report'] = False
		#save screenshot
		self.browser['instance'].save_screenshot(pathes['actual_report'])
		#check actual screenshot was saved
		self.log('Start screen processing for url %s'%item['url'])
		if os.path.isfile(pathes['actual_report']):
			#try find approve screenshot
			if os.path.getsize(pathes['actual_report']) < 1:
				self.log('Remove empty actual screenshot for url %s'%item['url'], level='ERROR')
				os.remove(pathes['actual_report'])
				raise PedantError('Actual screenshot is empty. Url: %s Path: %s'%(item['url'],pathes['actual_report']))
			if os.path.isfile(pathes['approved']):
				#check file size, if empty - raise error
				if os.path.getsize(pathes['approved']) > 0:
					shutil.copyfile(pathes['approved'], pathes['approved_report'])
					self.log('Try compare screen for url %s'%item['url'])
					return compare_images(pathes['approved'], pathes['actual_report'], pathes['diff_report'])
				else:
					self.log('Remove empty approved image for url %s'%item['url'], level='ERROR')
					os.remove(pathes['approved'])
					raise PedantError('Saving error: Screenshot is empty. Path: %s'%pathes['actual_report'])
			#have not approved
			else:
				return ('APPROVED_NOT_FOUND', PedantWorker._FAILED)
		else:
			raise PedantError('Saving error. Path: %s'%pathes['actual_report'])

	def get_pathes_for_item( self, item ):
		pathes = {}
		for key,path in self.path_skeletons.iteritems():
			pathes[key] = create_folder_for_file( path % item['id'].encode('utf-8') )
		return pathes

	def save_result(self, item, report_info={}):
		pathes = self.get_pathes_for_item(item)
		bro = self.browser.copy()
		del bro['instance']
		if not item.has_key('load_time'):
			item['load_time'] = 0
		report = {
				'item': item,
				'browser': bro,
				'state': {'id': self.state.get_id(), 'description': self.state.get_description()},
				'comparison_result': 'None',
				'status': 'unknown',
				'exceptions': []
				}
		report.update(report_info)
		#calc stats
		item_unique = "%s-%s-%s"%(item['id'],self.state.get_id(),self.browser['id'])
		if report["status"] == PedantWorker._PASSED:
			self._PASSED_QUEUE.put(item_unique)
		elif report["status"] == PedantWorker._SKIPPED:
			self._SKIPPED_QUEUE.put(item_unique)
		else:
			self._FAILED_QUEUE.put(item_unique)
		self._FINISHED_QUEUE.put(item_unique)
		self.log("Save report for item: %s "%item['url'])
		with open(pathes['report_json'], 'wb') as file_:
			json.dump(report, file_)
		return

"""
This function compare two images and save difference in diff_path
@param image_A_path string - path to first image
@param image_B_path string - path to second image
@param diff_path string - path to save difference image
@return bool - True if images has a difference, and false - if images are same
"""
def compare_images(image_A_path, image_B_path, diff_path):
	#
	dataA = open(image_A_path, 'rb').read()
	dataB = open(image_B_path, 'rb').read()
	if hashlib.md5(dataA).hexdigest() != hashlib.md5(dataB).hexdigest():
		#make one size
		# ToDo
		if diff_path:
			imageA = Image.open(image_A_path)
			imageB = Image.open(image_B_path)
			#get max image size
			w_size = max( [ imageA.size[0] , imageB.size[0] ] )
			h_size = max( [ imageA.size[1] , imageB.size[1] ] )
			#if sizes not match - resize smalled
			if (imageA.size != imageB.size):
				#make new size image
				imageA = imageA.transform((w_size, h_size), Image.EXTENT , [0,0,w_size,h_size])
				imageB = imageB.transform((w_size, h_size), Image.EXTENT , [0,0,w_size,h_size])
			#calculate dirty diff
			diff = ImageChops.difference(imageA, imageB).convert("RGB")
			#for big images - skip pretty difference transforming, because it eating memory 
			# if w_size < 3000 and h_size < 3000:
			# 	#better pretty diff (very hardly, only for small images)
			# 	background = Image.new('RGBA', (w_size,h_size), (200, 200, 200, 100))
			# 	mask = Image.new('L', (w_size,h_size), 0xC0)
			# 	imageA.paste(background, (0,0) , mask)
			# 	imageA = imageA.convert("RGBA")
			# 	diffList = list(diff.getdata())
			# 	imageA.putdata( [ (255,0,0,180) if diffList[key] != (0,0,0) else x for key,x in enumerate(imageA.getdata())] )
			# 	imageA = imageA.convert("RGB")
			# 	#save diff
			# 	imageA.save(diff_path , "PNG")
			# else:
			#save black diff
			diff.save(diff_path , "PNG")
		return ('DIFF_FOUNDED', PedantWorker._FAILED)
	return ('SAME_IMAGES', PedantWorker._PASSED)