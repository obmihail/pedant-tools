% include('header.tpl', title='Launch ' + project )

% include('breadcrumbs.tpl', crumbs = [ ( '/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('/projects/%s/bdd/build'%project,'BDD'),('','Launch') ])

<h3>Launch BDD Features for {{project}}</h3>

% include('client_side_templates.tpl')
% include('prj_edit_modals.tpl')


<script>
	$(document).ready(function() {
		load_project_config( function(data){
			pedant_get_request('/api/projects/'+project+'/bdd/features',function(bdd_data){
				if (bdd_data.features.length) {
					$('.launch-form').html( _.template( $('#launch-bdd-form-tpl').html(), { features: bdd_data.features } ))
				}
				else {
					$(document).trigger("add-alerts", [
						{ 'message': "Sorry, features not found in project "+project+". Create features before launch", 'priority': 'error' }
					]);
				}				
			})

		});
	});
	$(document)
	.on("click", ".launch-bdd", function() {
		var start_url = '/api/projects/'+project+'/bdd/build/start'
		var data = {'browsers':[], filter:{'features':[],'scenarios':[],'steps':[]}, 'threads': config.threads }
		checked_ids = []
		$('.browsers-list input:checked').each(function(){ checked_ids.push( $(this).val() ) });
		data.browsers = config.browsers.filter(function(bro){
			return ( checked_ids.indexOf(bro.id) > -1 )
		})
		$(' input.feature:checked').each(function() {
			data.filter.features.push($(this).val());
		});
		$(' input.scenario:checked').each(function() {
			data.filter.scenarios.push($(this).val());
		});
		$(' input.step:checked').each(function() {
			data.filter.steps.push($(this).val());
		});
		if (data.filter.features.length || data.filter.scenarios.length || data.filter.steps.length){
			pedant_post_request(start_url, data,
				function(data){
					//disable start button
					$(this).attr('disabled','disabled')
					$(".current-status").text('Started')
					var url = '/api/projects/'+project+'/bdd/build/status'
					$(".launch-info").val('');
					$(".progress-bar").width( '0%');
					$(".launch-statistic").html(_.template( $('#small-stat-tpl').html(), { 'stat': {} } ))
					window.update_interval_id = setInterval( function() { update_launch_info(url) }, 2000 )
				},
				function(data){
					$(document).trigger("add-alerts", [
							{ 'message': data.msg, 'priority': 'error' }
					]);
					$(".start-project").removeAttr("disabled")
					$(".current-status").text('ERROR')
			})
		} else {
			$(document).trigger("add-alerts", [
				{ 'message': 'Empty features, scenarios and steps. Nothing scan', 'priority': 'error' }
			]);
		}
	}).on("click",".stop-project", function(){
		//send ajax for stoppin and wait answer
		$(this).attr('disabled','disabled')
		var stop_url = $(this).data('url')
		//send ajax for stopping
		pedant_post_request(stop_url, function(data){
			return;
		})
		//alert( "STOP operation is not fast, wait correct stopping")
		$(this).removeAttr('disabled')
	}).on("click",".dry-run", function(){
		var start_url = '/api/projects/'+project+'/bdd/launch/dry-run'
		var data = {'browsers':[], 'features':[]}
		checked_ids = []
		$('.browsers input:checked').each(function(){ checked_ids.push( $(this).val() ) });
		data.browsers = config.browsers.filter(function(bro){
			return ( checked_ids.indexOf(bro.id) > -1 )
		})
		$('.features input:checked').each(function() {
			data.features.push($(this).val());
		});
		if (data.features){
			pedant_post_request(start_url, data,
				function(data){
					//write log
					$(".launch-info").val(data.log);
				})
		}
	}).on("click","input.parent-checkbox", function(){
		var ischecked= $(this).is(':checked');
		$(this).closest("div.accordion-group").find("div.accordion-body input.filter-checkbox").prop('checked', ischecked );
	})
</script>

<div class="modal fade" id="help-modal"></div>

<div class="launch-form"></div>

<!-- Launch log -->
<h4>Log: </h4>
<div class="container-fluid">
	<div class="row"> <!-- Give this div your desired background color -->
		<div class="container">
			<div class="row">
				<div class="col-md-12">
					<textarea class="launch-info col-md-12" rows="10"></textarea>
				</div>
			</div>
		</div>
	</div>
</div>

% include('footer.tpl')