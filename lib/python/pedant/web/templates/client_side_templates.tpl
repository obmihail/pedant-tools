<!-- EDIT PROJECT TEMPLATES -->
<script type="text/template" id="browser-table-tpl" charset="UTF-8">
	<caption>Browsers</caption>
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
<!----><% $.each(browsers, function( index, browser ) { %>
		<tr class = "browser-row" data-id = "<%= browser.id %>">
			<td><%= browser.id %></td>
			<td><%= browser.type %></td>
			<td><%= browser.window_size[0]%>X<%= browser.window_size[1] %></td>
			<td><%= browser.wd_url %></td>
			<td><%= JSON.stringify(browser.desired_capabilities) %></td>
			<td><%= browser.description %></td>
			<td class="col-md-4">
				<a class="edit-browser" data-toggle="modal" data-target="#edit_browser_modal"><span class="glyphicon glyphicon-pencil"></span></a> 
				<a class="delete-browser" data-toggle="modal" data-target="#delete_browser_modal"><span class="glyphicon glyphicon-remove text-danger"></span></a>
			</td>
		</tr>
<!----><% }); %>
	</tbody>
</script>

<script type="text/template" id="modes-table-tpl" charset="UTF-8">
	<thead>
		<caption>Launch modes</caption>
		<tr>
			<th>Unique name</th>
			<th>Browsers</th>
			<th>States</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
<!----><% $.each(modes, function( name, mode ) { %>
		<tr data-name= "<%= name %>" data-config = "<%= escape( JSON.stringify(mode) ) %>">
			<td><%= name %></td>
			<td><%= JSON.stringify(mode.browsers) %></td>
			<td><%= JSON.stringify(mode.states) %></td>
			<td>
				<a class="edit-mode" data-toggle="modal" data-target="#edit_launch_mode_modal" data-mode="edit" data-id="<%= name %>"><span class="glyphicon glyphicon-pencil"></span></a> 
				<a class="delete-mode" data-toggle="modal" data-target="#delete_launch_mode_modal" data-mode="delete" data-id="<%= name %>"><span class="glyphicon glyphicon-remove text-danger"></span></a>
			</td>
		</tr>
<!---->	<% }); %>
	</tbody>
</script>

<script type="text/template" id="states-table-tpl" charset="UTF-8">
	<thead>
		<caption>States</caption>
		<tr>
			<th>Unique name</th>
			<th>Browsers</th>
			<th>Details</th>
		</tr>
	</thead>
	<tbody>
<!----><% $.each(states, function( i, state ) { %>
		<tr>
			<td><%= state.id %></td>
			<td><%= state.browsers_list.map(function(browser){ return browser.id }) %></td>
			<td>
			<button type="button" class="btn btn-small" data-toggle="modal" data-target="#project-state-modal" data-config = "<%- JSON.stringify(state) %>">Show details</button>
			</td>
		</tr>
<!---->	<% }); %>
	</tbody>
</script>

<!-- TODO: refactor modes: add states and show one modal for mode, state and browsers -->
<script type="text/template" id="browsers-for-mode-checkboxes-tpl" charset="UTF-8">
<!----><% $.each(config.modes['*']['browsers'], function(index, browser) { %>
		<label>
			<input type="checkbox" value="<%= browser %>" <%=(data.browsers.indexOf(browser)>-1) ? 'checked="checked"' : ''%> ><%= browser %>
		</label>
<!---->	<% }); %>
</script>

<script type="text/template" id="browsers-checks-tpl" charset="UTF-8">
<!---->	<% if (typeof without_controls === undefined) { %>
<!---->		<% var without_controls = false %>
<!---->	<% } %>
		<p> <span class="text-block">Browsers: 
<!---->	<% if (!without_controls) { %>
			<span class="glyphicon glyphicon-plus text-success" data-toggle="modal" data-target="#edit_browser_modal"></span>
<!---->	<% } %>
			</span>
		<div class="accordion" id="accordion2">
