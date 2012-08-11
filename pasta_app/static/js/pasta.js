$(function() {
  window.File = Backbone.Model.extend({});
  window.FileView = Backbone.View.extend({
    el: $('#files'),
    model: File,
    render: function() {
      var template = _.template($('#file_template').html(), {});
      $(this.el).append(template);
    }
  });

  window.Pasta = Backbone.Collection.extend({
    model: File,
    initialize: function(models, options) {
      this.bind("add", function(model) {
      });
    }
  });
  window.PastaView = Backbone.View.extend({
    el: $('.container'),
    initialize: function() {
      this.msgIfEmpty();
      this.collection.bind('add', _.bind(this.msgIfEmpty, this));

      var createAndRender = function(file) { return new FileView({ model: file }).render(); };
      this.collection.bind('add', createAndRender);
      this.collection.each(createAndRender);
    },
    msgIfEmpty: function() {
      var msg = '';
      if (this.collection.length === 0) {
        if (this.options.permissions.indexOf('write') !== -1) {
          msg = "<h4>There doesn't seem to be anything here. Use the button to the right to add some files <i class='icon-arrow-right'></i></h4>";
        } else {
          msg = "<h4>There's nothing in this Pasta yet. Wait for someone to add some files.</h4>";
        }
      }
      $('#empty-message').html(msg);
    },
    events: {
      "click #add-file": "addFile"
    },
    addFile: function() {
      this.collection.add(new File());
    }
  });
});
