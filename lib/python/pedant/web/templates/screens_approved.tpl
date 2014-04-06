% include('header.tpl', title='Approved images for' + project )

% include('breadcrumbs.tpl', crumbs = [ ( '/', 'Home'), ( '/projects','Projects'), ( '/projects/%s'%project, project ), ( '/projects/%s/screens/build'%project, 'Screens' ), ('','Approved images') ])

% include('client_side_templates.tpl')

<h3>Approved images for project {{project}}:</h3>

<script type="text/javascript">
	$(document).ready(function() { 
		var _items = []
		pedant_get_request("/api/projects/"+project+"/screens/approved",function(data){
			var html = _.template($('#approved-row-tpl').html(), {data: data.items})
			$("#approved-images").html(html)
			//$('#approved-images tbody').html( _.template( $('#approved-row-tpl').html(), { data: approved_items } ))
			$("img.lazy").lazyload({skip_invisible : false});
		});

		$('#item-modal').on('show.bs.modal', function (event) {
			var item = jQuery.parseJSON(decodeURI($(event.relatedTarget).closest('tr').data('config')))
			$(this).html(_.template($('#item-details-modal-tpl').html(), { title: 'approved info', items: item }))
		});

		$("#approved-images").on('click','.delete-item', function (event){
			var url = '/api/projects/'+ project + '/screens/approved/delete'
			if (confirm('Are you sure?')) {
				var data = { 'items': [ { 'item_id': $(this).data('item-id'), 'state_id': $(this).data('state-id'), 'browser_id': $(this).data('browser-id') }]}
				var to_remove = $(this).closest('tr')
				pedant_post_request(url, data, function(data){
					if ( data.items[0].status == 'OK' ) {
						console.log(data.items[0].status)
						$(document).trigger("add-alerts", [
							{ 'message': 'Removed', 'priority': 'success' }
						])
						to_remove.remove()
					}
					else {					
						$(document).trigger("add-alerts", [
							{ 'message': data.items[0].msg, 'priority': 'error' }
						]);
					}
				})
			};
		});

		
	});
</script>

<div class="modal fade" id="item-modal"></div>
<div id="approved-images"></div>