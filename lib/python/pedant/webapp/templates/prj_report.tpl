% include('header.tpl', title='Report:' + timestamp)
<div class="container">

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

<div data-alerts="alerts" data-titles="{'warning': '<em>Warning!</em>'}" data-ids="myid" data-fade="2000" ></div>

<div class="btn-group">

	<button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown">
		<span class="caret"></span>
		<span class="sr-only">Group actions</span>
	</button>
	<ul class="dropdown-menu" role="menu">
		<li><a class="toggle-all select">Select all</a></li>
		<li><a class="toggle-not-approved select">Select not approved</a></li>
		<li><a class="toggle-diffs select">Select diffs</a></li>
		<li class="divider"></li>
		<li><a class="approve-disapprove-selected approve-selected">Approve selected</a></li>
	</ul>
	
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
	<tbody>
		% for num,item_report in enumerate(report_list):
			% if item_report['msg'] == 'success':
				<tr class="item success"
			% else:
				<tr class="item error"
			% end
			item-id = "{{num}}" data-source-uniq="{{item_report['item']['unid']}}" data-browser-uniq="{{item_report['browser']['unid']}}">
				<td>
				{{num}}
				</td>
				<td>
				<a href="{{item_report['item']['url']}}" target="_blank"> {{item_report['item']['name']}} 
				</td>
				<td>
					<span> {{item_report['browser']['unid']}} </span>
				</td>
				<td class="screenshot approved">
					%include( 'prj_report_image.tpl' , img = item_report['images']['approved'], alt="Approved" , status=item_report['msg'] )
				</td>
				<td class="screenshot approved_report">
					%include( 'prj_report_image.tpl' , img = item_report['images']['approved_report'], alt="Approved in report", status=item_report['msg'] )
				</td>
				<td class="screenshot actual">
					%include( 'prj_report_image.tpl' , img = item_report['images']['actual'], alt="Actual", status='success' )
				</td>
				<td class="screenshot diff">
					%include( 'prj_report_image.tpl' , img = item_report['images']['diff'], alt="Diff", status=item_report['msg'] )
				</td>
				<td>
					<span>{{item_report['item']['load_time']}} sec</span>
				</td>
				<td class="actions">
					<a class="approve-action pedant-icon approve" 
						title="Approve actual sreenshot"
						data-approve-path="/{{project}}/ajax/approve/{{timestamp}}/{{item_report['item']['unid']}}/{{item_report['browser']['unid']}}"
						data-cancel-approve-path="/{{project}}/ajax/cancel-approve/{{timestamp}}/{{item_report['item']['unid']}}/{{item_report['browser']['unid']}}"
					></a>
				</td>
			</tr>
		% end
	</tbody>
</table>


</div>