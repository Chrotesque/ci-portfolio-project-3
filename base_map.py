# Import of 3rd party modules
import random
import colorama as c

# Import of game specific modules
import func

class BaseMap:
    def __init__(self):
        ""
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

    def set_entry(self, level, map):
        """
        Decides and sets the entry into the level based on level
        """
        lane = func.get_entry_lane(level)
        side = func.get_entry_side(lane)
        entry = c.Back.GREEN + " " + c.Style.RESET_ALL

        list_from_map_lane = list(map[side])
        list_from_map_lane[5] = entry
        map[side] = "".join(list_from_map_lane)
        return map

    def set_path():
        """
        Creates and sets the main path through the level
        """

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
        map = self.set_entry(10, map)

        self.display_map(map)