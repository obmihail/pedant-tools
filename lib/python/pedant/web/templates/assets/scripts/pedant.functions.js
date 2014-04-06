update_launch_info = function(url) {
	$('.current-status').fadeOut(1000);
	pedant_get_request( url , function(data) {
		//set log
		$(".launch-info").val(data.log);
		$(".progress-bar").addClass("active")
		//calc progress bar percents
		console.log(data)
		var percent = ( data.stat.SKIPPED.length + data.stat.FAILED.length + data.stat.PASSED.length ) * 100 / data.stat.TOTAL.length
		//check status
		if ( 'FINISHED' == data._status )
		{
			percent = 100
			$(".progress-bar").removeClass("active")
			//stop_log_updating()
			clearInterval( window.update_interval_id )
			$(".start-project").removeAttr("disabled")
			$(".current-status").text('FINISHED')
		}
		$(".progress-bar").width( parseInt(percent, 10).toString()+'%');
		//set stat
		var stat = {}
		for (key in data.stat) { stat[key] = data.stat[key].length }
		$(".launch-statistic").html(_.template( $('#small-stat-tpl').html(), { 'stat': stat } ))
	}, function(data){
		$(document).trigger("add-alerts", [
			{ 'message': data.msg, 'priority': 'error' }
		]);
		clearInterval( window.update_interval_id )
		$(".start-project").removeAttr("disabled")
		$(".current-status").text('ERROR')
	})
	$('.current-status').fadeIn(1000);
}

send_approve_request = function(selector, action){
	var approve_items = []
	//collect data
	$.each(selector, function(index) {
		approve_items.push({ 
			item_id: $(this).find("td.actions a").data('item-id'),
			state_id: $(this).find("td.actions a").data('state-id'),
			browser_id: $(this).find("td.actions a").data('browser-id'),
			})
	})

	pedant_post_request( "/api/projects/"+project+"/screens/reports/"+report['timestamp']+"/"+action, {'items':approve_items}, 
		function(data){
			//parse data
			$.each(data.items, function(index,itemdata) {
				if (itemdata.status != 'OK') {
					//show error
					show_error("Error in ".concat(action).concat(": ").concat(itemdata.msg))
				}
				else {
					var id = itemdata.result.item.id.concat('-').concat(itemdata.result.browser.id).concat('-').concat(itemdata.result.state.id)
					var element_index = $("tr#".concat(id)).children('.item-index').text().trim()
					var html = _.template( $('#report-item-tpl').html(), 
						{data: [itemdata.result], action: action, element_index: element_index})
					var element = $("tr#".concat(id))
					element.replaceWith(html)
				}
			})
			$("img.lazy").lazyload({skip_invisible : true});
		})
}

ajax_request = function(params) {
	var defaults = {
		type: 'GET',
		url: '/',
		success: (function(data){}),
	}
	$.ajax($.extend(true,defaults,params))
		.fail(function(jqxhr, textStatus, error) {
			$(document).trigger(
				"add-alerts", [
					{ 'message': "Server error: " + jqxhr.responseText + " . Status: " + textStatus,
				'priority': 'error' }]
				)})
}

pedant_post_request = function( url, send_data, f_success, f_error, async_val ) {
	var async_val = (typeof async_val != 'undefined')?async_val:true
	var f_success = (typeof f_success != 'undefined' && f_success)?f_success:function(data){}
	var f_error = (typeof f_error != 'undefined' && f_error)?f_error:function(data){$(document).trigger("add-alerts", [{ 'message': data.msg, 'priority': 'error' }])}
	var request_params = {
		type: 'POST',
		url: url,
		data: JSON.stringify(send_data),
		success: ( function(data) { f_success(data) }),
		dataType: 'json',
		async: async_val
	}
	ajax_request(request_params)
}

pedant_get_request = function( url, f_success, f_error, async_val ) {

	var async_val = (typeof async_val != 'undefined')?async_val:true
	var f_success = (typeof f_success != 'undefined' && f_success)?f_success:function(data){}
	var f_error = (typeof f_error != 'undefined' && f_error)?f_error:function(data){$(document).trigger("add-alerts", [{ 'message': data.msg, 'priority': 'error' }])}
	var request_params = {
		url: url,
		success: (function(data){ f_success(data)}),
		async: async_val
	}
	ajax_request(request_params)
}

chunk_array = function(data,chunkSize) {
	var array=data;
	return [].concat.apply([],
		data.map(function(elem,i) {
			return i%chunkSize ? [] : [data.slice(i,i+chunkSize)];
		})
	);
}

