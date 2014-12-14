% include('header.tpl', title='Launch ' + config['prj_name'] )
<div class="container">

% include('breadcrumbs.tpl', crumbs = [ ( '/','Home'), ('/projects','Projects'), ('/projects/'+config['prj_name'],config['prj_name']),('','Launch') ])

<h3>Launch {{config['prj_name']}}</h3>

<script type="text/javascript">

	var config = {{ !config_str }}

	var custom_config = {{ !config_str }}

	var update_interval_id = false

	var default_browsers = {
		"ANDROID" : { unid:"ANDROID_800x600", type:"ANDROID", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome android browser", desired_capabilities: {'platform': 'ANDROID', 'browserName': 'android', 'version': '', 'javascriptEnabled': true} },
		"CHROME" : { unid:"CHROME_800x600", type:"CHROME", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome chrome browser", desired_capabilities: {'platform': 'ANY', 'browserName': 'chrome', 'version': '', 'javascriptEnabled': true} },
		"FIREFOX" : { unid:"FIREFOX_800x600", type:"FIREFOX", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome firefox browser", desired_capabilities: {'platform': 'ANY', 'browserName': 'firefox', 'version': '', 'javascriptEnabled': true} },
		"INTERNETEXPLORER" : { unid:"INTERNETEXPLORER_800x600", type:"INTERNETEXPLORER", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "IE", desired_capabilities: {'platform': 'WINDOWS', 'browserName': 'internet explorer', 'version': '', 'javascriptEnabled': true} },
		"IPAD" : { unid:"IPAD_800x600", type:"IPAD", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome ipad browser", desired_capabilities: {'platform': 'MAC', 'browserName': 'iPad', 'version': '', 'javascriptEnabled': true} },
		"IPHONE" : { unid:"IPHONE_800x600", type:"IPHONE", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome iphone browser", desired_capabilities: {'platform': 'MAC', 'browserName': 'iPhone', 'version': '', 'javascriptEnabled': true} },
		"OPERA" : { unid:"OPERA_800x600", type:"OPERA", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome opera browser", desired_capabilities: {'platform': 'ANY', 'browserName': 'opera', 'version': '', 'javascriptEnabled': true} },
		"PHANTOMJS" : { unid:"PHANTOMJS_800x600", type:"PHANTOMJS", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome phantom browser", desired_capabilities: {'platform': 'ANY', 'browserName': 'phantomjs', 'version': '', 'javascriptEnabled': true, "phantomjs.page.settings.resourceTimeout": "3000" } },
		"SAFARI" : { unid:"SAFARI_800x600", type:"SAFARI", window_size:[800,600], wd_url: "http://127.0.0.1:4444/wd/hub", info: "My awesome safari browser", desired_capabilities: {'platform': 'ANY', 'browserName': 'safari', 'version': '', 'javascriptEnabled': true} }
	}

</script>

<!-- Template for browsers  -->
<script type="text/template" id="launch-custom-tab-tpl" charset="UTF-8">

	<div class="form-group">
		<label for="prj_threads">Maximum pedant-screens threads</label>
		<input type="number" class="form-control" id="prj_threads" min="1" max="20" placeholder="Enter maximum workers count" value="{{ !'<%= config.max_workers %>'}}">
	</div>

	<div class="form-group">
		<label for="prj_urls">Urls</label>
		{{!"<% if ( config.urls === undefined ) config.urls = [] %>"}}
		<textarea class="form-control" id="prj_urls" rows="5">{{ !'<%= config.urls.join("\\r\\n") %>'}}</textarea>
	</div>

	<div class="form-group browsers-list">
	{{ !'<% $.each(config.modes.full, function( index, browser ) { %>' }}
				<label>
					<input type="checkbox" value="{{ !"<%= browser.unid %>"}}" checked='checked'>{{ !"<%= browser.unid %>" }}
					<a class="edit-browser" data-toggle="modal" data-target="#editBrowserModal" data-mode="edit" data-unid="{{!"<%= browser.unid %>"}}">[[Edit]]</a> 
					<a class="delete-browser" data-toggle="modal" data-target="#deleteBrowserModal" data-mode="delete" data-unid="{{!"<%= browser.unid %>"}}">[[Del]]</a>
				</label>
	{{ !"<% }); %>" }}
	</div>
	<div class="form-group">
		<a class="pedant-icon add-item add-browser" data-toggle="modal" data-target="#editBrowserModal" data-mode="add">Add</a>
	</div>

</script>

% include('prj_edit_modals.tpl')

 <!-- Nav tabs -->
<ul class="nav nav-tabs" role="tablist">
	<li role="presentation" class="stored-mode active"><a href="#launch-by-mode" aria-controls="launch-by-mode" role="tab" data-toggle="tab">Launch by stored mode</a></li>
	<li role="presentation" class="custom-mode"><a href="#launch-custom-config" aria-controls="launch-custom-config" role="tab" data-toggle="tab">Launch custom config</a></li>
</ul>

<!-- Tab panes -->
<div class="tab-content border-row">
	<div role="tabpanel" class="tab-pane active" id="launch-by-mode">
		<div class="form-group">
			<label for="mode-choise">Project modes</label>
			<select class="form-control mode-choise" id="mode-choise">
				% for modename,mode in config["modes"].iteritems():
					<option>{{modename}}</option>
				% end
			</select>
		</div>
	</div>
	<div role="tabpanel" class="tab-pane" id="launch-custom-config">
		
	</div>
</div>

<div class="form-group">
	<button type="button" class="btn btn-default start-project" data-url="/ajax/projects/{{config['prj_name']}}/launch/start">RUN</button>
	<button type="button" class="btn btn-default stop-project" data-url="/ajax/projects/{{config['prj_name']}}/launch/stop">STOP</button>
	<a class="btn btn-default" target="_blank" href="/projects/{{config['prj_name']}}/reports/last">Last project detail report</a>
	<h4>Status: <span class='text-danger current-status'>N\A</span></h4>
</div>

<!-- WORK RESULTS -->
<div class="container-fluid">
    <div class="row"> <!-- Give this div your desired background color -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                	<textarea class="launch-info col-md-12" rows="20"></textarea>
                </div>
        	</div>
    	</div>
	</div>
</div>

</div>

% include('footer.tpl')