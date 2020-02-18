from random import randrange
import utilities
import color_samples

testData = color_samples.colorSamples

def countColors(color,testData):
  count = 0
  for value in testData:
    if(value[1] == color):
      count += 1
  return count

#DO NOT CHANGE CODE ABOVE THIS LINE!

#Your task is to write a function using Python that correctly returns a color based on the red, green, and blue values.

#The identifyColor function should return "red","yellow","cyan", or "green" based on the red, green, and blue values. These values are numbers between 0 - 255.

#Your task is to write this function

def identifyColor(colorValues):
  red = colorValues[0]
  green = colorValues[1]
  blue = colorValues[2]
  
  if((red >= 235 and red <= 255) and (green >= 220 and green <= 255) and (blue >= 15 and blue <= 110)):
    return "yellow"
  elif((red >= 0 and red <= 125) and (green >= 220 and green <= 255) and (blue >= 235 and blue <= 255)):
    return "cyan"
  elif((red >= 0 and red <= 105) and (green >= 240 and green <= 255) and (blue >= 55 and blue <= 135)):
    return "green"
  elif((red >= 195 and red <= 255) and (green >= 5 and green <= 70) and (blue >= 25 and blue <= 80)):
    return "red"

  return "unknown"

#This function is designed to figure out how many transitions from one color to the next have occured as the color wheel rotates. One complete rotation should involve eight transitions. This function should call your identifyColor function on the full array of testData

def countTransitions(testData):
  numberOfTransitions = 0
  currentColor = "unknown"
  for value in testData:
    #Your code should go here. Watch the indentation of the code you put below as it should match this one.
    oldColor = currentColor
    currentColor = identifyColor(value[0])
    if(currentColor != oldColor):
      numberOfTransitions += 1

  #Your final answer should be stored in the variable called numberOfTransitions.
  return numberOfTransitions


def testFunction():
  
  redCorrect = 0
  greenCorrect = 0
  yellowCorrect = 0
  cyanCorrect = 0
  for value in testData:
    if(identifyColor(value[0])==value[1]):
      if(value[1] == 'red'):
        redCorrect += 1
      elif(value[1] == 'green'):
        greenCorrect +=1
      elif(value[1] == 'yellow'):
        yellowCorrect += 1
      else:
        cyanCorrect += 1

  correctAnswers = redCorrect + greenCorrect + yellowCorrect + cyanCorrect
  print("Accuracy: {}% of the test data was classified correctly".format(round(correctAnswers*100.0/len(testData))))
  print("{} % of the red data was classified correctly".format(round(redCorrect*100.0/countColors('red',testData),2)))
  print("{} % of the green data was classified correctly".format(round(greenCorrect*100.0/countColors('green',testData),2)))
  print("{} % of the yellow data was classified correctly".format(round(yellowCorrect*100.0/countColors('yellow',testData),2)))
  print("{} % of the cyan data was classified correctly".format(round(cyanCorrect*100.0/countColors('cyan',testData),2)))
  print("{} transitions counted".format(countTransitions(testData)))



testFunction()

