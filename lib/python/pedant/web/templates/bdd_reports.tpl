% include('header.tpl', title='Reports for '+ project )

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/%s'%project, project), ('/projects/%s/bdd/build'%project, 'BDD'), ('', 'Reports') ])

% include('client_side_templates.tpl')

<script>
	$(document).ready(function() { 
		pedant_get_request("/api/projects/"+project+"/bdd/reports",function(data){
			$('.reports').html( _.template( $('#reports-tpl').html(), { 'reports': data.reports, 'type': 'bdd' } ))
		});
	});
	$(document)
		.on('click', '.delete-bdd-report',(function() {
			pedant_post_request( $(this).data("delete-url"), {},function(data){ 
				pedant_get_request("/api/projects/"+project+"/bdd/reports",function(data){
					$('.reports').html( _.template( $('#reports-tpl').html(), { 'reports': data.reports, 'type': 'bdd' } ))
				});

				//redraw_reports('bdd');
			})
		}))
</script>

<h3>Reports list for {{project}}:</h3>
<div class="reports"></div>

% include('footer.tpl')