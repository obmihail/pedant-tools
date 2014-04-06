% include('header.tpl', title='Launch ' + project )

% include('breadcrumbs.tpl', crumbs = [ ( '/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('/projects/%s/bdd/build'%project,'BDD'),('','Help') ])

<h3>BDD reference for {{project}}</h3>

% include('client_side_templates.tpl')

<script>
	$(document).ready(function() {
		
		pedant_get_request('/api/projects/'+project+'/bdd/reference',function(data){
			console.log(data)
			$(".help-content").html( _.template( $('#bdd-help-tpl').html(),{data:data.reference}) )
			$("select").select2()
		})
	});
</script>

<div class="modal fade" id="help-modal"></div>
<div class="help-content"></div>