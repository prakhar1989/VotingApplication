(function($) {

var fill_with_default = function(votes_array, default_string){
    //instantiates votes_array to a default value
    for(i=0; i<=20; i++){
        votes_array[i] = default_string;
    }
}

var add_to_votes_array =  function(votes_array, username, post_id){
    votes_array[post_id] = username;
};

var votes_array = {};
fill_with_default(votes_array, "default");

var app = $.sammy('#main', function() {
    this.use('Template');

    this.get('#/', function(context){
        this.redirect('#/1');
    });

    this.get('#/:post_id', function(context){
        this.trigger('addVotesInArray');
        context.app.swap('');
        this.load('/post/' +  this.params['post_id'])
            .then(function(candidates){
                //Use post data generated to add help_text for each post generated
                $('.post_heading').text(candidates[0][0]["post_name"]);
                $('.post_heading').data("post_id", candidates[0][0]["post_id"]);
                $.each(candidates[1], function(i, candidate){
                    context.render("static/templates/candidate.template", {candidate:candidate})
                    .appendTo(context.$element());
                });
        });
    });
    
    this.bind('addVotesInArray', function(){
        current_post_id = $('.post_heading').data("post_id");
        candidate_username = $('.candidate_selected').data("username");
        add_to_votes_array(votes_array, candidate_username, current_post_id);
        console.log(votes_array);
    });

    $(function() {
        app.run('#/');
    });

});

})(jQuery);