<!---->		<% $.each(browsers, function(index,browser) { %>
			<div class="accordion-group bordered-div">
				<div class="accordion-heading">
					<span class="check-item">
						<label>
							<input class="browser" type="checkbox" value="<%= browser.id %>" checked='checked'/>  
						</label>
						<span class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse-browser-<%= index %>">
						<!----><%= browser.id %>
						</span>
<!---->						<% if (!without_controls) { %>
						<!-- ACTIONS -->
						<a class="edit-browser left-15" data-toggle="modal" data-target="#edit_browser_modal" data-id="<%= browser.id %>"><span class="glyphicon glyphicon-pencil"></span></a>
						<a class="delete-browser" data-toggle="modal" data-target="#delete_browser_modal" data-id="<%= browser.id %>"><span class="glyphicon glyphicon-remove text-danger"></span></a>
<!---->						<% } %>
					</span>
				</div>
				<div id="collapse-browser-<%= index %>" class="accordion-body collapse">
					<div class="accordion-inner left-15">
						<span class="text-block">id: <%- browser.id %></span>
						<span class="text-block">Type: <%- browser.type %></span>
						<span class="text-block">Description: <%- browser.description %></span>
						<span class="text-block">WD: <a href="<%- browser.wd_url %>" target=_blank><%- browser.wd_url %></a></span>
						<span class="text-block">Window size: <%- browser.window_size.join('x') %></span>

					</div>
				</div>
			</div>
<!---->		<% }); %>
		</div>
		</p>
</script>

<script type="text/template" id="states-checks-tpl" charset="UTF-8">
		<p> <span class="text-block">States: 
			</span>
		<div class="accordion" id="accordion2">
<!---->		<% $.each(states, function(index,state) { %>
			<div class="accordion-group bordered-div">
				<div class="accordion-heading">
					<span class="check-item">
						<label>
							<input class="state" type="checkbox" value="<%= state.id %>" checked='checked'/>  
						</label>
						<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse-state-<%= index %>">
						<!----><%= state.id %>
						</a>
					</span>
				</div>
				<div id="collapse-state-<%= index %>" class="accordion-body collapse">
					<div class="accordion-inner left-15">
						<span class="text-block">id: <%- state.id %></span>
						<span class="text-block">Description: <%- state.description %></span>
						<span class="text-block">Browser regexp: <%- state.browsers_regexp %></span>
						<span class="text-block">Matched browsers: <%- state.browsers_list.map(function(browser){ return browser['id']}).join(', ') %></span>
						<span class="text-block">Urls regexp: <%= state.urls_regexp %> </span>
						<span class="text-block">Matched urls: <%= state.urls_list.join(', ') %> </span>
					</div>
				</div>
			</div>
<!---->		<% }); %>
		</div>
		</p>
</script>


<!-- BDD launch form -->
<script type="text/template" id="small-stat-tpl" charset="UTF-8">
<!--stat --><% $.each(stat, function(status, count) { %>
				<span class="stat-<%= status.toLowerCase() %>">  <%= status.toUpperCase() %>: <%= count %> </span>
<!--stat --><% })%>
</script>

<script type="text/template" id="launch-bdd-form-tpl" charset="UTF-8">
	<div class="row-fluid">
	<!-- features -->
		<div class="form-group features span6">
			<p>Features: <br>
			<div class="accordion" id="accordion2">
