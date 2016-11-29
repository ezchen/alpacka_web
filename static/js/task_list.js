var Task = Backbone.Model.extend();
var Tasks = Backbone.Collection.extend({
  model: Task
})

var data = new Tasks([]);

var EmptyItemView = Backbone.Marionette.View.extend({
  template: '#empty_state',
  tagname: 'div'
})

var TaskItemView = Backbone.Marionette.View.extend({
  template: '#task_item',
  tagname: 'div',
  events: {
    'click .cancel': 'cancel_task',
  },
  modelEvents: {
    "change": function() { this.render(); }
  },
  cancel_task(event) {
    console.log("cancel");
    var settings = {
      "async": true,
      "url": "/api/v1/tasks/" + this.model.attributes.id + "/",
      "method": "DELETE",
      "success": function(data, textStatus, jqXHR) {
        window.location = "/dashboard"
      }
    }
  	$.ajax(settings).done(function (response) {
  	});
  }
});

var TaskListView = Backbone.Marionette.CollectionView.extend({
    el: '#task_list',
    tagname: 'ul',
    childView: TaskItemView,
    emptyView: EmptyItemView
});

var TaskListView = new TaskListView({
  collection: data
});

$(document).ready(function() {
	var settings = {
	    "async": true,
	    "url": "/api/v1/accounts/my_account/my_tasks",
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
      TaskListView.render();
	});
});
