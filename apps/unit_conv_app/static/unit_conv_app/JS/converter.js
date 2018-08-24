//Function for calcatating the conversion:
function conversion(unit_inputA, unit_inputB, sum){
    //INCHES TO INCHES
    if(unit_inputA == "inches" && unit_inputB == "inches"){
        return $('#output_B').html(sum);
      }
      //INCHES To Feet
      else if(unit_inputA == "inches" && unit_inputB == "feet"){
        return $('#output_B').html(sum/12);
      }
      //INCHES to Yards
      else if(unit_inputA == "inches" && unit_inputB == "yards"){
        return $('#output_B').html(sum/36);
      }
      //INCHES to miles
      else if(unit_inputA == "inches" && unit_inputB == "miles"){
        return $('#output_B').html(sum/63360);
      }
      
      //FEET to Inches
      else if(unit_inputA == "feet" && unit_inputB == "inches"){
        return $('#output_B').html(sum*12);
      }
      //FEET to Feet
      else if(unit_inputA == "feet" && unit_inputB == "feet"){
        return $('#output_B').html(sum);
      }
  
      //FFET to Yard
      else if(unit_inputA == "feet" && unit_inputB == "yards"){
        return $('#output_B').html(sum/3);
      }
      //FEET to Mile
      else if(unit_inputA == "feet" && unit_inputB == "miles"){
        return $('#output_B').html(sum/5280);
      }
  
      //YARD to inches
      else if(unit_inputA == "yards" && unit_inputB == "inches"){
        return $('#output_B').html(sum*36);
      }
      //YARD to Feet
      else if(unit_inputA == "yards" && unit_inputB == "feet"){
        return $('#output_B').html(sum*3);
      }
      //YARD to yard
      else if(unit_inputA == "yards" && unit_inputB == "yards"){
        return $('#output_B').html(sum);
    }
      //YARD to mile
      else if(unit_inputA == "yards" && unit_inputB == "miles"){
        return $('#output_B').html(sum/1760);
      }
  
      //MILE to inches
      else if(unit_inputA == "miles" && unit_inputB == "inches"){
        return $('#output_B').html(sum*63360);
      }
      //MILE to feet
      else if(unit_inputA == "miles" && unit_inputB == "feet"){
        return $('#output_B').html(sum*5280);
      }
      //MILE to yard
      else if(unit_inputA == "miles" && unit_inputB == "yards"){
        return $('#output_B').html(sum*1760);
      }
      //MILE to mile
      else if(unit_inputA == "miles" && unit_inputB == "miles"){
        return $('#output_B').html(sum);
    }
}