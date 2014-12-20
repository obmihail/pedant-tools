stop_log_updating = function() {
	console.log( "TIMER STOPPED")
	clearInterval( update_interval_id )
	$(".start-project").removeAttr("disabled")
	$(".current-status").text('Stopped')
}

start_log_updating = function( url, interval ) {
	//global var - update_interval_id
	update_interval_id = setInterval( function() { update_launch_log(url); } , interval)
}

refresh_statistic = function() {
	$("span.total-count").text( $('tr.item').length );
	$("span.error-count").text( $('tr.error').length );
	$("span.selected-count").text( $('tr.selected').length );
}

prepare_approve_data = function( items, action )
{
	var json_data = []
	//collect data
	$.each(items, function(index) {
		json_data.push( 
		 	{ element_id: $(this).attr("id"), 
		 	  path: $(this).find("td.actions a").data( action + "-path") } 
		)
	});
	return json_data
}

update_launch_log = function( url ) {

	$('.current-status').fadeOut(1000);
	pedant_get_request( url , function(data) {
		$(".launch-info").val( data.msg );
		if ( 'Runned' != data.state )
		{
			stop_log_updating()
		}
	})
	$('.current-status').fadeIn(1000);
}

send_approve_request = function( data, action ){

	pedant_post_request( "/ajax/projects/image/"+action, data, function(data){ 
		console.log( data.items )
		draw_report_items( data.items, action )
	})
}

pedant_post_request = function( url, data, f_success, f_error ) {
	var jqxhr = $.post( url, JSON.stringify(data), function(data) {
		if ( data.status == 'OK' )
		{
			f_success(data)
		}
		else
		{
			if ( f_error != undefined )
			{
				f_error(data)
			}
			else
			{
				$(document).trigger("add-alerts", [
					{ 'message': data.msg, 'priority': 'error' }
				]);	
			}
		}
	}).fail(function(jqxhr, textStatus, error) {
		$(document).trigger("add-alerts", [
				{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
			]);
	},"json")
}

pedant_get_request = function( url, f_success, f_error ) {
	var jqxhr = $.get( url, function(data) {
		if ( data.status == 'OK' )
		{
			f_success( data )
		}
		else
		{
			if ( f_error != undefined )
			{
				f_error( data )
			}
			else
			{
				$(document).trigger("add-alerts", [
					{ 'message': data.msg, 'priority': 'warning' }
				]);
			}
		}
	}).fail(function(jqxhr, textStatus, error) {
		$(document).trigger("add-alerts", [
				{ 'message': "Server error: " + error + " . Status: " + textStatus, 'priority': 'error' }
			]);
	},"json")

}

set_browser_modal_values = function( modal, data ) {

	modal.find(".modal-title").text( data['title'] )
	modal.find("#browser-type").val( data['type'] );
	modal.find("#browser-unid").val( data['unid'] )
	modal.find("#wd-url").val( data['wd_url'] )
	modal.find("#window-w").val( data['window_size'][0] )
	modal.find("#window-h").val( data['window_size'][1] )
	modal.find("#browser-info").val( data['info'] )
	modal.find("#browser-caps").val( JSON.stringify(data['desired_capabilities']) )
}

get_browser_modal_values = function( modal ) {

	var data = { window_size: [] }
	data['type'] = modal.find("#browser-type").val();
	data['unid'] = modal.find("#browser-unid").val()
	data['wd_url'] = modal.find("#wd-url").val()
	data['window_size'][0] = modal.find("#window-w").val()
	data['window_size'][1] = modal.find("#window-h").val()
	data['info'] = modal.find("#browser-info").val()
	var caps = false
	try 
	{
		caps = JSON.parse( modal.find("#browser-caps").val() )
	}
	catch (exception) {
		console.error(exception)
		alert('DESIRED CAPABILITIES VALUE IS NOT VALID JSON STRING. See browser console for details')
	}
	data['desired_capabilities'] = caps
	return data

}

chunk_array = function(data,chunkSize) {
	var array=data;
	return [].concat.apply([],
		data.map(function(elem,i) {
			return i%chunkSize ? [] : [data.slice(i,i+chunkSize)];
		})
	);
}

delete_project = function( name ) {
	if ( confirm("Are you sure? This action remove all reports and all approved images for project " + name ) )
	{
		pedant_get_request( "/ajax/projects/remove/"+name, function(data){
			priority = 'success'

			var index = projects.map(function(prj) { return prj.name; }).indexOf( name ); //projects.indexOf( name );
			if ( index != -1 )
			{
				projects.splice(index, 1);
			}
			redraw_projects();
		})
	}
}

remove_approved_item = function( elem ) {
	pedant_get_request( $(elem).data("delete-url"), function(data) {
		priority = 'success'
		approved_items.splice( $(elem).closest("tr").attr("id"), 1);
		$(elem).closest("tr").remove();
	})
}

draw_report_items = function( items , action )
{
	if(typeof(action)==='undefined')
	{
		action = ''
	}

	var title = ( action === 'approve' ? "Cancel" : "Approve");
	var action_class = ( action === 'approve' ? "cancel-approve" : "approve");

	//if action is unknown - append items to table
	if ( action === '') {
		var html_data = _.template( $('#item-row-tpl').html(), 
			{ 	data: items, 
				action:{ class: action_class, title: title } } 
			)
		$('tbody.items').append( html_data )
	}
	//else update elements with concrette ids
	else
	{
		for(var key in items) {

			var item_row = $( "tr#"+items[key].element_id )
			var html_data = _.template( $('#item-row-tpl').html(), 
				{ 	data: [ items[key] ], 
					action:{ class: action_class, title: title } } 
				)				
			item_row.replaceWith( html_data )
		}
	}
	//lazy images
	$("img.lazy").lazyload({skip_invisible : false});
	//draw statistic 
	refresh_statistic()
}

redraw_report_items = function() {
	if ( window.items === undefined || $('tbody.items').length < 1 ) return
	//set elements ids
	for ( var i=0; i<items.length; i++ ) {
		items[i].element_id = i
	}
	//clear items table
	$('tbody.items').empty()
	var chunked = chunk_array(items,512)
	//append table rows
	for (var i=0; i<chunked.length; i++) {
		//set new items by data
		draw_report_items( chunked[i] )
	}
}

redraw_interface = function() {
	redraw_report_items()
	redraw_browsers_and_modes()
	redraw_projects()
	redraw_approved()
	redraw_custom_launch_tabs()
}

redraw_browsers_and_modes = function() {
	if ( $('#browsers-table tbody').length > 0 ){
		$('#browsers-table tbody').html(_.template( $('#browser-row-tpl').html(), { data: config.modes.full } ) )
	}
	if ( $('#modes-table tbody').length > 0 ) {	
		$('#modes-table tbody').html(_.template( $('#modes-row-tpl').html(), { data: config.modes } ) )
	}
}

redraw_projects = function() {
	if ( window.projects === undefined || $('#projects tbody').length < 1 ) return
	$('#projects tbody').html( _.template( $('#project-row-tpl').html(), { data: projects } ) )
}

redraw_approved = function() {
	if (window.approved_items === undefined || $('#approved-images tbody').length < 1 ) return
	$('#approved-images tbody').html( _.template( $('#approved-row-tpl').html(), { data: approved_items } ))
}

redraw_custom_launch_tabs = function() {
	if (window.config === undefined || $('#launch-custom-config').length < 1 ) return
	$('#launch-custom-config').html( _.template( $('#launch-custom-tab-tpl').html(), { data: custom_config } ))
}