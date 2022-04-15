from random import randrange
import colorama as c
import func

class BaseMap:

    MAP = []
    BASE = []
    ROOMS = {
            "closed":[],
            "open":{
                "all":[],
                "main":[],
                "branches":[]
            }
    }
    ENTITIES = {
        "entry":{
            "sym":"triright",
            "instance":[
                {
                    "draw":True,
                    "coords":[]
                }
            ]
        },
        "exit":{
            "sym":"tridown",
            "instance":[
                {
                    "draw":True,
                    "coords":[]
                }
            ]
        },
        "player":{
            "sym":"disc",
            "instance":[
                {
                    "draw":True,
                    "coords":[]
                }
            ]
        },
        "vendor":{
            "sym":"hamburger",
            "instance":[
                {
                    "draw":True,
                    "coords":[]
                }
            ]
        },
        "enemy":{
            "sym":"sword",
            "instance":[
                {
                    "draw":True,
                    "coords":[]
                }
            ]
        },
        "loot":{
            "sym":"star",
            "instance":[
                {
                    "draw":True,
                    "coords":[]
                }
            ]
        }
    }

    def __init__(self, level):
        self.level = level
        self.lane = func.get_entry_lane(self.level)
        self.side = func.get_entry_side(self.lane)

    def set_base_map(self):
        """
        Creates the base map layout in list format
        """
        self.BASE = [
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

    def set_entry_coords(self):
        """
        Writes the entry & player coordinates (as they're always linked)
        to ENTITIES 
        """
        self.ENTITIES["entry"]["instance"][0]["coords"] = [self.side, 5]
        self.ENTITIES["player"]["instance"][0]["coords"] = [self.side, 7]

    def set_exit_coords(self, coords):
        """
        Writes the exit coordinates into ENTITIES at the main paths end
        """
        self.ENTITIES["exit"]["instance"][0]["coords"] = [coords[0], coords[1]+2]

    def set_path(self):
        """
        Creates and sets the main path through the level
        """
        prev_coords = [func.lane_to_xcoord(self.side),0]
        readable_coords = prev_coords[:]

        # loop until path reaches the end of the map
        while readable_coords[1] < 18:
            path = func.get_path_options(prev_coords, readable_coords, True, True)
            prev_coords = readable_coords[:]
            real_coords = func.get_coords(readable_coords)
            self.ROOMS["open"]["main"].append(real_coords)
            self.ROOMS["open"]["all"].append(real_coords)
            readable_coords = func.next_coordinate(readable_coords, path)
            self.remove_wall(real_coords, path)
            if readable_coords[1] == 18:
                self.set_exit_coords(real_coords)

    def set_branches(self):
        """
        Creates and sets a variable amount of branches through the level until they hit an 
        open room
        """
        branch_amount = 0
        while branch_amount < 4:
            branch_amount += 1
            new_open_rooms = []
            prev_coords = self.ROOMS["closed"][randrange(0,len(self.ROOMS["closed"]))]
            self.ROOMS["closed"].remove(prev_coords)
            new_open_rooms.append(prev_coords)
            prev_coords = func.get_coords(prev_coords, True)
            readable_coords = prev_coords[:]
            
            finish = False
            # carve out a branch until an open room is hit
            while finish == False:
                branch = func.get_path_options(prev_coords, readable_coords, False, False)
                prev_coords = readable_coords[:]
                real_coords = func.get_coords(readable_coords)
                readable_coords = func.next_coordinate(readable_coords, branch) 
                # next room is on closed room list
                if func.get_coords(readable_coords) in self.ROOMS["closed"]:
                    self.ROOMS["closed"].remove(func.get_coords(readable_coords))
                    new_open_rooms.append(func.get_coords(readable_coords))
                    self.remove_wall(real_coords, branch)
                # next room was on closed room list and already opened up
                elif func.get_coords(readable_coords) in new_open_rooms:
                    continue
                # next room is on open room list
                elif func.get_coords(readable_coords) in self.ROOMS["open"]["all"]:
                    self.remove_wall(real_coords, branch)
                    finish = True
                    break
                else:
                    print("this shouldn't happen")

            # add newly opened rooms to open room list
            for i in range(len(new_open_rooms)):
                self.ROOMS["open"]["all"].append(new_open_rooms[i])
                self.ROOMS["open"]["branches"].append(new_open_rooms[i])

            # extend the while loop if branch is super short
            if len(new_open_rooms) < 2:
                branch_amount -= 1

    def remove_wall(self, coords, side, replacer=" "):
        """
        Removes a wall of a given side based off of coordinates
        """
        if side == "up":
            wall = list(self.BASE[coords[0]-1])
            wall[coords[1]-1] = replacer
            wall[coords[1]] = replacer
            wall[coords[1]+1] = replacer
            self.BASE[coords[0]-1] = "".join(wall)
        elif side == "down":
            wall = list(self.BASE[coords[0]+1])
            wall[coords[1]-1] = replacer
            wall[coords[1]] = replacer
            wall[coords[1]+1] = replacer
            self.BASE[coords[0]+1] = "".join(wall)
        elif side == "right":
            wall = list(self.BASE[coords[0]])
            wall[coords[1]+2] = replacer
            self.BASE[coords[0]] = "".join(wall)
        else: # side == "left"
            wall = list(self.BASE[coords[0]])
            wall[coords[1]-2] = replacer
            self.BASE[coords[0]] = "".join(wall)

    def set_closed_room_list(self):
        """
        Creates lists of all closed rooms after initial path creation
        """
        # for each row
        for i in range(5):
            # for each column
            for j in range(18):
                coords = func.get_coords([i,j])
                top = list(self.BASE[coords[0]-1])
                mid = list(self.BASE[coords[0]])
                bot = list(self.BASE[coords[0]+1])

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

                if status == False:
                    self.ROOMS["closed"].append(coords)

                j += 1
            i += 1

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

    def attempt_move(self, entity, instance, direction):
        """

        """
        coords = self.ENTITIES.get(entity)["instance"][instance]["coords"]
        if direction == "w":
            map = list(self.BASE[coords[0]-1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]-2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return True
            else:
                return False
        elif direction == "s":
            map = list(self.BASE[coords[0]+1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]+2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return True
            else:
                return False
        elif direction == "a":
            map = list(self.BASE[coords[0]])
            if map[coords[1]-2] == " ":
                new_coords = [coords[0], coords[1]-4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return True
            else:
                return False
        elif direction == "d":
            map = list(self.BASE[coords[0]])
            if map[coords[1]+2] == " ":
                new_coords = [coords[0], coords[1]+4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return True
            else:
                return False


    def update_entity_coords(self, entity, instance, old_coords, new_coords):
        """
        Updates an entities coordinates in ENTITIES
        """
        self.ENTITIES.get(entity)["instance"][instance]["coords"] = new_coords


    def set_entities(self):
        """
        Places all entities from ENTITIES
        """
        # copies the base map 
        self.MAP = self.BASE[:]
        # completes the map with entities
        for item in self.ENTITIES:
            for i in range(len(self.ENTITIES[item]["instance"])):
                if self.ENTITIES[item]["instance"][i]["coords"]: #change to draw later
                    draw = list(self.MAP[self.ENTITIES[item]["instance"][i]["coords"][0]])
                    draw[self.ENTITIES[item]["instance"][i]["coords"][1]] = func.sym(self.ENTITIES[item]["sym"])
                    self.MAP[self.ENTITIES[item]["instance"][i]["coords"][0]] = "".join(draw)

    def get_map(self):
        self.set_entities()
        return self.MAP

    def build_map(self):
        self.set_base_map()
        self.set_entry_coords()
        self.set_path()
        self.set_closed_room_list()
        self.set_branches()
        self.set_entities()