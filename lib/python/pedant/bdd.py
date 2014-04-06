import os,sys,json,shutil,inspect,re,glob,time,traceback,hashlib,imp,pedant,datetime,copy,random,thread,Queue,StringIO
from collections import OrderedDict
from pedant.errors import *
from pedant import get_json_from_file,put_json_to_file,load_module_from_file
from pedant.application import PedantWorker,PedantApplication
from pedant.screens import compare_images
#behave
from behave.runner_util import parse_features
from behave.configuration import Configuration, ConfigError
from behave.runner import Runner,Context
from behave.i18n import languages
from behave.formatter._registry import make_formatters
from behave.formatter.base import StreamOpener
from behave.formatter.json import JSONFormatter
from behave.formatter.plain import PlainFormatter
from behave.runner_util import make_undefined_step_snippet
from behave import step_registry
from behave.model import ScenarioOutline,Step
#
from behave.runner_util import print_undefined_step_snippets, \
	InvalidFileLocationError, InvalidFilenameError, FileNotFoundError
import six
#wd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_feature_dict(feature):
	feature_keys = ['name','filename','keyword','line','description','tags','type','scenarios','status','duration','background','line','error_message']
	language = feature.parser.language
	feature = dict((name, getattr(feature, name)) for name in dir(feature) if name in feature_keys)
	if feature.has_key('background') and feature['background']:
		feature['background'] = get_background_dict(feature['background'])
	feature['elements'] = [ get_scenario_dict(scenario) for scenario in feature['scenarios'] ]
	feature['language'] = language
	del feature['scenarios']
	return feature

def get_background_dict(background):
	return {
		'location': background.location.__dict__,
		'keyword': background.keyword,
		'steps': [ get_step_dict(step) for step in background.steps ],
		'name' : background.name
	}

def get_scenario_dict(scenario):
	scenario_keys = ['name','filename','keyword','line','description','tags','type','steps','status','error_message','_scenarios']
	scenario = dict((name, getattr(scenario, name)) for name in dir(scenario) if name in scenario_keys)
	scenario['steps'] = [ get_step_dict(step) for step in scenario['steps'] ]
	if scenario.has_key('_scenarios'):
		scenario['_scenarios'] = [ get_scenario_dict(_scenario) for _scenario in scenario['_scenarios'] ]
	return scenario

def get_step_dict(step):
	step_keys = ['name','filename','keyword','line','description','tags','type','step_type','status','error_message','screenshot_name']
	return dict((name, getattr(step, name)) for name in dir(step) if name in step_keys)

def is_screens_taking_scenario(scenario):
	if 'screenshots' in scenario.tags:
		return True
	return False

def is_screens_comparison_scenario(scenario):
	if 'compare' in scenario.tags:
		return True
	return False

def is_ui_scenario(scenario):
	if 'ui' in scenario.tags or is_screens_taking_scenario(scenario) or is_screens_comparison_scenario(scenario):
		return True
	return False

def is_ui_feature(feature):
	for scenario in feature.scenarios:
		if is_ui_scenario(scenario):
			return True
	return False

def is_parallel_feature(feature):
	if 'parallel' in feature.tags and not 'parallelscenarios' in feature.tags:
		return True
	return False

def is_parallel_scenarios_feature(feature):
	if 'parallelscenarios' in feature.tags:
		return True
	return False

class CustomPlainFormatter(PlainFormatter):
	def add_current_step_screenshot(self,key,screenshot):
		pass

	def modify_current_element(self, mod_dict):
		pass

	def modify_current_step_result(self, res_dict):
		pass

	def update_status_data(self,status=None):
		pass

	def update_step_result(self,step_index,result):
		pass

