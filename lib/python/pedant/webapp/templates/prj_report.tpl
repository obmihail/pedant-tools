% include('header.tpl', title='Report:' + timestamp, breadcrumbs = crumbs )
<div class="container">

<script type="text/javascript">
	var items = {{ !report_list }}
</script>
<script type="text/template" id="item-row-tpl" charset="UTF-8">
	{{ !'<% $.each(data, function( index, item ) { %>' }}
			<tr class="item {{!"<%= ( item.msg === 'success' ? 'success' : 'danger') %>"}}"
			id="{{ !"<%= item.element_id %>"}}" 
			data-source-uniq="{{ !"<%= item.item.unid %>" }}" 
			data-browser-uniq="{{ !"<%= item.browser.unid %>" }}"
			data-config="{{ !"<%= escape( JSON.stringify(item) ) %>"}}" >
				<td>
					{{ !"<%= item.item.unid %>" }}
				</td>
				<td>
				<a href="{{!"<%= item.item.url %>"}}" target="_blank"> {{ !"<%= item.item.unid %>" }}
				</a></td>
				<td>
					<span> {{!"<%= item.browser.unid %>" }} </span>
				</td>
				<td class="screenshot approved">
					{{!"<% if ( item.images.approved != false ) { %> "}}
						<a class="status-success fancybox" rel="group" href="{{!"<%= item.images.approved %>"}}">
							<img class="lazy" data-original="{{!"<%= item.images.approved %>"}}" alt="Approved image" src="" style="display: inline;">
						</a>
					{{!"<% } else { %>"}}
						<i class="pedant-icon no-screenshot"></i>
					{{!"<% } %>"}}
				</td>
				<td class="screenshot approved_report">
					{{!"<% if ( item.images.approved_report != false ) { %> "}}
						<a class="status-success fancybox" rel="group" href="{{!"<%= item.images.approved_report %>"}}">
							<img class="lazy" data-original="{{!"<%= item.images.approved_report %>"}}" alt="Approved image" src="" style="display: inline;">
						</a>
					{{!"<% } else { %>"}}
						<i class="status-approve404 pedant-icon no-screenshot"></i>
					{{!"<% } %>"}}
				</td>
				<td class="screenshot actual">
	
					{{!"<% if ( item.images.actual != false ) { %>  "}}
						<a class="status-success fancybox" rel="group" href="{{!"<%= item.images.actual %>"}}">
							<img class="lazy" data-original="{{!"<%= item.images.actual %>"}}" alt="Approved image" src="" style="display: inline;">
						</a>
					{{!"<% } else { %>"}}
						<i class="status-approve404 pedant-icon no-screenshot"></i>
					{{!"<% } %>"}}

				</td>

				<td class="screenshot diff">
					{{!"<% if ( item.images.diff != false ) { %> "}}
						<a class="status-success fancybox" rel="group" href="{{!"<%= item.images.diff %>"}}">
							<img class="lazy" data-original="{{!"<%= item.images.diff %>"}}" alt="Approved image" src="" style="display: inline;">
						</a>
					{{!"<% } else { %>"}}
						<i class="status-approve404 pedant-icon no-screenshot"></i>
					{{!"<% } %>"}}
				</td>
				<td>
					<span>{{!"<%= item.item.load_time %>"}} sec</span>
				</td>
				<td class="actions">
					<a class="approve-action pedant-icon {{!"<%= action.class %>"}}" 
						title="{{!"<%= action.title %>"}}" 
						data-approve-path="/ajax/projects/{{project}}/approve/{{timestamp}}/{{!"<%= item.item.unid %>"}}/{{!"<%= item.browser.unid %>"}}"
						data-cancel-approve-path="/ajax/projects/{{ project }}/cancel-approve/{{timestamp}}/{{!"<%= item.item.unid %>"}}/{{!"<%= item.browser.unid %>"}}"></a>
				</td>
			</tr>
		}
	}
	{{ !"<% }); %>" }}
</script>

<h3>Here is a report {{timestamp}}</h3>

<div>
	<ul class="list-group">
		<li class="list-group-item">
			Total:
			<span class="total-count badge">0</span>
		</li>
		<li class="list-group-item">
			Errors:
			<span class="error-count badge badge-important">0</span>
		</li>
		<li class="list-group-item">
			Selected:
			<span class="selected-count badge badge-info">0</span>
		</li>
	</ul>
<div>



<div class="btn-group">
  <button type="button" class="btn btn-danger">Action</button>
  <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
    <span class="caret"></span>
    <span class="sr-only">Toggle Dropdown</span>
  </button>
  <ul class="dropdown-menu" role="menu">
	<li><a class="toggle-all select">Select all</a></li>
	<li><a class="toggle-not-approved select">Select not approved</a></li>
	<li><a class="toggle-diffs select">Select diffs</a></li>
	<li class="divider"></li>
	<li><a class="approve-disapprove-selected approve-selected">Approve selected</a></li>
  </ul>
</div>
	
</div>

<table class="table items-table table-striped">
	<thead>
		<tr>
			<th>#</th>
			<th>Item name</th>
			<th>Browser configuration</th>
			<th>Approved now</th>
			<th>Approved from past</th>
			<th>Actual image</th>
			<th>Diff image</th>
			<th>Page load time</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody class="items">
		
	</tbody>
</table>


</div>