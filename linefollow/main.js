$(document).ready(function() {

	var PLANE_WIDTH = 3; 	// cells
	var PLANE_HEIGHT = 3;	// cells
	var CELL_SIZE = 60; 	// pixels
	 
	var encoded_plane = "000000000";

	// Set the dimensions of the plane div. The addition in calculating the
	// width and height is due to each cell's right border adding an extra
	// pixel to the cell's width.
	$('#plane').css('width', ((PLANE_WIDTH*CELL_SIZE) + PLANE_WIDTH)+'px');
	$('#plane').css('height', ((PLANE_HEIGHT*CELL_SIZE) + PLANE_HEIGHT)+'px');
	
	for (var y = 0; y < PLANE_HEIGHT; y++) {
		for (var x = 0; x < PLANE_WIDTH; x++) {
			var chr = encoded_plane.charAt(x + (y * PLANE_WIDTH));
			$('#plane').append('<div class="cell">'+chr+'</div>');
		}
	}





	return;

	var socket = new WebSocket("ws://localhost:8888/stream");
	socket.onmessage = function(msg) {
		$('#console').append(msg.data+"</br>");
		
		// var colors = msg.data.split(",");
		// var red = parseInt(colors[0]);
		// var green = parseInt(colors[1]);
		// var blue = parseInt(colors[2]);
		// red = Math.floor(red / 2.55);
		// green = Math.floor(green / 2.55);
		// blue = Math.floor(blue / 2.55);
		// $('#console').append("<div style='width: 50px; height: 50px; background-color: rgb("+red+","+green+","+blue+");'></div>");
		
	}
	$('#start_button').click(function() {
		$.ajax({
			type: "POST",
			url: "/start"
		});
	})
	$('#stop_button').click(function() {
		$.ajax({
			type: "POST",
			url: "/stop"
		});
	})

});


