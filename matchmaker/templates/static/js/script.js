(function($) { 

	$('[data-toggle="tooltip"]').tooltip();

	$('#resulttabs a').click(function (e) {
  		e.preventDefault()
  		$(this).tab('show')
	})

	// using javascrip Cookie library
	var csrftoken = Cookies.get('csrftoken'); 
	var mlevel = Cookies.get('mlevel');

	var solooneplayed = false;
	var solotwoplayed = false;

	if (mlevel == 'b') {
		$('#musicianlevel-begginer').prop('checked', true);
	} else if(mlevel == 'i'){
		$('#musicianlevel-intermediate').prop('checked', true);
	} else if(mlevel == 'p'){
		$('#musicianlevel-pro').prop('checked', true);
	}


	// code using $ as alias to jQuery

	function check_musician_value(radiovalue) {
		if (radiovalue === undefined){
			if ( $('.alert-danger').length ){
				$('.alert-danger').hide();
				$('.alert-danger').show();
			} else {
				$('#alerts').append('<div class="alert alert-danger" role="alert">Choose your level as musician.</div>');
			}
			return 0;
		} else {
			return 1;
		}
	}

	$('input[type="radio"]').click(function(event){
		$('.alert-danger').hide();
	});


	// $('#logout-link').click(function(event){
	// 	alert(click);
	// 	Cookies.remove('mlevel');
	// });

	$(document).on ("click", "#logout-link", function () {
        Cookies.remove('mlevel');
    });


    $('#lvlnxt-btn').click(function(event){
    	radiovalue = $('input[name=musicianlevel]:checked', '#levelchooseform').val()
		if ( !check_musician_value(radiovalue) ){
			return 0;
		} else {
			$.ajax({
				beforeSend: function(xhr, settings) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
			    },
				type: 'POST',
				url: '/contest/addmlevel/',
				data: {level: radiovalue},
				success: function(data) {
					window.location.replace("/contest/");
				}
			});
		}
    });


    function vote (voteurl, matchtype, winner, usewinner) {
    	$.ajax({
			beforeSend: function(xhr, settings) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		    },
			type: 'POST',
			url: voteurl,
			data: {matchtype: matchtype, winner: winner, usewinner: usewinner},
			success: function(data) {
				$('.like-button').attr('disabled','disabled');
				$('#div-refresh-btn').show();
			}
		});
    }

    $('#draw-btn').click(function(event){
    	voteurl = '/contest/vote/';
		matchtype = $('#matchtype').val();
		winner = 0;
		usewinner = 0;

		if ( $('#usefirst').is(":checked") || $('#usesecond').is(":checked") ) {
			usewinner = 1;
		}

		vote(voteurl, matchtype, winner, usewinner);
    });
  
	$('#vote-on-first').click(function(event){
		voteurl = '/contest/vote/';
		matchtype = $('#matchtype').val();
		winner = 1;
		usewinner = 0;

		if ( $('#usefirst').is(":checked") ) {
			usewinner = 1;
		}

		vote(voteurl, matchtype, winner, usewinner);
	});


	$('#vote-on-second').click(function(event){
		voteurl = '/contest/vote/';
		matchtype = $('#matchtype').val();
		winner = 2;
		usewinner = 0;

		if ( $('#usesecond').is(":checked") ) {
			usewinner = 1;
		}

		vote(voteurl, matchtype, winner, usewinner);
	});


	$('#inputPassword, #inputConfirmPassword').focus(function(){
		$('#alerts').hide();
	});


	$('#ipt-change-pass').click(function(event){
		new_pass = $('#inputPassword').val()
		confirm_pass = $('#inputConfirmPassword').val()
		if (new_pass != confirm_pass) {
			$('.alert-danger').remove();
			$('#alerts').hide();
			event.preventDefault();
			$('#alerts').append('<div class="alert alert-danger" role="alert">Passwords do not match</div>');
			$('#alerts').show();
		};
	});

	$('#ipt-add-musician').click(function(event){
		new_pass = $('#inputPassword').val()
		confirm_pass = $('#inputConfirmPassword').val()
		if (new_pass != confirm_pass) {
			$('.alert-danger').remove();
			$('#alerts').hide();
			event.preventDefault();
			$('#alerts').append('<div class="alert alert-danger" role="alert">Passwords do not match</div>');
			$('#alerts').show();
		};
	});


	function show_vote_buttons(){
		if (solooneplayed &&  solotwoplayed) {
			// $('#vote-on-first, #vote-on-second, #draw-btn').show();
			$('#vote-on-first, #vote-on-second').show();
		}
	}


	$('#audio-solo-one').on('ended',function(event){
		solooneplayed = true;
		show_vote_buttons();
	});

	$('#audio-solo-two').on('ended',function(event){
		solotwoplayed = true;
		show_vote_buttons();
	});

	$('#audio-solo').on('ended',function(event){
		$('#sbt-solo-eval').show();
	});
	

	$('#refresh-button').click(function(event){
		window.location.reload(true);
	});


	// Scripts do viewresults
	$('.playcontest').click(function(event){
		event.preventDefault()
		playurl = $( this ).attr('href');

		// alert(url);

		$('#show-selected-contest').hide();

		$.ajax({
			type: 'GET',
			dataType: 'json',
			url: playurl,
			success: function(data) {
				$('#audio-solo-random').attr('src',data['solo_random']);
				$('#audio-solo-allrules').attr('src',data['solo_allrules']);

				$('#show-selected-contest').show('fast');

			}
		});

	});


	$('.playsolo').click(function(event){
		event.preventDefault()
		playurl = $( this ).attr('href');

		// alert(url);

		$('#show-selected-solo').hide();

		$.ajax({
			type: 'GET',
			dataType: 'json',
			url: playurl,
			success: function(data) {
				$('#audio-solo').attr('src', data['solo']);
				$('#show-selected-solo').show('fast');
				$('#audio-solo').attr('autoplay', true);
			}
		});

	});


	$('#sbt-solo-eval').click(function(event){
		if ( !$('input[name=solo-rate]:checked').length > 0 ){
			event.preventDefault();
			$('#alerts').append('<div class="alert alert-danger" role="alert">Select a enjoyment value</div>');
		}
		else if ( !$('input[name=usesolo]:checked').length > 0 ) {
			event.preventDefault();
			$('p.check-use-solo').addClass('alert alert-danger');
		}
	});


	$('#go-to-evals').click(function(event){
		$.ajax({
			beforeSend: function(xhr, settings) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		    },
			type: 'POST',
			url: '/contest/firstaccess/',
			success: function(data) {
				window.location.replace("/contest/");
			}
		});
	});


	// $(window).bind('unload', function(){
	// 	Cookies.remove('mlevel');
	// });


})(jQuery);