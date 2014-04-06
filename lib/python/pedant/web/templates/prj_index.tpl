% include('header.tpl', title='Pedant projects' )

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('','Projects') ] )

<script type="text/template" id="project-row-tpl" charset="UTF-8">
<!----> <% if (projects.length > 0) { %>
<!---->		<% $.each( projects, function( index, project ) { %>
			<tr class='item project-item'>
				<td>
					<a href="/projects/<%= project['name'] %>"> <%= project['name'] %> 
				</td>
				<td>
					<!-- Single button -->
					<div class="btn-group">
						<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">Pages<span class="caret"></span>
						</button>
						<ul class="dropdown-menu" role="menu">
							<li><a href="/projects/<%= project['name']%>/edit">Edit configuration</a></li>
							<li class="divider"></li>
							<li><a href="/projects/<%= project['name']%>/screens/build">Run screenshots compare</a></li>
							<li class="divider"></li>
							<li><a href="/projects/<%= project['name']%>/screens/reports/last">Last screenshots comparison report</a></li>
							<li><a href="/projects/<%= project['name']%>/screens/reports">Screenshots comparison reports</a></li>
							<li class="divider"></li>
							<li><a href="/projects/<%= project['name']%>/screens/approved">Approved images for screenshots comparison</a></li>
							<li class="divider"></li>
							<li><a href="/api/projects/<%= project['name']%>/screens/approved.zip/export">Download approved images for screenshots comparison</a></li>
							<li class="divider"></li>
							<li><a href="/projects/<%= project['name']%>/bdd/build">Run BDD features</a></li>
							<li><a href="/projects/<%= project['name']%>/bdd">BDD reference</a></li>
							<li><a href="/projects/<%= project['name']%>/bdd/features">BDD features</a></li>
							<li class="divider"></li>
							<li><a href="/projects/<%= project['name']%>/bdd/reports">BDD reports list</a></li>
							<li><a href="/projects/<%= project['name']%>/bdd/reports">BDD last report</a></li>
							<li class="divider"></li>
							<li><a class="delete-project" data-name="<%- project['name'] %>">Remove</a></li>
						</ul>
					</div>
				</td>
			</tr>
<!---->		<% }); %>
<!---->	<% } else { %>
		<h3>Projects not found</h3>
<!---->	<% } %>
</script>

<script type="text/javascript">
	$(document).ready(function() { 
		pedant_get_request("/api/projects",function(data){
			$('#projects tbody').html( _.template( $('#project-row-tpl').html(), { 'projects': data.projects } ))
		});

	$(".attach-projects-btn").click(function() {
			var input = $("#path")
			if ( input.val().length < 1 )
			{
				input.closest(".form-group").addClass("has-error")
				return
			}
			//send ajax
			pedant_post_request("/api/projects/attach", {'path':input.val()}, function(data){
				show_error(data.msg)
				pedant_get_request("/api/projects",function(data){
					$('#projects tbody').html( _.template( $('#project-row-tpl').html(), { 'projects': data.projects } ))
				});
			},
			function(data){
				//hide preloader
				$(document).trigger("add-alerts", [
					{ 'message': data.msg, 'priority': 'error' }
				]);
			})
			
		});
	})
	$(document)
		.on('click', '.delete-project',(function() {
			if (confirm("Are you sure? This action remove all reports and all approved images for project " + name)){
				pedant_post_request( "/api/projects/"+$(this).data('name')+"/delete", [], 
					function(data){
						pedant_get_request("/api/projects",function(data){
							$('#projects tbody').html( _.template( $('#project-row-tpl').html(), { 'projects': data.projects } ))
							});
					})
			}
		}))
</script>

<h3>Here is a project lists:</h3>
<div> 
	<fieldset>
		<div class="form-group required-input form-inline">
			<label for="path">Path: </label>
			<input type="text" class="form-control" id="path" placeholder="Path for scanning" value="{{!search_directory}}">
        	<img class="preloader hidden" src="/assets/img/preload.gif"/>
			<a href="#" class="btn btn-default active attach-projects-btn" role="button" data-url="">Attach projects</a>
		</div>
		<a href="/projects/new" class="btn btn-default active" role="button">Add project</a>
	</fieldset>
</div>
<table class="table table-striped" id="projects">
	<thead>
		<tr>
			<th>Project name</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
	</tbody>
</table>

% include('footer.tpl')