from random import randrange

def getColorSensorData(color):
  redSamples = [(255, 8, 48),(225, 25, 62),(199,33,28),(227,55,57),(227,68,70),(254,13,39),(254,36,56),(254,55,76)]
  greenSamples = [(0,245,69),(0,253,77),(101,253,130),(25,250,113),(59,246,103),(18,247,61),(80,251,90),(18,249,64)]
  yellowSamples = [(247,244,106),(252,248,19),(252,247,51),(248,246,100),(239,248,71),(251,223,83),(249,245,70),(250,238,75)]
  cyanSamples = [(53,241,245),(0,248,256),(0,247,249),(97,247,256),(0,241,240),(122,241,240),(1,226,240),(40,223,240)]

  if (color == "red"):
    randomIndex = randrange(0,len(redSamples))
    baseColor = redSamples[randomIndex]
  elif(color == "yellow"):
    randomIndex = randrange(0,len(yellowSamples))
    baseColor = yellowSamples[randomIndex]
  elif(color == "cyan"):
    randomIndex = randrange(0,len(cyanSamples))
    baseColor = cyanSamples[randomIndex]
  elif(color == "green"):
    randomIndex = randrange(0,len(greenSamples))
    baseColor = greenSamples[randomIndex]
  else:
    return None
  newColor = []
  for color in baseColor:
    newColorSample = color + randrange(-2,3)
    if newColorSample < 0:
      newColorSample = 0
    if newColorSample > 255:
      newColorSample = 255
    newColor.append(newColorSample)


  return (newColor[0],newColor[1],newColor[2])

