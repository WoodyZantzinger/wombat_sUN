__author__ = 'woodyzantzinger'

def wombat(state, time_left):

    #Get core variables
    if "path" in state:
        directions = state["path"]
    else:
        directions = {}

    orientation = state["arena"][3][3]["contents"]["orientation"]

    #Define Functions

    def path_to(arena, type):
        frontier = []
        came_from = {}
        goal = None

        start = arena[3][3]
        start["coords"] = [3, 3]

        frontier.append(start)
        came_from[str(start["coords"])] = None

        while len(frontier) > 0 and goal == None:
            current = frontier.pop(0)
            x, y = current["coords"]

            for dif in [[-1,0], [1,0], [0,-1], [0,1]] :
                if ((x+dif[0]) < 0 or (x+dif[0]) > 6): continue
                if ((y + dif[1]) < 0 or (y + dif[1]) > 6): continue

                next = arena[x+dif[0]][y+dif[1]]
                next["coords"] = [x + dif[0], y + dif[1]]

                if (next["contents"]["type"] == type or next["contents"]["type"] == "open") and str(next["coords"]) not in came_from:
                    frontier.append(next)
                    came_from[str(next["coords"])] = current

                    if next["contents"]["type"] == type:
                        goal = next
                        break

        if goal != None:
            path = [goal]
            current = goal
        else:
            #return a path to the furthest area we can get to
            available_spaces = []
            tmp = came_from.keys()
            for x in tmp: available_spaces.append(eval(x))

            def getKey(item):
                return abs((item[0]+item[1])-6)

            goal = came_from[ str(sorted(available_spaces, key = getKey).pop()) ]
            path = [goal]
            current = goal

        while current != start:
            current = came_from[str(current["coords"])]
            path.append(current)
        return path[:-1]

    def move():
        return {
            'command': {
                'action': 'move',
                'metadata': {}
            },
            'state': {
                'path': directions,
                'hello': state

            }
        }

    def turn_to(dir):
        action = ""

        if dir == "n":
            if orientation == "s": action = "about-face"
            if orientation == "e": action = "left"
            if orientation == "w": action = "right"
        if dir == "s":
            if orientation == "n": action = "about-face"
            if orientation == "e": action = "right"
            if orientation == "w": action = "left"
        if dir == "e":
            if orientation == "s": action = "left"
            if orientation == "n": action = "right"
            if orientation == "w": action = "about-face"
        if dir == "w":
            if orientation == "s": action = "right"
            if orientation == "e": action = "about-face"
            if orientation == "n": action = "left"
        return {
            'command': {
                'action': 'turn',
                'metadata': {
                    'direction': action
                }
            },
            'state': {
                'path': directions,
                'hello': state

            }
        }

    def move_to(x, y):
        if y == 3:
            # We need to move up, down

            if x < 3:
                # move up!
                if orientation == "n":
                    directions.pop()
                    return move()
                else:
                    return turn_to("n")
            else:
                # move down!
                if orientation == "s":
                    directions.pop()
                    return move()
                else:
                    return turn_to("s")

        elif x == 3:
            # we need to move left / right
            if y < 3:
                # move left!
                if orientation == "w":
                    directions.pop()
                    return move()
                else:
                    return turn_to("w")

            else:
                # move right!
                if orientation == "e":
                    directions.pop()
                    return move()
                else:
                    return turn_to("e")


    #CORE LOGIC

    #find things to shoot

    #find food, if none, find another space to go
    directions = path_to(state["arena"], "food")

    x, y = directions[len(directions) - 1]["coords"]
    return move_to(x, y)
