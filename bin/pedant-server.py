#!/usr/bin/python
import __init__,os,sys,glob,shutil,zipfile,uuid,json
from bottle import bottle

templates_dir = os.path.realpath( __file__ + os.sep + '..' + os.sep + '..' + os.sep + 'lib'+ os.sep +'templates' )
#static_root = os.path.realpath( __file__ + os.sep + '..' + os.sep + '..' + os.sep + 'web'+ os.sep +'assets' )

config = {}

execfile( os.path.realpath( __file__ + os.sep + '..' + os.sep + "pedant.conf" ), config)

bottle.TEMPLATE_PATH.insert(0, templates_dir)


def template( template , **kwargs ):
	return bottle.template( ''.join(open(templates_dir + os.sep + template, 'r').readlines()), kwargs )

def json_success( message ):
	return { 'status':'OK', 'msg':message }

def json_error( message ):
	return { 'status':'WARN', 'msg':message }

def get_report_data( project, timestamp ):
	prj_root = config['data_storage_root'] + os.sep + project
	approved_root = prj_root + os.sep + 'approved'
	report_root = prj_root + os.sep + 'reports' + os.sep + timestamp
	data = list()
	for json_path in glob.glob( report_root + os.sep + '*' + os.sep + '*' + os.sep + 'report.json' ):
		json_content=open(json_path)
		json_data = json.load(json_content)
		json_content.close()
		json_data['images'] = { 'approved': False, 'actual': False, 'approved_report': False, 'diff': False}
		approved_path = approved_root + os.sep + json_data['item']['unid'] + os.sep + json_data['browser']['unid'] + os.sep + 'approved.png'
		report_dir = report_root + os.sep + json_data['item']['unid'] + os.sep + json_data['browser']['unid'] + os.sep
		#check images exists
		if os.path.isfile( approved_path ):
			json_data['images']['approved'] = '/' + project + '/static/approved/' + json_data['item']['unid'] + '/' + json_data['browser']['unid'] + os.sep + 'approved.png'
		if os.path.isfile( report_dir + 'approved_report.png' ):
			json_data['images']['approved_report'] = '/' + project + '/static/reports/' + timestamp + '/' + json_data['item']['unid'] + '/' + json_data['browser']['unid'] + os.sep + 'approved_report.png'
		if os.path.isfile( report_dir + 'actual.png' ):
			json_data['images']['actual'] = '/' + project + '/static/reports/' + timestamp + '/' +  json_data['item']['unid']  + '/' + json_data['browser']['unid'] + os.sep + 'actual.png'
		if os.path.isfile( report_dir + 'diff.png' ):
			json_data['images']['diff'] = '/' + project + '/static/reports/' + timestamp + '/' + json_data['item']['unid'] + '/' + json_data['browser']['unid'] + os.sep + 'diff.png'		
		data.append( json_data )
	return data

def get_approved_images( project ):
	approved_root = config['data_storage_root'] + os.sep + project + os.sep + 'approved' 
	web_path_root = "/" + project + '/static/approved/'
	data = list()
	print  approved_root + os.sep + '*' + os.sep + '*' + os.sep + 'approved.png'
	for img in glob.glob( approved_root + os.sep + '*' + os.sep + '*' + os.sep + 'approved.png' ):
		
		itemname = os.path.basename( os.path.dirname( os.path.dirname( img ) ) )
		browser = os.path.basename( os.path.dirname( img ) )
		data.append( { 'name':itemname,'browser':browser,'image':web_path_root + '/' + itemname + '/' + browser + '/approved.png' } )
	return data

#pedant static
@bottle.route('/assets/<path:path>')
def callback(path):
    return bottle.static_file(path,templates_dir + os.sep + 'assets')

#pedant report images
@bottle.route('/<project>/static/<path:path>')
def callback(project,path):
    return bottle.static_file(path,config['data_storage_root']+os.sep+project)

#coming soon page
@bottle.route('/coming_soon')
def index():
	return template( template='coming_soon.tpl' )

#main page
@bottle.route('/')
def index():
	prj_list = map(lambda x: os.path.basename( os.path.dirname(x) ), glob.glob( config['data_storage_root'] + os.sep + '*' + os.sep ) )
	return template( template='index.tpl', prj_list=prj_list )

#project main page. static
@bottle.route('/<project>')
def index(project):
	bottle.redirect("/coming_soon")
	#return template( template='prj_index.tpl', project=project)

