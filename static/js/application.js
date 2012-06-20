$(function() {
    //hide the show_message label by default
    $('#show_message').hide();

    $('#coupon_form').submit(function(){
        $.ajax({
            url: $SCRIPT_ROOT+'/coupon/new',
            type: "POST",
            data: $(this).serialize(),
            success: function(data) {
                $('#coupon_value').text(data.coupon);
                $('#show_message').text(data.msg);
                $('#show_message').show();
            }
        });
        return false;
    });
});