show_error = function(text) {
	$(document).trigger( 
		"add-alerts", 
		[{ 'message': text, 'priority': 'error' }])
}

draw_report_items = function(items, action) {
	$('div.report-content').html( _.template($('#report-items-tpl').html(), {data: items}) )
	//lazy images
	$("img.lazy").lazyload({skip_invisible : true});
}

redraw_report_items = function() {
	//load items
	pedant_get_request("/api/projects/"+project+"/screens/reports/"+report['timestamp'],function(data){
		_items = data.items
		$('div.report-content').empty()
		// var chunked = chunk_array(_items,512)redraw_re
		// if (chunked.length < 1)
		// {
		// 	draw_report_items(chunked)
		// }
		// for (var i=0; i<chunked.length; i++) {
		// 	//set new items by data
		// 	draw_report_items(chunked[i])
		// }
		$('div.report-content').html( _.template($('#report-items-tpl').html(), {data: _items}) )
		$("img.lazy").lazyload();
		redraw_filter()
		//set stat
		$(".stat-group").empty()
		var stat = {'total':0}
		_items.reduce( function(stat,item){ stat.total++;stat[item.status] = stat.hasOwnProperty(item.status)?stat[item.status]+1:1; return stat }, stat )
		$.each(stat, function(key, value) {
			$(".stat-group").append(
				$('<li class="list-group-item stat-'+key.toLowerCase()+'"></li>')
					.text(key.toUpperCase())
					.append( $('<span class="total-count badge"></span>').text(value))
			)
		});
	});
}

load_bdd_report = function(functions) {
	pedant_get_request("/api/projects/"+project+"/bdd/reports/"+report['timestamp'],function(data){
		functions.forEach(function(f){
			f(data.items)
		})
	});
}

get_scenario_stat = function(scenario) {
	var stat = { total: 0 }
	scenario.steps.reduce(function(prev, step) {
		stat.total = stat.total + 1
		var status = (step.result) ? step.result.status : 'untested';
		stat[status] = ( stat.hasOwnProperty(status) ? stat[status]+1:1); 
	}, 0);
	return stat
}

draw_stat = function(stat) {
	$(".stat-group").empty()
	$.each(stat, function(key, value) {
		$(".stat-group").append(
			$('<li class="list-group-item stat-'+key.toLowerCase()+'"></li>')
				.text(key.toUpperCase())
				.append( $('<span class="total-count badge"></span>').text(value))
		)
	});	
}

redraw_filter = function() {
	filter_params = {'status':[], 'browser':[], 'state':[], 'exceptions':[], 'comparison_result':[]}
	_items.forEach(function(item, i, arr) {
		for(var key in item) {
			if (!filter_params.hasOwnProperty(key))
			{
				continue;
			}
			if ( item[key] instanceof Array ) 
			{
				filter_params[key] = filter_params[key].concat(item[key])
			}
			else if (item[key].hasOwnProperty('id'))
			{
				filter_params[key].push(item[key].id)
			}
			else
			{
				filter_params[key].push(item[key])
			}
			filter_params[key] = _.uniq(filter_params[key])
		}
	});
	//make range of items load_time
	filter_params["load_time"] = _.uniq(_items
		.map(function(item) { 
			return item.item.load_time 
		}))
		.sort()
		//stay six ranges of load_time values
		.filter(function(time,index,load_times){
			return (!(index > 0 && index < load_times.length-1 && load_times.length-5 < index))
		})
		//make strings of range load_time: [ min1-max1, min2-max2, min3-max3 ]
		.map(function(time,i,ranges){
			return time+'-'+ranges[i+1]
		})
		//remove garbage
		.filter(function(time){ return (time.indexOf('undefined')<0) })

	//console.log(filter_params)
	$('div.report-filter').html( _.template($('#items-filter-tpl').html(), {data: filter_params}) )
	$('select').select2()
}

load_project_config = function(post_load_function) {
	var url = "/api/examples/configuration"
	var states_url = "/api/examples/screens/states"
	if (project.length > 0)
	{
		url = "/api/projects/"+project
		states_url = "/api/projects/"+project+"/screens/states"
	}
	//set default browsers to modal select
	pedant_get_request("/api/examples/browsers",function(data){
		default_browsers = data.browsers
		//add types to modal
		$.each(default_browsers, function(key, value) {   
			$('#browser-type')
				.append($("<option></option>")
				.attr("value",key)
				.text(key));
		});
	});
	pedant_get_request(url,function(data){
		//set global config
		window.config = data.config
		//window.urls = data.urls
		//load states
		pedant_get_request(states_url,function(data){ window.states = data.states},false,false)
		post_load_function(data)
	});
}