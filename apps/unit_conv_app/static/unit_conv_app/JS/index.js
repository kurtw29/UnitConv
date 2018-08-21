$(document).ready(function(){
  //initalize variable, "sum" for outputA
  var sum = ""
  //concate the clicked number on keypad to the existing "sum"
  $('.input_num').click(function(){
    var num = $(this).html()
    sum = sum+num
    $("#outputA").html(sum)
  })
  //clear the "sum" amount upon click "clear"
  $('#clear').click(function(){
    sum = " "
    $("#outputA").html(sum)
  })
  //truncate the last number when click "backspace"
  $('#backspace').click(function(){
    sum = parseInt(sum)
    sum = sum/10 | 0;
    $("#outputA").html(sum)
  })
  //Select one of the output A's units (and stay clicked until other)
  $('.unitA').click(function(e){
    $('.unitA').not(this).removeClass('active');
    $(this).toggleClass('active');
    e.preventDefault();
  })

  //Select one of the output B's units (and stay clicked until other)
  $('.unitB').click(function(e){
    $('.unitB').not(this).removeClass('active');
    $(this).toggleClass('active');
    e.preventDefault();
  })

});
