from math import *
import random

landmarks = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise = 0.0;
        self.sense_noise = 0.0;

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise = float(new_t_noise);
        self.sense_noise = float(new_s_noise);

    def sense(self):
        # return dstances with four landmark
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'

            # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size  # cyclic truncate
        y %= world_size

        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):

        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
            # using Gaussian distribution to measure the probability weather the particle is near robot
        return prob

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

#calculate the mean error of all the particles with the robot
def eval(r, p):
    sum = 0.0;
    for i in range(len(p)):  # calculate mean error
        dx = (p[i].x - r.x + (world_size / 2.0)) % world_size - (world_size / 2.0)
        dy = (p[i].y - r.y + (world_size / 2.0)) % world_size - (world_size / 2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))


# myrobot = robot()
# myrobot.set_noise(5.0, 0.1, 5.0)
# myrobot.set(30.0, 50.0, pi/2)
# myrobot = myrobot.move(-pi/2, 15.0)
# print myrobot.sense()
# myrobot = myrobot.move(-pi/2, 10.0)
# print myrobot.sense()

####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####
myrobot = robot()
myrobot = myrobot.move(0.1, 5.0)
Z = myrobot.sense()

N = 1000
T = 2
p = []
# run twice means all the following steps is execute twice,
# in another word, all the particles move, sense, and resample twice
for i in range(N):
    x = robot()
    x.set_noise(0.05, 0.05, 5.0)
    p.append(x)

p2 = []
for i in range(N):
    p2.append(p[i].move(0.1, 5.0))
p = p2

w = []
# insert code here!
for i in range(N):
    # w.append(p[i].measurement_prob(p[i].sense())) wrong
    w.append(p[i].measurement_prob(Z))
    # why the parament of measurement_prob() is only Z?
    # because Z is the benchmark of Gaussian function
# print w

#### DON'T MODIFY ANYTHING ABOVE HERE! ENTER CODE BELOW ####
# You should make sure that p3 contains a list with particles
# resampled according to their weights.
# Also, DO NOT MODIFY p.
''''
W = sum(w)
nw = []
nw.append(w[0] / W)
for i in range(1 , N):
    nw.append(nw[i - 1] + w[i] / W)
'''
# print nw

p3 = []

# my way
''''
for i in range(N):
    ran = random.random()
    l = 0
    r = N-1
    while r - l > 1:
        m = l + (r - l) / 2
        if ran < nw[m]:
            r = m
        elif ran > nw[m]:
            l = m
        else:
            p3.append(p[m])
            continue
    p3.append(p[r])
'''

# his way, his way is not good as in his class show
# so he doesn't add the weight together to make a circle
beta = 0.0
index = int(random.random() * N)
wm = max(w)
for i in range(N):
    beta += random.random() * 2.0 * wm
    while w[index] < beta:
        beta -= w[index]
        index = (index + 1) % N
    p3.append(p[index])

print p3
