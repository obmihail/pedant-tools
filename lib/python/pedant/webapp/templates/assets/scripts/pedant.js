$(document).ready(function() {
		$(".fancybox").fancybox();

		$(function() {
    		$("img.lazy").lazyload({skip_invisible : false});
		});

		$("table.items-table").on('click', 'a.approve-action',function () {
			if ( $( this ).is( ".cancel-approve" ) ) {
				send_approve_request( prepare_approve_data( $( this ).closest("tr"), "cancel-approve") , "cancel-approve" )
			}
			else {
				send_approve_request( prepare_approve_data( $( this ).closest("tr"), "approve") , "approve" )
			}
		});
		
		$(".toggle-all").click(function() {
				if ( $( this ).is( ".select" ) ) {
					$(".items-table tr.item").addClass("selected")
					$( this ).removeClass( "select" ).addClass("unselect");
					$( this ).text('Unselect all')
				} 
				else {
					$(".items-table tr.item").removeClass("selected")
					$( this ).removeClass( "unselect" ).addClass("select");
					$( this ).text('Select all')
				}
				refresh_statistic()
		});

		$(".toggle-not-approved").click(function() {
				if ( $( this ).is( ".select" ) ) {
					$(".items-table td.approved i.status-approve404").closest("tr").addClass("selected")
					$( this ).removeClass( "select" ).addClass("unselect");
					$( this ).text('Unselect not approved')
				} 
				else {
					$(".items-table td.approved i.status-approve404").closest("tr").removeClass("selected")
					$( this ).removeClass( "unselect" ).addClass("select");
					$( this ).text('Select not approved')
				}
				refresh_statistic()
		});

		$(".toggle-diffs").click(function() {
				if ( $( this ).is( ".select" ) ) {
					$(".items-table td.diff a.status-diff").closest("tr").addClass("selected")
					$( this ).removeClass( "select" ).addClass("unselect");
					$( this ).text('Unselect all diffs')
				} 
				else {
					$(".items-table td.diff a.status-diff").closest("tr").removeClass("selected")
					$( this ).removeClass( "unselect" ).addClass("select");
					$( this ).text('Select all diffs')
				}
				refresh_statistic()
		});
		
		$(".approve-disapprove-selected").click(function() {
				if ( $( this ).is( ".approve-selected" ) ) {
					send_approve_request( prepare_approve_data($(".items-table tr.selected") , "approve") , "approve" )
					$( this ).removeClass( "approve-selected" ).addClass("cancel-selected");
					$( this ).text('Cancel approve selected')
				} 
				else {
					send_approve_request( prepare_approve_data($(".items-table tr.selected") , "cancel-approve") , "cancel-approve" )
					$( this ).removeClass( "cancel-selected" ).addClass("approve-selected");
					$( this ).text('Approve selected')
				}
				refresh_statistic()
		});

		$(".delete-item").click(function() {
			var to_remove = $( this ).closest("tr")
			var jqxhr = $.getJSON( $(this).data("delete-url"), function(data) {
				if ( data.status == 'OK' )
				{
					//drop report tr
					to_remove.remove()
					return
				}
				//not ok
				$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': 'warning' }
					]);
			}).fail(function(jqxhr, textStatus, error) {
				$(document).trigger("add-alerts", [
						{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
					]);
			})
		});

		$(".required-input").change(function() {
			if ( $(this).find("input").val().length > 0 )
			{
				$(this).removeClass("has-error")
				return
			}
			$(this).addClass("has-error")
		});


		$(".scan_projects").click(function() {
			var input = $("#dir_path")
			if ( input.val().length < 1 )
			{
				input.closest(".form-group").addClass("has-error")
				return
			}
			$("img.preloader").removeClass("hidden").addClass("show")
			$(this).addClass("hidden")
			//send ajax
			var jqxhr = $.post("/ajax/projects/scan", JSON.stringify({'path':input.val()}), function(data) {
				var priority = 'warning'
				$(".scan_projects").removeClass("hidden")
				$("img.preloader").addClass("hidden").removeClass("show")
				if (data.status === 'OK')
				{
					projects = data.projects
					redraw_projects()
				}
				else
				{
					$(document).trigger("add-alerts", [
							{ 'message': data.msg, 'priority': priority }
						]);
				}
			}).fail(function(jqxhr, textStatus, error) {
				$(".scan_projects").removeClass("hidden")
				$("img.preloader").addClass("hidden").removeClass("show")
				$(document).trigger("add-alerts", [
						{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
					]);
			})
			
		});

		$('#editBrowserModal').on('show.bs.modal', function (event) {
			var initiator = $(event.relatedTarget)
			var mode = initiator.data('mode')
			var modal = $(this)
			var data = {}

			if ( mode != "edit" )
			{
				//use default data
				data = default_browsers["FIREFOX"]
				data.title = "Add browser"
				modal.data('mode','add')
				modal.find("#browser-type").removeAttr('disabled')
				modal.find("#browser-unid").removeAttr('disabled')
			}
			else
			{
				var data_str = unescape( initiator.closest(".browser-row").data('config') )
				data = JSON.parse( data_str )
				data.title = "Edit " + data['unid']
				modal.data('mode','update')
				//disable select when browser is edit
				modal.find("#browser-type").attr('disabled', 'disabled')
				modal.find("#browser-unid").attr('disabled', 'disabled')
			}
			set_browser_modal_values( modal, data )
			//call save function
		})

		$('#editLMModal').on('show.bs.modal', function (event) {
			var initiator = $(event.relatedTarget)
			var modal = $(this)
			var mode = initiator.data('mode')
			var data = { browsers: [], name: 'My_awesome_mode' }
			modal.data('mode',mode)
			if ( mode != "edit" )
			{
				//use default data
				data.title = "Add launch mode"
				modal.find("#mode-name").removeAttr( 'disabled', 'disabled' )
			}
			else
			{
				//browsers array
				$.each( JSON.parse( unescape( initiator.closest("tr").data("config") ) ), function(index,browser) {
					data.browsers.push( browser.unid )
				});
				
				data.title = "Edit launch mode"
				data.name = initiator.closest("tr").find("td").first().text()
				modal.find("#mode-name").attr( 'disabled', 'disabled' )
				//disable select when browser is edit
			}
			//draw checboxes
			modal.find(".browsers-for-mode").html( _.template( $('#browsers-for-mode-checkboxes-tpl').html(), { data: data } ) )
			modal.find(".modal-title").text( data.title )
			modal.find("#mode-name").val( data.name )
		})

		$('#deleteBrowserModal').on('show.bs.modal', function (event) {
			var browser_config = JSON.parse( unescape( $(event.relatedTarget).closest("tr").data("config") ) )
			console.log(browser_config)
			$(this).data('unid', browser_config.unid )  
		})

		$('#deleteLMModal').on('show.bs.modal', function (event) {
			var name = $(event.relatedTarget).closest("tr").data('name')
			$(this).data('name', name )
		})
		

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
			}
			data['desired_capabilities'] = caps
			return data

		}

		$( document ).on("change", "#browser-type", function() {
			var modal = $(this).closest("#editBrowserModal")
			var data = default_browsers[ $( this ).val() ]
			set_browser_modal_values( modal, data )
		});

		$(".delete-browser").click(function() {
			//delete browser from all modes in config and redraw()
			var modal = $(this).closest("#deleteBrowserModal") 
			var unid = modal.data('unid')
			//$.each( config.modes, function( modename, mode ) {
			for(var modename in config.modes ) {
				for(var i = 0; i < config.modes[modename].length; i++) {
					if ( unid.toLowerCase() === config.modes[modename][i].unid.toLowerCase() )
					{
						config.modes[ modename ].splice( i , 1 )
					}
				}
				if ( config.modes[modename].length < 1 && 'full' != modename )
				{
					delete config.modes[modename]
				}
			//})
			}
			redraw()
			modal.modal('hide')
		});

		$(".test-browser").click(function() {
			//send config to server for testing
			//show results
		});

		$(".save-browser").click(function() {
			var modal = $(this).closest("#editBrowserModal")
			var mode = modal.data('mode')
			var data = get_browser_modal_values( modal )
			if ( false === data.desired_capabilities )
			{
				return alert('DESIRED CAPABILITIES VALUE IS NOT VALID JSON STRING. See console for details')
			}
			//if mode === add then add new browser
			if ( 'add' === mode )
			{
				var err = false 
				$.each( config.modes.full, function( index, browser ) {
					if ( data.unid.toLowerCase() === browser.unid.toLowerCase() )
					{
						err = true
					}
				});
				if ( err ) return alert( "Browser with this unid already exists")
				config.modes.full.push( data )
			}
			else
			{
				if ( data === false ) return 
				$.each( config.modes, function( modename, mode ) {
					$.each( mode, function( index, browser ) {
						if ( data.unid.toLowerCase() === browser.unid.toLowerCase() )
						{
							config.modes[modename][index] = data
						}
					})
				})
			}
			redraw()
			modal.modal('hide')
		});
		
		$(".start-project").click(function() {
			//block button
			$(this).attr('disabled','disabled')
			var start_url = $(this).data('url')
			$(".current-status").text('Started')
			//send ajax for start
			//var state_url = false
			//url = '/ajax/projects/'+ config['prj_name'] + '/log/' + timestamp
			var jqxhr = $.post( start_url, JSON.stringify({ mode: $("#mode-choise option:selected").val() }), function(data) {
				if ( data.status == 'OK' )
				{
					//global var - state url
					state_url = data.state_url
					//global var - update_interval_id
					update_interval_id = setInterval( update_launch_log , 2000)
				}
				else
				{
					$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': 'warning' }
					]);
					stop_updating()
				}

				}).fail(function(jqxhr, textStatus, error) {
					$(document).trigger("add-alerts", [
							{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
						]);
				},"json")
			//create timer, who will send ajax and update info every 5 sec
		})

		update_launch_log = function()
		{
			$('.current-status').fadeOut(1000);
			var jqxhr = $.get( state_url, function(data) {
						if ( data.status == 'OK' )
						{
							//update launch info
							$(".launch-info").val( data.msg );
							if ( 'Runned' != data.state )
							{
								stop_updating()
							}
						}
						else
						{
							$(document).trigger("add-alerts", [
								{ 'message': data.msg, 'priority': 'warning' }
							]);
							stop_updating()
						}

						}).fail(function(jqxhr, textStatus, error) {
							stop_updating()
							$(document).trigger("add-alerts", [
									{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
								]);
						},"json")
			$('.current-status').fadeIn(1000);
		}

		stop_updating = function()
		{
			//console.log( "TIMER STOPPED")
			clearInterval( update_interval_id )
			$(".start-project").removeAttr("disabled")
			$(".current-status").text('Stopped')
		}

		$(".stop-project").click(function() {
			//send ajax for stoppin and wait answer
			alert( "STOP operation is not fast, wait correct stopping")
			$(this).attr('disabled','disabled')
			var stop_url = $(this).data('url')
			//send ajax for stopping
			var jqxhr = $.get( stop_url, function(data) {
				if ( data.status == 'OK' )
				{
					//global var - update_interval_id
					stop_updating()
				}
				else
				{
					$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': 'warning' }
					]);
				}

				}).fail(function(jqxhr, textStatus, error) {
					$(document).trigger("add-alerts", [
							{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
						]);
				},"json")
			$(this).removeAttr('disabled')
		})

		$(".save-mode").click(function() {
			var modal = $(this).closest("#editLMModal")
			var name = modal.find("#mode-name").val()
			var mode = modal.data("mode")
			var unids = []
			var browsers = []
			$( ".browsers-for-mode input:checked" ).each(function( index ) {
				// console.log( $(this).val() )
				unids.push( $(this).val() )
			});
			$.each( config.modes.full, function( index, browser ) {
				if ( unids.indexOf( browser.unid ) > -1 )
				{
					browsers.push( browser )
				}
			});
			if ( 'add' === mode )
			{
				if ( typeof config.modes[ name ] !== 'undefined' ) return alert( 'MODE WITH NAME ALREADY EXISTS')
			}
			if ( name.length < 1 ) return alert( 'MODE NAME IS REQUIRED')
			if ( browsers.length < 1 ) return alert( 'CHECK ONE OR MORE BROWSERS' )
			// console.log(browsers)
			config.modes[ name ] = browsers
			redraw()
			modal.modal('hide')
		});

		$(".delete-mode").click(function() {
			//delete mode from config and redraw
			var modal = $(this).closest("#deleteLMModal")
			var name = modal.data('name')
			delete config.modes[ name ]
			redraw()
			modal.modal('hide')
		});

		$(".btn-create-prj").click(function() {

			config['urls'] = $("#prj_urls").val().split("\n")
			var url = $(this).data('url')
			// console.log(config)
			
			current_prj_name = $("#prj_name").val()
			if ( current_prj_name != config['prj_name'] )
			{
				config['oldName'] = config['prj_name']
			}
			config['prj_name'] = current_prj_name

			var jqxhr = $.post( url, JSON.stringify(config), function(data) {
				var priority = 'warning'
				if ( data.status == 'OK' )
				{
					priority = 'success'
					if ( data.url !== undefined )
					{
						alert(data.msg)
						document.location.href = data.url;	
					}
				}

				$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': priority }
					]);
			}).fail(function(jqxhr, textStatus, error) {
				$(document).trigger("add-alerts", [
						{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
					]);
			},"json")

		});

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

		send_approve_request = function( data, action ){
			var jqxhr = $.post("/ajax/projects/image/"+action, JSON.stringify(data), function(data) {
				var priority = 'warning'
				if ( data.status == 'OK' )
				{
					priority = 'success'
					draw_report_items( data.items, action )
				}
			}).fail(function(jqxhr, textStatus, error) {
				$(document).trigger("add-alerts", [
						{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
					]);
			},"json")
			
		}

		draw_report_items = function( items , action )
		{
			if(typeof(action)==='undefined')
			{
				action = ''
			}

			var title = ( action === 'approve' ? "Cancel" : "Approve");
			var action_class = ( action === 'approve' ? "cancel-approve" : "approve");

			
			//if action is unknown - append items in table
			if ( action === '') {
				var html_data = _.template( $('#item-row-tpl').html(), 
					{ 	data: items, 
						action:{ class: action_class, title: title } } 
					)
				$('tbody.items').append( html_data )
			}
			//else update elements with ids
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
			$("img.lazy").lazyload({skip_invisible : false});
			refresh_statistic()
		}

		redraw_browsers_and_modes = function() {
			if ( $('#browsers-table tbody').length > 0 ){
				$('#browsers-table tbody').html(_.template( $('#browser-row-tpl').html(), { data: config.modes.full } ) )
			}
			if ( $('#modes-table tbody').length > 0 ) {	
				$('#modes-table tbody').html(_.template( $('#modes-row-tpl').html(), { data: config.modes } ) )
			}
		}

		chunk_array = function(data,chunkSize) {
			var array=data;
			return [].concat.apply([],
				data.map(function(elem,i) {
					return i%chunkSize ? [] : [data.slice(i,i+chunkSize)];
				})
			);
		}

		redraw_report_items = function() {

			if ( window.items === undefined ) return

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

		redraw_projects = function() {

			if ( window.projects === undefined ) return
			//set elements ids
			$('#projects tbody').html( _.template( $('#project-row-tpl').html(), { data: projects } ) )
		}

		delete_project = function( name ) {
			if ( confirm("Are you sure? This action remove all reports and all approved images for project " + name ) )
			{
				var jqxhr = $.get("/ajax/projects/remove/"+name, function(data) {
				var priority = 'warning'
				if ( data.status == 'OK' )
				{
					priority = 'success'
					var index = projects.indexOf( name );
					projects.splice(index, 1);
					redraw_projects();
				}
				}).fail(function(jqxhr, textStatus, error) {
					$(document).trigger("add-alerts", [
							{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
						]);
				},"json")
			}
		}

		redraw_browsers_and_modes();
		redraw_report_items();
		redraw_projects();
		
	});
