# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
# Have your robot turn clockwise by pi/2, move
# 15 m, and sense. Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
#
# Your program should print out the result of
# your two sense measurements.
#
# Don't modify the code below. Please enter
# your code at the bottom.

from math import *
import random



landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 500.0


class robot:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0 #angle measured in radians. Zero angle is directed East, North is pi/2 radians

        self.timer = 0.0
        self.loopTime = 0.02 #seconds for control loop to run
        self.velocity = 0.0
        self.left_motor_velocity = 0.0
        self.right_motor_velocity = 0.0
        self.wheel_base = 25.0 #cm distance between drive wheels
        self.wheel_radius = 8.0 #cm
        self.max_speed = 50.0

        #add simulated sensors
        self.left_encoder = 0.0
        self.right_encoder = 0.0
        self.compass = 0.0 #Zero degrees is North. This is to match a traditional compass.

        #advanced settings for simulating noisy sensors - leave at zero for now
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0

        #add a history of coordinates for plotting later often
        self.history = [[],[],[]]
        self.loopCount = 0
        self.reportInterval = 1


    #when setting the position of a new robot, check for location in the world
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise (ValueError, 'X coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise (ValueError, 'Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise (ValueError, 'Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        self.compass = ( pi/2.0 - self.orientation ) * 180.0/pi


    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);

    def move_motors_distance(self,left_distance,right_distance):
        if(left_distance==right_distance):
            new_x = self.x+right_distance*cos(self.orientation)
            new_y = self.y+right_distance*sin(self.orientation)
            new_orientation = self.orientation
        else:
            new_orientation = (right_distance - left_distance)*1./self.wheel_base + self.orientation
            new_x = self.x + 0.5*self.wheel_base*(left_distance+right_distance)*1./(right_distance - left_distance)*(sin(new_orientation)- sin(self.orientation))
            new_y = self.y - 0.5*self.wheel_base*(left_distance+right_distance)*1./(right_distance - left_distance)*(cos(new_orientation)- cos(self.orientation))

        self.x = new_x
        self.y = new_y
        self.orientation = new_orientation % (2*pi)

    def set_motor_velocity(self,left_velocity,right_velocity):
        if(abs(left_velocity)>self.max_speed):
            left_velocity = self.max_speed
        if(abs(right_velocity))> self.max_speed:
            right_velocity=self.max_speed
        self.left_motor_velocity = left_velocity
        self.right_motor_velocity = right_velocity

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def set_velocity(self,velocity,angle):
      self.orientation = angle
      self.velocity = velocity

    def update_compass(self):
      self.compass = ( pi/2.0 - self.orientation ) * 180.0/pi

    def reset_encoders(self):
      self.left_encoder = 0
      self.right_encoder = 0



    def update(self):

      self.move_motors_distance(self.left_motor_velocity*self.loopTime,self.right_motor_velocity*self.loopTime)
      self.left_encoder += self.left_motor_velocity*self.loopTime
      self.right_encoder += self.right_motor_velocity*self.loopTime
      self.update_compass()
      self.loopCount += 1
      self.timer += self.loopTime
      if(self.loopCount%self.reportInterval == 0):
        self.history[0].append(self.x)
        self.history[1].append(self.y)
        self.history[2].append(self.orientation)



    def move(self, turn, forward):
        #if forward < 0:
        #    raise (ValueError, "Robot can't move backwards" )

        # turn, and add randomness to the turning command
        orientation = self.orientation  + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)

        self.x = self.x + (cos(orientation) * dist)
        self.y = self.y + (sin(orientation) * dist)
        #x %= world_size    # cyclic truncate
        #y %= world_size

        # set particle
        #res = robot()
        #res.set(x, y, orientation)
        #res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        #return res

    def Gaussian(self, mu, sigma, x):

        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def reset_timer(self):
      self.timer = 0

    def __repr__(self):
        return "[t = {} x= {} y= {} orient= {} compass = {} left_encoder = {} right_encoder = {}]".format(round(self.timer,2),round (self.x,2), round(self.y,2), round(self.orientation,2),round(self.compass,0),round(self.left_encoder,1),round(self.right_encoder,1))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))


'''
####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####

# Make a robot called myrobot that starts at
# coordinates 30, 50 heading north (pi/2).
myrobot = robot()
myrobot.set(30, 50, pi/2)
print(myrobot)

# Have your robot turn clockwise by pi/2, move
# 15 m, and sense.
myrobot = myrobot.move(-pi/2, 15)
print(myrobot.sense())

# Then have it turn clockwise
# by pi/2 again, move 10 m, and sense again.
myrobot = myrobot.move(-pi/2, 10)
print(myrobot.sense())
'''
