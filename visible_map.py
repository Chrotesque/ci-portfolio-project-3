import colorama as c
from func import sym

class VisibleMap:

    MASK = []
    VISIBLE = []

    def __init__(self, map):
        self.map = map[:]

    def set_mask(self):
        """
        Creates an the initial MASK
        """
        for i in range(11):
            if i == 0 or i == 10:
                list_map = list(self.map[i])
                for n in range(78):
                    list_map[n] = "O"
                self.MASK.append("".join(list_map))
            else:
                list_map = list(self.map[i])
                list_map = list_map[:6]
                for k in range(len(list_map)):
                    list_map[k] = "O"
                for j in range(72):
                    list_map.append("X")
                self.MASK.append("".join(list_map))
        

    def reveal_area(self, coords):
        """
        Adds the portion the player is in as visible to the MASK
        """
        replacer = "O", "O", "O", "O", "O"
        if coords[0] == 1:
            list_map = list(self.MASK[coords[0]])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]] = "".join(list_map)

            list_map = list(self.MASK[coords[0]+1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]+1] = "".join(list_map)
        elif coords[0] == 9:
            list_map = list(self.MASK[coords[0]])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]] = "".join(list_map)

            list_map = list(self.MASK[coords[0]-1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]-1] = "".join(list_map)
        else:
            list_map = list(self.MASK[coords[0]+1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]+1] = "".join(list_map)

            list_map = list(self.MASK[coords[0]])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]] = "".join(list_map)

            list_map = list(self.MASK[coords[0]-1])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer
            self.MASK[coords[0]-1] = "".join(list_map)

    def reveal_map(self):
        """
        Uses the MASK to reveal portions of the map
        """
        self.VISIBLE = self.map[:]
        # per row
        for i in range(len(self.map)):
            list_map = list(self.map[i])
            mask_map = list(self.MASK[i])
            # per column
            for j in range(len(list_map)):
                if mask_map[j] == "X":
                    list_map[j] = " "
            self.VISIBLE[i] = "".join(list_map)

    def colorize_map(self):
        """
        Adds colors to certain elements of the visible map
        """
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
        for i in range(len(self.VISIBLE)):
            # exclude all irrelevant lines
            if i % 2 != 0:
                list_map = list(self.VISIBLE[i])
                # for each item in current map rows list
                for j in range(len(list_map)):
                    # for each item in colorization dict
                    for k in range(len(col_key)):
                        # if a match is found, change it according to the colorize dict
                        if list_map[j] == col_key[k]:
                            list_map[j] = getattr(c.Fore, col_val[k]["Fore"]) + getattr(c.Back, col_val[k]["Back"]) + col_key[k] + c.Style.RESET_ALL
                # convert from list to string again
                self.VISIBLE[i] = "".join(list_map)

    def display_map(self, coords):
        """
        Displays the map after formatting (like colorization) is finished
        """
        self.reveal_area(coords)
        self.reveal_map()
        self.colorize_map()
        for i in range(len(self.VISIBLE)):
            print(self.VISIBLE[i])