class CustomJsonFormatter(JSONFormatter):

	def __init__(self, stream_opener, config):
		super(CustomJsonFormatter, self).__init__(stream_opener, config)

	def modify_current_element(self, mod_dict):
		self.current_feature_element.update(mod_dict)

	def add_current_step_screenshot(self,key,screenshot):
		steps = self.current_feature_element['steps']
		step_index = self._step_index-1 if self._step_index>0 else self._step_index
		if steps[step_index]['screenshots'].has_key(key) and steps[step_index]['screenshots'][key]: 
			steps[step_index]['screenshots'][key].append(screenshot)
		else:
			steps[step_index]['screenshots'][key] = [screenshot]

	def modify_current_step_result(self, res_dict):
		steps = self.current_feature_element['steps']
		step_index = self._step_index-1
		step_index = 0 if step_index<0 else step_index
		if not steps[step_index].has_key('result'):
			steps[step_index]['result'] = {}
		result_element = steps[step_index]['result']
		result_element.update(res_dict)

	def update_status_data(self,status=None):
		if self.current_feature_data and self.current_feature_data['status'] == 'untested':
			self.current_feature_data['status'] = self.current_feature.status
		if status:
			self.current_feature_data['status'] = status

	def update_step_result(self,step_index,result):
		steps = self.current_feature_element['steps']
		if not steps[step_index].has_key('result'):
			steps[step_index]['result'] = {
				'status': result.status,
				'duration': result.duration,
			}
		else:
			steps[step_index]['result']['status'] = result.status
			steps[step_index]['result']['duration'] = result.duration
		#store previously error
		error_message = result.error_message
		#error_message =  '%s\n%s'%(prev_error,result.error_message)
		if self.split_text_into_lines and "\n" in error_message:
			error_message = error_message.splitlines()
			#steps[step_index]['result']['error_message'] = error_message
		if not steps[step_index]['result'].has_key('error_message'):
			steps[step_index]['result']['error_message'] = []

		steps[step_index]['result']['error_message'].append("\n Also: ")
		steps[step_index]['result']['error_message'].append(error_message)
			

	def step(self, step):
		s = {
			'keyword': step.keyword,
			'step_type': step.step_type,
			'name': step.name,
			'location': six.text_type(step.location),
			'screenshots': {'actual':[]}
		}

		if step.text:
			text = step.text
			if self.split_text_into_lines and "\n" in text:
				text = text.splitlines()
			s['text'] = text
		if step.table:
			s['table'] = self.make_table(step.table)
		element = self.current_feature_element
		element['steps'].append(s)

	def scenario(self, scenario):
		element = self.add_feature_element({
			'type': 'scenario',
			'keyword': scenario.keyword,
			'name': scenario.name,
			'tags': scenario.tags,
			'location': six.text_type(scenario.location),
			'browser_config': scenario.browser_config if hasattr(scenario,'browser_config') else False,
			'steps': [],
		})
		if scenario.description:
			element['description'] = scenario.description
		self._step_index = 0

	def scenario_outline(self, scenario_outline):
		element = self.add_feature_element({
			'type': 'scenario_outline',
			'keyword': scenario_outline.keyword,
			'name': scenario_outline.name,
			'tags': scenario_outline.tags,
			'location': six.text_type(scenario_outline.location),
			'steps': [],
			'examples': [],
		})
		if scenario_outline.description:
			element['description'] = scenario_outline.description
		self._step_index = 0

class CustomBehaveContext(Context):

	def __init__(self,runner):
		Context.__init__(self,runner)
		self.should_run = True

	def set_browser_config(self,browser):
		self.browser_config = browser
		return self

	def start_browser(self):
		self.browser = None
		#set browser info to scenario report
		#for formatter in self._runner.formatters:
		#	formatter.modify_current_element({'browser_config': })
		if self.browser_config:
			try:
				caps = getattr(DesiredCapabilities , self.browser_config['type'].upper()) if hasattr(DesiredCapabilities , self.browser_config['type'].upper()) else {}
				if self.browser_config.has_key('desired_capabilities'):
					caps.update(self.browser_config['desired_capabilities']) #= dict( caps.items() + .items() )
				#print caps
				self.browser = webdriver.Remote(
				command_executor=str(self.browser_config['wd_url']),
				desired_capabilities=caps,
				keep_alive=False)
			except Exception as e:
				raise BeforeScenarioError(e,self.scenario)
		return self

	def set_screens_directory(self,directory):
		self.screenshots_dir = directory
		return self

	def get_project(self):
		return self._runner.get_poject()

	def get_browser(self):
		if hasattr(self,'browser') and self.browser:
			return self.browser
		raise Exception('Browser not initialized')

	def stop_browser(self):
		if hasattr(self,'browser') and self.browser:
			self.browser.quit()
		return self


