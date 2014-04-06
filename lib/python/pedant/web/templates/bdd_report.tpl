% include('header.tpl', title='Report: ' + report['pretty'] )

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('/projects/%s/bdd/build'%project, 'BDD'), ('/projects/%s/bdd/reports'%project, 'Reports'), ('',report['pretty']) ])

% include('client_side_templates.tpl')

<script type="text/javascript">
	var _items = []
	$(document).ready(function() { 
		load_bdd_report([
			function(data){
				console.log(data)
				$('div.report-content').html( _.template($('#bdd-report-tpl').html(), {features: data}) )
			},
			function(items) {
				var stat = {total: 0}
				//get statuses
				items.reduce(function(stat, current) {
					current.elements.reduce(function(prev,current_scenario){
						if (current_scenario.type == 'background') return stat
						stat.total += 1
						//check passed steps
						var scenario_stat = get_scenario_stat(current_scenario)
						var scenario_status = (scenario_stat.hasOwnProperty('passed') && scenario_stat.passed === scenario_stat.total ) ? 'passed' : 'failed'
						stat[scenario_status] = ( stat.hasOwnProperty(scenario_status) ? stat[scenario_status] + 1 : 1);
						return stat
			  		},stat)
			  		return stat
				}, stat);
				draw_stat(stat)
		}
			]
		)
		//filter
		$('#report-modal').on('show.bs.modal', function (event) {
			var feature = $(event.relatedTarget).closest('div.feature').data('json')
			var html = _.template( $('#item-details-modal-tpl').html(), { title: feature.name, header_data: feature, items: feature } )
			$(this).html(html)
		})
		$(".report-content").on('click', '.more-error-link',(function() {
			$(this).closest('.step').find('.more-error').toggle();
		}))

	});
	$(document)
		.on("click",".approve-step-screenshot", function(){
			var data = { items: [ {'filename': $(this).data('filename'), 'browser_id': $(this).data('browser_id')}] }
			var elem = $(this)
			pedant_post_request( '/api/projects/'+project+'/bdd/reports/'+report['timestamp']+'/approve', data, 
				function(data){
					if (data.items[0].status != 'OK') {
						show_error(data.items[0].msg)
						return
					}
					elem.removeClass("approve-step-screenshot").addClass("cancel-approve-step-screenshot").text('Cancel approve')
				})
		})
		.on("click",".cancel-approve-step-screenshot", function(){
			var data = { items: [{'filename': $(this).data('filename'), 'browser_id': $(this).data('browser_id')}] }
			var elem = $(this)
			pedant_post_request( '/api/projects/'+project+'/bdd/reports/'+report['timestamp']+'/cancel-approve', data, function(data){
					if (data.items[0].status != 'OK') {
						show_error(data.items[0].msg)
						return
					}
					elem.removeClass("cancel-approve-step-screenshot").addClass("approve-step-screenshot").text("Approve actual")
				})
		})
</script>

<h3>Report {{report['pretty']}}</h3>

<div class="modal fade" id="report-modal"></div>

<div class="statistic">
	<ul class="list-group stat-group"></ul>
</div>

<!-- FILTER -->
<div class="form-group">
	<div class="col-sm-12">
		<div class="report-filter"></div>
		<!-- <div class="btn-group"></div> -->
	</div>
</div>
<!-- REPORT -->
<div class="report-content"></div>