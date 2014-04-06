% include('header.tpl', title='Feature detail page' )

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('/projects/%s/bdd/build'%project, 'BDD'), ('', 'Features') ])

% include('client_side_templates.tpl')

<script type="text/javascript">
	$(document).ready(function() {

		pedant_get_request('/api/projects/'+project+'/bdd/features', function(data){
			$('div.features').html(_.template($('#bdd-report-tpl').html(), {features: data.features}))
		})
		$('#report-modal').on('show.bs.modal', function (event) {
			var feature = $(event.relatedTarget).closest('div.feature').data('json')
			var html = _.template( $('#item-details-modal-tpl').html(), { title: feature.name, header_data: feature, items: feature } )
			$(this).html(html)
		})
	})
</script>

<h3>Features of {{project}}</h3>
<div class="modal fade" id="report-modal"></div>
<!-- Feature -->
<div class="features"></div>