#project reports list. reports
@bottle.route('/<project>/reports')
def index(project):
	rep_list = map(lambda x: os.path.basename( os.path.dirname(x) ), glob.glob( config['data_storage_root'] + os.sep + project + os.sep + 'reports' + os.sep + '*' + os.sep ) )
	rep_list.sort( reverse=True )
	return template( template='prj_reports.tpl', project=project, reports_list=rep_list)

#project last report
@bottle.route('/<project>/reports/last')
def index(project):
	rep_list = map(lambda x: os.path.basename( os.path.dirname(x) ), glob.glob( config['data_storage_root'] + os.sep + project + os.sep + 'reports' + os.sep + '*' + os.sep ) )
	rep_list.sort( reverse=True )
	if len( rep_list ) < 1:
		bottle.redirect( "/" + project + "/reports")
	timestamp = rep_list[0]
	data = get_report_data( project , timestamp )
	return template( template='prj_report.tpl', project=project, timestamp=timestamp , report_list=data )

#project report detail
@bottle.route('/<project>/reports/<timestamp>')
def index(project,timestamp):
	return template( template='prj_report.tpl', project=project, timestamp=timestamp, report_list=get_report_data( project , timestamp ) )

#project approved images
@bottle.route('/<project>/approved')
def index(project):
	return template( template='prj_approved.tpl', project=project, approved_list=get_approved_images( project ) )

#project item timeline
@bottle.route('/<project>/timeline/<item>')
def index(project,item):
	return bottle.redirect("/coming_soon")
	
#approve actual image in project file
@bottle.route('/<project>/ajax/approve/<timestamp>/<item>/<browser>')
def index(project,timestamp,item,browser):
	#find actual image for file
	item_dir = item + os.sep + browser + os.sep
	item_web_path = item + '/' + browser + '/'
	report_dir = config['data_storage_root'] + os.sep + project + os.sep + 'reports' + os.sep + timestamp + os.sep + item_dir
	approved_path = config['data_storage_root'] + os.sep + project + os.sep + 'approved' + os.sep + item_dir + os.sep + 'approved.png'
	#if approved_report exists - move it ot {original_path}.bckp
	if os.path.isfile( report_dir + 'approved_report.png'):
		os.rename( report_dir + 'approved_report.png' , report_dir + 'approved_report.bckp' )
	#backup diff
	if os.path.isfile( report_dir + 'diff.png'):
		os.rename( report_dir + 'diff.png' , report_dir + 'diff.bckp' )
	#backup global approved
	if os.path.isfile( approved_path):
		os.rename( approved_path, approved_path + '.bckp' )
	#backup json
	if os.path.isfile( report_dir + 'report.bckp' ):
		report_dir + 'report.bckp'
	os.rename( report_dir + 'report.json', report_dir + 'report.bckp' )
	#get original json data
	json_file=open(report_dir + 'report.bckp')
	json_data = json.load(json_file)
	json_file.close()

	#create approved folder if it's need
	if not os.path.isdir( os.path.dirname(approved_path) ):
		os.makedirs(os.path.dirname(approved_path))
	#copy actual to approved and report
	shutil.copyfile( report_dir + 'actual.png', approved_path )
	shutil.copyfile( report_dir + 'actual.png', report_dir + 'approved_report.png' )
	#update json, save it to file
	json_data['msg'] = "success"
	obj = open( report_dir + 'report.json' , 'wb')
	json.dump( json_data, obj )
	obj.close
	#additional info
	json_data['status'] = "OK"
	json_data['images'] = {
		'approved': template( 
						template='prj_report_image.tpl', 
						img = '/' + project + '/static/approved/' + item_web_path + 'approved.png',
						alt = 'Approved',
						status = json_data['msg'] ),
		'approved_report': template( 
						template='prj_report_image.tpl', 
						img = '/' + project + '/static/reports/' + timestamp + '/' + item_web_path + 'approved_report.png',
						alt = 'Approved in report',
						status = json_data['msg'] ),
		'diff': template( 
						template='prj_report_image.tpl', 
						img = False,
						alt = 'Diff',
						status = json_data['msg'] )
	}
	#return data
	return json_data

