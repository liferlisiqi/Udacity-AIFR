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

# This function will have to be called multiple times before you
# have enough information to accurately predict the next position.
def estimate_next_pos(measurement, OTHER):
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER
    return xy_estimate, OTHER

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
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
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
test_target.set_noise(0.0, 0.0, 0.0)  # no noise
# measurement_noise = 0.05 * test_target.distance
# test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading(estimate_next_pos, test_target)
