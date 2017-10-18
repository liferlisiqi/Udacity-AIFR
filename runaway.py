# ----------
# Background
#
# A robotics company named Trax has created a line of small self-driving robots
# designed to autonomously traverse desert environments in search of undiscovered
# water deposits.
#
# A Traxbot looks like a small tank. Each one is about half a meter long and drives
# on two continuous metal tracks. In order to maneuver itself, a Traxbot can do one
# of two things: it can drive in a straight line or it can turn.
#
# So to make a right turn, A Traxbot will drive forward, stop, turn 90 degrees,
# then continue driving straight.
#
# This series of questions involves the recovery of a rogue Traxbot. This bot has
# gotten lost somewhere in the desert and is now stuck driving in an almost-circle: it has
# been repeatedly driving forward by some step size, stopping, turning a certain
# amount, and repeating this process...
# Luckily, the Traxbot is still sending all of its sensor data back to headquarters.
#
# In this project, we will start with a simple version of this problem and
# gradually add complexity. By the end, you will have a fully articulated
# plan for recovering the lost Traxbot.
#
# ----------
# Part One
#
# Let's start by thinking about circular motion (well, really it's polygon(duo bian xing) motion
# that is close to circular motion). Assume that Traxbot lives on
# an (x, y) coordinate plane and (for now) is sending you PERFECTLY ACCURATE sensor
# measurements.
#
# ----------
# YOUR JOB
# 1 Figure out the heading angle, step size and the turning angle that Traxbot is moving with.
# 2 Complete the estimate_next_pos function.
#
# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess
# for the robot's next position.
#
# ----------
# YOUR JOB
# Complete the function estimate_next_pos with noisy measurement

from robot import *
from math import *
from matrix import *
import random
import turtle

def compute_circle_center(measurement1, measurement2, measurement3):
    #  last two measurement and the measurement at present
    x1 = measurement1[0]
    y1 = measurement1[1]
    x2 = measurement2[0]
    y2 = measurement2[1]
    x3 = measurement3[0]
    y3 = measurement3[1]

    # the middle point between the adjacent two measurement
    m1x = (x1 + x2) / 2.0
    m1y = (y1 + y2) / 2.0
    m2x = (x2 + x3) / 2.0
    m2y = (y2 + y3) / 2.0

    # two perpendicular bisector
    if abs(y1 - y2) < 0.00001:
        k1 = (x2 - x1) / 0.00001
    else:
        k1 = (x2 - x1) / (y1 - y2)

    if abs(y2 - y3) < 0.00001:
        k2 = (x3 - x2) / 0.00001
    else:
        k2 = (x3 - x2) / (y2 - y3)

    b1 = m1y - m1x * k1
    b2 = m2y - m2x * k2

    # the coordiante of the rotate circle
    if abs(k1 - k2) < 0.00001:
        cx = (b2 - b1) / 0.00001
    else:
        cx = (b2 - b1) / (k1 - k2)
    cy = k1 * cx + b1

    # the redius
    r1 = sqrt((cx - x1) ** 2 + (cy - y1) ** 2)
    r2 = sqrt((cx - x2) ** 2 + (cy - y2) ** 2)
    r3 = sqrt((cx - x3) ** 2 + (cy - y3) ** 2)
    r = (r1 + r2 + r3) /3

    # the steering angle: alpha
    alpha1 = atan2(0.5, r1)
    alpha2 = atan2(0.5, r2)
    alpha3 = atan2(0.5, r3)
    alpha = ((alpha1 + alpha2 + alpha3) / 3) % (2 * pi)

    # the turning angle: beta
    h1 = sqrt((cx - m1x) ** 2 + (cy - m1y) ** 2)
    h2 = sqrt((cx - m2x) ** 2 + (cy - m2y) ** 2)
    beta1 = (acos(h1 / r) * 2) % (2 * pi)
    beta2 = (acos(h2 / r) * 2) % (2 * pi)
    beta = ((beta1 + beta2) / 2) % (2 * pi)

    # the distance
    d1 = beta1 * (r1 + r2) / 2
    d2 = beta2 * (r2 + r3) / 2
    d = (d1 + d2) / 2

    return [cx, cy], r, alpha, beta, d

