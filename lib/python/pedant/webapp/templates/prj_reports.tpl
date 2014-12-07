% include('header.tpl', title='Pedant main page', breadcrumbs = crumbs )
<div class="container">

<h3>Here is a reports list for {{project}}:</h3>

<div data-alerts="alerts" data-titles="{'warning': '<em>Warning!</em>'}" data-ids="myid" data-fade="2000" ></div>

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
					<a href="/projects/{{project}}/reports/{{report}}"> {{report}} </a>
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