$(document).ready(function(){
  //initalize variable, "sum" for outputA, "sum2" for outputB
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

  //concate the clicked number on keypad to the existing "sum"
  $('.input_num').click(function(){
    var num = $(this).html()
    if(sum.length > 15 || sum > 100000){
      $('#input_warning').html("eep! The number's too high. Please click 'clear' to restart")
    } else{
      sum = sum+num;
      $('#output_A').html(sum);
      conversion(unit_inputA, unit_inputB, sum)
      $('#input_warning').html()
      };
    console.log()    
  })
    

  //clear the "sum" amount upon click "clear"
  $('#clear').click(function(){
    sum = ''
    $("#output_A").html("")
    $("#output_B").html("")
    $('#input_warning').html()
  })
  //truncate the last number when click "backspace"
  $('#backspace').click(function(){
    sum = parseInt(sum)
    sum = sum/10 | 0;
    $("#output_A").html(sum)
    $('#input_warning').html()
  })
  // //Select one of the output A's units (and stay clicked until other)
  // $('.unitA').click(function(e){
  //   $('.unitA').not(this).removeClass('active');
  //   $(this).toggleClass('active');
  //   e.preventDefault();
  // })

  // //Select one of the output B's units (and stay clicked until other)
  // $('.unitB').click(function(e){
  //   $('.unitB').not(this).removeClass('active');
  //   $(this).toggleClass('active');
  //   e.preventDefault();
  // });

  //Function for calcatating the conversion:
  function conversion(unit_inputA, unit_inputB, sum){
    //INCHES TO INCHES
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