#disapprove actual image in project file
@bottle.route('/<project>/ajax/cancel-approve/<timestamp>/<item>/<browser>')
def index(project,timestamp,item,browser):
	item_dir = item + os.sep + browser + os.sep
	item_web_path = item + '/' + browser + '/'
	report_dir = config['data_storage_root'] + os.sep + project + os.sep + 'reports' + os.sep + timestamp + os.sep + item_dir
	approved_path = config['data_storage_root'] + os.sep + project + os.sep + 'approved' + os.sep + item_dir + os.sep + 'approved.png'
	#web imgs
	approved_img_web = False
	approved_report_img_web = False
	diff_img_web = False
	
	#restore backup approved
	if os.path.isfile( approved_path ):
		os.remove(approved_path)
	if os.path.isfile( approved_path + '.bckp' ):
		os.rename( approved_path + '.bckp', approved_path )
		approved_img_web = '/' + project + '/static/approved/' + item_web_path + 'approved.png'
	
	#restore backup approved_report
	if os.path.isfile( report_dir + 'approved_report.png' ):
		os.remove(report_dir + 'approved_report.png')
	if os.path.isfile( report_dir + 'approved_report.bckp' ):
		os.rename( report_dir + 'approved_report.bckp' , report_dir + 'approved_report.png' )
		approved_report_img_web = '/' + project + '/static/reports/' + timestamp + '/' + item_web_path + 'approved_report.png'
	
	#restore backup diff
	if os.path.isfile( report_dir + 'diff.bckp' ):
		os.rename( report_dir + 'diff.bckp' , report_dir + 'diff.png' )
		diff_img_web = '/' + project + '/static/reports/' + timestamp + '/' + item_web_path + 'diff.png'

	#restore report.json
	if os.path.isfile( report_dir + 'report.json' ):
		os.remove( report_dir + 'report.json' )
	os.rename( report_dir + 'report.bckp' , report_dir + 'report.json' )
	#read report
	json_file=open(report_dir + 'report.json')
	json_data = json.load(json_file)
	json_file.close()
	json_data['images'] = {
		'approved': template( 
						template='prj_report_image.tpl', 
						img = approved_img_web,
						alt = 'Approved',
						status = json_data['msg'] ),
		'approved_report': template( 
						template='prj_report_image.tpl', 
						img = approved_report_img_web,
						alt = 'Approved in report',
						status = json_data['msg'] ),
		'diff': template( 
						template='prj_report_image.tpl', 
						img = diff_img_web,
						alt = 'Diff',
						status = json_data['msg'] )
	}
	json_data['status'] = "OK"
	return json_data

#remove report
@bottle.route('/<project>/ajax/delete/report/<timestamp>')
def index(project,timestamp):
	#remove report
	path = config['data_storage_root'] + os.sep + project + os.sep + 'reports' + os.sep + timestamp + os.sep
	if os.path.isdir( path ):
		shutil.rmtree( path )
		return {'status':'OK','message':'removed'}
	else:
		return {'status':'ERROR', 'message':'report not exists'}
	#return "I'm remove report <" +timestamp+ ">"


#export approved images in zip archieve
@bottle.route('/<project>/ajax/export/approved/zip')
def index(project):
	zipfilename = project + '.zip'
	zipfilepath = config['tmp_root'] + os.sep + zipfilename
	what_need_zip = config['data_storage_root'] + os.sep + project + os.sep + 'approved'
	root = os.path.realpath( what_need_zip )
	#create zip archieve in tmp file
	if os.path.isdir( root ):
		files = glob.glob( what_need_zip + os.sep + '*' + os.sep + '*' + os.sep + 'approved.png' )
		if len(files) < 1:
			files = glob.glob( what_need_zip + os.sep + '*' + os.sep + '*' + os.sep )
		zf = zipfile.ZipFile( zipfilepath, "w",zipfile.ZIP_DEFLATED)
		for filepath in files:
			zf.write( filepath , os.sep + os.path.relpath(filepath, root) )
		zf.close()
	    #if file created
		if os.path.isfile( zipfilepath ):
			retfile = bottle.static_file(zipfilename, root=config['tmp_root'], download= project + '_approved.zip')
			#remove tmp file
			os.remove( zipfilepath )
			return retfile
	return json_error( "Sorry. I can not generate approved archieve ")

#import approved images
#todo catch errors
@bottle.route('/<project>/ajax/import/approved/zip')
def index(project):
	filename = config['tmp_root'] + os.sep + 'production_small_approved.zip'
	prj_root = config['data_storage_root'] + os.sep + project + os.sep + 'approved'
	if project == os.path.basename( filename ).replace( '_approved.zip' ,  ''):
		with zipfile.ZipFile(filename, "r") as z:
			z.extractall( prj_root )
	return json_error( "Sorry zip file are broken. Do you have another file?")

bottle.run(host=config['web_host'], port=config['web_port'])