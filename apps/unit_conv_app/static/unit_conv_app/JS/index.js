$(document).ready(function(){
  //initalize variable, "sum" for output_A, "sum2" for output_B
  var sum = '';
  //Determine the initial units
  var unit_inputA = $("input[type=radio][name=unitA]:checked").val();
  console.log("initial unit_inputA:", unit_inputA)
  var unit_inputB = $("input[type=radio][name=unitB]:checked").val();
  console.log("initial unit_inputB:", unit_inputB)
  //Determine the units upon radio click
  $('.containerA').children("input").click(function(){
    unit_inputA = $("input[type=radio][name=unitA]:checked").val();
    console.log("changed unit_inputA: ", unit_inputA);
    conversion(unit_inputA, unit_inputB, sum);
  })
  $('.containerB').children("input").click(function(){
    unit_inputB = $("input[type=radio][name=unitB]:checked").val();
    console.log("changed unit_inputB: ", unit_inputB);
    conversion(unit_inputA, unit_inputB, sum);
  })
  
  //   //Identified the units
  $('.containerA').children("button").click(function(){
    var unit_inputA = $(this).text();
    console.log(unit_inputA);
  })
  $('.containerB').children("button").click(function(){
    var unit_inputB = $(this).text();
    console.log(unit_inputB)
  })
  
  $('.key_warning').hide()
  //concate the clicked number on keypad to the existing "sum"
  $('.input_num').click(function(){
    if(sum == 0){
      sum = ""
    }
    var num = $(this).html()
    if(sum.length > 15 || sum > 100000){
      $('.key_warning').show()
    } else{
      sum = sum+num;
      $('#output_A').html(sum);
      conversion(unit_inputA, unit_inputB, sum)
      $('.key_warning').hide()
    };
    console.log('This is the sum after the click, outside of the function', sum)
    console.log('This is the input_num.val() after the click, outside of the function', $(this).val())

    $.ajax({
      url: "display_image/"+$(this).val(),
      success: function(serverResponse){
        console.log('SUCCESS! This is servereResponse', serverResponse);
        $('.image_placeholder').html(serverResponse);
        $('#image_convert').css('width', '100%');
        $('#image_convert').css('height', '100%');
        $('#image_convert').css('object-fit', 'contain');
        // $(document).on('load',"#image_convert", function(){}
      }
    })    
  })
  //clear the "sum" amount upon click "clear"
  $('#clear').click(function(){
    // $('#image_convert').attr('src', 'static/unit_conv_app/images/can.png')
    sum = ''
    $("#output_A").html("Clear")
    $("#output_B").html("Clear")
    $(".image_placeholder").html("")
    $('.key_warning').hide()
  })
  //truncate the last number when click "backspace"
  $('#backspace').click(function(){
    sum = parseInt(sum)
    if(sum < 10){
      sum = 0
    } else{
    sum = sum/10 | 0;
    }
    $("#output_A").html(sum)
    conversion(unit_inputA, unit_inputB, sum)
    $(".image_placeholder").html("")
  })

  //


  // Create conversion function to be called when keypad's clicked and convert the number
  function conversion(unit_inputA, unit_inputB, sum){
    //INCHES TO INCHES
    // $.ajax({
    //   url: "/display_image"

    // })
    console.log("CONVERSION image change")
    if(unit_inputA == "inches" && unit_inputB == "inches"){
        return $('#output_B').html(sum);
      }
      //INCHES To Feet
      else if(unit_inputA == "inches" && unit_inputB == "feet"){
        outB = sum/12
        return $('#output_B').html(outB.toFixed(2));
      }
      //INCHES to Yards
      else if(unit_inputA == "inches" && unit_inputB == "yards"){
        outB = sum/36
        return $('#output_B').html(outB.toFixed(2));
      }
      //INCHES to miles
      else if(unit_inputA == "inches" && unit_inputB == "miles"){
        outB = sum/63360
        return $('#output_B').html(outB.toFixed(2));
      }
      
      //FEET to Inches
      else if(unit_inputA == "feet" && unit_inputB == "inches"){
        outB = sum*12
        return $('#output_B').html(outB.toFixed(2));
      }
      //FEET to Feet
      else if(unit_inputA == "feet" && unit_inputB == "feet"){
        return $('#output_B').html(sum);
      }

      //FFET to Yard
      else if(unit_inputA == "feet" && unit_inputB == "yards"){
        outB = sum/3
        return $('#output_B').html(outB.toFixed(2));
      }
      //FEET to Mile
      else if(unit_inputA == "feet" && unit_inputB == "miles"){
        outB = sum/5280
        return $('#output_B').html(outB.toFixed(2));
      }

      //YARD to inches
      else if(unit_inputA == "yards" && unit_inputB == "inches"){
        outB = sum*36
        return $('#output_B').html(outB.toFixed(2));
      }
      //YARD to Feet
      else if(unit_inputA == "yards" && unit_inputB == "feet"){
        outB = sum*3
        return $('#output_B').html(outB.toFixed(2));
      }
      //YARD to yard
      else if(unit_inputA == "yards" && unit_inputB == "yards"){
        return $('#output_B').html(sum);
    }
      //YARD to mile
      else if(unit_inputA == "yards" && unit_inputB == "miles"){
        outB = sum/1760
        return $('#output_B').html(outB.toFixed(2));
      }

      //MILE to inches
      else if(unit_inputA == "miles" && unit_inputB == "inches"){
        outB = sum*63360
        return $('#output_B').html(outB.toFixed(2));
      }
      //MILE to feet
      else if(unit_inputA == "miles" && unit_inputB == "feet"){
        outB = sum*5280
        return $('#output_B').html(outB.toFixed(2));
      }
      //MILE to yard
      else if(unit_inputA == "miles" && unit_inputB == "yards"){
        outB = sum*1760
        return $('#output_B').html(outB.toFixed(2));
      }
      //MILE to mile
      else if(unit_inputA == "miles" && unit_inputB == "miles"){
        return $('#output_B').html(sum);
    }
  }
});