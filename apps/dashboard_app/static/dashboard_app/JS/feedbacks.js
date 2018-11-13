$('#feedback_tot').click(function(e){
    e.preventDefault();
    $('#feedback_tot_chart').toggle()
});
$('#feedback_rating').click(function(a){
    a.preventDefault();
    $('#feedback_rating_bar').toggle()
});
$('#feedback_comments').click(function(a){
    a.preventDefault();
    $('#feedback_comment_pie').toggle()
});

//JQUERY UI for Date Range
$( function() {
    var dateFormat = "mm/dd/yy",
      from = $( "#from" )
        .datepicker({
          defaultDate: "+1w",
          changeMonth: true,
          numberOfMonths: 3
        })
        .on( "change", function() {
          to.datepicker( "option", "minDate", getDate( this ) );
        }),
      to = $( "#to" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3
      })
      .on( "change", function() {
        from.datepicker( "option", "maxDate", getDate( this ) );
      });
 
    function getDate( element ) {
      var date;
      try {
        date = $.datepicker.parseDate( dateFormat, element.value );
      } catch( error ) {
        date = null;
      }
 
      return date;
    }
  } );


//Ajax the search feedbacks results
function ajaxfunction(){
    $.ajax({
        url: $('#feedbacks_form_ajax').attr('action'),
        method: "POST",
        data: $('#feedbacks_form_ajax').serialize(),
        success: function(serverResponse){
        console.log("SUCCESS, this is serverResponse: ", serverResponse)
            $("#feedbacks_ajax_display").html(serverResponse);
        }
    })
}

// Run Ajax when there's any change in the feedbacks_search_form
$("#feedbacks_form_ajax").change(function(){
  console.log("keyup is working for feedback_id")
  ajaxfunction()
});

// if user type in 'id' number, run ajax upon keyup
$("#feedback_id").keyup(function(){
    console.log("keyup is working for feedback_id")
    ajaxfunction()
});

/* NOTE: seralized data is a string of key/value pair data concated by "&" eg) "key1=value1&key2=value2&key3=value3"
If we have multiple of the same key, eg) key1=val1, key1=val2, key1=val3.
Then when it gets to server, the POST will be dict of key and value of an array eg) request.POST['key1'] -> {'key1':['val1', 'val2', 'val3']} */
// $("input[type=checkbox]").click(function(){
//   console.log('This checkbox has been checked # of rating & improv area?', $(this).val() )
//   console.log("this is what form.serialized look like: ", $('#feedbacks_form_ajax').serialize());
//   ajaxfunction()
// })

// If user select one of the email radio's, run ajax
// $("input[type=radio]").click(function(){
//     console.log("radio check is working for feedback_email")
//     ajaxfunction()
// });
// // If user type anything in 'feedback search' run ajax (deprecataed)    
// $("#feedback_contains").keyup(function(){
//     console.log("keyup is working for feedback_id")
//     ajaxfunction()
// });


// Run ajax, if user make changes to the date range
  // $("select[name=feedback_status]").change(function(){
  //     console.log("keyup is working for feedback_id")
  //     ajaxfunction()
  // });


