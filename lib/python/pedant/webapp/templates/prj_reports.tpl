% include('header.tpl', title='Reports for '+ project )
<div class="container">

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/'+project, project), ('', 'Reports') ])

<h3>Here is a reports list for {{project}}:</h3>

<table class="table table-striped">
	<thead>
		<tr>
			<th>Report</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
		% for report in reports_list:
			<tr>
				<td>
					<a href="/projects/{{project}}/reports/{{report['timestamp']}}"> {{report['pretty']}} </a>
				</td>
				<td>
					<a href="javascript:remove_approved_item(this);" class="pedant-icon delete-item delete-report" data-delete-url="/ajax/projects/{{project}}/delete/report/{{report}}"></a>
				</td>
			</tr>
		% end
	</tbody>
</table>

</div>
% include('footer.tpl')