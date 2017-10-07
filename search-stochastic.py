import copy

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0]) - 1]  # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5
failure_prob = (1.0 - success_prob) / 2.0  # Probability(stepping left) = prob(stepping right) = failure_prob

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']  # Use these when creating your policy grid.

def compute_value(grid, value, policy, x, y):
    if x == goal[0] and y == goal[1]:
        return value[goal[0]][goal[1]]
    min_value = 999
    policy_temp = -1
    for i in range(len(delta)):
        temp_value = 0.0
        x_f = x - delta[i][0]
        y_f = y - delta[i][1]
        if x_f >= 0 and x_f < len(grid) and y_f >= 0 and y_f < len(grid[0]): temp_value += value[x_f][y_f] * success_prob
        else: temp_value += 100 * success_prob

        x_l = x - delta[(i + 1) % 4][0]
        y_l = y - delta[(i + 1) % 4][1]
        if x_l >= 0 and x_l < len(grid) and y_l >= 0 and y_l < len(grid[0]): temp_value += value[x_l][y_l] * failure_prob
        else: temp_value += 100 * failure_prob

        x_r = x - delta[(i - 1) % 4][0]
        y_r = y - delta[(i - 1) % 4][1]
        if x_r >= 0 and x_r < len(grid) and y_r >= 0 and y_r < len(grid[0]): temp_value += value[x_r][y_r] * failure_prob
        else: temp_value += 100 * failure_prob

        if min_value > temp_value:
            min_value = temp_value
            policy_temp = i
    if policy_temp >= 0:
        policy[x][y] = delta_name[(policy_temp + 2) % 4]
    return int((min_value + cost_step) * 10000) / 10000.0

def DP_re(grid, value, policy, x, y):
    value[x][y] = compute_value(grid, value, policy, x, y)
    grid[x][y] = 1
    for i in range(len(delta)):
        x2 = x - delta[i][0]
        y2 = y - delta[i][1]
        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
            value[x2][y2] = DP_re(grid, value, policy, x2, y2)

    return value[x][y]

def stochastic_value(grid, goal):
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    value[goal[0]][goal[1]] = 0
    policy[goal[0]][goal[1]] = '*'
    for i in range(50):
        grid2 = copy.deepcopy(grid)
        DP_re(grid2, value, policy, goal[0], goal[1])

    return value, policy #  so easy to return two results

value, policy = stochastic_value(grid, goal)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 100.00, 100.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
