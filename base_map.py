# Import of 3rd party modules
import random
import colorama as c

# Import of game specific modules
import func

class BaseMap:

    def __init__(self, level):
        self.level = level
        self.lane = func.get_entry_lane(self.level)
        self.side = func.get_entry_side(self.lane)

    def set_base_map(self):
        """
        Creates the base map layout in list format
        """
        map = [
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
        return map

    def set_entry(self, map):
        """
        Decides and sets the entry into the level based on level
        """
        entry = func.sym("triright")

        # extracts and transforms string from map list into list
        list_from_map_lane = list(map[self.side])  
        # placing entry starting at index 5
        list_from_map_lane[5] = entry 
        # converting list back to string and placing it back
        map[self.side] = "".join(list_from_map_lane) 
        return map

    def set_path(self, map): # x0-4, y0-17
        """
        Creates and sets the main path through the level
        """
        prev_coords = [func.lane_to_xcoord(self.side),0]
        coords = prev_coords[:]
        prev_coords[1] -= 1
        lane = self.side

        while coords[1] < 18:
            path = func.get_path_options(prev_coords, coords, True, True)
            prev_coords = coords[:]
            list_coords = func.get_coords(coords)
            if path == "up":
                section = list(map[list_coords[0]-1])
                section[list_coords[1]-1] = " "
                section[list_coords[1]] = " "
                section[list_coords[1]+1] = " "
                map[list_coords[0]-1] = "".join(section)
                coords[0] -= 1
            if path == "down":
                section = list(map[list_coords[0]+1])
                section[list_coords[1]-1] = " "
                section[list_coords[1]] = " "
                section[list_coords[1]+1] = " "
                map[list_coords[0]+1] = "".join(section)
                coords[0] += 1
            if path == "right":
                section = list(map[list_coords[0]])

                if coords[1] == 17:
                    section[list_coords[1]+2] = func.sym("tridown")
                else:
                    section[list_coords[1]+2] = " "

                map[list_coords[0]] = "".join(section)
                coords[1] += 1

        return map

    def set_exit():
        """
        Set down the level exit at the end of the main path
        """

    def set_branches(self, map, avail_rooms):
        """
        Creates and sets branches going off of the main path
        """


    def get_room_list(self, map):
        """
        Checks all rooms for their accessibility status
        """
        rooms = {
                "closed":[],
                "open":[]
        }

        # for each row
        for i in range(5):
            # for each column
            for j in range(18):
                coords = func.get_coords([i,j])
                top = list(map[coords[0]-1])
                mid = list(map[coords[0]])
                bot = list(map[coords[0]+1])

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
                    rooms["open"].append(coords[:])
                else:
                    rooms["closed"].append(coords)

                j += 1
            i += 1

        return rooms

    def set_room_list(self, room_list, room, change):
        """
        Modify list of rooms
        """

        

        return room_list

    def set_items():
        """
        Set down all collectible items within accessible rooms
        """

    def set_enemies():
        """
        Set down enemy encounters within accessible rooms
        """

    def set_npcs():
        """
        Set down NPCs like vendors within accessible rooms        
        """

    def set_event():
        """
        Set down events within accessible rooms
        """

    def display_map(self, map):
        """

        """
        for i in range(len(map)):
            print(map[i])
            i += 1

    def build_map(self):
        map = self.set_base_map()
        map = self.set_entry(map)
        map = self.set_path(map)
        room_list = self.get_room_list(map)
        #map = self.set_branches(map, room_list)

        # colorpass function
        self.display_map(map)