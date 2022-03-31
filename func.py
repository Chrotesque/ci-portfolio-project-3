import random

def get_entry_lane(level):
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