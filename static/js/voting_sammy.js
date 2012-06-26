(function($) {

var app = $.sammy('#main', function() {
    this.use('Template');

    this.get('#/', function(context){
        this.redirect('#/1');
    });

    this.get('#/:post_id', function(context){
        context.app.swap('');
        this.load('/post/' +  this.params['post_id'])
            .then(function(candidates){
                $('.post_heading').text(candidates[0]);
                $.each(candidates[1], function(i, candidate){
                    context.render("static/templates/candidate.template", {candidate:candidate})
                    .appendTo(context.$element());
                });
        });
    });

    $(function() {
        app.run('#/');
    });

});

})(jQuery);
