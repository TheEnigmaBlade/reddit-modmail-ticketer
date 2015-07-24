function init_status_buttons() {
	
	function get_status_label_class(status) {
		switch(status) {
			case "open": return "success";
			case "active": return "primary";
			case "closed": return "default";
			case "ignored": return "danger";
			default: return "default";
		}
	}
	
	function update_status_button($button, oldClass, newText, newClass) {
		$button.text(newText);
		$button.removeClass(oldClass);
		$button.addClass(newClass);
		
		var $ddBtn = $button.siblings(".status-dropdown-button");
		$ddBtn.removeClass(oldClass);
		$ddBtn.addClass(newClass);
	}
	
	// Status increment button
	$('.status-button').click($.throttle(500, function() {
		console.log("Status button pressed");
		var $this = $(this),
			$ticket = $this.parents('.ticket'),
			ticketId = $ticket.data('ticketId'),
			status = $ticket.data('ticketStatus'),
			oldClass = "btn-"+get_status_label_class(status),
			csrftoken = $.cookie('csrftoken');
		
		// Update server with new status
		$.post("/api/ticket/" + ticketId + "/modify/?inc_status=" + status, {csrfmiddlewaretoken: csrftoken})
			// Success
			.done(function(data) {
				console.log(data);
				if(data["success"]) {
					var newText = data['status_text'],
						newStatus = data['status'],
						newClass = "btn-" + data['status_class'];
					
					$ticket.attr('ticket_status', newStatus);
					update_status_button($this, oldClass, newText, newClass);
				}
			})
			// Failure
			.fail(function(data) {
				console.error(data);
			});
	}));
	
	// Status set buttons
	$('.status-button-set').click($.throttle(500, function() {
		console.log("Status button pressed");
		var $this = $(this),
			$ticket = $this.parents('.ticket'),
			ticketId = $ticket.data('ticketId'),
			status = $this.attr('status'),
			oldStatus = $ticket.data('ticketStatus'),
			oldClass = "btn-"+get_status_label_class(oldStatus),
			csrftoken = $.cookie('csrftoken');
		
		// Update server with new status
		$.post("/api/ticket/" + ticketId + "/modify/?set_status=" + status, {csrfmiddlewaretoken: csrftoken})
			// Success
			.done(function(data) {
				console.log(data);
				if(data["success"]) {
					var newText = data['status_text'],
						newStatus = data['status'],
						newClass = "btn-" + data['status_class'];
					
					$ticket.attr('ticket_status', newStatus);
					var $button = $ticket.find('.status-button');
					update_status_button($button, oldClass, newText, newClass);
				}
			})
			// Failure
			.fail(function(data) {
				console.error(data);
			});
	}));
}

function init_message_hover() {
	function hide_message_previews() {
		$('.col-subject a').popover("destroy");
	}
	
	$('.col-subject a').hoverIntent({
		timeout: 1000,
		over: function() {
			var $this = $(this),
				$ticket = $this.parents('.ticket'),
				ticketId = $ticket.data('ticketId');
			
			hide_message_previews();
			$this.popover({"content": "<span class='glyphicon glyphicon-refresh glyphicon-spin'></span> Loading preview...", "placement": "auto bottom", "html": true});
			$this.popover("show");
			
			var $popoverContent = $this.siblings('.popover').find('.popover-content');
			
			$.get("/api/ticket/" + ticketId + "/" + status)
				// Success
				.done(function(data) {
					console.log(data);
					if(data["success"]) {
						$popoverContent.html(data["message"]);
					}
					else {
						$popoverContent.text("Failed to load preview");
					}
				})
				// Failure
				.fail(function(data) {
					console.error(data);
					$popoverContent.text("Failed to load preview");
				});
		}
	});
	
	$('body').on('click', function(e) {
		var $target = $(e.target);
		if($target.data('toggle') !== 'popover' && $target.parents('.popover.in').length === 0) {
			hide_message_previews();
		}
	});
}

function init_last_modified_hover() {
	$('.status-button').hoverIntent({
		timeout: 200,
		over: function() {
			var $this = $(this),
				$parent = $this.parent(),
				$ticket = $this.parents('.ticket'),
				lastModifiedBy = $ticket.data('lastModifiedBy');
			
			$parent.popover({"content": "last modified by " + lastModifiedBy, "placement": "left", "html": false});
			$parent.popover("show");
		},
		out: function() {
			var $this = $(this),
				$parent = $this.parent();
			$parent.popover("destroy");
		}
	});
}

// Stuff to do at page load

$(function() {
	init_status_buttons();
	init_message_hover();
	init_last_modified_hover();
});
