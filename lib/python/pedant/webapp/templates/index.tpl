% include('header.tpl', title='Pedant main page')
<div class="container">

<h3>Here is a project lists:</h3>

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
							<li><a href="/{{prj}}/reports">Project detail page</a></li>
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