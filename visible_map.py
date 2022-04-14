import colorama as c
from func import sym

class VisibleMap:

    VISIBLE = []
    COLORED = []

    def __init__(self, map):
        print("init")
        self.map = map[:]

    def set_visible_map(self):
        """
        Creates an empty map
        """
        row = ""
        for i in range(71):
            row += " "

        for i in range(11):
            if i == 0 or i == 10:
                self.VISIBLE.append(self.map[i])
            else:
                list_map = list(self.map[i])
                list_map = list_map[:6]
                for j in range(71):
                    list_map.append(" ")
                self.VISIBLE.append("".join(list_map))
        

    def reveal_area(self, coords):
        """
        Reveals the portion the player is in based off of the base map
        """
        if coords[0] == 1:
            list_map = list(self.VISIBLE[coords[0]])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]] = "".join(list_map)

            list_map = list(self.VISIBLE[coords[0]+1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]+1])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]+1] = "".join(list_map)
        elif coords[0] == 9:
            list_map = list(self.VISIBLE[coords[0]])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]] = "".join(list_map)

            list_map = list(self.VISIBLE[coords[0]-1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]-1])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]-1] = "".join(list_map)
        else:
            list_map = list(self.VISIBLE[coords[0]+1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]+1])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]+1] = "".join(list_map)

            list_map = list(self.VISIBLE[coords[0]])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]] = "".join(list_map)

            list_map = list(self.VISIBLE[coords[0]-1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = list(self.map[coords[0]-1])[coords[1]-2:coords[1]+3]
            self.VISIBLE[coords[0]-1] = "".join(list_map)

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
        self.COLORED = self.VISIBLE[:]
        colorization = {
            sym("disc"):{
                "Fore":"GREEN",
                "Back":"RESET"
            },
            sym("tridown"):{
                "Fore":"MAGENTA",
                "Back":"RESET"
            },
            sym("triright"):{
                "Fore":"MAGENTA",
                "Back":"RESET"
            }
        }
        col_key = list(colorization.keys())
        col_val = list(colorization.values()) 
        # for each line of the map list
        for i in range(len(self.COLORED)):
            # exclude all irrelevant lines
            if i % 2 != 0:
                list_map = list(self.COLORED[i])
                # for each item in current map rows list
                for j in range(len(list_map)):
                    # for each item in colorization dict
                    for k in range(len(col_key)):
                        # if a match is found, change it according to the colorize dict
                        if list_map[j] == col_key[k]:
                            list_map[j] = getattr(c.Fore, col_val[k]["Fore"]) + getattr(c.Back, col_val[k]["Back"]) + col_key[k] + c.Style.RESET_ALL
                # convert from list to string again
                self.COLORED[i] = "".join(list_map)

    def display_map(self, coords):
        """
        Displays the map after formatting (like colorization) is finished
        """
        self.reveal_area(coords)
        self.colorize_map()
        for i in range(len(self.COLORED)):
            print(self.COLORED[i])

        for i in range(len(self.map)):
            print(self.map[i])