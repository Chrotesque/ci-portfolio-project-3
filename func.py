# Import of 3rd party modules
import random

def sym(symbol):
    """
    Converts a string into a symbol using unicode characters
    https://unicode-table.com/en/blocks/geometric-shapes/
    """
    switchcase = {
        "square":"\u25a0",
        "triangle":"\u25bc",
        "disc":"\u25cf",
        "heart":"\u2665",
        "sword":"\u2694",
        "death":"\u2620"
    }
    
    return switchcase.get(symbol, "nothing")

def get_entry_lane(level):
    """
    Chooses the level entry lane based on a random number and the current level
    Factor numbers specifically chosen for Lane 1 to reach ~40% at Level 10+,
    Lane 2 ~35% and Lane 3 ~25%
    """
    rand_num = random.randrange(1,101)
    lane_factors = {
        1:6.7,
        3:3.12
    }
    lane_ranges = {
        1:0,
        2:0,
        3:0
    }

    if level > 1:
        for i in range(10):
            lane_ranges[1] = 100 - ((level - 1) * lane_factors[1])
            lane_ranges[2] = 100 - ((level - 2) * lane_factors[3])
            i += 1
        
        if rand_num > lane_ranges[2]:
            lane = 3
        elif rand_num >= lane_ranges[1]:
            lane = 2
        else:
            lane = 1
    
    else:
        lane = 1

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

def get_path_options():
    """
    Decides on the amount of avail paths depending on the lane
    """
    test = {
        1:[0,1,1,1], # right
        2:[1,0,1,1], # down
        3:[1,0,1,1], # down
        4:[1,1,2,1], # right
        5:[1,0,2,1], # up
        6:[0,1,1,0]  # right
    }
    return test
