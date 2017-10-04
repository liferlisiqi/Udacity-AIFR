# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0],
#         [0, 0, 1, 1, 1, 0],
#         [0, 0, 0, 0, 1, 0]]

# grid = [[0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0],
#         [0, 0, 1, 0, 1, 0]]

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

# grid = [[0, 1, 1, 1, 1],
#         [0, 1, 0, 0, 0],
#         [0, 0, 0, 1, 0],
#         [1, 1, 1, 1, 0],
#         [0, 0, 0, 1, 0]]

heuristic = [[9, 8, 7, 6, 5, 4],
             [8, 7, 6, 5, 4, 3],
             [7, 6, 5, 4, 3, 2],
             [6, 5, 4, 3, 2, 1],
             [5, 4, 3, 2, 1, 0]]

# unconnected component, how to do? don't warry, is not have to consider
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]  # [4, 5]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost):
    row = len(grid)
    col = len(grid[0])
    open_list = [[0, init[0], init[1]]]
    path = [[' ' for c in range(col)] for r in range(row)]
    expand = [[-1 for c in range(col)] for r in range(row)]
    g_value = 0

    # print expand
    # what is the order of init of 2D array?is he wrong? mistake col with row? yes, i am right

    while len(open_list) != 0:
        g_min_index = 0
        for i in range(1, len(open_list)):
            f_value = open_list[i][0] + heuristic[open_list[i][1]][open_list[i][2]]
            f_value_min = open_list[g_min_index][0] + heuristic[open_list[g_min_index][1]][open_list[g_min_index][2]]
            if f_value_min > f_value:
                g_min_index = i
        next = open_list.pop(g_min_index)
        g = next[0]
        x = next[1]
        y = next[2]
        grid[x][y] = 1
        expand[x][y] = g_value
        g_value += 1

        for i in range(len(delta)):
            x2 = x + delta[i][0]
            y2 = y + delta[i][1]
            # if the grid is over the board
            if x2 >= 0 and x2 < row and y2 >= 0 and y2 < col:
                # if the grid is occupied and is not the goal
                if grid[x2][y2] == 0 and (x2 != goal[0] or y2 != goal[1]):
                    grid[x2][y2] = 1
                    path[x2][y2] = delta_name[i]
                    open_list.append([g + cost, x2, y2])
                # find the goal
                elif x2 == goal[0] and y2 == goal[1]:
                    path[x2][y2] = delta_name[i]
                    expand[x2][y2] = g_value
                    # return path
                    #return str([g + cost, x2, y2])
                    return str(expand)
        #print "expand gird: " + str(next)
        #print "open list: " + str(open_list)

    return str(expand)

# return the path, must be the same ? it is ridiculous
def path(deltas):
    paths = [[' ' for c in range(len(deltas[0]))] for r in range(len(deltas))]
    paths[goal[0]][goal[1]] = '*'
    grid = [goal[0], goal[1]]
    while grid != init:
        delta_temp = deltas[grid[0]][grid[1]]
        delta_index = delta_name.index(delta_temp)
        grid = [grid[0] - delta[delta_index][0], grid[1] - delta[delta_index][1]]
        paths[grid[0]][grid[1]] = delta_temp
    return paths


# why my output is wrong? no

print search(grid, init, goal, cost)
#deltas = search(grid, init, goal, cost)
#print path(deltas)
