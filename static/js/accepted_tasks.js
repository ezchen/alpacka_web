var Task = Backbone.Model.extend();
var Tasks = Backbone.Collection.extend({
  model: Task
})

var data = new Tasks([]);

var TaskItemView = Backbone.Marionette.View.extend({
  template: '#task_item',
  tagname: 'div',
  events: {
    'click .btn': 'cancel',
  },
  modelEvents: {
    "change": function() { this.render(); }
  },
  cancel(event) {
    console.log(this.model.attributes);
    var jsonData = {
      "id": this.model.attributes.id,
      "remove_courier": true
    }
    console.log(jsonData);
    var settings = {
      "async": true,
      "url": "/api/v1/courier/tasks",
      "method": "PATCH",
      "data": jsonData
    }
  	$.ajax(settings).done(function (response) {
      console.log(response);
  	});
  }
});

var TaskListView = Backbone.Marionette.CollectionView.extend({
    el: '#task_list',
    tagname: 'ul',
    childView: TaskItemView
});

var TaskListView = new TaskListView({
  collection: data
});

$(document).ready(function() {
	var settings = {
	    "async": true,
	    "url": "/api/v1/courier/tasks",
	    "method": "GET",
	    "headers": {
                "cache-control": "no-cache",
	    },
      "statusCode": {
        401: function() {
          window.location="/login"
        }
      }
	}

	$.ajax(settings).done(function (response) {
      _.each(response, function(el) {data.push(el);})
	});
  TaskListView.render();
});