class CustomBehaveRunner(Runner):

	def stop_capture(self):
		pass

	def start_capture(self):
		self.stderr_capture = StringIO.StringIO()
		self.log_capture = StringIO.StringIO()
		pass

	def setup_capture(self):
		pass

	def teardown_capture(self):
		pass

	def get_features(self):
		return self.features

	def load_features(self,filter_params={}):
		self.features = []
		self.config = copy.copy(self.config)
		feature_locations = [ filename for filename in self.feature_locations() if not self.config.exclude(filename) ]
		features = parse_features(feature_locations, language=self.config.lang)
		self.features.extend(features)
		#make a feature deep copy for launch in threads
		# for feature in self.features:
		# 	#make a copy of scenarios objects with steps
		# 	feature.scenarios = [ copy.copy(scenario) for scenario in feature.walk_scenarios() ]
		# 	for scenario in feature.walk_scenarios():
		# 		if scenario._background_steps:
		# 			scenario._background_steps = copy.deepcopy(scenario._background_steps)
		# 		scenario.steps = copy.deepcopy(scenario.steps)
		# 		#for step in scenario.all_steps:
		# 		#	#print scenario,id(scenario),step.name,id(step)
		self.filter_features(filter_params)
		return self

	def filter_features(self,filter_params):
		filter_d = {'features':[],'scenarios':[],'steps':[],'tags':[]}
		filter_d.update(filter_params)
		if filter_d['features']:
			#filter features by name or filename
			self.features = filter(lambda feature: (feature.name in filter_d['features'] or feature.location.filename in filter_d['features']), self.features)
		if filter_d['tags']:
			#todo
			pass
		#filter steps and scenarios
		for feature in self.features:
			if filter_d['scenarios']:
				#filter scenarios by name or filename:line
				feature.scenarios = filter(lambda scenario: (scenario.name in filter_d['scenarios'] or '%s:%d'%(scenario.location.filename,scenario.location.line) in filter_d['scenarios']), feature.walk_scenarios())
			for scenario in feature.walk_scenarios():
				if filter_d['steps']:
					#filter steps by name or filename:line
					scenario.steps = filter(lambda step: (step.name in filter_d['steps'] or '%s:%d'%(step.location.filename,step.location.line) in filter_d['steps']), scenario.steps)
			#remove empty scenarios
			feature.scenarios = filter(lambda scenario: len(scenario.steps) > 0, feature.walk_scenarios())
		#remove empty features
		self.features = filter(lambda feature: len(feature.scenarios) > 0, self.features)
		return self

	def add_hooks(self,hooks_dict):
		for key in hooks_dict.keys():
			if not self.hooks.has_key(key):
				self.hooks[key] = []
			elif type(self.hooks[key]) is not list:
				self.hooks[key] = [ self.hooks[key] ]
			[ self.hooks[key].append(func) for func in hooks_dict[key] ]
		return self

	def run_hook(self, name, context, *args):
		if not self.config.dry_run and (name in self.hooks):
			with context.user_mode():
				if type(self.hooks[name]) is list:
					for hook_f in self.hooks[name]:
						hook_f(context, *args)
				else:
					self.hooks[name](context, *args)

	def set_worker(self,worker):
		self._worker = worker

	def set_project(self,project):
		self._project = project

	def get_poject(self):
		return self._project

	#make a feature deep copy for launch in threads
	def make_feature_deep_copy(self,feature):
		#make a copy of scenarios objects with steps
		feature.scenarios = [ copy.copy(scenario) for scenario in feature.walk_scenarios() ]
		for scenario in feature.walk_scenarios():
			#print scenario.__dict__
			if scenario.background:
				scenario.background = copy.deepcopy(scenario.background)
			scenario.steps = [copy.copy(step) for step in scenario.steps ]
		return feature

	def chunk_self(self,features_count=0,scenarios_count=0):
		clones = []
		if features_count:
			features_parts = [self.features[x:x+features_count] for x in xrange(0, len(self.features), features_count)]
			for part in features_parts:
				_f_runner = copy.copy(self)
				_f_runner.features = part
				clones.append(_f_runner)
		elif scenarios_count:
			features = []
			for feature in self.features:
				all_scenarios = feature.walk_scenarios()
				scenarios_parts = features_parts = [all_scenarios[x:x+scenarios_count] for x in xrange(0, len(all_scenarios), scenarios_count)]
				for part in scenarios_parts:
					#make clone
					_s_runner = copy.copy(self)
					_feature = copy.copy(feature)
					#set scenarios
					_feature.scenarios = part
					#set one feature
					_s_runner.features=[_feature]
					clones.append(_s_runner)
		else:
			pass
		return clones

	def reload_formatters(self,streams):
		self.formatters = [ CustomJsonFormatter(streams[0],self.config), CustomPlainFormatter(streams[1],self.config) ]

	def fail_step(self,exception,pretty_index=None):
		#if index - get current index from formatter
		scenario = self.context.scenario
		if pretty_index == 'previous':
			step_index = self.formatters[0]._step_index-1 if self.formatters[0]._step_index>0 else 0
		elif pretty_index == 'current':
			step_index = self.formatters[0]._step_index if self.formatters[0]._step_index>0 else 0
		elif pretty_index == 'next':
			step_index = self.formatters[0]._step_index+1 if self.formatters[0]._step_index<len(scenario.all_steps) else self.formatters[0]._step_index
		elif pretty_index == 'last':
			step_index = len(scenario.all_steps)-1
		elif pretty_index == 'first':
			step_index = 0
		else:
			return
		i = 0
		for step in scenario.all_steps:
			if i >= step_index:
				step.status = 'failed'
				step.error_message = traceback.format_exc(exception)
				[ formatter.update_step_result(step_index, step) for formatter in self.formatters ]
				break
			i=i+1
		return self

	def run(self,streams):
		failed = False
		self.reload_formatters(streams)
		self.run_hook('before_all', self.context) #catch it
		run_feature = True
		failed_count = 0
		for feature in self.features:
			feature = self.make_feature_deep_copy(feature)
			if run_feature:
				failed_scenarios_count = 0
				scenario_error = ''
				self.feature = feature
				for formatter in self.formatters:
					formatter.uri(feature.filename)
				self.context._push()
				self.context.feature = feature
				for formatter in self.formatters:
					formatter.feature(feature)
				self.context.tags = set(feature.tags)
				hooks_called = False
				if not self.config.dry_run and run_feature:
					hooks_called = True
					for tag in feature.tags:
						self.run_hook('before_tag', self.context, tag)
					self.run_hook('before_feature', self.context, feature)
					run_feature = feature.should_run()
				if feature.background and (run_feature or self.config.show_skipped):
					for formatter in self.formatters:
						formatter.background(feature.background)
				failed_scenarios_count = 0
				for scenario in feature.walk_scenarios():
					# scenario.steps = copy.deepcopy(scenario.steps)
					# for step in scenario.all_steps:
					# 	print self._worker,scenario,id(scenario),step.name,id(step)
					#continue
					try:
						if scenario._row:
							self.context._set_root_attribute('active_outline', scenario._row)
						scenario.browser_config = self.context.browser_config
						self.context.scenario = scenario
						#open browser
						if is_ui_scenario(scenario):
							self.context.start_browser()
						scenario.run(self)
						#close browser
						self.context.stop_browser()
						#self.context._set_root_attribute('active_outline', None)
					except BeforeScenarioError as e:
						#print scenario to formatter
						[ formatter.scenario(scenario) for formatter in self.formatters ]
						[ formatter.step(step) for step in scenario.all_steps for formatter in self.formatters ]
						self.fail_step(e,'first')
					except BeforeStepError as e:
						self.fail_step(e,'current')
					except AfterStepError as e:
						#update previous step result
						self.fail_step(e,'previous')
					except AfterScenarioError as e:
						#update last step result
						self.fail_step(e,'last')
					self.context._set_root_attribute('active_outline', None)
					final_status = scenario.compute_status()
					self._worker._FINISHED_QUEUE.put(scenario.name)
					if 'passed' in final_status:
						self._worker._PASSED_QUEUE.put(scenario.name)
					elif 'skipped' in final_status :
						self._worker._SKIPPED_QUEUE.put(scenario.name)
					else:
						failed_scenarios_count = failed_scenarios_count+1
						self._worker._FAILED_QUEUE.put(scenario.name)
				if failed_scenarios_count:
					for formatter in self.formatters:
						formatter.update_status_data('failed')
					#feature.status = 'failed'
				if hooks_called:
					try:
						self.run_hook('after_feature', self.context, feature)
						for tag in feature.tags:
							self.run_hook('after_tag', self.context, tag)
					except Exception as e:
						self._worker.log('Runner catch exception after feature: %s'%str(e))

				self.context._pop()
				if run_feature or self.config.show_skipped:
					for formatter in self.formatters:
						formatter.eof()
				#
				if self.config.stop or self.aborted or self._worker._stopped:
					run_feature = False
		for formatter in self.formatters:
			formatter.close()
		self.run_hook('after_all', self.context)
		return

	def prepare_launch(self):
		self.config.outputs = []
		self.context = CustomBehaveContext(self)
		self.setup_paths()
		self.hooks = {}
		#replace exception
		try:
			self.load_hooks()
			self.load_step_definitions()
		except Exception,e:
			raise PedantError( traceback.format_exc(e) )
		return self

	def run_with_paths(self):
		return self.run_model()