<!---->	<% $.each(features, function(f_index,feature) { %>
				<div class="accordion-group bordered-div">
					<div class="accordion-heading">
						<span class="check-item">
							<label>
								<input class="parent-checkbox filter-checkbox feature" type="checkbox" value="<%- feature.name %>" checked='checked'/>  
							</label>
						<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse<%= f_index %>">
						<!----><%= feature.name %> (<%= feature.filename%>)
						</a>
						</span>
					</div>
					<div id="collapse<%= f_index %>" class="accordion-body collapse">
						<div class="accordion-inner">
							<!-- scenarios -->
							<div class="accordion left-15" id="accordion2">
<!---->						<% $.each(feature.elements, function(s_index,scenario) { %>
								<div class="accordion-group">
									<div class="accordion-heading">
										<span class="check-item">
											<label>
												<input class="parent-checkbox filter-checkbox scenario" type="checkbox" value="<%- scenario.name %>" checked='checked'/>  
											</label>
											<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse<%= f_index %>-<%= s_index %>">
													<!----><%= scenario.name %> (<%= scenario.filename %>:<%= scenario.line %>)
											</a>
										</span>
									</div>
									<div id="collapse<%= f_index %>-<%= s_index %>" class="accordion-body collapse">
										<div class="accordion-inner">
										<!-- STEPS -->
											<div class="accordion left-15" id="accordion2">
<!---->										<% $.each(scenario.steps, function(st_index,step) { %>
												<span class="check-item">
													<label>
														<input class="filter-checkbox step" type="checkbox" value="<%- step.name %>" checked='checked'/>  
														<!----><%= step.name %> (<%= step.filename %>:<%= step.line %>)
													</label>
												</span>
<!---->										<% }); %>
											</div>
										</div>
									</div>
								</div>
<!---->						<% }); %>
							</div>
						</div>
					</div>
				</div>
<!---->	<% }); %>
			</div>
			</p>
		</div>
		<!-- browsers -->
		<div class="form-group browsers-list span6">
		<!---->	<%= _.template( $('#browsers-checks-tpl').html(), { 'browsers': config.browsers } ) %>
		</div>
	</div>
	<div class="form-group">
		<label for="prj_threads">Threads</label>
		<input type="number" class="form-control input-small" id="threads" min="1" max="50" placeholder="Threads" value="<%= config.threads %>">
	</div>
	<div class="progress">
		<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
			<span class="sr-only">45% Complete</span>
		</div>
	</div>
	<div class="form-group">
		<button type="button" class="btn btn-default launch-bdd" data-action="run">RUN</button>
		<!--<button type="button" class="btn btn-default dry-run" data-run="dry-run">DRY-RUN</button>-->
		<button type="button" class="btn btn-default stop-project" data-url="/api/projects/{{project}}/bdd/build/stop">STOP</button>
		<a class="btn btn-default" target="_blank" href="/projects/{{project}}/bdd/reports/last">Last report</a>
		<span class="launch-status">Status: <span class='text-danger current-status'>N\A</span></span>
		<span class="launch-statistic"><%= _.template( $('#small-stat-tpl').html(), { 'stat': {} } ) %></span>
	</div>
</script>

<!-- Template for screens launch -->
<script type="text/template" id="launch-screens-form-tpl" charset="UTF-8">
 	<!-- Nav tabs -->
	<ul class="nav nav-tabs" role="tablist">
		<li role="presentation" class="stored-mode active"><a href="#launch-by-mode" aria-controls="launch-by-mode" role="tab" data-toggle="tab">Launch by stored mode</a></li>
		<li role="presentation" class="custom-mode"><a href="#launch-custom-config" aria-controls="launch-custom-config" role="tab" data-toggle="tab">Custom launch</a></li>
	</ul>

	<div class="tab-content border-row">
		<div role="tabpanel" class="tab-pane active" id="launch-by-mode">
			<div class="form-group">
				<label for="mode-choise">Project modes</label>
				<select class="form-control mode-choise" id="mode-choise">
					<!-- --><% $.each(data.config.modes, function(modename,mode) { %>
						<option val="<%- modename %>"><%- modename %></option>
					<!-- --><% }) %>
				</select>
			</div>
		</div>
		<!-- --><% console.log(data.config.diffs_saving) %>
		<div role="tabpanel" class="tab-pane" id="launch-custom-config">
			<div class="row-fluid">
				<!-- browsers -->
				<div class="form-group browsers-list span6">
				<!---->	<%= _.template( $('#browsers-checks-tpl').html(), { 'browsers': data.config.browsers } ) %>
				</div>
				<div class="form-group states-list span6">
				<!---->	<%= _.template( $('#states-checks-tpl').html(), { 'states': data.states } ) %>
				</div>
			</div>
			<div class="form-group">
				<label for="prj_threads">Urls</label>
				<textarea class="form-control" id="urls" rows="5"><%= data.urls.join("\r\n") %></textarea>
			</div>
		</div>
	</div>

	<div class="form-group">
		<label for="prj_threads">Threads</label>
		<input type="number" class="form-control input-small" id="threads" min="1" max="50" placeholder="Threads" value="<%= config.threads %>">
	</div>
	<div class="checkbox">
		<label>
			<input class="diffs-checkbox" type="checkbox" <%= (data.config.diffs_saving)? "checked='checked'" : '' %>> Generate diffs images for screenshots (in screens build)
		</label>
	</div>
	<div class="progress">
		<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
			<span class="sr-only">0% Complete</span>
		</div>
	</div>
	<div class="form-group">
		<button type="button" class="btn btn-default start-project" data-action="run">RUN</button>
		<button type="button" class="btn btn-default stop-project" data-url="/api/projects/{{project}}/screens/build/stop">STOP</button>
		<a class="btn btn-default" target="_blank" href="/projects/{{project}}/screens/reports/last">Last report</a>
		<span class="launch-status">Status: <span class='text-danger current-status'>N\A</span></span>
		<span class="launch-statistic"><%= _.template( $('#small-stat-tpl').html(), { 'stat': {} } ) %></span>
	</div>

