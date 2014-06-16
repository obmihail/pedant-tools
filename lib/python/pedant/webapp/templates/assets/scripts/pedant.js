$(document).ready(function() {
		$(".fancybox").fancybox();

		$(".approve-action").click(function() {
			//try approve or cancel
			var params = { url: $( this ).data("approve-path") , new_title: "Cancel approve for this", new_class: "cancel-approve" }

			if ( $( this ).is( ".cancel-approve" ) ){
				params['url'] = $( this ).data("cancel-approve-path")
				params['new_title'] = "Approve this"
				params['new_class'] = "approve-it"
			}
			var self = $( this )
			//send cancel|approve query
			var jqxhr = $.getJSON( params['url'], function(data) {
				var priority = 'warning'
				if ( data.status == 'OK' )
				{
					priority = 'success'
					self.attr( 'title' , params['new_title'] );
					self.removeClass( "cancel-approve" ).removeClass( "approve-it" ).addClass( params['new_class'] )		
					item_tr = self.closest("tr")
					//images
					item_tr.children("td.approved").html( data.images.approved )
					item_tr.children("td.approved_report").html( data.images.approved_report )
					item_tr.children("td.diff").html( data.images.diff )
					//item_tr.removeClass("selected")
					if ( data.msg == 'success' )
					{
						item_tr.removeClass('error').addClass("success")
					}
					else
					{
						item_tr.removeClass('success').addClass("error")
					}
					refresh_statistic()
					return
				}
				$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': priority }
					]);
			}).fail(function(jqxhr, textStatus, error) {
				$(document).trigger("add-alerts", [
						{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
					]);
			})
			refresh_statistic()
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
					$(".items-table tr.selected td.actions a.approve-it").trigger('click');
					$( this ).removeClass( "approve-selected" ).addClass("cancel-selected");
					$( this ).text('Cancel approve on selected')
				} 
				else {
					$(".items-table tr.selected td.actions a.cancel-approve").trigger('click');
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

		refresh_statistic = function() {
			$("span.total-count").text( $('tr.item').length );
    		$("span.error-count").text( $('tr.error').length );
    		$("span.selected-count").text( $('tr.selected').length );
		}
		refresh_statistic()
	});
