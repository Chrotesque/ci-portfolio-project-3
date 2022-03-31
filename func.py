import random

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
            result = 3
        elif rand_num >= lane_ranges[1]:
            result = 2
        else:
            result = 1
    
    else:
        result = 1

    return result

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

