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


def make_robot():
    """
    Resets the robot back to the initial position and drift.
    You'll want to call this after you call `run`.
    """
    robot = Robot()
    robot.set(0, 1, 0)
    robot.set_steering_drift(10 / 180 * np.pi)
    return robot

def run(myrobot, params, n = 100, speed = 1.0):
    x_trajectory = [myrobot.x]
    y_trajectory = [myrobot.y]
    int_cte = 0.0
    pre_cte = myrobot.y
    error = 0.0
    # systematic bias, can not be done by proportional and differential, can be solved by integral
    # PID control, why make a circle?
    for i in range(2 * n):
        # a big bug here, the differential is zero all the time
        cte = myrobot.y
        diff_cte = cte - pre_cte
        pre_cte = cte
        int_cte += cte
        steer = -params[0] * pre_cte - params[1] * diff_cte - params[2] * int_cte
        myrobot = myrobot.move(steer, speed)
        x_trajectory.append(myrobot.x)
        y_trajectory.append(myrobot.y)
        if i > n:
            error += cte**2
    return x_trajectory, y_trajectory, error / n

# Make this tolerance bigger if you are timing out!
# don not understand, what are you talking about?
def twiddle(tol=0.2):
    # TODO: Add code here
    # Don't forget to call `make_robot` before you call `run`!
    p = [0, 0, 0]
    dp = [1, 1, 1]
    #dp[1] = 0.0
    robot = make_robot()
    best_error = run(robot, p)[2]
    # there are three parameters, how can only get one?
    # only a brackets will work

    it = 0
    while sum(dp) > tol:
        print("Iteration {}, parameters {},best error = {}".format(it, p, best_error))
        for i in range(3):
            p[i] += dp[i]
            robot = make_robot()
            error = run(robot, p)[2]

            if error < best_error:  # if better
                best_error = error  # update best_error
                dp[i] *= 1.1        # increment dp[i]
            else:               # worse, try the other direction
                p[i] -= 2 * dp[i]
                robot = make_robot()
                error = run(robot, p)[2]  # the other direction try

                if error < best_error:  # if better
                    best_error = error  # update best_error
                    dp[i] *= 1.1        # increment dp[i]
                else:
                    p[i] += dp[i]   # two directions will both be worse, it seams that dp[i] is too big
                    dp[i] *= 0.9    # so decrease dp[i]
        it += 1
    return p

params = twiddle()
robot = make_robot()
x_trajectory, y_trajectory, error = run(robot, params)
n = len(x_trajectory)

plt.plot(x_trajectory, y_trajectory, 'g', label='PD controller')
plt.plot(x_trajectory, np.zeros(n), 'r', label='reference')
plt.legend()
plt.show()