</script>

<!-- REPORT TEMPLATES -->

<!-- REPORTS LIST -->
<script type="text/template" id="reports-tpl" charset="UTF-8">
	<table class="table table-striped" id="reports">
		<thead>
			<tr>
				<th>Report</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
	<!----><% $.each(reports, function( index, report ) { %>
			<tr>
				<td>
					<a href="/projects/<%= project %>/<%= type %>/reports/{{!"<%= report['timestamp'] %>"}}">{{!"<%= report['pretty'] %>"}}</a>
				</td>
				<td>
					<a href="#" class="pedant-icon delete-item delete-<%= type %>-report" data-delete-url="/api/projects/<%= project %>/<%= type %>/reports/{{!"<%= report['timestamp'] %>"}}/delete"></a>
				</td>
			</tr>
	<!----><% }); %>
		</tbody>
	</table>
</script>

<!-- BDD REPORT ITEMS -->
<script type="text/template" id="bdd-report-tpl" charset="UTF-8">
<!----><% console.log(features) %>
<!----><% $.each(features, function(feature_index, feature) { %>
<!--feature-->
<!--feature info-->
	<div class="panel panel-default feature <%= feature.status %> bordered-div" data-json="<%- JSON.stringify(feature) %>">
		<div class="feature-title feature-toggle">
			<span>
				<h4>
				<!----><% if (feature.tags) { %> 
					<span class="text-block tags"><strong>
					<!----><%= ( feature.tags.length ) ? feature.tags.map(function(tag){ return '@'+tag; }).join(' ') : '' %>
					</strong></span>
				<!----><% } %>
					<b><%= feature.keyword %>:</b> <%= feature.name %>.
			<!----><% if (feature.language) { %>
				<span>#lang: (<%= feature.language %>)</span>
			<!----><%}%>
				<strong>
				<span class="glyphicon glyphicon-info-sign" aria-hidden="true" data-toggle="modal" data-target="#report-modal"></span>
				<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span><span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>
				</strong>
				</h4>
			</span>
		</div>
		<div class="panel-body" style="<%= (feature.status == 'passed') ? 'display: none;' : 'display: block;' %>" >
	<!----><% if (feature.background != null ) { %>
			<div class="panel panel-default background" style="">
				<div class="scenario-title panel-heading">
					<h3 class="panel-title scenario-toggle">
						<p>
							<b><%= feature.background.keyword %>: </b><%= feature.background.name %>
							<b>
								<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span><span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>
							</b>
						</p>
					</h3>
				</div>
			<div class="panel-body scenario-body" style="display: none;" >
			<!----><% $.each(feature.background.steps, function(step_index, step) { %>
						<span class="step step-untested">
							<span class='step-text'>
								<p><b><%= step.keyword %></b>: <%- step.name %></p>
							</span>
						</span>
			<!---->	<% }); %>
			</div>
		</div>
	<!---->	<% } %>
	<!----><% $.each(feature.elements, function(scenario_index, scenario) { %>
	<!----><% if (scenario.type == 'background' ) { %>
			<div class="panel panel-default background" style="">
				<div class="scenario-title panel-heading">
					<h3 class="panel-title scenario-toggle">
						<p>
							<b><%= scenario.keyword %>: </b><%= scenario.name %>
							<b>
								<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span><span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>
							</b>
						</p>
					</h3>
				</div>
			<div class="panel-body scenario-body" style="display: none;" >
			<!----><% $.each(scenario.steps, function(step_index, step) { %>
						<span class="step step-untested">
							<span class='step-text'>
								<p><b><%= step.keyword %></b>: <%- step.name %></p>
							</span>
						</span>
			<!---->	<% }); %>
			</div>
		</div>
	<!----><% } else { %>
		<div class="panel panel-default scenario bordered-div" style="">
	<!----><%
			var stat = get_scenario_stat(scenario)
			var scenario_status = (stat.hasOwnProperty('passed') && stat.passed === stat.total ) ? 'passed' : 'failed'
	<!---->%>
			<div class="scenario-title panel-heading scenario-<%- scenario_status %>">
				<h3 class="panel-title scenario-toggle">
					<!----><% if (scenario.tags) { %> 
					<span class="text-block tags"><strong>
					<!----><%= ( scenario.tags.length ) ? scenario.tags.map(function(tag){ return '@'+tag; }).join(' ') : '' %>
					</strong></span>
					<!----><% } %>
					<p>
						<b><%= scenario.keyword %>: </b><%= scenario.name %>
						<!----><% if (scenario.browser_config) { %> 
							-- <%= ( scenario.browser_config.id ) ? scenario.browser_config.id : 'None' %> 
						<!----><% } %>
						<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span><span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>
					</p>
					<span class='statistic-small'><%= _.template( $('#small-stat-tpl').html(), { 'stat': stat } ) %></span>
					<!-- <p><b>Location: </b><%= scenario.location %></p> -->
				</h3>
			</div>
			<div class="panel-body scenario-body" style="<%= (scenario_status == 'passed') ? 'display: none;' : 'display: block;' %>">
			<!----><% $.each(scenario.steps, function(step_index, step) { %>
					<!--step-->
					<!----><% 
						var final_result = step.result ? step.result.status : 'untested'
						var step_error = (step.result && step.result.error_message) ? step.result.error_message : ''
						step_error = (typeof step_error === 'string') ? step_error : step_error.join("\n")
					<!---->%>
					<div class="panel step panel-default">
						<div class="panel-heading step-toggle step step-<%= final_result %>"><p><b><%= step.keyword %></b>: <%- step.name %>. --- <%= final_result %>. - <%= (step.result && step.result.duration) ? Math.round(step.result.duration*100)/100 : '0' %> sec.</div>
						<div class="panel-body step-body" style="<%= (['passed','untested'].indexOf(final_result)!=-1)? 'display: none;' : 'display: block;' %>">
							<span class="text-danger step error" style="margin-left: 7px;"><%- step_error %></span>
							<!----><% if (typeof step.screenshots != 'undefined' && $.map(step.screenshots,function(val){return val}).length ) { %>
							<span class="step-screenshots">
							<!----><% if (typeof step.screenshots.actual != 'undefined' && step.screenshots.actual.length) { %>
							<span><a class="approve-step-screenshot" data-browser_id="<%= scenario.browser_config.id %>" data-filename="<%= step.screenshots.actual[0].filename %>">Approve actual</a></span>
							<!----><% } %>
							<!----><% $.each(step.screenshots, function(screenshot_type, screenshots) { %>
								<!----><% $.each(screenshots, function(i, screenshot) { %>
										<span class='step-screenshot <%= screenshot_type %>' style="margin-left: 20px">
											<a class="status-success fancybox" rel="group" href="<%= screenshot.src %>">
												<img src="<%= screenshot.src %>" alt="<%= screenshot_type %>-<%= i %>" width='80px' />
											</a>
										</span>
								<!----><% }) %>
							<!----><% }) %>
							<!----><% } %>
							</span>
						</div>
					</div>
					<!--/step-->
			<!---->	<% }); %>

			</div>
		</div>
	<!----><% } %>	
		<!--/scenario-->
	<!---->	<% }); %>
		</div>
<!--/feature-->
	</div>
<!---->	<% }); %>
</script>

