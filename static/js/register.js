var RegisterView = Backbone.Marionette.View.extend({
    el: '#register',
    template: false,

    ui: {
      template: '#register'
    },

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
        var dial_code = $("#phone").intlTelInput("getSelectedCountryData").dialCode;


        var form = new FormData();
        form.append("email", email);
        form.append("password", password);
        form.append("phone", "+" + dial_code + phone);
        form.append("first_name", first_name);
        form.append("last_name", last_name);

        console.log(form);

        var me = this;

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
            "success": function() {
              me.hide();
            },
            "error": function(xhr, ajaxOptions, thrownError) {
              $('#register').effect('shake');
            }
      	}

      	$.ajax(settings).done(function (response) {
          console.log(response.data);
      	});
    },

    hide() {
      var showPhone = function () {
        var showPhone2 = function() {
          $('#phone_verification').fadeIn(400)
        }
        window.setTimeout(showPhone2, 500);
      }
      $("#register").fadeOut(400, showPhone);
    },

    showPassword(event) {
        console.log('showPass');
    }

});

$("#phone").intlTelInput();
var myView = new RegisterView();
myView.render();

var PhoneVerificationView = Backbone.Marionette.View.extend({
  el: '#phone_verification',
  template: false,

  events: {
    'keyup #pin1': 'keypress1',
    'keyup #pin2': 'keypress2',
    'keyup #pin3': 'keypress3',
    'keyup #pin4': 'keyUp4',
  },

  handleKeyUp(e, currentElement) {
    var currentInput = parseInt(currentElement.substring(4,5));
    var code = e.keyCode || e.which;
    // Backspace pressed
    if (code == 8) {
      if (currentInput != 1) {
        previousInputNum = currentInput - 1;
        previousInput = '#pin' + previousInputNum;

        $(previousInput).focus();
      }
    }
    if (code >= 48 && code <= 57) {

      if (currentInput != 4) {
        nextInputNum = currentInput + 1;
        nextInput = '#pin' + nextInputNum;

        $(nextInput).focus();
      } else {
        this.submit()
      }
    }
  },

  handleKeyEvent(e, currentElement) {
    var currentInput = parseInt(currentElement.substring(4,5));
    var code = e.keyCode || e.which;

    if (code >= 48 && code <= 57) {

      if (currentInput != 4) {
        nextInputNum = currentInput + 1;
        nextInput = '#pin' + nextInputNum;

        $(nextInput).focus();
      } else {
        this.submit()
      }
    }
  },

  keypress1(e) {
        this.handleKeyEvent(e, '#pin1');
  },

  keypress2(e) {
        this.handleKeyEvent(e, '#pin2');
  },

  keypress3(e) {
        this.handleKeyEvent(e, '#pin3');
  },

  keyUp1(e) {

    this.handleKeyUp(e, '#pin1');
  },

  keyUp2(e) {

    this.handleKeyUp(e, '#pin2');
  },

  keyUp3(e) {

    this.handleKeyUp(e, '#pin3');
  },

  keyUp4(e) {

    this.handleKeyUp(e, '#pin4');
  },

  submit() {
    var pin = "";
    for (var i = 1; i <= 4; i++) {
      pin += $('#pin' + i).val();
    }

    var form = new FormData();
    form.append("verification_code", pin);
    console.log(form);

    var me = this;
    var settings = {
        "async": true,
        "url": "/api/v1/auth/verify-phone/",
        "method": "POST",
        "headers": {
                  "cache-control": "no-cache",
        },
        "processData": false,
        "contentType": false,
        "mimeType": "multipart/form-data",
        "data": form,
        "success": function() {
          var showDone = function () {
            var showDone2 = function() {
              $('#all_done').fadeIn(400)
            }
            window.setTimeout(showDone2, 500);
          }

          $('#pin_input').fadeOut(400, showDone);
        },
        "error": function(xhr, ajaxOptions, thrownError) {
          $('#pin_input').effect('shake');
        }
    }

    $.ajax(settings).done(function (response) {
      console.log(response.data);
    });
  }
})

var phoneView = new PhoneVerificationView();
phoneView.render();
