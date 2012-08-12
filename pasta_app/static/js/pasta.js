$(function() {
  window.File = Backbone.Model.extend({});
  window.FileView = Backbone.View.extend({
    parentEl: $('#pasta-files'),
    template: _.template($('#pasta-file-template').html()),
    model: File,
    initialize: function() {
      this.render();
    },
    render: function() {
      this.$el = $(this.template({ file: this.model })).appendTo(this.parentEl);
      $('.pasta-content', this.$el).focus();
    },
    events: {
      "click .remove-file": "removeFile",
      "change .pasta-file-name": "setName",
      "change .pasta-content": "setContent"
    },
    removeFile: function() {
      console.log(this.model);
      this.model.destroy();
      this.$el.remove();
    },
    setName: function(e) {
      this.model.set({ path: $(e.currentTarget).val() });
    },
    setContent: function(e) {
      this.model.set({ content: $(e.currentTarget).val() });
    }
  });

  window.Pasta = Backbone.Collection.extend({
    model: File
  });
  window.PastaView = Backbone.View.extend({
    el: $('.container'),
    initialize: function() {
      var that = this;
      this.msgIfEmpty();
      this.collection.on('add', _.bind(this.msgIfEmpty, this));
      this.collection.on('remove', _.bind(this.msgIfEmpty, this));

      var createAndRender = function(file) { return new FileView({ model: file }) };
      this.collection.on('add', createAndRender);
      this.collection.each(createAndRender);
    },
    msgIfEmpty: function() {
      var msg = '';
      if (this.collection.length === 0) {
        if (this.options.permissions.indexOf('write') !== -1) {
          msg = "<h4>There doesn't seem to be anything here. Use the button in the navbar to add some files <i class='icon-arrow-up'></i></h4>";
        } else {
          msg = "<h4>There's nothing in this Pasta yet. Wait for someone to add some files.</h4>";
        }
      }
      $('#empty-message').html(msg);
    },
    events: {
      "click #add-file": "addFile",
      "click #do-commit": "showCommitDialog"
    },
    addFile: function() {
      this.collection.add(new File());
    },
    showCommitDialog: function() {
      $("#commit-modal").modal('show');
      $("#commit-message").focus();
    }
  });
});