<!-- SCREENS REPORT -->
<script type="text/template" id="report-item-tpl" charset="UTF-8">
<!-- counter --> <% var counter = 0;  %>
<!---->	<% $.each(data, function(index, itemdata) { %>
<!-- --> <% counter++; var tr_index = (typeof element_index != 'undefined')? element_index:counter; %>
				<tr class="item <%= itemdata.status.toLowerCase() %>" 
				id="<%= itemdata.item.id %>-<%= itemdata.browser.id %>-<%= itemdata.state.id %>" 
				data-item-id="<%= itemdata.item.id %>" 
				data-browser-id="<%= itemdata.browser.id %>"
				data-config="<%= encodeURI(JSON.stringify(itemdata))%>">
					<td class="item-index">
<!---->					<%= tr_index %>
					</td>
					<td class="col-md-2">
						<a style="word-break: break-all;" href="<%= itemdata.item.url %>" target="_blank"><%= itemdata.item.url %></a>
						<p>In state: <b><%= itemdata.state.id %></b></p>
					</td>
					<td>
<!---->						<%= itemdata.browser.id %>
					</td>
					<td class="screenshot approved">
<!---->					<% if ( itemdata.images.approved != false ) { %>
							<a class="status-success fancybox" rel="group" href="<%= itemdata.images.approved %>">
								<img class="lazy" data-original="<%= itemdata.images.approved_thumbnail %>" alt="Approved image" src="" style="display: inline;">
							</a>
<!---->						<% } else { %>
							<i class="status-approve404 pedant-icon no-screenshot"></i>
<!---->					<% } %>
					</td>
					<td class="screenshot approved_report">
<!---->						<% if ( itemdata.images.approved_report != false ) { %>
							<a class="status-success fancybox" rel="group" href="<%= itemdata.images.approved_report %>">
								<img class="lazy" data-original="<%= itemdata.images.approved_report_thumbnail %>" alt="Approved image" src="" style="display: inline;">
							</a>
<!---->					<% } else { %>
							<i class="status-approve404 pedant-icon no-screenshot"></i>
<!---->					<% } %>
					</td>
					<td class="screenshot actual">
		
<!---->						<% if ( itemdata.images.actual != false ) { %>
							<a class="status-success fancybox" rel="group" href="<%= itemdata.images.actual %>">
								<img class="lazy" data-original="<%= itemdata.images.actual_thumbnail %>" alt="Approved image" src="" style="display: inline;">
							</a>
<!---->					<% } else { %>
							<i class="status-approve404 pedant-icon no-screenshot"></i>
<!---->					<% } %>
					</td>

					<td class="screenshot diff">
<!---->						<% if ( itemdata.images.diff != false ) { %>
							<a class="status-success fancybox" rel="group" href="<%= itemdata.images.diff %>">
								<img class="lazy" data-original="<%= itemdata.images.diff_thumbnail %>" alt="Approved image" src="" style="display: inline;">
							</a>
<!---->						<% } else { %>
							<i class="status-approve404 pedant-icon no-screenshot"></i>
<!---->						<% } %>
					</td>
					<td>
					<span><%= itemdata.item.load_time %> sec</span>
					</td>
					<td>
						<button type="button" class="btn btn-primary btn-small" data-toggle="modal" data-target="#report-modal">Details
						</button>
					</td>
					<td class="actions">
<!--approved-->			<% if (typeof action != 'undefined' && action == 'approve') { %>
							<a class="approve-action pedant-icon cancel-approve" title="Cancel approve action" data-item-id="<%= itemdata.item.id %>" data-state-id="<%= itemdata.state.id %>" data-browser-id="<%= itemdata.browser.id %>"></a>
<!-- canceled|unknown -->
<!--not approved-->		<% } else { %>
							<a class="approve-action pedant-icon approve" title="Approve" data-item-id="<%= itemdata.item.id %>" data-state-id="<%= itemdata.state.id %>" data-browser-id="<%= itemdata.browser.id %>"></a>
<!---->						<% } %>
					</td>
				</tr>
<!---->	<% }); %>
</script>

