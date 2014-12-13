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

		$(".delete-report").click(function() {
			var to_remove = $( this ).closest("tr")
			pedant_get_request( $(this).data("delete-url"), function(data){ to_remove.remove() } )
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
			//show preloader
			$("img.preloader").removeClass("hidden").addClass("show")
			$(this).addClass("hidden")
			//send ajax
			pedant_post_request("/ajax/projects/scan", {'path':input.val()}, function(data){
				$(document).trigger("add-alerts", [
					{ 'message': data.msg, 'priority': 'warning' }
				]);
				projects = data.projects
				redraw_interface()
				//hide preloader
				$(".scan_projects").removeClass("hidden")
				$("img.preloader").addClass("hidden").removeClass("show")
			},
			function( data ){
				//hide preloader
				$(".scan_projects").removeClass("hidden")
				$("img.preloader").addClass("hidden").removeClass("show")
				$(document).trigger("add-alerts", [
					{ 'message': data.msg, 'priority': 'error' }
				]);
			})
			
		});

		$('#editBrowserModal').on('show.bs.modal', function (event) {
			var unid = $(event.relatedTarget).data('unid')
			var modal = $(this)
			var data = false
			
			if ( unid === undefined )
			{
				//use default data
				data = default_browsers["FIREFOX"]
				data.title = "Add browser"
			}
			else
			{
				modal.data('unid',unid)
				//find data in full config

				$.each( config.modes.full, function( index, browser ) {
					if ( unid.toLowerCase() === browser.unid.toLowerCase() )
					{
						data = browser
						return
					}
					})
				if ( data === false )
				{
					console.error('Browser not exists ' + unid )
					return modal.modal('hide')
				}
				data.title = "Edit " + data['unid']
				
			}
			set_browser_modal_values( modal, data )
		})

		$('#editLMModal').on('show.bs.modal', function (event) {

			var unid = $(event.relatedTarget).data('unid')
			var modal = $(this)
			var data = { browsers: [], name: 'My_awesome_mode' }

			if ( unid === undefined )
			{
				//use default data
				data.title = "Add launch mode"
			}
			else
			{
				modal.data('unid', unid )
				//browsers for this mode
				$.each( config.modes[ unid ], function(index,browser) {
					data.browsers.push( browser.unid )
				});
				
				data.title = "Edit launch mode"
				data.name = unid
			}
			//draw checboxes
			modal.find(".browsers-for-mode").html( _.template( $('#browsers-for-mode-checkboxes-tpl').html(), { data: data } ) )
			modal.find(".modal-title").text( data.title )
			modal.find("#mode-name").val( data.name )
		})

		$('#deleteBrowserModal').on('show.bs.modal', function (event) {
			//var browser_config = JSON.parse( unescape( $(event.relatedTarget).closest("tr").data("config") ) )
			$(this).data('unid')
		})

		$('#deleteLMModal').on('show.bs.modal', function (event) {
			var name = $(event.relatedTarget).closest("tr").data('name')
			$(this).data('name', name )
		})

		$( document ).on("change", "#browser-type", function() {
			var modal = $(this).closest("#editBrowserModal")
			var data = default_browsers[ $( this ).val() ]
			set_browser_modal_values( modal, data )
		});

		//validate value by attrs 
		$( document ).on("change", "input[type='number']", function() {

			switch( true )
			{
				case isNaN( parseInt($(this).val()) ):
				return $(this).val( $(this).attr('max') )

				case ( parseInt($(this).val()) < parseInt($(this).attr('min')) ):
				return $(this).val( $(this).attr('min') )

				case ( parseInt($(this).val()) > parseInt($(this).attr('max')) ):
				return $(this).val( $(this).attr('max') )

				default:
				return $(this).val( parseInt($(this).val()) )
			}
		});

		$( document ).on("change", "input#prj_threads", function() {
			config.max_workers = parseInt($(this).val())
		});
		
		$( document ).on("change", "input#window-w", function() {
			var modal = $(this).closest("#editBrowserModal")
			var value = modal.find("#browser-type").val() + '_'+modal.find("#window-w").val()+'x'+modal.find("#window-h").val();
			modal.find("#browser-unid").val( value )
		});

		$( document ).on("change", "input#window-h", function() {
			var modal = $(this).closest("#editBrowserModal")
			var value = modal.find("#browser-type").val() + '_'+modal.find("#window-w").val()+'x'+modal.find("#window-h").val();
			modal.find("#browser-unid").val( value )
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
			redraw_interface()
			modal.modal('hide')
		});

		$(".save-browser").click(function() {
			var modal = $(this).closest("#editBrowserModal")
			var unid = modal.data('unid')
			var data = get_browser_modal_values( modal )

			if ( false === data.desired_capabilities ) return

			//if unid is empty - add new browser
			if ( unid === undefined )
			{
				var err = false 
				//check browser unid is unique
				pos = config.modes.full.map(function(browser) { return browser.unid.toLowerCase(); }).indexOf( data.unid.toLowerCase() );
				if ( pos != -1 ) return alert( "Browser with this unid already exists")
				config.modes.full.push( data )
			}
			//else update existing
			else
			{
				if ( data === false ) return
				//update browser in modes
				$.each( config.modes, function( modename, mode ) {
					$.each( mode, function( index, browser ) {
						if ( unid.toLowerCase() === browser.unid.toLowerCase() )
						{
							config.modes[modename][index] = data
						}
					})
				})
			}
			redraw_interface()
			modal.modal('hide')
		});
		
		$(".start-project").click(function() {
			var start_url = $(this).data('url')
			//prepare data
			//if selected tab - send custom config to launch
			if ( $("li.custom-mode.active").length > 0 )
			{
     			var custom_config = $.extend(true, {}, config );
     			custom_config.modes.full = [];
				var unids = [];
				$('.browsers-list input:checked').each( function() { unids.push(  $(this).val() ) });
     			//get only checked browsers
     			custom_config.modes.full = config.modes.full.filter( function(browser){  
     				return ( unids.indexOf( browser.unid ) != -1 )
     			})
     			if ( custom_config.modes.full.length < 1 )
     			{
     				$(document).trigger("add-alerts", [
						{ 'message': 'No browsers checked. Can not start', 'priority': 'error' }
					]);
					return
     			}

				var data = { mode: 'full', config: custom_config }
				data.config.urls = $("#prj_urls").val().split("\n")
			}
			else
			{
				//default - send selected config
				var data = { mode: $("#mode-choise option:selected").val(), config: false }
			}
			//block button
			$(this).attr('disabled','disabled')
			$(".current-status").text('Started')
			//else data = stored mode
			pedant_post_request( start_url, data, 
			function( data ){
				start_log_updating( data.state_url , 2000 )
			},
			function( data ){
				$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': 'error' }
				]);
				console.log(data)
				stop_log_updating()
			})
		})

		$(".stop-project").click(function() {
			//send ajax for stoppin and wait answer
			alert( "STOP operation is not fast, wait correct stopping")
			$(this).attr('disabled','disabled')
			var stop_url = $(this).data('url')
			//send ajax for stopping
			pedant_get_request( stop_url, function(data){ stop_log_updating() } )
			$(this).removeAttr('disabled')
		})

		$(".save-mode").click(function() {
			var modal = $(this).closest("#editLMModal")
			var name = modal.find("#mode-name").val()
			var unid = modal.data('unid')
			var checked_browsers_unids = []
			var browsers_for_mode = []
			
			$( ".browsers-for-mode input:checked" ).each(function( index ) {
				checked_browsers_unids.push( $(this).val() )
			});

			browsers_for_mode = config.modes.full.filter( function(browser){ return checked_browsers_unids.indexOf( browser.unid ) != -1 } )
			//check fields values
			if ( name.length < 1 ) return alert( 'MODE NAME IS REQUIRED')
			if ( checked_browsers_unids.length < 1 ) return alert( 'CHECK ONE OR MORE BROWSERS' )

			if ( unid === undefined )
			{
				//check unid is unique
				if ( typeof config.modes[ name ] !== 'undefined' ) return alert( 'MODE WITH NAME ALREADY EXISTS')
			}
			else
			{
				//update mode name
				if ( name.toLowerCase() != unid.toLowerCase() )
				{
					//check unique new name
					if ( typeof config.modes[ name ] !== 'undefined' ) return alert( 'MODE WITH NAME ALREADY EXISTS')
					//remove mode with old name
					delete config.modes[ unid ]
				}	
			}

			if ( name.toLowerCase() === 'full' ) return alert( "Can not change full mode")
			config.modes[ name ] = browsers_for_mode

			redraw_interface()
			modal.modal('hide')
		});

		$(".delete-mode").click(function() {
			//delete mode from config and redraw
			var modal = $(this).closest("#deleteLMModal")
			var name = modal.data('name')
			delete config.modes[ name ]
			redraw_interface()
			modal.modal('hide')
		});
		

		$(".btn-create-prj").click(function() {

			if ( $("#prj_urls").length > 0 ) config['urls'] = $("#prj_urls").val().split("\n")
			else config['without_urls'] = true
			
			config['url_mask'] = $("#static_mask").val()
			var url = $(this).data('url')
			//rename if project renaming
			current_prj_name = $("#prj_name").val()
			if ( current_prj_name != config['prj_name'] )
			{
				config['oldName'] = config['prj_name']
			}
			config['prj_name'] = current_prj_name

			pedant_post_request( url, config, function( data ) {
				if ( data.url !== undefined )
				{
					alert(data.msg)
					document.location.href = data.url;	
				}
			})
		});

		redraw_interface();

	});
