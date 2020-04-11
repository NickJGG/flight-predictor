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
			
		$('#loading-box').css('display', 'flex');
		$('#results-box').css('display', 'none');
		
		$.ajax({
			 'type': "GET",
			 'url': location.protocol + "//" + location.host + "/flightdata/" + departure + "+" + arrival + "/",
			 'data': {
				'departure': departure,
				'arrival': arrival
			 },
			 'error': function(e){
				 $('#loading-box').css('display', 'none');
			 },
			 'dataType': 'json',
			 'success': function (data){
				 console.log(data);
				 
				 $('#predicted-price').text("$" + data['predicted_price']);
				 $('#lower-bound').text("$" + data['lower_bound']);
				 $('#upper-bound').text("$" + data['upper_bound']);
				 
				$('#loading-box').css('display', 'none');
				$('#results-box').css('display', 'flex');
				 
				console.log("SUCCESS");
			}
		});
		
		return false;
	});
});