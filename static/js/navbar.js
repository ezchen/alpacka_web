var NavbarView = Backbone.Marionette.View.extend({
    el: '#navbar',
    template: false,

    events: {
        'click .logout': 'logout',
    },

    logout(event) {
      console.log("logout");
      var settings = {
        "async": true,
        "url": "/api/v1/auth/logout/",
        "method": "POST"
      }
    	$.ajax(settings).done(function (response) {
        window.location = "/login";
    	});
    },

});

var myView = new NavbarView();
myView.render();
