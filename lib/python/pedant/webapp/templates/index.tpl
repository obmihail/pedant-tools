% include('header.tpl', title='Pedant main page')
<div class="container">

<h3>Here is a project lists:</h3>
<div data-alerts="alerts" data-titles="{'warning': '<em>Warning!</em>'}" data-ids="myid" data-fade="2000" ></div>
<div>  
  <fieldset>
    <div class="form-group required-input">
      <input type="text" class="form-control" id="dir_path" placeholder="Path for scanning">
    </div>
    <a href="#" class="btn btn-default btn-lg active scan_projects" role="button">Find projects</a>
    <a href="/projects/new" class="btn btn-default btn-lg active" role="button">Add manually</a>
    <img class="preloader hidden" src="/assets/img/preload.gif"/>
  </fieldset>
</div>
<table class="table table-striped">
	<thead>
		<tr>
			<th>Project name</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
		% for prj in prj_list:
			<tr>
				<td>
				<a href="/{{prj}}/reports"> {{prj.upper()}} 
				</td>
				<td>
					<!-- Single button -->
					<div class="btn-group">
						<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
							Actions <span class="caret"></span>
						</button>
						<ul class="dropdown-menu" role="menu">
							<li><a href="/projects/{{prj}}/launch">Launch project</a></li>
							<li><a href="/{{prj}}/reports/last">Last report</a></li>
							<li><a href="/{{prj}}/reports">Reports list</a></li>
							<li><a href="/{{prj}}/approved">Approved</a></li>
							<li class="divider"></li>
							<li><a href="/{{prj}}/ajax/export/approved/zip">Download approved images</a></li>
						</ul>
					</div>
				</td>
			</tr>
		% end
	</tbody>
</table>

</div>
% include('footer.tpl')