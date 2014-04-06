% include('header.tpl', title='Report: ' + report['pretty'] )

% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('/projects/%s/screens/build'%project, 'Screens'), ('/projects/%s/screens/reports'%project, 'Reports'), ('',report['pretty']) ])

% include('client_side_templates.tpl')

<script type="text/javascript">
	var _items = []
	$(document).ready(function() { 
		redraw_report_items()
		//filter
		$('#report-modal').on('show.bs.modal', function (event) {
			var item = jQuery.parseJSON(decodeURI($(event.relatedTarget).closest('tr').data('config')))
			var html = _.template( $('#item-details-modal-tpl').html(), { items: [item], title: 'Details for item: '+item['url'] } )
			$(this).html(html)
		})

		$(".report-content")
			.on('click', 'a.approve-action',function () {
				if ($(this).is(".cancel-approve")) {
					send_approve_request($(this).closest("tr"),'cancel-approve')
				}
				else {
					send_approve_request($(this).closest("tr"),'approve')
				}
		})
		$(".report-filter")
			.on("click", '.clear-filter', function () { 
				$(".select-filter").val(null).trigger("change");
				//redraw items
				redraw_report_items()
			})
			.on("click", '.filter-all', function () { 
				//.val(null).trigger("change");
				var filtered_items = []
				var filtered_indexes = []
				var selected_items = $(".select-filter").select2('data')//$(this).select2('data')
				for(var i=0;i<selected_items.length;i++) {
					var key = $(selected_items[i].element).data('key')
					var value = $(selected_items[i].element).val()
					//find items by selected key&value
					filtered_items = filtered_items.concat(_items.filter(function(item) {
						var _search_item = item.hasOwnProperty(key) ? item[key] : item.item.hasOwnProperty(key) ? item.item[key] : false
						if (_search_item === false ) return _search_item
						return ((_search_item.hasOwnProperty('id') && _search_item['id'] === value)
							|| ( !isNaN(parseFloat(value.split('-')[0])) && _search_item >= parseFloat(value.split('-')[0]) && _search_item <= parseFloat(value.split('-')[1])) //range time match
							|| ( ['string','array'].indexOf($.type(_search_item))>-1 && _search_item.indexOf(value) > -1))
					}));
				}
				//filtered_items	
				draw_report_items(filtered_items)
			})
			.on("click", '.filter-exact', function () { 
				var filter_params = {}
				//get filter_params
				var selected_items = $(".select-filter").select2('data')//$(this).select2('data')
				for(var i=0;i<selected_items.length;i++) {
					var key = $(selected_items[i].element).data('key')
					filter_params[key] = $.isArray(filter_params[key]) ? filter_params[key] : []
					filter_params[key].push( $(selected_items[i].element).val() )
				}
				var filtered_items = _items.slice()
				var founded_exact = []
				$.each(filter_params, function(key, values) {
					//filter all by current key and store
					var current_founded_items = []
					$.each(values, function(i,value)
					{
						current_founded_items = current_founded_items.concat(filtered_items.filter(function(item) {
							var _search_item =  item.hasOwnProperty(key) ? item[key] : item.item.hasOwnProperty(key) ? item.item[key] : false
							if (_search_item === false) return _search_item
							return ((_search_item.hasOwnProperty('id') && _search_item['id'] === value) //id match
								|| ( !isNaN(parseFloat(value.split('-')[0])) && _search_item >= parseFloat(value.split('-')[0]) && _search_item <= parseFloat(value.split('-')[1])) //range time match
								|| ( ['string','array'].indexOf($.type(_search_item))>-1 && _search_item.indexOf(value) > -1))
						}));
					})
					filtered_items = current_founded_items
					founded_exact = founded_exact.concat(current_founded_items)
				});
				draw_report_items(filtered_items)
			})
			.on("click", '.cancel-approve-group', function() {
				send_approve_request($("a.cancel-approve").closest("tr"),'cancel-approve')
			})
			.on("click", '.approve-group', function() {
				send_approve_request($("a.approve").closest("tr"),'approve')
			});
});

	
</script>

<h3>Report {{report['pretty']}}</h3>

<div class="modal fade" id="report-modal"></div>

<div class="statistic">
	<ul class="list-group stat-group"></ul>
</div>

<!-- FILTER -->
<div class="form-group clearfix">
	<div class="col-sm-12">
		<div class="report-filter"></div>
		<!-- <div class="btn-group"></div> -->
	</div>
</div>
<!-- REPORT -->
<div class="report-content"></div>