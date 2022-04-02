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
        self.build_map()

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
        lane = self.side



        return map

    def set_exit():
        """
        Set down the level exit at the end of the main path
        """

    def set_branches():
        """
        Creates and sets branches going off of the main path
        """

    def get_accessible_rooms():
        """
        Collects all accessible rooms for entity distribution
        """

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

        # colorpass function
        self.display_map(map)