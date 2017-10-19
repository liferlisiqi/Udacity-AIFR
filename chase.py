# ----------
# Part Three
#
# Now you'll actually track down and recover the runaway Traxbot.
# In this step, your speed will be about twice as fast the runaway bot,
# which means that your bot's distance parameter will be about twice that
# of the runaway. You can move less than this parameter if you'd
# like to slow down your bot near the end of the chase.
#
# ----------
# YOUR JOB
#
# Complete the next_move function. This function will give you access to
# the position and heading of your bot (the hunter); the most recent
# measurement received from the runaway bot (the target), the max distance
# your bot can move in a given timestep, and another variable, called
# OTHER, which you can use to keep track of information.
#
# Your function will return the amount you want your bot to turn, the
# distance you want your bot to move, and the OTHER variable, with any
# information you want to keep track of.

from robot import *
from math import *
from matrix import *
import random

def compute_circle(measurement1, measurement2, measurement3):
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
    if abs(y1 - y2) < 0.00001: # bug
        k1 = (x2 - x1) / 0.00001
    else:
        k1 = (x2 - x1) / (y1 - y2)

    if abs(y2 - y3) < 0.00001: # bug
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

    return cx, cy, r, alpha, beta, d

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER=None):
    if not OTHER: # first two time return
        OTHER = ([target_measurement], [0.0 for i in range(6)])  # now I can keep track of history
        heading_to_target = get_heading(hunter_position, target_measurement)
        turning = heading_to_target - hunter_heading
        return turning, max_distance, OTHER

    if len(OTHER[0]) > 1:
        OTHER[0].append(target_measurement)
        cx, cy, r, alpha, beta, d = compute_circle(OTHER[0][-3], OTHER[0][-2], OTHER[0][-1])
        print (cx, cy, r, alpha, beta, d)
        if abs(target_measurement[1] - cy) < 0.00001:
            if target_measurement[1] - cy < 0:
                theta = atan2(target_measurement[0] - cx, 0.00001)
            else:
                theta = atan2(target_measurement[0] - cx, -0.00001)
        else:
            theta = atan2(target_measurement[0] - cx, cy - target_measurement[1])
        print (theta)
        target_next_x = target_measurement[0] + r * (sin(beta + theta) - sin(theta))
        target_next_y = target_measurement[1] + r * (cos(theta) - cos(beta + theta))
        heading_to_target = get_heading(hunter_position, (target_next_x, target_next_y))
        turning = heading_to_target - hunter_heading
        distance = distance_between((target_next_x, target_next_y), hunter_position)
        if distance > max_distance:
            distance = max_distance
        return turning, distance, OTHER

    else:  # the second time
        OTHER[0].append(target_measurement)
        heading_to_target = get_heading(hunter_position, target_measurement)
        turning = heading_to_target - hunter_heading
        return turning, max_distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER=None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we
    will grade your submission."""
    max_distance = 1.94 * target_bot.distance  # 1.94 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance  # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:
        print (ctr)
        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        print ("hunter: " + str(hunter_position))
        target_position = (target_bot.x, target_bot.y)
        print ("target: " + str(target_position))
        separation = distance_between(hunter_position, target_position)
        print ("separation: " + str(separation))
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance,
                                                 OTHER)

        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi


def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading


def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all
    the target measurements, hunter positions, and hunter headings over time, but it doesn't
    do anything with that information."""
    if not OTHER:  # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings)  # now I can keep track of history
    else:  # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER  # now I can always refer to these variables

    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning = heading_difference  # turn towards the target
    distance = max_distance  # full speed ahead!
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5) # x, y, heading, turning, distance
# measurement_noise = .05*target.distance
# target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

print demo_grading(hunter, target, next_move)





