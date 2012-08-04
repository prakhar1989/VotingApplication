(function($) {

var fill_with_default = function(votes_array, default_string){
    //instantiates votes_array to a default value
    for(i=0; i<=20; i++){
        votes_array[i] = default_string;
    }
}

var app = $.sammy('#main', function() {
    this.use('Template');
    this.use('Session');

    var votes_array = this.session('votes_array', function(){
        return {};
    });

    if (votes_array == {}) { fill_with_default(votes_array, "blank"); }

    this.get('#/', function(context){
        this.redirect('#/1');
        $('#status').hide();
        $('#modalClick').trigger('click');
    });

    this.get("#/submit", function(context){
        this.redirect('#/1');
        var max_votes_for_post = $('.post_heading').data('maxCount');
        var current_count = $('.candidate_selected').length;
        if (current_count > max_votes_for_post) {
            alert("Please select valid number of candidates before proceeding");
            return false;
        }
        console.log(JSON.stringify(votes_array));
        $.ajax({
            type: 'POST',
            url: '/submit',
            cache: false,
            dataType: 'json',
            data: JSON.stringify(votes_array),
            success: function(data){
                $('.white_bg').hide();
                $('.sidebar').hide();
                $('.navbar').hide();
                $('.close_btn').trigger('click');
                $('#status').show();
                $('#message').text(data['status']);
                setTimeout(function(){
                    $('#logoutBtn').trigger('click');
                }(),15000);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                alert(errorThrown);
            }
        });
    });

    this.get('#/:post_id', function(context){
        this.trigger('addVotesInArray');
        context.app.swap('');

        this.load('/post/' +  this.params['post_id'])
            .then(function(candidates){
                //Use post data generated to add help_text for each post generated
                $('.post_heading').text(candidates[0][0]["post_name"]);
                $('.post_help_text').text(candidates[0][0]["post_help_text"]);
                $('.post_heading').data("post_id", candidates[0][0]["post_id"]);
                $('.post_heading').data("maxCount", candidates[0][0]["post_max_votes"]);
                $.each(candidates[1], function(i, candidate){
                    context.render("static/templates/candidate.template", 
                                    {candidate:candidate})
                    .appendTo(context.$element())
                    .then(function(){
                        var ht = $('.topdiv').css("height");
                        var cur_ht = $('.sidebar').css("height");
                        if (parseInt(cur_ht) < parseInt(ht)){
                            $('.sidebar')
                            .css("height", (parseInt(ht)) + "px");
                        }})
                    .then(function(){
                        var chosen_votes = votes_array[context.params['post_id']];
                        if (chosen_votes && chosen_votes.length > 0 && chosen_votes != "blank") {
                            for (i=0; i < chosen_votes.length; i++) {
                                var u_name = chosen_votes[i];
                                $('#main').find("[data-username='" + u_name + "']")
                                          .addClass('candidate_selected')
                                          .find('.checkbox').addClass('checkbox_selected');
                            }
                        }
                    });
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
       if (selected_candidate_list.length > 0) {
           //dont add blank lists to votes_array
           //add_to_votes_array(votes_array, selected_candidate_list, current_post_id);
           votes_array[current_post_id] = selected_candidate_list;
           this.session('votes_array', votes_array);
       }
    });


    $(function() {
        app.run('#/');
    });

});

})(jQuery);

