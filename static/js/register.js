var RegisterView = Backbone.Marionette.View.extend({
    el: '#register',
    template: false,

    events: {
        'click #btn-login': 'register',
    },

    register(event) {
        console.log('register');
        var email = $('#register').find('input[name="email"]').val();
        var password = $('#register').find('input[name="password"]').val();
        var phone = $('#register').find('input[name="phone"]').val();
        var first_name = $('#register').find('input[name="first_name"]').val();
        var last_name = $('#register').find('input[name="last_name"]').val();


        var form = new FormData();
        form.append("email", email);
        form.append("password", password);
        form.append("phone", "+1" + phone);
        form.append("first_name", first_name);
        form.append("last_name", last_name);

        console.log(form);

      	var settings = {
      	    "async": true,
      	    "url": "/api/v1/accounts/",
      	    "method": "POST",
      	    "headers": {
                      "cache-control": "no-cache",
      	    },
      	    "processData": false,
      	    "contentType": false,
      	    "mimeType": "multipart/form-data",
      	    "data": form,
            "statusCode": {
              200: {
                window.location="/dashboard"
              }
            }
      	}

      	$.ajax(settings).done(function (response) {
      	});
    },

    showPassword(event) {
        console.log('showPass');
    }

});

var myView = new RegisterView();
myView.render();