<script type="text/template" id="report-items-tpl" charset="UTF-8">
<!----><% if ( data.length > 0 ) { %>
	<table class="table items-table table-striped">
	<thead>
		<tr>
			<th>#</th>
			<th>Item name</th>
			<th>Browser</th>
			<th>Approved now</th>
			<th>Approved from past</th>
			<th>Actual image</th>
			<th>Diff image</th>
			<th>Load time</th>
			<th>Report</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody class="items">
<!----><%= _.template( $('#report-item-tpl').html(), { data: data } ) %>
	</tbody>
	</table>
<!----><% } else { %>
		<p><h3>Items not found in report</h3></p>
<!----><% } %>
</script>

<script type="text/template" id="items-filter-tpl" charset="UTF-8">
	<p>
		<label for="skill" class="col-sm-2 control-label">Filter: </label>
		<select class="select-filter form-control" multiple="" tabindex="-1" style="display: none;">
<!----><% $.each(data, function(key, data) { %>
			<optgroup label="<%= key %>">
<!---->			<% $.each(data, function(index, text) { %>
					<option data-key="<%= key %>" value="<%= text %>"><%= text %></option>
<!---->			<% }); %>
			</optgroup>
<!----><% }); %>
		</select>
	</p>
	<button type="button" class="btn btn-info filter-all">Filter all match</button>
	<button type="button" class="btn btn-info filter-exact">Filter exact matching</button>
	<button type="button" class="btn btn-info clear-filter">Reset</button>
	
	<div class="btn-group" role="group">
    <button type="button" class="btn btn-default btn-success dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
      Approve presented
      <span class="caret"></span>
    </button>
    <ul class="dropdown-menu" role="menu">
      <li><a class="approve-group" href="#">Approve</a></li>
      <li><a class="cancel-approve-group" href="#">Cancel</a></li>
    </ul>
  	</div>
