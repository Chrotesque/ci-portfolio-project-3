# Import of 3rd party modules
import random
import numpy.random as np

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
        "death":"\u2620"
    }
    
    return switchcase.get(symbol, "nothing")

def get_entry_lane(level):
    """
    Chooses the level entry lane based on a probability and level
    """
    lanes = [1,2,3]
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

def get_coords(coords):
    """
    Converts normalized coordinates to actual grid coordinates
    """
    result = [0,0]

    # x - lanes/rows
    result[0] = coords[0] * 2 + 1

    # y - columns
    result[1] = 7 + 4 * coords[1]

    return result

def advance_coords():
    """
    Advances coordinates for path creation
    """
    return [False, True, False] # for testing purposes

def get_path_options(prev_coords, coords):
    """
    Decides on the amount of avail paths depending on the lane
    """
           

        
def can_advance(prev_coords, coords, mode=0):
    """
    Returns a dictionary of booleans to indicate in which direction
    a path can be generated based on a previous and current set of
    coordinates
    """
    advance = {
        "up":True,
        "right":True,
        "down":True,
        "left":True
    }

    # map boundaries
    if coords[0] == 0:
        advance["up"] = False
    elif coords[0] == 4:
        advance["down"] = False
    
    if coords[1] == 0:
        advance["left"] = False
    elif coords[1] == 16:
        advance["right"] = False

    # inner map movements
    if prev_coords[1] < coords[1]:
        advance["left"] = False
    elif prev_coords[1] > coords[1]:
        advance["right"] = False

    if prev_coords[0] < coords[0]:
        advance["up"] = False
    elif prev_coords[0] > coords[0]:
        advance["down"] = False
  
    # mode 1 being called by path generation, 
    if mode == 1:
        advance["left"] = False

    return advance