import random
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
#
# this is the Robot class
#

class Robot(object):
    def __init__(self, length=20.0):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets a robot coordinate.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # make a new copy
        res = Robot()
        res.length = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            res.x = self.x + distance2 * np.cos(self.orientation)
            res.y = self.y + distance2 * np.sin(self.orientation)
            res.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * np.pi)
            res.x = cx + (np.sin(res.orientation) * radius)
            res.y = cy - (np.cos(res.orientation) * radius)

        return res

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)


# ------------------------------------------------------------------------
#
# run - does a single control run

def run(myrobot, tau_p, tau_d, tau_i, n = 300, speed = 1.0):
    x_trajectory = [myrobot.x]
    y_trajectory = [myrobot.y]
    int_cte = 0.0
    cte = myrobot.y
    # systematic bias, can not be done by proportional and differential, can be solved by integral
    # PID control, why make a circle?
    myrobot.set_steering_drift(10.0 / 180.0 * np.pi)
    for i in range(n):
        # a big bug here, the differential is zero all the time
        diff_cte = myrobot.y - cte
        cte = myrobot.y
        int_cte += myrobot.y
        steer = -tau_p * cte - tau_d * diff_cte - tau_i * int_cte
        myrobot = myrobot.move(steer, speed)
        x_trajectory.append(myrobot.x)
        y_trajectory.append(myrobot.y)
    return x_trajectory, y_trajectory


robot = Robot()
robot.set(0, 1, 0)
x_trajectory, y_trajectory = run(robot, 0.2, 3.0, 0.01)
n = len(x_trajectory)

plt.plot(x_trajectory, y_trajectory, 'g', label='PD controller')
plt.plot(x_trajectory, np.zeros(n), 'r', label='reference')
plt.legend()
plt.show()