</script>

<script type="text/template" id="item-by-type-tpl" charset="UTF-8">
<!---->		<% if (typeof val == 'undefined' || val == null)  { %>
				<span class='text grey'>undefined<span><br/>
<!---->		<% } else if (val.constructor === Array )  { %>
				<div class="left-15">
<!---->			<% val.forEach(function(value) { %>
<!---->    		<%= _.template($('#item-by-type-tpl').html(), {val: value}) %><br>
<!---->			<% }); %>
				</div>
<!---->		<% } else if (typeof val == 'object' ) { %>
				<div class="left-15">
<!---->			<% $.each(val, function(key, value) { %>
					<b><%= key %>: </b>
<!---->			<%= _.template($('#item-by-type-tpl').html(), {val: value}) %>
<!---->			<% }); %>
				</div>
<!---->		<% } else { %>
				<span class='text'><%= val %><span><br/>
<!---->		<% } %>
</script>

<script type="text/template" id="item-details-modal-tpl" charset="UTF-8">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title">Detail report of <%= title %></h4>
			</div>
			<div class="modal-body">
			<p class="wb">
<!---->			<%= _.template($('#item-by-type-tpl').html(), {val: items}) %>
			</p>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
			</div>
		</div>
	</div>
</script>

<script type="text/template" id="bdd-help-tpl" charset="UTF-8">
		<div class="row-fluid">
			<div class="span6">
				<h3>Languages</h3>
				<p class='bdd-lang-select'>
<!---->				<% $.each(data.languages, function(lang, words) { %>
						<h3><%= lang %></h3>
<!---->					<% $.each(words, function(keyword, values) { %>
							<div class="details-text">
								<b><%= keyword %>: </b> <%= values %>
							</div>
<!---->					<% }); %>
<!---->			<% }); %>
				</p>
			</div>
			<div class="span6">
				<h3>Step definitions</h3>
				<p>
<!---->				<% $.each(data.step_definitions, function(keyword, data) { %>
						<h3><%= ( data.length ? keyword.toUpperCase() : '' ) %></h3>
<!---->						<% $.each(data, function(index, definition) { %>
<!---->							<br><div class="details-text">
    								<b><%- definition.text %></b>
    								<p><%= definition.location %> : <%= definition.source_code[1] %></p>
    								<code><% $.each(definition.source_code[0], function(line, str) { %>
<!---->								<%= line %>:<%- str %><br>
<!---->								<% }); %>
									</code>    							
  								</div>
<!---->						<% }); %>
<!---->				<% }); %>
				</p>
			</div>
		</div>
</script>

<script type="text/template" id="item-details-modal-tpl-bckp" charset="UTF-8">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title">Report details</h4>
			</div>
			<div class="modal-body">
					<p style='word-break: break-all;'>Item URL: <%= item.item.url %></p>
<!---->				<% if (item.item.hasOwnProperty('load_time')) { %>
					<p>Page loading time (seconds): <%= item.item.load_time %> </p>
<!---->				<% } %>
					<!--browser-->
					<hr class="divider">
					<p>Browser id: <%= item.browser.id %> </p>
					<p>Browser type: <%= item.browser.type %> </p>
					<p>Webdriver URL: <%= item.browser.wd_url %> </p>
					<p>Browser description: <%= item.browser.description %> </p>
					<p>Window size: <%= item.browser.window_size[0] %> x <%= item.browser.window_size[1] %> </p>
					<!--state-->
					<hr class="divider">
					<p>State id: <%= item.state.id %> </p>
					<p>State description: <%= item.state.description %> </p>
