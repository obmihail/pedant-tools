% include('header.tpl', title='Reports for '+ project )

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/%s'%project, project), ('/projects/%s/screens/build'%project, 'Screens'), ('', 'Reports') ])

% include('client_side_templates.tpl')

<script>
	$(document).ready(function() { 
		pedant_get_request("/api/projects/"+project+"/screens/reports",function(data){
			$('.reports').html( _.template( $('#reports-tpl').html(), { 'reports': data.reports, 'type': 'screens' } ))
		});
	})
	$(document)
		.on('click', '.delete-screens-report',(function() {
			pedant_post_request( $(this).data("delete-url"), {}, function(data){ 
				pedant_get_request("/api/projects/"+project+"/screens/reports",function(data){
					$('.reports').html( _.template( $('#reports-tpl').html(), { 'reports': data.reports, 'type': 'screens' } ))
				});
			})
	}))
</script>

<h3>Reports list for {{project}}:</h3>
<div class="reports"></div>

% include('footer.tpl')