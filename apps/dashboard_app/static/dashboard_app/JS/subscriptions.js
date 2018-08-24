{
    $('#unsub_click').click(function(){
        $.ajax({
            url: "unsubscribe/{{subscription.id}}",
            success: function(serverResponse) {
                console.log("*_"*15, "Received this from service:", serverResponse)
                $('#repopulate').html(serverResponse)
            }
        }
    })
}