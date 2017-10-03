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

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]  # [4, 5]
cost = 1

delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

def search(grid,init,goal,cost):
    row = len(grid)
    col = len(grid[0])
    open_list = [[0, init[0], init[1]]]
    # so ugly, change to one list with element of list of three element
    while len(open_list) != 0:
        g_min_index = 0
        for i in range(1, len(open_list)):
            if open_list[g_min_index][0] > open_list[i][0]:
                g_min_index = i
        next = open_list.pop(g_min_index)
        g = next[0]
        x = next[1]
        y = next[2]
        grid[x][y] = 1

        for i in range(len(delta)):
            x2 = x + delta[i][0]
            y2 = y + delta[i][1]
            # if the grid is over the board
            if x2 >= 0 and x2 < row and y2 >= 0 and y2 < col:
                # if the grid is occupied and is not the goal
                if grid[x2][y2] == 0 and (x2 != goal[0] or y2 != goal[1]):
                    grid[x2][y2] = 1
                    open_list.append([g + cost, x2, y2])
                # find the goal
                elif x2 == goal[0] and y2 == goal[1]:
                    return str([g + cost, x2, y2])
        print "expand gird: " + str(next)
        print "open list: " + str(open_list)

    return 'fail'
# why my output is wrong?
print search(grid, init, goal, cost)