<!---->				<% if (item.hasOwnProperty('exceptions')) { %>
						<hr class="divider">
						<!-- exceptions -->
<!---->					<% if ( item.exceptions.length ) { %>
							<p class="alert-danger">Exceptions: </p>
<!----> 					<% $.each(item.exceptions, function(key, exception_text) { %>
								<span class="alert-danger"><%= exception_text %></span>
<!---->						<% }); %>
<!---->					<% } else { %>
							<p class="alert-success">Exceptions: None</p>
<!---->					<% } %>	
<!---->				<% } %>
<!---->				<% if ( item.hasOwnProperty('status') ) { %>
						<hr class="divider">
						<!-- status -->
						<p class="<%= item.status == 'PASSED' ? 'alert-success' : 'alert-danger' %>">Status: <%= item.status %></p>
						<hr class="divider">
<!---->				<% } %>
<!---->				<% if ( item.hasOwnProperty('comparation_result') ) { %>
						<p>Comparation result: <%= item.comparison_result.length ? item.comparison_result : "None" %> </p>
<!---->				<% } %>
<!---->				<% if ( item.hasOwnProperty('report') ) { %>
						<p>Approved from report <a target="_blank" href="/projects/<%= project %>/reports/<%= item.report %>"><%= item.report %></a></p>
<!---->				<% } %>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
			</div>
		</div>
	</div>
</script>

<!-- PROJECT STATES -->
<script type="text/template" id="project-states-modal-tpl" charset="UTF-8">
	<div class="modal-header"><h4 class="modal-title">States:</h4></div>
	<div class="modal-body">
<!---->	<% $.each(states, function( index, state ) { %>
		<div class="state-info">
			<div class="param">
				<center><b>State: </b>		<%= state.id %>		</center>
			</div>
			<div class="param">
				<p><b>Description:</b>		<%= state.description %>		</p>
			</div>
			<div class="param">
				<p><b>Urls(<%= _.escape(state.urls_regexp) %>):</b><%= state.urls_list.length ? state.urls_list : 'empty' %></p>
			</div>
			<div class="param">
<!---->			<% var bro_list = state.browsers_list.map(function(b){ return b.id }) %>		
				<p><b>Browsers(<%= _.escape(state.browsers_regexp) %>):</b><%= bro_list.length ? bro_list : 'empty' %></p>
			</div>
			<div class="param">
				<p><b>Before all items methods: </b><%= state.before_all_methods.length ? state.before_all_methods : 'empty' %></p>
			</div>
			<div class="param">
				<p><b>Before one item methods: </b><%= state.before_one_methods.length ? state.before_one_methods : 'empty' %></p>
			</div>
			<div class="param">
				<p><b>Before screenshot methods: </b><%= state.before_screenshot_methods.length ? state.before_screenshot_methods : 'empty' %></p>
			</div>
			<div class="param">
				<p><b>After one methods: </b><%= state.after_one_methods.length ? state.after_one_methods : 'empty' %></p>
			</div>
			<div class="param">
				<p><b>After all methods: </b><%= state.after_all_methods.length ? state.after_all_methods : 'empty' %></p>
			</div>
		</div>
<!---->	<% }); %>
	</div>
	<div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button></div>
</script>


<!-- Approved images -->
<script type="text/template" id="approved-row-tpl" charset="UTF-8">
<!-- --> <% console.log('approved row') %>
<!-- --><% if (data.length>0) { %>
			<table class="table items-table table-striped" >
				<thead>
					<tr>
						<th>#</th>
						<th>Url</th>
						<th>Browser</th>
						<th>Approved image</th>
						<th>Info</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
<!-- -->	<% $.each(data, function( i,item ) { %>
				<tr class="item success" id='<%= i++ %>' data-config="<%= encodeURI(JSON.stringify(item)) %>">
					<td><span><%= i %></span></td>
					<td>
						<a target="_blank" href="<%= item.item.url %>"><%= item.item.url %></a>
						<br>
						<b>State: </b><span><%= item.state.id %></span>
					</td>
					<td><span><%= item.browser.id %></span></td>

					<td class="screenshot approved">
<!---->				<% if ( item['images']['approved'] ) { %>		
						<a class="status-success fancybox" rel="group" href="<%- item['images']['approved'] %>">
							<img class="lazy" data-original="<%= item['images']['approved'] %>" alt="Approved" />
						</a>
<!---->				<% } else { %>
						<i class="status-approve404 pedant-icon no-screenshot"></i>
<!---->				<% } %>
					</td>
					<td>
					<button type="button" class="btn btn-primary btn-small" data-toggle="modal" data-target="#item-modal">Details
						</button>
					</td>
					<td>
						<a class="pedant-icon delete-item" data-item-id="<%= item.item.id %>" data-state-id="<%= item.state.id %>" data-browser-id="<%= item.browser.id %>"></a>
					</td>
				</tr>
<!-- -->	<% }); %>
			</tbody>
			</table>
<!-- --><% } else { %>
		<p><h3>Images not found</h3></p>
<!-- --><% } %>
</script>