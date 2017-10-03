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
    open_list = [init]
    # so ugly, change to one list with element of list of three element
    g_value = [0]
    while len(open_list) != 0:
        g_min_index = g_value.index(min(g_value))
        expand = open_list[g_min_index]

        for i in range(len(delta)):
            move = delta[i]
            print expand
            print move
            successor = [expand[0] + move[0], expand[1] + move[1]]
            print successor
            if successor[0] < 0 or successor[0] > row - 1 or successor[1] < 0 or successor[1] > col - 1:
                continue
            elif grid[successor[0]][successor[1]] == 1:
                continue
            else:
                print "expand: " + str(g_value.pop(g_min_index)) + ' ' + str(open_list.pop(g_min_index))
                open_list.append(successor)

                g_value.append(g_value[g_min_index] + cost)


        print expand

    return 'fail'

search(grid, init, goal, cost)
