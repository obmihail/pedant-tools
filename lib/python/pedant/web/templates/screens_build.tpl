% include('header.tpl', title='Launch ' + project )

% include('breadcrumbs.tpl', crumbs = [ ( '/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('/projects/%s/screens/build'%project,'Screens'),('','Launch') ])

<h3>Launch {{project}}</h3>

% include('client_side_templates.tpl')
% include('prj_edit_modals.tpl')

<script>
	$(document).ready(function() {
		load_project_config( function(data){
			var states_url = '/api/projects/'+project+'/screens/states'
			pedant_get_request(states_url, function(states_data){
				var params = {'config': data.config, 'states': states_data.states, 'urls': data.urls}
				$('.launch-form').html( _.template( $('#launch-screens-form-tpl').html(), { data: params } ))	
			})
		});
	});
	$(document)
		.on("click",".stop-project", function(){
			//send stop request
			var stop_url = '/api/projects/'+project+'/screens/build/stop'
			pedant_post_request( stop_url, {},
				function(data){
					//show message
					$(document).trigger("add-alerts", [{ 'message': data.msg, 'priority': 'error' }]);
				}
			)
		})
		.on("click",".start-project", function(){
			//if selected tab - send custom config to launch
			if ( $("li.custom-mode.active").length > 0 )
			{
				data = {}
				bro_ids = []
				states_ids = []
				//browsers
				$('.browsers-list input:checked').each(function(){ bro_ids.push( $(this).val() ) });
				data.browsers = config.browsers.filter(function(bro){ return ( bro_ids.indexOf(bro.id) > -1 ) })
				//urls
				data.urls = $("#urls").val().split("\n")
				//states
				$('.states-list input:checked').each(function(){ states_ids.push( $(this).val() ) });
				data.states = states_ids
				var start_url = '/api/projects/'+project+'/screens/build/start/custom'
				var ids = [];
				$('.browsers-list input:checked').each(function(){ ids.push($(this).val()) });
			}
			else
			{
				var start_url = '/api/projects/'+project+'/screens/build/start'
				var mode = $("#mode-choise").val()
				if ( mode === null ) 
				{
					return alert('Select launch params for continue')
				}
				data = {mode:mode}
			}
			data.threads = parseInt($("#threads").val())
			data.diffs_saving = config.diffs_saving
			pedant_post_request( start_url, data,
				function( data ){
					//disable start button
					$(this).attr('disabled','disabled')
					$(".current-status").text('Started')
					var url = '/api/projects/'+project+'/screens/build/status'
					$(".launch-info").val('');
					$(".progress-bar").width( '0%');
					$(".launch-statistic").html(_.template( $('#small-stat-tpl').html(), { 'stat': {} } ))
					window.update_interval_id = setInterval( function() { update_launch_info(url) }, 2000 )
				},
				function( data ){
					$(document).trigger("add-alerts", [{ 'message': data.msg, 'priority': 'error' }]);
					$(".start-project").removeAttr("disabled")
					$(".current-status").text('ERROR')
			})
		})
</script>

<!-- tabs -->


<div class="launch-form"></div>

<!-- WORK RESULTS -->
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