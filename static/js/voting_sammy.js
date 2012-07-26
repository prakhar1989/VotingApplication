(function($) {

var votes_array = {};

var fill_with_default = function(votes_array, default_string){
    //instantiates votes_array to a default value
    for(i=0; i<=20; i++){
        votes_array[i] = default_string;
    }
}

fill_with_default(votes_array, "default");

var add_to_votes_array = function(votes_array, username_list, post_id){
    //something wrong here
    votes_array[post_id] = username_list;
};


var app = $.sammy('#main', function() {
    this.use('Template');

    this.get('#/', function(context){
        this.redirect('#/1');
    });

    this.get('#/:post_id', function(context){
        this.trigger('addVotesInArray');
        //console.log("Votes Array " + votes_array);
        //var posts_votes = votes_array[this.params['post_id'] - 1];
        console.log(votes_array);
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
       var current_post_id = $('.post_heading').data("post_id");
       var selected_candidates = $('.candidate_selected');
       var selected_candidate_list = [];
       for (i = 0; i < selected_candidates.length; i++) {
            selected_candidate_list.push($(selected_candidates[i]).data("username"));
       }
       add_to_votes_array(votes_array, selected_candidate_list, current_post_id);
    });

    $(function() {
        app.run('#/');
    });

});

})(jQuery);

