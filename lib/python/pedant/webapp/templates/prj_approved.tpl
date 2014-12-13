% include('header.tpl', title='Approved images for' + project, breadcrumbs = crumbs )
<div class="container">

<h3>Here is a approved images for project {{project}}:</h3>

<script type="text/javascript">
	var approved_items = {{ !items }}
</script>
<script type="text/template" id="approved-row-tpl" charset="UTF-8">
	{{!"<% if (data.length > 0) { %>"}}
		{{ !'<% $.each( data, function( index, item ) { %>' }}
			<tr class="item success" id='{{!"<%= index %>"}}'>
				<td>
					<span>{{!"<%= index %>"}}</span>
				</td>
				<td>
					<span>{{!"<%= item.name %>"}}</span>
				</td>
				<td>
					<span> {{!"<%= item.browser %>"}} </span>
				</td>
				<td class="screenshot approved">
					<a class="status-success fancybox" rel="group" href="{{!"<%= item['image'] %>"}}">
						<img class="lazy" data-original="{{!"<%= item['images']['approved'] %>"}}" alt="Approved" />
					</a>
				</td>
				<td class="screenshot approved">
					<a class="pedant-icon delete-item" data-delete-url='/ajax/projects/{{project}}/images/approved/delete/{{!"<%= item.name %>"}}/{{!"<%= item.browser %>"}}' onclick='remove_approved_item(this);'></a>
				</td>
			</tr>
		{{ !'<% }); %>' }}
	{{ !'<% } else { %>' }}
		<h3>Images not found</h3>
	{{!"<% } %>"}}
</script>

<table class="table items-table table-striped" id="approved-images">
	<thead>
		<tr>
			<th>#</th>
			<th>Item name</th>
			<th>Browser name</th>
			<th>approved</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
	</tbody>
</table>


</div>