class UndefinedSteps(Queue.Queue):
	def __contains__(self, item):
		with self.mutex:
			return item in self.queue

class Application(PedantApplication):

	def __init__(self, project, verbose=False, logging=True, behave_args=[], dry_run=False):
		#workers list
		self.steps_queue = UndefinedSteps()
		behave_needle_args = [
			'--no-capture',
			'--no-summary'
		]
		#names = ['CustomJsonFormatter','plain']
		#CustomJsonFormatter(StreamOpener(outfile), self.config)
		if dry_run:
			behave_needle_args.append('--dry-run')
		PedantApplication.__init__(self,project,verbose,logging)
		#super(Application,self).__init__(self,project,verbose,logging)
		self.reports_dir = os.path.join(project.get_sources_dir(), 'pedant_data', 'bdd', 'reports')
		self.approved_dir = os.path.join(project.get_sources_dir(), 'pedant_data', 'bdd', 'approved')
		features_dir = os.path.join(project.get_sources_dir(),'bdd')
		if not behave_args:
			behave_args = [features_dir]
		behave_args.extend(behave_needle_args)

		#available langs
		self.behave_config = Configuration(behave_args)


	def get_bdd_info(self):
		result = { 'step_definitions': OrderedDict([('given',[]),('when',[]),('then',[])]), 'languages': languages }
		try:
			runner = CustomBehaveRunner(self.behave_config).prepare_launch()
			features = runner.get_features()
		except InvalidFilenameError:
			return result
		all_mathchers = step_registry.registry.steps
		for key in all_mathchers.keys():
			if not result['step_definitions'].has_key(key):
				result['step_definitions'][key] = []
			for matcher in all_mathchers[key]:
				result['step_definitions'][key].append({
					'text': matcher.string,
					'source_code': inspect.getsourcelines(matcher.func),
					'location': '%s'%inspect.getsourcefile(matcher.func),
					})
		return result

	def get_features(self, filter_d={}):
		try:
			features = CustomBehaveRunner(self.behave_config).load_features().filter_features(filter_d).get_features()
		except InvalidFilenameError:
			features = []
		except Exception as e:
			raise e
		return features

	def get_worker(self,browsers,runner):
		return Worker(browsers,runner,self.report_dir,self.statistic,self.steps_queue)

	def build(self, filter_d):
		self.timestamp = time.time()
		self.report_dir = os.path.join(self.reports_dir, str(self.timestamp))
		self.threads_limit = self.project.get_threads_count()
		if self.logging:
			self.log_file = os.path.join(self.report_dir, 'log.txt')
			os.makedirs(os.path.dirname(self.log_file)) if not os.path.isdir(os.path.dirname(self.log_file)) else None
		#filter features
		runner = CustomBehaveRunner(self.behave_config).load_features(filter_d)
		runner.set_project(self.project)
		runner.prepare_launch()
		all_features = runner.get_features()
		#feature grouping
		grouped_features = {
			'parallel': [feature.filename for feature in all_features if is_parallel_feature(feature) and not is_ui_feature(feature)],
			'parallel_scenarios': [feature.filename for feature in all_features if is_parallel_scenarios_feature(feature) and not is_ui_feature(feature)],
			'no_parallel': [feature.filename for feature in all_features if not is_parallel_feature(feature) and not is_parallel_scenarios_feature(feature) and not is_ui_feature(feature)],
			'ui_parallel': [feature.filename for feature in all_features if is_parallel_feature(feature) and is_ui_feature(feature)],
			'ui_parallel_scenarios': [feature.filename for feature in all_features if is_parallel_scenarios_feature(feature) and is_ui_feature(feature)],
			'ui_no_parallel': [feature.filename for feature in all_features if not is_parallel_feature(feature) and not is_parallel_scenarios_feature(feature) and is_ui_feature(feature)],
		}
		browsers = self.project.get_browsers()
		#parallel features
		if grouped_features['ui_parallel']:
			for browser in browsers:
				ui_parallel_runner = copy.copy(runner)
				ui_parallel_runner.filter_features({'features':grouped_features['ui_parallel']})
				features_runners = ui_parallel_runner.chunk_self(features_count=1)
				for feature_runner in features_runners:
					self.expectation_workers_list.append(self.get_worker([browser], feature_runner))
		#parallel scenarios
		if grouped_features['ui_parallel_scenarios']:
			for browser in browsers: 
				ui_parallel_s_runner = copy.copy(runner)
				ui_parallel_s_runner.filter_features({'features':grouped_features['ui_parallel_scenarios']})
				scenarios_runners = ui_parallel_s_runner.chunk_self(scenarios_count=1)
				for ps_runner in scenarios_runners:
					self.expectation_workers_list.append(self.get_worker([browser], ps_runner))
		#no parallel workers
		if grouped_features['ui_no_parallel']:
			ui_no_parallel_runner = copy.copy(runner)
			ui_no_parallel_runner.filter_features({'features':grouped_features['ui_no_parallel']})
			self.expectation_workers_list.append(self.get_worker(browsers, ui_no_parallel_runner))
		#parallel features
		if grouped_features['parallel']:
			parallel_runner = copy.copy(runner)
			parallel_runner.filter_features({'features':grouped_features['parallel']})
			features_runners = parallel_runner.chunk_self(features_count=1)
			for feature_runner in features_runners:
				self.expectation_workers_list.append(self.get_worker([False], feature_runner))
		#parallel scenarios
		if grouped_features['parallel_scenarios']: 
			parallel_s_runner = copy.copy(runner)
			parallel_s_runner.filter_features({'features':grouped_features['parallel_scenarios']})
			scenarios_runners = parallel_s_runner.chunk_self(scenarios_count=1)
			for s_runner in scenarios_runners:
				self.expectation_workers_list.append(self.get_worker([False], s_runner))
		#no parallel workers
		if grouped_features['no_parallel']:
			no_parallel_runner = copy.copy(runner)
			no_parallel_runner.filter_features({'features':grouped_features['no_parallel']})
			self.expectation_workers_list.append(self.get_worker([False], no_parallel_runner))
		#put all scenarios from all workers to statistic
		total_items = []
		[ total_items.extend(w.get_full_scenarios_list()) for w in self.expectation_workers_list]
		[self.statistic['TOTAL'].put(scenario) for scenario in total_items ]
		return self

	def stop(self):
		PedantApplication.stop(self)
		und_steps = list(self.steps_queue.queue)
		if und_steps:
			self.log( "Found undefined steps: \n%s"%"\n".join(und_steps) )
		return self

	def dry_run(self):
		#create runner with dry run
		#capture stdout
		#return stdout
		pass

	def approve_image(self,timestamp,browser_id,filename):
		if not self.project.access():
			raise PedantError("Have not access to project %s, can not approve image" % self.project.get_root_dir())
		json_filename = os.path.splitext(os.path.basename(filename))[0]
		pathes = {
			'actual_image': os.path.join(self.reports_dir, timestamp, browser_id, filename),
			'approved_image': os.path.join(self.approved_dir, browser_id, filename),
			'approved_image_bckp': os.path.join(self.approved_dir, browser_id, filename+'.bckp'),
			'approved_json': os.path.join(self.approved_dir, browser_id, json_filename),
			'approved_json_bckp': os.path.join(self.approved_dir, browser_id, json_filename+'.bckp')
		}
		if not os.path.isfile(pathes['actual_image']):
			raise PedantError('Actual image %s not found'%pathes['actual_image'])
		approved_info = { 'report': timestamp, 'time': time.time() }
		#backup approved image if exists
		os.remove( pathes['approved_image_bckp'] ) if os.path.isfile( pathes['approved_image_bckp'] ) else None
		os.rename( pathes['approved_image'], pathes['approved_image_bckp'] ) if os.path.isfile( pathes['approved_image'] ) else None
		#backup approved_json_path
		os.remove( pathes['approved_json_bckp'] ) if os.path.isfile( pathes['approved_json_bckp'] ) else None
		os.rename( pathes['approved_json'], pathes['approved_json_bckp'] ) if os.path.isfile( pathes['approved_json'] ) else None
		#copy actual to approved
		if not os.path.isdir(os.path.dirname(pathes['approved_image'])):
			os.makedirs(os.path.dirname(pathes['approved_image']))
		shutil.copyfile(pathes['actual_image'], pathes['approved_image'])
		#put json
		put_json_to_file(pathes['approved_json'], approved_info)

	def cancel_approve_image(self,timestamp,browser_id,filename):
		if not self.project.access():
			raise PedantError("Have not access to project %s, can not cancel approve image" % self.project.get_root_dir())
		json_filename = os.path.splitext(os.path.basename(filename))[0]
		pathes = {
			'actual_image': os.path.join(self.reports_dir, timestamp, browser_id, filename),
			'approved_image': os.path.join(self.approved_dir, browser_id, filename),
			'approved_image_bckp': os.path.join(self.approved_dir, browser_id, filename+'.bckp'),
			'approoved_json': os.path.join(self.approved_dir, browser_id, json_filename),
			'approoved_json_bckp': os.path.join(self.approved_dir, browser_id, json_filename+'.bckp')
		}
		if not os.path.isfile(pathes['actual_image']):
			raise PedantError('Actual image %s not found'%pathes['actual_image'])
		approved_info = { 'report': timestamp, 'time': time.time() }
		#backup approved image if exists
		os.remove( pathes['approved_image'] ) if os.path.isfile( pathes['approved_image'] ) else None
		os.rename( pathes['approved_image_bckp'], pathes['approved_image'] ) if os.path.isfile( pathes['approved_image_bckp'] ) else None
		#backup approved_json_path
		os.remove( pathes['approoved_json'] ) if os.path.isfile( pathes['approoved_json'] ) else None
		os.rename( pathes['approoved_json_bckp'], pathes['approoved_json'] ) if os.path.isfile( pathes['approoved_json_bckp'] ) else None

	def get_approved_images(self):
		data = list()
		for img_path in glob.glob( os.path.join( self.approved_dir, '*', '*.png' ) ):
			info_path = img_path.replace('.png','.json')
			if not os.path.isfile(info_path):
				continue
			info = get_json_from_file(info_path)
			filename = os.path.basename(img_path) 
			screen_web_skeleton = '/projects/%s/static/bdd/approved/'%self.project.get_name()+'%s/%s',
			info['images'] = {
				'approved': screen_web_skeleton%(info['browser_id'],filename)
			}
			data.append(info)
		return data

	def get_report(self, timestamp):
		data = list() 
		skeletons = {
			'actual': '/projects/%s/static/pedant_data/bdd/reports/%s/'%(self.project.get_name(),timestamp)+'%s/%s',
			'approved': '/projects/%s/static/pedant_data/bdd/approved/'%self.project.get_name()+'%s/%s',
			'diff': '/projects/%s/static/pedant_data/bdd/reports/%s/'%(self.project.get_name(),timestamp)+'%s/%s'
		}
		rand = random.random()
		for json_file in glob.glob(os.path.join(self.reports_dir, timestamp, '*', '*.json')):
			json_report = get_json_from_file(json_file)
			#set images
			data.extend(json_report)
		joined_features = {}
		for feature in data:
			#set web pathes for screenshots
			for scenario in feature['elements']:
				for step in scenario['steps']:
					if step.has_key('screenshots'):
						for key in step['screenshots'].keys():
							for i,filename in enumerate(step['screenshots'][key]):
								step['screenshots'][key][i] = {
									'src': skeletons[key]%(scenario['browser_config']['id'],filename+'?%s'%rand),
									'filename': filename
								}
			#join features
			if joined_features.has_key(feature['location']):
				#fix status
				if feature['status'] != joined_features[feature['location']] and feature['status'] != 'passed':
					joined_features[feature['location']]['status'] = 'failed'
				joined_features[feature['location']]['elements'].extend(feature['elements'])
			else:
				joined_features[feature['location']] = feature

		#fix backgrounds
		for feature in joined_features.values():
			backs = []
			scenarios = []
			#delete same backgrounds
			for scenario in feature['elements']:
				if scenario['type'] == 'background':
					if len(backs) < 1:
						backs.append(scenario)
				else:
					scenarios.append(scenario)
			feature['elements'] = scenarios
			if len(backs):
				feature['elements'].insert(0,backs[0])
		return joined_features.values()