# This function will have to be called multiple times before you
# have enough information to accurately predict the next position.
def estimate_next_pos(measurement, OTHER):
    if not OTHER:  # this is the first measurement
        OTHER = [measurement]
        return measurement, OTHER
    if len(OTHER) == 1:  # this is the second measurement
        OTHER.append(measurement)
        return measurement, OTHER

    if len(OTHER) == 2:  # this is the third measurement
        cc, r, alpha, beta, d = compute_circle_center(OTHER[0], OTHER[1], measurement)
        theta = ((asin((measurement[0] - cc[0]) / r) + acos((cc[1] - measurement[1]) / r)) / 2) % (2 * pi)
        x_estimate = measurement[0] + r * (sin(beta + theta) - sin(theta))
        y_estimate = measurement[1] + r * (cos(theta) - cos(beta + theta))
        OTHER.pop(0)
        OTHER.append(measurement)
        OTHER.append([cc, r, alpha, beta, theta, d])
        return (x_estimate, y_estimate), OTHER

    cc, r, alpha, beta, d = compute_circle_center(OTHER[0], OTHER[1], measurement)
    cc[0] = 0.8 * OTHER[2][0][0] + 0.2 * cc[0]
    cc[1] = 0.8 * OTHER[2][0][1] + 0.2 * cc[1]
    r = 0.8 * OTHER[2][1] + 0.2 * r
    alpha = 0.8 * OTHER[2][2] + 0.2 * alpha
    beta = 0.8 * OTHER[2][3] + 0.2 * beta
    d = 0.8 * OTHER[2][5] + 0.2 * d

    thetax = asin((measurement[0] - cc[0]) / r)
    thetay = acos((cc[1] - measurement[1]) / r)
    theta = ((thetax + thetay) / 2) % (2 * pi)
    x_estimate = measurement[0] + r * (sin(beta + theta) - sin(theta))
    y_estimate = measurement[1] + r * (cos(theta) - cos(beta + theta))
    OTHER[0] = OTHER[1]
    OTHER[1] = measurement
    OTHER[2] = [cc, r, alpha, beta, theta, d]

    # must return xy_estimate, OTHER
    return (x_estimate, y_estimate), OTHER

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Note that the OTHER variable allows you to store any information that you want.
# Visualization: the red circle represents the measured position of the broken robot,
# the blue arrow represents your prediction for where the broken robot will be,
# and the green turtle represents the true position of where the broken robot will be.
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0

    # For Visualization
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier = 25.0  # change Size of animation

    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.3, 0.3, 0.3)

    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.3, 0.3, 0.3)

    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.3, 0.3, 0.3)

    broken_robot.penup()
    measured_broken_robot.penup()
    prediction.penup()
    # End of Visualization

    while not localized and ctr <= 10:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        print("guess: " + str(position_guess))
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        print("true: " + str(true_position))
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 10:
            print "Sorry, it took you too many steps to localize the target."
        # More Visualization
        measured_broken_robot.setheading(target_bot.heading * 180 / pi)
        measured_broken_robot.goto(measurement[0] * size_multiplier, measurement[1] * size_multiplier - 200)
        measured_broken_robot.stamp()

        broken_robot.setheading(target_bot.heading * 180 / pi)
        broken_robot.goto(target_bot.x * size_multiplier, target_bot.y * size_multiplier - 200)
        broken_robot.stamp()

        prediction.setheading(target_bot.heading * 180 / pi)
        prediction.goto(position_guess[0] * size_multiplier, position_guess[1] * size_multiplier - 200)
        prediction.stamp()
        # End of Visualization
    return localized

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2 * pi / 34.0, 1.5)  # x, y, heading, turning, distance
# test_target.set_noise(0.0, 0.0, 0.0)  # no noise
# [2.1, 4.3], [3.26, 5.25], [4.23, 6.39], [4.97, 7.70], [5.46, 9.12]
# [5.68, 10.60], [5.62, 12.10], [5.29, 13.56], [4.69, 14.94], [3.86, 16.18]
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading(estimate_next_pos, test_target)
