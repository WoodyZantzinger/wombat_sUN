__author__ = 'woodyzantzinger'


#    0
#  3 X 1
#    2


def wombat(state, time_left):

    #Get core variables

    directions = state["path"]
    orientation = get_orientation(state["arena"])


    #Define Functions
    def path_to_food(arena):
        frontier = Queue()
        visited = {}
        goal = None

        start = arena[3][3]
        start["coords"] = {3, 3}

        frontier.put(start)
        came_from[start] = None

        while not frontier.empty():
            current = frientier.get()
            x, y = current["coords"]
            for xDiff in range(-1, 1):
                for yDiff in range(-1, 1):
                    next = arena[x+xDiff][y+yDiff]
                    if next not in came_from and (next["contents"]["type"] == "food" or next["contents"]["type"] == "open"):
                        next["coords"] = {x+xDiff,y+yDiff}
                        frontier.put(next)
                        came_from[next] = {x,y}
                        if next[""] == "food":
                            goal = next
                            break

        if goal != None:
            path = [goal]
            current = goal
            while current != start:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
        else:
            return None

    def get_orientation(arena):
        return arena[3][3]["contents"]["orientation"]

    def nearest_food(state):
        for row in state["arena"]:
            for block in row:
                if block["contents"]["type"] == "food":
                    return [state.index(row[0]), row.index(block)]
        return [-1, -1]

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
            if orientation == "e": action = "right"
            if orientation == "w": action = "left"
        if dir == "s":
            if orientation == "n": action = "about-face"
            if orientation == "e": action = "left"
            if orientation == "w": action = "right"
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

    #CORE LOGIC

    if len(directions) < 1:
        #We have no previous directions, find some
        directions = path_to_food(state["arena"])
    else:
        #peek at top, turn if needed. If facing the right way, pop off and move
        x,y = directions[len(directions-1)]["coords"]
        if x == 3:
            #We need to move up, down

            if y > 3:
                #move up!
                if orientation == "n":
                    directions.pop()
                    return move()
                else:
                    turn_to("n")
            else:
                #move down!
                if orientation == "s":
                    directions.pop()
                    return move()
                else:
                    turn_to("s")

        elif y == 3:
            #we need to move left / right
            if x < 3:
                #move left!
                if orientation == "w":
                    directions.pop()
                    return move()
                else:
                    turn_to("w")

            else:
                #move right!
                if orientation == "e":
                    directions.pop()
                    return move()
                else:
                    return turn_to("e")
