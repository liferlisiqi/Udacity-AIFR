# ----------
# User Instructions:
#
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid) - 1, len(grid[0]) - 1]  # [4, 5]
cost = 1  # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def min_neighbor(grid, value, x, y):
    if x == goal[0] and y == goal[1]:
        return value[goal[0]][goal[1]]
    min_value = 99
    for i in range(len(delta)):
        x2 = x - delta[i][0]
        y2 = y - delta[i][1]
        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 1:
            if min_value > value[x2][y2]:
                min_value = value[x2][y2]
    return min_value + cost

# fuck, it is so hard to write a recursive
def compute_value_re(grid, cost, value, x, y):
    value[x][y] = min_neighbor(grid, value, x, y)
    grid[x][y] = 1
    for i in range(len(delta)):
        x2 = x - delta[i][0]
        y2 = y - delta[i][1]
        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
            value[x2][y2] = compute_value_re(grid, cost, value, x2, y2)

    return value[x][y]


def compute_value(grid, goal, cost):
    value = [[99 for col in range(len(grid[0]))] for row in range(len(grid))]
    value[goal[0]][goal[1]] = 0
    compute_value_re(grid, cost, value, goal[0], goal[1])
    return value


value = compute_value(grid, goal, cost)
for i in range(len(value)):
    print value[i]
