% include('header.tpl', title='Pedant main page')
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
					<a href="/{{project}}/reports/{{report}}"> {{report}} </a>
				</td>
				<td>
					<a class="pedant-icon delete-item" data-delete-url="/{{project}}/ajax/delete/report/{{report}}"></a>
				</td>
			</tr>
		% end
	</tbody>
</table>

</div>
% include('footer.tpl')