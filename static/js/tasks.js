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
    'click .accept_task': 'accept_task',
  },
  modelEvents: {
    "change": function() { this.render(); }
  },
  accept_task(event) {
    console.log(this.model.attributes);
    var jsonData = {
      "id": this.model.attributes.id,
      "set_courier": true
    }
    console.log(jsonData);
    var settings = {
      "async": true,
      "url": "/api/v1/courier/tasks",
      "method": "PATCH",
      "data": jsonData,
      "success": function(data, textStatus, jqXHR) {
        window.location = "/accepted_tasks"
      }
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
  collection: data,
  emptyView: EmptyItemView
});

$(document).ready(function() {
	var settings = {
	    "async": true,
	    "url": "/api/v1/tasks/",
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
