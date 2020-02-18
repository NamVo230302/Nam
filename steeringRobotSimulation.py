# Write your code here :-)
import robot
from math import *
import time

import pygame



#create a new robot
myRobot = robot.robot()
# usage: myRobot.set(x-coordinate,y-coordinate, orientation in radians)
myRobot.set(0,0,pi/2)


#****************************************************************************#
# Mr. Weinberg's example functions are here:
def runStraightTwoSeconds():
  #Run robot straight with both motors at 10 cm/s for 1.0 seconds
  straightTime = 2.0
  myRobot.set_motor_velocity(50.0,50.0)
  while(myRobot.timer < straightTime):
    myRobot.update()

def driveStraightOneMeter():
  myRobot.reset_encoders()
  while(myRobot.left_encoder < 100.0):
    myRobot.set_motor_velocity(50,50)
    myRobot.update()
  print(myRobot)

def turnEastProportionalControl():
  # This sets up a proportional control loop to turn to a compass heading of 90 (East)
  #This control loop controls the left motor velocity based on the turn error from a compass heading of 90 degrees (East).
  # The right motor stays off (zero velocity).

  k = 1.5
  robot_compass_setpoint = 90.0 # Compass heading of 90 degrees is East

  #Calculate initial error
  error = robot_compass_setpoint - myRobot.compass

  while(abs(error) > 0.1):
    myRobot.update()
    error = robot_compass_setpoint - myRobot.compass
    outputVelocity = k*error
    #based on the error, move the left motor forward and keep the right motor stopped.
    myRobot.set_motor_velocity(outputVelocity,0)
    #print(myRobot)

def driveStraightDistanceProportionalControl():
  # This sets up a proportional control loop to drive to a position of 100.0 centimeters headed in a North direction
  #This control loop controls the left motor velocity based on the turn error from a compass heading of 90 degrees (East).
  # The right motor stays off (zero velocity).

  k = 1.5
  robot_encoder_setpoint = 100.0 # Travel distance of 100.0

  #Calculate initial error
  error = robot_encoder_setpoint - myRobot.left_encoder

  while(abs(error) > 1.0):
    myRobot.update()
    error = error = robot_encoder_setpoint - myRobot.left_encoder
    outputVelocity = k*error
    #based on the error, move both motors forward.
    myRobot.set_motor_velocity(outputVelocity,outputVelocity)

  #stop the robot
  myRobot.set_motor_velocity(0,0)
#                                                                            #
#****************************************************************************#
# Now it's time for you to write your functions.

def driveSquare():
    # Write code that makes the robot drive in a square. Simplest code wins.
    for i in range(4):
        #print(myRobot.compass)
        driveStraightDistance(150)
        #turnEastProportionalControl()
        leftTurn()
        myRobot.reset_encoders()
    #leave this last line
    print(myRobot)


def driveCircle():
    # Write code that drives the robot in a circle that fills the green screen, but doesn't go outside of it.
    driveStraightDistance(150)

    while (not myRobot.compass > 89):
        myRobot.reset_encoders()
        myRobot.set_motor_velocity(50, 25)
    #leave this last line
    print(myRobot)

def leftTurn():
    # Write code that turns the robot 90 degrees by running the motors for a given amount of time.
    k = 2
    robot_compass_setpoint = myRobot.compass + 90
    error = robot_compass_setpoint - myRobot.compass

    while(abs(error) > 0.1):
        myRobot.update()
        outputVelocity = k*error
        myRobot.set_motor_velocity(outputVelocity, 0)
        error = robot_compass_setpoint - myRobot.compass
    #leave this last line
    print(myRobot)


def driveStraightDistance(distance):
    # Write code that drives the robot straight for an input distance in centimeters using the encoders.
    # Use a proportional control to do this and make it fast.
    k = 2
    error = distance - myRobot.left_encoder

    while(abs(error) > 1.0):
        myRobot.update()
        error = distance - myRobot.left_encoder
        outputVelocity = k*error
        myRobot.set_motor_velocity(outputVelocity,outputVelocity)
    #leave this last line
    print(myRobot)


#****************************************************************************#
# Call your functions below.

#runStraightTwoSeconds()
#driveStraightOneMeter()
#turnEastProportionalControl()
#myRobot.reset_encoders()
#driveStraightDistanceProportionalControl()
#driveSquare()
#driveStraightDistance(200)
leftTurn()
#driveCircle()


print(myRobot)


#****************************************************************************#
# KEEP THE CODE BELOW THE SAME! THAR PIRATES BE...

WIDTH, HEIGHT = 800,  800
backgroundColor = 80,  150,  80

frameCount = 0
robot_image = Actor('robot_small.png')



def draw():
    global frameCount
    global myRobot
    global robot_image

    screen.fill(backgroundColor)
    #robot_image.pos = 0,0
    #robot_image.draw()
    if(frameCount<len(myRobot.history[0])):
        showRobot(myRobot.history[0][frameCount],myRobot.history[1][frameCount],myRobot.history[2][frameCount])
    frameCount += 1
    time.sleep(0.05)

def update():
    global frameCount
    global myRobot


    #screen.fill(backgroundColor)
    if(frameCount<len(myRobot.history[0])):
        showRobot(myRobot.history[0][frameCount],myRobot.history[1][frameCount],myRobot.history[2][frameCount])


    frameCount += 1


def showRobot(x,y,orientation):

    robot_image.center = x, y

    robot_image.angle = -orientation*180.0/3.14159
    robot_image.draw()

