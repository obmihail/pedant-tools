% include('header.tpl', title='Approved images for' + project, breadcrumbs = crumbs )
<div class="container">

<h3>Here is a approved images for project {{project}}:</h3>

<table class="table items-table table-striped">
	<thead>
		<tr>
			<th>#</th>
			<th>Item name</th>
			<th>Browser configuration</th>
			<th>Approved now</th>
		</tr>
	</thead>
	<tbody>
		% for num,item in enumerate(approved_list):
			<tr class="item success">
				<td>
					<span>{{num}}</span>
				</td>
				<td>
					<span> {{item['name']}} </span>
				</td>
				<td>
					<span> {{item['browser']}} </span>
				</td>
				<td class="screenshot approved">
					%include( 'prj_report_image.tpl' , img = item['image'], alt="Approved" , status='success' )
				</td>
			</tr>
		% end
	</tbody>
</table>


</div>