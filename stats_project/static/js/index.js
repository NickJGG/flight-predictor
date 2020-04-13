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
		$('#error-box').css('display', 'none');
		
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
				$('#loading-box').css('display', 'none');
				
				console.log(data);
				 
				if (data['success']){
					showResults(data);
				} else {
					showError(data);
				}
			}
		});
		
		return false;
	});
});

function showResults(data){
	$('#results-box').css('display', 'flex');
					
	$('#predicted-price').text("$" + data['confidence_interval']['predicted_price']);
	$('#lower-bound').text("$" + data['confidence_interval']['lower_bound']);
	$('#upper-bound').text("$" + data['confidence_interval']['upper_bound']);
	
	var city_from = $('.weather-city').eq(0);
	var city_to = $('.weather-city').eq(1);
	
	$(city_from).find('.city-name').text(data['cities'][0]);
	$(city_to).find('.city-name').text(data['cities'][1]);
	
	$(city_from).find('.city-temp').text(data['weather']['from']['temp'] + '°');
	$(city_to).find('.city-temp').text(data['weather']['to']['temp'] + '°');
	
	$(city_from).find('.city-main').text(data['weather']['from']['main']);
	$(city_to).find('.city-main').text(data['weather']['to']['main']);
	
	$('#opinion').text(data['opinion']);
	
	$('#results-box').css('height', $('#form-container').outerHeight());
}
function showError(data){
	$('#error-box').css('display', 'flex');
					
	$('#error-message').text(data['error_message']);
}