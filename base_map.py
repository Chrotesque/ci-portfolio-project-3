# Import of 3rd party modules
import random as r
import colorama as c

# Import of game specific modules
import func

class BaseMap:

    MAP = []
    ROOMS = {
            "closed":[],
            "open":[]
    }

    def __init__(self, level):
        self.level = level
        self.lane = func.get_entry_lane(self.level)
        self.side = func.get_entry_side(self.lane)

    def set_base_map(self):
        """
        Creates the base map layout in list format
        """
        self.MAP = [
        "     +===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+",
        " L3  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
        "     +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+",
        " L2  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
        "     +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+",
        " L1  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
        "     +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+",
        " L2  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
        "     +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+",
        " L3  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |",
        "     +===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+===+"
        ]

    def set_entry(self):
        """
        Decides and sets the entry into the level based on level
        """
        entry = func.sym("triright")

        # extracts and transforms string from map list into list
        list_from_map_lane = list(self.MAP[self.side])  
        # placing entry starting at index 5
        list_from_map_lane[5] = entry 
        # converting list back to string and placing it back
        self.MAP[self.side] = "".join(list_from_map_lane) 

    def set_exit(self, coords):
        """
        Sets the exit into the level at the paths end
        """
        exit = func.sym("tridown")

        list_from_map_lane = list(self.MAP[coords[0]])
        list_from_map_lane[coords[1]+2] = exit
        self.MAP[coords[0]] = "".join(list_from_map_lane)

    def set_path(self):
        """
        Creates and sets the main path through the level
        """
        prev_coords = [func.lane_to_xcoord(self.side),0]
        readable_coords = prev_coords[:]

        while readable_coords[1] < 18:
            path = func.get_path_options(prev_coords, readable_coords, True, True)
            prev_coords = readable_coords[:]
            real_coords = func.get_coords(readable_coords)
            readable_coords = func.next_coordinate(readable_coords, path)
            self.remove_wall(real_coords, path)
            if readable_coords[1] == 18:
                self.set_exit(real_coords)

    def set_branches(self):
        """
        Creates and sets branches through the level until they hit an open room
        """
        prev_coords = self.ROOMS["closed"][r.randrange(0,len(self.ROOMS["closed"]))]

        list_map = list(self.MAP[prev_coords[0]]) # temp
        list_map[prev_coords[1]] = func.sym("disc") # temp
        self.MAP[prev_coords[0]] = "".join(list_map) # temp

        prev_coords = func.get_coords(prev_coords, True)
        readable_coords = prev_coords[:]


        i = 0
        while i < 10:
            branch = func.get_path_options(prev_coords, readable_coords, False, False)
            prev_coords = readable_coords[:]
            real_coords = func.get_coords(readable_coords)
            print(f"coords before removal: {readable_coords}")
            readable_coords = func.next_coordinate(readable_coords, branch) 
            print(f"coords next: {readable_coords}")
            
            if self.check_room(readable_coords) == False:
                self.remove_wall(real_coords, branch)
                break
            self.remove_wall(real_coords, branch)
            i += 1
  

    def remove_wall(self, coords, side, replacer=" "):
        """
        Removes a wall of a given side based off of coordinates and returns
        changed coordinates in accordance with the walls direction
        """
        if side == "up":
            wall = list(self.MAP[coords[0]-1])
            wall[coords[1]-1] = replacer
            wall[coords[1]] = replacer
            wall[coords[1]+1] = replacer
            self.MAP[coords[0]-1] = "".join(wall)
        elif side == "down":
            wall = list(self.MAP[coords[0]+1])
            wall[coords[1]-1] = replacer
            wall[coords[1]] = replacer
            wall[coords[1]+1] = replacer
            self.MAP[coords[0]+1] = "".join(wall)
        elif side == "right":
            wall = list(self.MAP[coords[0]])
            wall[coords[1]+2] = replacer
            self.MAP[coords[0]] = "".join(wall)
        else: # side == "left"
            wall = list(self.MAP[coords[0]])
            wall[coords[1]-2] = replacer
            self.MAP[coords[0]] = "".join(wall)

    def check_room(self, coords):
        """
        WIP
        """
        print(f"b4: {coords}")
        coords = func.get_coords(coords)
        print(f"aft: {coords}")
        top = list(self.MAP[coords[0]-1])
        mid = list(self.MAP[coords[0]])
        bot = list(self.MAP[coords[0]+1])
        if top[coords[1]] == " ":
            mid[coords[1]] = "O"
            self.MAP[coords[0]] = "".join(mid)
            print("opening found")
            status = False
        elif bot[coords[1]] == " ":
            mid[coords[1]] = "O"
            self.MAP[coords[0]] = "".join(mid)
            print("opening found")
            status = False
        elif mid[coords[1]-2] == " ":
            mid[coords[1]] = "O"
            self.MAP[coords[0]] = "".join(mid)
            print("opening found")
            status = False
        elif mid[coords[1]+2] == " ":
            mid[coords[1]] = "O"
            self.MAP[coords[0]] = "".join(mid)
            print("opening found")
            status = False
        else:
            mid[coords[1]] = "X"
            self.MAP[coords[0]] = "".join(mid)
            print("closed room")
            status = True

        return status

    def get_room_list(self):
        """
        Checks all rooms for their accessibility status
        """
        # for each row
        for i in range(5):
            # for each column
            for j in range(18):
                coords = func.get_coords([i,j])
                top = list(self.MAP[coords[0]-1])
                mid = list(self.MAP[coords[0]])
                bot = list(self.MAP[coords[0]+1])

                if top[coords[1]] == " ":
                    status = True
                elif bot[coords[1]] == " ":
                    status = True
                elif mid[coords[1]-2] == " ":
                    status = True
                elif mid[coords[1]+2] == " ":
                    status = True
                else:
                    status = False

                if status == True:
                    self.ROOMS["open"].append(coords[:])
                else:
                    self.ROOMS["closed"].append(coords)

                j += 1
            i += 1

    def set_room_list(self, room, change):
        """
        Modify list of rooms
        """

        return room_list


    def set_items(self):
        """
        Set down all collectible items within accessible rooms
        """

    def set_enemies(self):
        """
        Set down enemy encounters within accessible rooms
        """

    def set_npcs(self):
        """
        Set down NPCs like vendors within accessible rooms        
        """

    def set_event(self):
        """
        Set down events within accessible rooms
        """

    def display_map(self):
        """

        """
        for i in range(len(self.MAP)):
            print(self.MAP[i])

    def build_map(self):
        self.set_base_map()
        self.set_entry()
        self.set_path()
        self.get_room_list()
        self.set_branches()

        # colorpass function
        self.display_map()