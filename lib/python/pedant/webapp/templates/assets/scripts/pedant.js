$(document).ready(function() {
		$(".fancybox").fancybox();

		$(function() {
    		$("img.lazy").lazyload({skip_invisible : false});
		});

		$(".approve-action").click(function() {
			
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
				 	{ num: $(this).attr("item-id") , path: $(this).find("td.actions a").data( action + "-path") } 
				)
			});
			return json_data
		}

		send_approve_request = function( data, action ){
			var jqxhr = $.post("/ajax/"+action, JSON.stringify(data), function(data) {
				var priority = 'warning'
				if ( data.status == 'OK' )
				{
					priority = 'success'
					set_items_interface( data.items, action )
				}

				$(document).trigger("add-alerts", [
						{ 'message': data.msg, 'priority': priority }
					]);
			}).fail(function(jqxhr, textStatus, error) {
				$(document).trigger("add-alerts", [
						{ 'message': "Error: " + error + " . Status: " + textStatus, 'priority': 'error' }
					]);
			},"json")
			
		}

		set_items_interface = function( items , action )
		{

			var params = {
					'approve': {
						new_title: "Cancel", 
						new_class: "cancel-approve" 
						},
					'cancel-approve': {
						new_title: "Approve", 
						new_class: "approve" 
						}
					}
			// console.log( params[ action ] );
			// console.log( items )
			for(var key in items)
			{
				var data = items[key]
				var item_row = $("tr[item-id='"+key+"']")
				//approve or cancel?
				item_row.find(".actions a").attr( 'title' , params[ action ]['new_title'] )
											.removeClass( "cancel-approve" )
											.removeClass( "approve" )
											.addClass( params[ action ]['new_class'] )		
				//images
				if( data.images.approved !== undefined )
				{
					item_row.children("td.approved").html( data.images.approved )
				}
				if (data.images.approved_report !== undefined)
				{
					item_row.children("td.approved_report").html( data.images.approved_report )
				}
				if (data.images.diff !== undefined)
				{
					item_row.children("td.diff").html( data.images.diff )
				}
				//item_tr.removeClass("selected")
				if ( data.msg == 'success' )
				{
					item_row.removeClass('error').addClass("success")
				}
				else
				{
					item_row.removeClass('success').addClass("error")
				}
			}
			$("img.lazy").lazyload({skip_invisible : false});
			refresh_statistic()
		}

		refresh_statistic()
	});
