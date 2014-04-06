$(document).ready(function() {
		$(".fancybox").fancybox();

		$(".required-input").change(function() {
			if ( $(this).find("input").val().length > 0 )
			{
				$(this).removeClass("has-error")
				return
			}
			$(this).addClass("has-error")
		});

		$('#edit_browser_modal').on('show.bs.modal', function (event) {
			if ( $(event.relatedTarget).closest("tr").length ) {
				var id = $(event.relatedTarget).closest("tr").data('id')
			}
			else
			{
				var id = $(event.relatedTarget).data('id')	
			}
			var modal = $(this)
			var data = false
			
			if ( id === undefined )
			{
				//use default data
				data = default_browsers["FIREFOX"]
				data.title = "Add browser"
			}
			else
			{
				modal.data('id',id)
				//find data in default config mode
				$.each( config.browsers, function( index, browser ) {
					if ( id.toLowerCase() === browser.id.toLowerCase() )
					{
						data = browser
						return
					}
					})
				if ( data === false )
				{
					console.error('Browser not exists ' + id )
					return modal.modal('hide')
				}
				data.title = "Edit " + data['id']
				
			}
			modal.find(".modal-title").text( data['title'] )
			modal.find("#browser-type").val( data['type'] );
			modal.find("#browser-id").val( data['id'] )
			modal.find("#wd-url").val( data['wd_url'] )
			modal.find("#window-w").val( data['window_size'][0] )
			modal.find("#window-h").val( data['window_size'][1] )
			modal.find("#browser-description").val( data['description'] )
			modal.find("#browser-caps").val( JSON.stringify(data['desired_capabilities']) )
		})

		$('#edit_launch_mode_modal').on('show.bs.modal', function (event) {

			var name = $(event.relatedTarget).closest("tr").data('name')
			var mode_browsers = []
			var mode_states = []
			if ( name === undefined )
			{
				//use default data
				$(this).find(".modal-title").text("Add launch mode")
				$(this).find("#mode-name").val('awesome_mode')
				mode_browsers = config.browsers
				mode_states = states
			}
			else
			{
				$(this).data('oldname', name)
				$(this).find("#mode-name").val(name)
				//browsers for this mode
				mode_browsers = config.browsers.filter(function(browser){ return config.modes[name]['browsers'].indexOf(browser.id) != -1 })
				//states for this mode
				mode_states = states.filter(function(state){ return config.modes[name]['states'].indexOf(state.id) != -1 })
				$(this).find(".modal-title").text("Edit mode "+name)
			}
			//draw all browsers checks
			var html = _.template($('#browsers-checks-tpl').html(), { browsers: config.browsers, without_controls: true })
			$(this).find(".browsers-for-mode").html(html)
			//uncheck all browsers
			$(this).find("input.browser").prop("checked",false)
			//check needle browsers
			modal = $(this)
			mode_browsers.forEach(function(browser) { modal.find("input[value='"+browser.id+"']").prop("checked",true) });
			//draw all states checks
			var html = _.template($('#states-checks-tpl').html(), { states: states })
			$(this).find(".states-for-mode").html(html)
			//uncheck all states
			$(this).find("input.state").prop("checked",false)
			mode_states.forEach(function(state) { modal.find("input[value='"+state.id+"']").prop("checked",true) });
		})

		$('#delete_browser_modal').on('show.bs.modal', function (event) {
			var id = $(event.relatedTarget).closest("tr").data("id")
			$(this).data('id', id)
		})

		$('#delete_launch_mode_modal').on('show.bs.modal', function (event) {
			var name = $(event.relatedTarget).closest("tr").data('name')
			$(this).data('name', name)
		})

		$( document )
		.on("change", "#browser-type", function() {
			var modal = $(this).closest("#edit_browser_modal")
			var data = default_browsers[ $( this ).val() ]
			modal.find(".modal-title").text( data['title'] )
			modal.find("#browser-type").val( data['type'] );
			modal.find("#browser-id").val( data['id'] )
			modal.find("#wd-url").val( data['wd_url'] )
			modal.find("#window-w").val( data['window_size'][0] )
			modal.find("#window-h").val( data['window_size'][1] )
			modal.find("#browser-description").val( data['description'] )
			modal.find("#browser-caps").val( JSON.stringify(data['desired_capabilities']) )
		}).on("change", "input[type='number']", function() {
			switch(true)
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
		}).on("change", "input#threads", function() {
			config.threads = parseInt($(this).val())
		}).on("change", ".diffs-checkbox", function() {
			config.diffs_saving = this.checked
		}).on("change", "input#window-w", function() {
			var modal = $(this).closest("#edit_browser_modal")
			var value = modal.find("#browser-type").val() + '_'+modal.find("#window-w").val()+'x'+modal.find("#window-h").val();
			modal.find("#browser-id").val(value)
		}).on("change", "input#window-h", function() {
			var modal = $(this).closest("#edit_browser_modal")
			var value = modal.find("#browser-type").val() + '_'+modal.find("#window-w").val()+'x'+modal.find("#window-h").val();
			modal.find("#browser-id").val( value )
		}).on('click', '.feature-toggle',(function() {
			$(this).closest('.panel.feature').find('div.panel-body').toggle();
		}))
		.on('click', '.scenario-toggle',(function() {
			$(this).closest('div.panel').find('div.scenario-body').toggle();
		}))
		.on('click', '.step-toggle',(function() {
			$(this).closest('div.panel').find('div.panel-body').toggle();
		}))
		$(".delete-browser").click(function() {
			//delete browser from all modes in config and redraw()
			var modal = $(this).closest("#delete_browser_modal")
			var id = modal.data('id')
			//$.each( config.modes, function( modename, mode ) {
			//delete from config
			config.browsers = config.browsers.filter(function(browser){ return ( browser.id != id ) })
			//delete from modes
			for(var modename in config.modes ) {
				config.modes[modename].browsers = config.modes[modename].browsers.filter(function(browser){ return (browser != id) })
			}
			//redraw forms 
			$('.launch-form .browsers').html( _.template( $('#browsers-tpl').html(), { browsers: config.browsers } ) )
			$('.launch-form .modes').html( _.template( $('#modes-tpl').html(), { modes: config.modes } ))
			//
			$('#browsers-table').html(_.template( $('#browser-table-tpl').html(), { browsers: config.browsers } ) )
			//
			$('#modes-table').html(_.template( $('#modes-table-tpl').html(), { modes: config.modes } ) )
			modal.modal('hide')
		});
		$(".save-browser").click(function() {
			var modal = $(this).closest("#edit_browser_modal")
			var old_id = modal.data('id')
			var data = { 'window_size':[], 'desired_capabilities':false }
			data['type'] = modal.find("#browser-type").val();
			data['id'] = modal.find("#browser-id").val()
			data['wd_url'] = modal.find("#wd-url").val()
			data['window_size'][0] = modal.find("#window-w").val()
			data['window_size'][1] = modal.find("#window-h").val()
			data['description'] = modal.find("#browser-description").val()
			try
			{
				data['desired_capabilities'] = JSON.parse( modal.find("#browser-caps").val() )
			}
			catch (exception) {
				console.error(exception)
				return alert('DESIRED CAPABILITIES VALUE IS NOT VALID JSON STRING. See browser console for details')
			}
			//if id is empty - add new browser
			if ( old_id === undefined )
			{
				var err = false 
				//check browser id is unique
				pos = config.browsers.map(function(browser) { return browser.id.toLowerCase(); }).indexOf( data.id.toLowerCase() );
				if ( pos > -1 ) return alert( "Browser with this id already exists")
				config.browsers.push(data)
			}
			//else update existing
			else
			{
				//update in config
				$.each(config.browsers, function(i,browser){ if (browser.id === old_id) { config.browsers[i] = data } });
				//update in modes
				$.each(config.modes, function( modename, mode ) {
					$.each( mode.browsers, function( index, browser ) {
						if ( old_id.toLowerCase() === browser.toLowerCase() )
						{
							config.modes[modename].browsers[index] = data.id
						}
					})
				})
			}

			//expanded block
			$('.browsers-list').html( _.template( $('#browsers-checks-tpl').html(), { browsers: config.browsers } ) )
			//table
			$('#browsers-table').html(_.template( $('#browser-table-tpl').html(), { browsers: config.browsers } ) )
			//
			$('#modes-table').html(_.template( $('#modes-table-tpl').html(), { modes: config.modes } ) )
			modal.modal('hide')
		});

		$(".save-mode").click(function() {
			var modal = $(this).closest("#edit_launch_mode_modal")
			var name = modal.find("#mode-name").val()
			var oldname = modal.data('oldname')
			var checked_browsers_ids = []
			var checked_states_ids = []
			var browsers_for_mode = []
			//browsers
			$( ".browsers-for-mode input:checked" ).each(function( index ) {
				checked_browsers_ids.push( $(this).val() )
			});
			//states
			$( ".states-for-mode input:checked" ).each(function( index ) {
				checked_states_ids.push( $(this).val() )
			});

			//check fields values
			if ( name.length < 1 ) return alert( 'MODE NAME IS REQUIRED')
			if ( checked_browsers_ids.length < 1 ) return alert( 'CHECK ONE OR MORE BROWSERS' )

			//update mode
			if ( oldname != undefined )
			{
				if ( name.toLowerCase() != oldname.toLowerCase() )
				{
					//check new name is unique
					if ( typeof config.modes[name] !== 'undefined' ) return alert( 'MODE WITH NAME ALREADY EXISTS')
					//remove mode with old name
					delete config.modes[oldname]
				}
			}
			//add mode with new name
			config.modes[name] = {'browsers': checked_browsers_ids, 'states': checked_states_ids}
			//redraw modes
			$('#modes-table').html(_.template( $('#modes-table-tpl').html(), { modes: config.modes } ) )
			modal.modal('hide')
		});

		$(".delete-mode").click(function() {
			//delete mode from config and redraw
			var modal = $(this).closest("#delete_launch_mode_modal")
			var name = modal.data('name')
			delete config.modes[ name ]
			$('#modes-table').html(_.template( $('#modes-table-tpl').html(), { modes: config.modes } ) )
			modal.modal('hide')
		});
		

		$(".save-project").click(function() {
			var urls = []
			if ( $("#urls").length > 0 && $("#urls").val().length > 0 ) urls = $("#urls").val().split("\n")
			config['base_url'] = $("#base_url").val()
			var url = $(this).data('url')
			config.name = $("#name").val()
			pedant_post_request( url, {config: config, urls: urls}, function( data ) {
				$(document).trigger("add-alerts", [
					{ 'message': data.msg, 'priority': 'success' }
				]);
				config = data.config
				if ( data.project_id !== undefined )
				{
					alert(data.msg)
					document.location.href = '/projects/'+data.project_id+'/edit';
				}
			})
		});
	});
