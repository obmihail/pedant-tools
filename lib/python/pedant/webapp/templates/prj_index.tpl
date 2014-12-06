% include('header.tpl', title='Pedant main page', breadcrumbs = crumbs )

<div class="container">

<script type="text/javascript">
	var projects = {{ !prj_list }}
</script>

<script type="text/template" id="project-row-tpl" charset="UTF-8">
	{{!"<% if (data.length > 0) { %>"}}
		{{ !'<% $.each( data, function( index, project ) { %>' }}
			<tr>
				<td>
				<a href="/projects/{{!"<%= project %>"}}"> {{!"<%= project %>"}} 
				</td>
				<td>
					<!-- Single button -->
					<div class="btn-group">
						<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
							Actions <span class="caret"></span>
						</button>
						<ul class="dropdown-menu" role="menu">
							<li><a href="/projects/{{!"<%= project %>"}}/launch">Launch project</a></li>
							<li><a href="/projects/{{!"<%= project %>"}}/edit">Edit configuration</a></li>
							<li class="divider"></li>
							<li><a href="/projects/{{!"<%= project %>"}}/reports/last">Last report</a></li>
							<li><a href="/projects/{{!"<%= project %>"}}/reports">Reports list</a></li>
							<li class="divider"></li>
							<li><a href="/projects/{{!"<%= project %>"}}/approved">Approved images</a></li>
							<li><a href="/ajax/projects/{{!"<%= project %>"}}/export/approved/zip">Download approved images</a></li>
							<li class="divider"></li>
							<li><a href="javascript:delete_project('{{!"<%= project %>"}}');">Remove</a></li>
						</ul>
					</div>
				</td>
			</tr>
		{{ !'<% }); %>' }}
	{{ !'<% } else { %>' }}
		<h3>Projects not found</h3>
	{{!"<% } %>"}}
</script>

<h3>Here is a project lists:</h3>
<div> 
  <fieldset>
  	<div class="form-group required-input form-inline">
        <input type="text" class="form-control" id="dir_path" placeholder="Path for scanning" value="{{!search_directory}}">
        <a href="#" class="btn btn-default active scan_projects" role="button" data-url="">Find projects</a>
    </div>
    
    <a href="/projects/new" class="btn btn-default btn-lg active" role="button">Add manually</a>
    <img class="preloader hidden" src="/assets/img/preload.gif"/>
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

</div>
% include('footer.tpl')