class Worker(PedantWorker):

	def __init__(self, browsers, runner, report_dir, stat_queues, und_steps_queue):
		PedantWorker.__init__(self, report_dir)
		self.set_queues(finished=stat_queues['FINISHED'],skipped=stat_queues['SKIPPED'],passed=stat_queues['PASSED'],failed=stat_queues['FAILED'])
		self.und_steps_queue = und_steps_queue
		self.browsers = browsers
		self.runner = runner

	def hooks(self):
		def should_stop(context,step):
			if self._stopped:
				message = 'Stopped by user before step (%s)'%step.name
				self.log(message,'ERROR')
				raise BeforeStepError(message,step)

		def screenshots_processing(context,step):
			scenario = context.scenario
			if is_screens_taking_scenario(scenario) or is_screens_comparison_scenario(scenario):
				filename = "%s.png"%random.random()
				#filename - hash from step.location.filename, step.location.line, example_row
				#filename = ''
				row_s = str(context.active_outline.as_dict()) if context.active_outline else ''
				bro_s = context.browser_config['id'] if context.browser_config else ''
				step_s = step.name + step.location.filename + str(step.location.line)
				identifier = hashlib.md5(step_s + row_s + bro_s).hexdigest()
				actual_screenshot_filename = identifier+'.png'
				approved_screenshot_filename = identifier+'.png'
				diff_screenshot_filename = identifier+'.diff.png'
				actual_path = os.path.join(self.screenshots_dir,actual_screenshot_filename)
				approved_path = os.path.join(self.approved_dir,approved_screenshot_filename)
				diff_path = os.path.join(self.screenshots_dir,diff_screenshot_filename)
				try:
					bro = context.get_browser()
					bro.save_screenshot(actual_path)
					for formatter in context._runner.formatters:
						formatter.add_current_step_screenshot('actual',actual_screenshot_filename)
				except Exception as e:
					error = str(e)
					self.log('Can not save screenshot to file %s. Cause: %s'%(actual_screenshot_filename,error), 'ERROR')
					raise AfterStepError(error,step)
				if is_screens_comparison_scenario(scenario):
					#comparison of screenshot
					if os.path.isfile(approved_path):
						for formatter in context._runner.formatters:
							formatter.add_current_step_screenshot('approved',approved_screenshot_filename)
						#try find differents in images
						txt_result, status = compare_images(approved_path,actual_path,diff_path)
						if status == PedantWorker._FAILED:
							#diff saved
							for formatter in context._runner.formatters:
								formatter.add_current_step_screenshot('diff',diff_screenshot_filename)
							raise AfterStepError('Comparison failed',step)
					else:
						raise AfterStepError('Approved image not found',step)

		return dict([
			('before_step',[should_stop]),
			('after_step',[screenshots_processing]),
			])

	def get_full_scenarios_list(self):
		features = self.runner.get_features()
		res = []
		for browser in self.browsers:
			browser = browser if browser else {'id':'none'}
			[[res.append( '%s --- %s '%(scenario.name,browser['id']) ) for scenario in feature.walk_scenarios()] for feature in features]
		return res

	"""
	run thread
	@return void
	"""
	def run(self):
		#each browsers
		
		for browser in self.browsers:
			#pathes
			bro_dirname = browser['id'] if browser else 'none'
			json_path = os.path.join(self.report_dir,bro_dirname,str(random.random())+'.json')
			screenshots_dir = os.path.join(self.report_dir,bro_dirname)
			approved_dir = os.path.join(os.path.dirname(os.path.dirname(self.report_dir)), 'approved', bro_dirname)
			runner = copy.copy(self.runner)
			#reload
			runner.prepare_launch()
			# set worker to context
			runner.set_worker(self)
			runner.context.set_browser_config(browser)
			self.screenshots_dir = screenshots_dir
			self.approved_dir = approved_dir
			#set screenshot dirs to steps
			features = runner.get_features()
			if not features:
				self.log('Runner is empty. Nothing to run.', level='ERROR')
				return
			#set screenshots dir for capture_screens() hook
			#[[ self.set_screenshot_dir_to_steps(screenshots_dir,scenario) for scenario in feature.scenarios ] for feature in features ]
			# add hooks
			runner.add_hooks(self.hooks())
			#try make dir for json
			try:
				os.makedirs(os.path.dirname(json_path))
				os.makedirs(approved_dir)
			except:
				pass
			plain_stream = StringIO.StringIO()
			#outputs
			streams = [StreamOpener(json_path),StreamOpener(stream=plain_stream)]
			runner.run(streams)
			if browser:
				name = 'configured with browser %s'%browser['id']
			else:
				name = ''
			plain_stream.seek(0)
			output = '\nRunner %s finished and say: \n %s'%(name, plain_stream.read())
			self.log(output)
			#collect undefined steps
			if self.runner.undefined_steps:
				for step in self.runner.undefined_steps:
					snippet = make_undefined_step_snippet(step)
					if snippet not in self.und_steps_queue:
						self.und_steps_queue.put(snippet)
		_stopped = True
		return