import colorama as c
from utils import sym

class VisibleMap:

    global_mask = []
    global_visible = []

    def __init__(self, map):
        self.map = map[:]

    def set_mask(self):
        """
        Creates the initial global_mask
        """
        self.global_mask.clear()
        for i in range(11):
            if i == 0 or i == 10:
                list_map = list(self.map[i])
                for n in range(78):
                    list_map[n] = "O"
                self.global_mask.append("".join(list_map))
            else:
                list_map = list(self.map[i])
                list_map = list_map[:6]
                for k in range(len(list_map)):
                    list_map[k] = "O"
                for j in range(72):
                    list_map.append("X")
                self.global_mask.append("".join(list_map))
        

    def reveal_area(self, coords):
        """
        Adds the portion the player is in as visible to the global_mask
        """
        replacer = "O", "O", "O", "O", "O"

        iterations = 2 if not coords[0] == 1 and not coords[0] == 9 else 1
        for i in range(iterations):

            if iterations == 1:
                if coords[0] == 1:
                    factor = -1
                else: 
                    factor = 1
            else:
                if i == 0:
                    factor = -1
                else:
                    factor = 1 

            # top & bottom
            list_map = list(self.global_mask[coords[0]-(1*factor)])
            list_upmap = list(self.global_mask[coords[0]-(2*factor)])
            list_actmap = list(self.map[coords[0]-(1*factor)])
            del list_map[coords[1]-2:coords[1]+3]
            list_map[coords[1]-2:coords[1]-2] = replacer

            list_upmap[coords[1]] = "O" if list_actmap[coords[1]] == " " else list_upmap[coords[1]]
            self.global_mask[coords[0]-(2*factor)] = "".join(list_upmap)
            self.global_mask[coords[0]-(1*factor)] = "".join(list_map)

        # middle
        list_map = list(self.global_mask[coords[0]])
        list_actmap = list(self.map[coords[0]])
        del list_map[coords[1]-2:coords[1]+3]
        list_map[coords[1]-2:coords[1]-2] = replacer

        list_map[coords[1]-4] = "O" if list_actmap[coords[1]-2] == " " else list_map[coords[1]-4]
        if coords[1] < 75:
            list_map[coords[1]+4] = "O" if list_actmap[coords[1]+2] == " " else list_map[coords[1]+4]

        self.global_mask[coords[0]] = "".join(list_map)


    def reveal_map(self):
        """
        Uses the global_mask to reveal portions of the map
        """
        self.global_visible = self.map[:]
        # per row
        for i in range(len(self.map)):
            list_map = list(self.map[i])
            mask_map = list(self.global_mask[i])
            # per column
            for j in range(len(list_map)):
                if mask_map[j] == "X":
                    list_map[j] = " "
            self.global_visible[i] = "".join(list_map)

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
            },
            sym("star"):{
                "Fore":"YELLOW",
                "Back":"RESET"
            }
        }
        col_key = list(colorization.keys())
        col_val = list(colorization.values()) 
        # for each line of the map list
        for i in range(len(self.global_visible)):
            # exclude all irrelevant lines
            if i % 2 != 0:
                list_map = list(self.global_visible[i])
                # for each item in current map rows list
                for j in range(len(list_map)):
                    # for each item in colorization dict
                    for k in range(len(col_key)):
                        # if a match is found, change it according to the colorize dict
                        if list_map[j] == col_key[k]:
                            list_map[j] = getattr(c.Fore, col_val[k]["Fore"]) + getattr(c.Back, col_val[k]["Back"]) + col_key[k] + c.Style.RESET_ALL
                # convert from list to string again
                self.global_visible[i] = "".join(list_map)

    def display_map(self, coords):
        """
        Displays the map after formatting (like colorization) is finished
        """
        self.reveal_area(coords)
        self.reveal_map()
        self.colorize_map()
        for i in range(len(self.global_visible)):
            print(self.global_visible[i])

        for i in range(len(self.map)):
            print(self.map[i])

        #for i in range(len(self.global_mask)):
        #    print(self.global_mask[i])