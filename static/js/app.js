var LoginView = Backbone.Marionette.View.extend({
    el: '#login',
    template: false,

    events: {
        'click #btn-login': 'login',
        'click .checkbox': 'showPassword'
    },

    login(event) {
        console.log('login');
        var email = $('#login').find('input[name="email"]').val();
        var password = $('#login').find('input[name="password"]').val();
        console.log(email);

        var form = new FormData();
        form.append("email", email);
        form.append("password", password);

        console.log(form);

	var settings = {
	    "async": true,
	    "url": "/api/v1/auth/login/",
	    "method": "POST",
	    "headers": {
                "cache-control": "no-cache",
	    },
	    "processData": false,
	    "contentType": false,
	    "mimeType": "multipart/form-data",
	    "data": form
	}

	$.ajax(settings).done(function (response) {
            console.log(response);
	});
    },

    showPassword(event) {
        console.log('showPass');
    }

});

var myView = new LoginView();
myView.render();
