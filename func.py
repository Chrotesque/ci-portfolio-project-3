# Import of 3rd party modules
import random
import numpy.random as np

ROW_INC = 4

def sym(symbol):
    """
    Converts a string into a symbol using unicode characters
    https://unicode-table.com/en/blocks/geometric-shapes/
    """
    switchcase = {
        "square":"\u25a0",
        "tridown":"\u25bc",
        "triright":"\u25ba",
        "disc":"\u25cf",
        "heart":"\u2665",
        "sword":"\u2694",
        "death":"\u2620",
        "hamburger":"\u1f354",
        "star":"\u2605",
        "dir_west":"\u25c1",
        "dir_east":"\u25b7",
        "dir_north":"\u25b3",
        "dir_south":"\u25bd"
    }
    
    return switchcase.get(symbol, "nothing")

def get_entry_lane(level):
    """
    Chooses the level entry lane based on a probability and level
    """
    lanes = [1,2,3]
    level = 11 if level > 11 else level
    probabilities = [
        1 - 0.06 * (level-1),
        0 + 0.04 * (level-1),
        0 + 0.02 * (level-1)
    ]
    lane = np.choice(lanes, 1, p=probabilities)

    return lane

def get_entry_side(lane):
    """
    Decides the lane side for lanes 2 & 3
    """
    rand_num = random.randrange(1,3)
    if lane == 2:
        if rand_num > 1:
            side = 3 # lane 2 top
        else:
            side = 7 # lane 2 bottom
    elif lane == 3:
        if rand_num > 1:
            side = 1 # lane 3 top
        else:
            side = 9 # lane 3 bottom
    else:
        side = 5 # lane 1
    
    return side

def lane_to_xcoord(lane):
    """
    Converts the initial lane (side rather) to the x coordinate
    """
    return int((lane-1)/2)

def get_coords(coords, reverse=False):
    """
    Converts coordinates from/to normalized to grid coordinates
    """
    result = [0,0]

    if reverse == False:
        # x - lanes/rows
        result[0] = coords[0] * 2 + 1
        # y - columns
        result[1] = 7 + 4 * coords[1]
    else:
        # x - lanes/rows
        result[0] = int((coords[0] - 1) / 2)
        # y - columns
        result[1] = int((coords[1] - 7) / 4)

    return result

def get_path_options(prev_coords, coords, exclude_left, create_exit):
    """
    Creates a path based on probabilities with properties to exclude 
    left and right for main path creation vs branch creation
    """
    lane = coords[0]
    row = coords[1]
    options = {}

    # probabilities
    if lane == 0:
        options["right"] = 0.3
        options["down"] = 0.4
        options["left"] = 0.3
    elif lane == 1:
        options["up"] = 0.2
        options["right"] = 0.25
        options["down"] = 0.3
        options["left"] = 0.25
    elif lane == 2:
        options["up"] = 0.25
        options["right"] = 0.25
        options["down"] = 0.25
        options["left"] = 0.25
    elif lane == 3:
        options["up"] = 0.3
        options["right"] = 0.25
        options["down"] = 0.2
        options["left"] = 0.25
    else: #lane == 4
        options["up"] = 0.4
        options["right"] = 0.3
        options["left"] = 0.3
        
    # option removal
    # going up
    if prev_coords[0] > coords[0] and "down" in options:
        del options["down"]
    # going down
    if prev_coords[0] < coords[0] and "up" in options:
        del options["up"]
    # going left
    if prev_coords[1] > coords[1] and "right" in options:
        del options["right"]
    # going right
    if prev_coords[1] < coords[1] and "left" in options:
        del options["left"]
    
    # can't go left
    if "left" in options and row == 0:
        del options["left"]
    # can't go right
    if "right" in options and row == 17 and create_exit == False:
        del options["right"]
    # can't go up
    if "up" in options and lane == 0:
        del options["up"]
    # can't go down
    if "down" in options and lane == 4:
        del options["down"]

    # for main path generation, to never go left
    if "left" in options and exclude_left == True:
        del options["left"]

    key_to_list = list(options.keys())
    val_to_list = list(options.values())

    # add probability difference to remaining probabilities
    if len(val_to_list) < 4 and len(val_to_list) != 0:
        diff = (1 - sum(val_to_list)) / len(val_to_list)
        for i in range(len(val_to_list)):
            val_to_list[i] += diff

    if len(val_to_list) != 0:
        result = np.choice(key_to_list, 1, p=val_to_list)
    else:
        result = "none"

    #print(result)
    return result

def next_coordinate(coords, direction):
    """
    Returns the coordinate of the room after the next move based on the direction
    """
    if direction == "up":
        coords[0] -= 1
    elif direction == "down":
        coords[0] += 1
    elif direction == "right":
        coords[1] += 1
    else: # direction == "left"
        coords[1] -= 1
    return coords


#