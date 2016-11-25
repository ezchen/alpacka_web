var PostTaskView = Backbone.Marionette.View.extend({
    el: '#post_task',
    template: false,

    events: {
        'click #btn-post': 'post_task'
    },

    post_task(event) {
        var price = $('#post_task').find('input[name="price"]').val();
        var task_heading = $('#post_task').find('input[name="task_heading"]').val();
        var task_description = $('#post_task').find('textarea[name="task_description"]').val();

        var form = new FormData();
        form.append("task_price", price);
        form.append("task_heading", task_heading);
        form.append("task_description", task_description);

        console.log(form);

      	var settings = {
      	    "async": true,
      	    "url": "/api/v1/tasks/",
      	    "method": "POST",
      	    "headers": {
                      "cache-control": "no-cache",
      	    },
      	    "processData": false,
      	    "contentType": false,
      	    "mimeType": "multipart/form-data",
      	    "data": form,
      	}

      	$.ajax(settings).done(function (response) {
                  console.log(response);
      	});
    }
});

var myView = new PostTaskView();
myView.render();
