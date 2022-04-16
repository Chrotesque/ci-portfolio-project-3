from random import randrange
import colorama as c
import func

class BaseMap:

    global_map = []
    global_base = []
    global_rooms = {
            "closed":[],
            "open":{
                "all":[],
                "main":[],
                "branches":[]
            }
    }
    global_level = 0
    global_entities = {
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
        self.global_level = level
        self.lane = func.get_entry_lane(self.global_level)
        self.side = func.get_entry_side(self.lane)

    def set_base_map(self):
        """
        Creates the base map layout in list format
        """
        self.global_base = [
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
        to global_entities 
        """
        self.global_entities["entry"]["instance"][0]["coords"] = [self.side, 5]
        self.global_entities["player"]["instance"][0]["coords"] = [self.side, 7]

    def set_exit_coords(self, coords):
        """
        Writes the exit coordinates into global_entities at the main paths end
        """
        self.global_entities["exit"]["instance"][0]["coords"] = [coords[0], coords[1]+2]

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
            self.global_rooms["open"]["main"].append(real_coords)
            self.global_rooms["open"]["all"].append(real_coords)
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
            prev_coords = self.global_rooms["closed"][randrange(0,len(self.global_rooms["closed"]))]
            self.global_rooms["closed"].remove(prev_coords)
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
                if func.get_coords(readable_coords) in self.global_rooms["closed"]:
                    self.global_rooms["closed"].remove(func.get_coords(readable_coords))
                    new_open_rooms.append(func.get_coords(readable_coords))
                    self.remove_wall(real_coords, branch)
                # next room was on closed room list and already opened up
                elif func.get_coords(readable_coords) in new_open_rooms:
                    continue
                # next room is on open room list
                elif func.get_coords(readable_coords) in self.global_rooms["open"]["all"]:
                    self.remove_wall(real_coords, branch)
                    finish = True
                    break
                else:
                    print("this shouldn't happen")

            # add newly opened rooms to open room list
            for i in range(len(new_open_rooms)):
                self.global_rooms["open"]["all"].append(new_open_rooms[i])
                self.global_rooms["open"]["branches"].append(new_open_rooms[i])

            # extend the while loop if branch is super short
            if len(new_open_rooms) < 2:
                branch_amount -= 1

    def remove_wall(self, coords, side, replacer=" "):
        """
        Removes a wall of a given side based off of coordinates
        """
        if side == "up":
            wall = list(self.global_base[coords[0]-1])
            wall[coords[1]-1] = replacer
            wall[coords[1]] = replacer
            wall[coords[1]+1] = replacer
            self.global_base[coords[0]-1] = "".join(wall)
        elif side == "down":
            wall = list(self.global_base[coords[0]+1])
            wall[coords[1]-1] = replacer
            wall[coords[1]] = replacer
            wall[coords[1]+1] = replacer
            self.global_base[coords[0]+1] = "".join(wall)
        elif side == "right":
            wall = list(self.global_base[coords[0]])
            wall[coords[1]+2] = replacer
            self.global_base[coords[0]] = "".join(wall)
        else: # side == "left"
            wall = list(self.global_base[coords[0]])
            wall[coords[1]-2] = replacer
            self.global_base[coords[0]] = "".join(wall)

    def set_closed_room_list(self):
        """
        Creates lists of all closed rooms after initial path creation
        """
        # for each row
        for i in range(5):
            # for each column
            for j in range(18):
                coords = func.get_coords([i,j])
                top = list(self.global_base[coords[0]-1])
                mid = list(self.global_base[coords[0]])
                bot = list(self.global_base[coords[0]+1])

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
                    self.global_rooms["closed"].append(coords)

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
        coords = self.global_entities.get(entity)["instance"][instance]["coords"]
        if direction == "w":
            map = list(self.global_map[coords[0]-1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]-2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            else:
                return 0
        elif direction == "s":
            map = list(self.global_map[coords[0]+1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]+2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            else:
                return 0
        elif direction == "a":
            map = list(self.global_map[coords[0]])
            if map[coords[1]-2] == " ":
                new_coords = [coords[0], coords[1]-4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            else:
                return 0
        elif direction == "d":
            map = list(self.global_map[coords[0]])
            if map[coords[1]+2] == " ":
                new_coords = [coords[0], coords[1]+4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
                # level advancement
            elif map[coords[1]+2] == func.sym("tridown"):
                return 2
            else:
                return 0


    def update_entity_coords(self, entity, instance, old_coords, new_coords):
        """
        Updates an entities coordinates in global_entities
        """
        self.global_entities.get(entity)["instance"][instance]["coords"] = new_coords


    def set_entities(self):
        """
        Places all entities from global_entities
        """
        # copies the base map 
        self.global_map = self.global_base[:]
        # completes the map with entities
        for item in self.global_entities:
            for i in range(len(self.global_entities[item]["instance"])):
                if self.global_entities[item]["instance"][i]["coords"]: #change to draw later
                    draw = list(self.global_map[self.global_entities[item]["instance"][i]["coords"][0]])
                    draw[self.global_entities[item]["instance"][i]["coords"][1]] = func.sym(self.global_entities[item]["sym"])
                    self.global_map[self.global_entities[item]["instance"][i]["coords"][0]] = "".join(draw)

    def get_map(self):
        self.set_entities()
        return self.global_map

    def build_map(self):
        self.set_base_map()
        self.set_entry_coords()
        self.set_path()
        self.set_closed_room_list()
        self.set_branches()
        self.set_entities()