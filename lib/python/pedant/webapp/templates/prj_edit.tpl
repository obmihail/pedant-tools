% include('header.tpl', title='Pedant main page', breadcrumbs = crumbs )
<div class="container">

% if action == 'add':
<h3>New project:</h3>
% else:
<h3>Edit project: {{ config['prj_name'] }}</h3>
% end

<div data-alerts="alerts" data-titles="{'warning': '<em>Warning!</em>'}" data-ids="myid" data-fade="5000" ></div>
<script type="text/javascript">


	var config = {{ !config_str }}

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

<script type="text/template" id="browser-row-tpl" charset="UTF-8">
	{{ !'<% $.each(data, function( index, browser ) { %>' }}
	<tr class = "browser-row" data-config="{{ !"<%= escape( JSON.stringify(browser) ) %>" }}">
          <td>{{ !"<%= browser.unid %>" }}</td>
          <td>{{ !"<%= browser.type %>" }}</td>
          <td>{{ !"<%= browser.window_size[0] %>" }}X{{ !"<%= browser.window_size[1] %>" }}</td>
          <td>{{ !"<%= browser.wd_url %>" }}</td>
          <td>{{ !"<%= JSON.stringify(browser.desired_capabilities) %>" }}</td>
          <td>{{ !"<%= browser.info %>" }}</td>
          <td class="col-md-4">
          	<a class="edit-browser" data-toggle="modal" data-target="#editBrowserModal" data-mode="edit">[[E]]</a> 
          	<a class="delete-browser" data-toggle="modal" data-target="#deleteBrowserModal" data-mode="delete">[[D]]</a>
          	<a class="test-browser" data-toggle="modal" data-target="#testBrowserModal" data-mode="test">[[T]]</a>
          </td>
    </tr>
	{{ !'<% }); %>' }}
</script>

<script type="text/template" id="modes-row-tpl" charset="UTF-8">
	{{ !'<% $.each(data, function( name, browsers ) { %>' }}
	<tr data-name= "{{ !"<%= name %>" }}" data-config = "{{ !"<%= escape( JSON.stringify(browsers) ) %>" }}">
          <td>{{ !"<%= name %>" }}</td>
          <td>{{ !"<%= JSON.stringify(browsers) %>" }}</td>
          <td>
          	{{ !"<% if ( name.toLowerCase() !== 'full' ) { %>"}}
          	<a class="edit-mode" data-toggle="modal" data-target="#editLMModal" data-mode="edit">[[E]]</a> 
          	<a class="delete-mode" data-toggle="modal" data-target="#deleteLMModal" data-mode="delete">[[D]]</a>
          	{{ !"<% } %>"}}
          </td>
        </tr>
	{{ !"<% }); %>" }}
</script>

<!-- TODO: refactor it -->
<script type="text/template" id="browsers-for-mode-checkboxes-tpl" charset="UTF-8">
	{{ !'<% $.each(config.modes.full, function( index, browser ) { %>' }}
		<label>
			<input type="checkbox" value="{{ !"<%= browser.unid %>"}}" 
			{{ !"<% if ( data.browsers.indexOf( browser.unid ) > -1 ) { %><%= checked='checked' %><% } %>"}} >{{ !"<%= browser.unid %>" }}</label>
	{{ !"<% }); %>" }}
</script>


% include('prj_edit_modals.tpl')

<form role="form">
  <div class="form-group">
    <label for="prj_name">Project name</label>
    <input type="text" class="form-control prj_name" id="prj_name" placeholder="Enter new project name" value="{{ config['prj_name'] }}">
  </div>
  <div class="form-group">
  	<label for="prj_urls">Urls for scanning (plain text, new line - new url)</label>
  	
    % if config.has_key('urls'):
      <textarea class="form-control" id="prj_urls" rows="7">{{ '\n'.join(config['urls']) }}</textarea>
    % else:
      <textarea class="form-control" id="prj_urls" rows="7"></textarea>
    % end
  </div>
  <div class="form-group">
  	<label for="prj_threads">Maximum pedant-screens threads. If you don't know what is - don't touch</label>
  	<input type="number" class="form-control" id="prj_threads" min="1" max="20" placeholder="Threads" value="3">
  </div>
  <div class="form-group">
  <label for="browsers-table">Browsers</label>
  <a class="pedant-icon add-item add-browser" data-toggle="modal" data-target="#editBrowserModal" data-mode="add">[[+]]</a> 
	<table class="table table-condensed table-hover" id="browsers-table" name="browsers">
      <thead>
        <tr>
          <th>Unique name</th>
          <th>Type</th>
          <th>Window_size</th>
          <th>Webdriver_url</th>
          <th>Capabilites</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <!-- browser row -->
      </tbody>
    </table>
  </div>
  <div class="form-group">
    <label for="modes-table">Launch modes</label>
    <a class="pedant-icon add-item add-launch-mode" data-toggle="modal" data-target="#editLMModal" data-mode="add">[[+]]</a> 
	<table class="table table-condensed" id="modes-table" name="modes">
      <thead>
        <tr>
          <th>Unique name</th>
          <th>Browsers</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
  </div>
  % if action == 'add':
  <a id="dLabel" class="btn btn-default btn-create-prj" href="#" data-url="/ajax/projects/add" role="button">ADD project</a>
  % else:
  <a id="dLabel" class="btn btn-default btn-create-prj" href="#" data-url="/ajax/projects/update" role="button">Update project</a>
  % end
</form>

</div>
% include('footer.tpl')