# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached.
#
# ??? what are you talking about? what does the total change
# observed in the update steps mean?
# ok, i know, it is represented by the total error of x and y for each point
# abs(delta x) + abs(delta y), and the tolerance is for the error
# between newpath and the update of newpath
#
# The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite
# correct).
# -----------

from copy import deepcopy

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path, newpath):
    for old, new in zip(path, newpath):
        print '[' + ', '.join('%.3f' % x for x in old) + \
              '] -> [' + ', '.join('%.3f' % x for x in new) + ']'


# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]


def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.000001):
    # Make a deep copy of path into newpath
    newpath = deepcopy(path)
    error = 1
    while error > tolerance:
        error = 0.0
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                temp = newpath[i][j]
                newpath[i][j] += weight_data * (path[i][j] - newpath[i][j]) + \
                                 weight_smooth * (newpath[i - 1][j] + newpath[i + 1][j] - 2.0 * newpath[i][j])
                error += abs(newpath[i][j] - temp)



    return newpath  # Leave this line for the grader!

newpath = smooth(path)
printpaths(path, smooth(path))
