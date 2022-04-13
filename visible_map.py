import colorama as c
from func import sym

class VisibleMap:
    def __init__(self, map):
        self.map = map

    def set_visible_map():
        """
        Creates an empty map
        """

    def reveal_area():
        """
        Reveals the portion the player is in based off of the base map
        """

    def get_avail_movement():
        """
        Get all available movement options based off of base map
        """

    def get_avail_actions():
        """
        Get all available actions based off of base map
        """

    def set_new_pos():
        """
        
        """

    def colorize_map(self):
        """
        Adds colors to certain elements of the map
        """
        colorization = {
            sym("disc"):{
                "Fore":"RED",
                "Back":"BLUE"
            },
            sym("tridown"):{
                "Fore":"BLUE",
                "Back":"GREEN"
            },
            sym("triright"):{
                "Fore":"MAGENTA",
                "Back":"RESET"
            }
        }
        col_key = list(colorization.keys())
        col_val = list(colorization.values()) 
        # for each line of the map list
        for i in range(len(self.map)):
            # exclude all irrelevant lines
            if i % 2 != 0:
                list_map = list(self.map[i])
                # for each item in current map rows list
                for j in range(len(list_map)):
                    # for each item in colorization dict
                    for k in range(len(col_key)):
                        # if a match is found, change it according to the colorize dict
                        if list_map[j] == col_key[k]:
                            list_map[j] = getattr(c.Fore, col_val[k]["Fore"]) + getattr(c.Back, col_val[k]["Back"]) + col_key[k] + c.Style.RESET_ALL
                # convert from list to string again
                self.map[i] = "".join(list_map)
            


    def display_map(self):
        """
        Displays the map after formatting (like colorization) is finished
        """
        self.colorize_map()
        for i in range(len(self.map)):
            print(self.map[i])