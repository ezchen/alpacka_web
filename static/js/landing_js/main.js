(function($) {
var App = { init: function() { App.HomepageHeight();
                               App.HomepageOpacity();
							   App.MaxImage_Slider();
							   App.MaxImage_Single();
							   App.ScrollToSomeplace();
							   App.Count_Down();
							   App.ContactForm();
               },


	// Homepage Height
	HomepageHeight: function() {
	"use strict";
	    var h = window.innerHeight;
	    $('.hero_fullscreen').css('height', h );
	    $('.mockup').css('height', h );
	},


	// Homepage Opacity - for single background image version
	HomepageOpacity: function() {
    "use strict";
        var h = window.innerHeight;
        $(window).on('scroll', function() {
            var st = $(this).scrollTop();
            $('#maximage_single').css('opacity', (1-st/h) );
        });
    },


	// MaxImage Fullscreen Background Slider
	MaxImage_Slider: function() {
	"use strict";
	    $('#maximage_slider').maximage();
	},


	// MaxImage Fullscreen Background Slider
	MaxImage_Single: function() {
	"use strict";
	    $('#maximage_single').maximage();
	},


	// Scroll To ...
    ScrollToSomeplace: function() {
    $('#more_info_btn').click(function () {$.scrollTo('#benefits',1000,{easing:'easeInOutExpo','axis':'y'});return false});
    },


    // Counter ...
	Count_Down: function() {
    "use strict";
        $("#countdown").countdown({
		date: "8 September 2020 09:00:00", // Change this to your desired date to countdown to
		format: "on"
		});
    },




    // Contact Form
    ContactForm: function() {
	     "use strict";
	    var options = {target: "#alert"}
	    $("#contact-form").ajaxForm(options);
    },

}


$(function() {
  App.init();
  $(window).resize(App.HomepageHeight);
	$('#register').on('touchstart click', function() {
		location.href = "/register";
	});

});

})(jQuery);
