$(document).ready(function(){
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});
	
	$('#submit').on('click', function(e){
		var departure = $('#departure').val(),
			arrival = $('#arrival').val();
		
		$.ajax({
			 'type': "GET",
			 'url': location.protocol + "//" + location.host + "/flightdata/" + departure + "+" + arrival + "/",
			 'data': {
				'departure': departure,
				'arrival': arrival
			 },
			 'dataType': 'json',
			 'success': function (data){		
				console.log("SUCCESS");
				console.log(data);
			}
		});
		
		return false;
	});
});