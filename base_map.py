from random import randrange
import colorama as c
import utils

class BaseMap:

    global_map = []
    global_base = []
    global_rooms = {}
    global_level = 0
    global_entities = {}

    def __init__(self, level):
        self.global_level = level
        self.lane = utils.get_entry_lane(self.global_level)
        self.side = utils.get_entry_side(self.lane)

    def create_base_map(self):
        """
        Creates and writes the base map layout in list format to global_base
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

    def write_entry_coords(self):
        """
        Writes the entry & player coords (as they're always linked) to global_entities
        """
        self.global_entities["entry"]["instance"][0]["coords"] = [self.side, 5]
        self.global_entities["player"]["instance"][0]["coords"] = [self.side, 7]

    def write_exit_coords(self, coords):
        """
        Writes the exit coords into global_entities at the main paths end
        """
        self.global_entities["exit"]["instance"][0]["coords"] = [coords[0], coords[1]+2]

    def create_path(self):
        """
        Creates and writes main path to global_base by wall removal and writes coords of 
        open rooms to global_rooms
        """
        prev_coords = [utils.lane_to_xcoord(self.side),0]
        readable_coords = prev_coords[:]

        # loop until path reaches the end of the map
        while readable_coords[1] < 18:
            path = utils.get_path_options(prev_coords, readable_coords, True, True)
            prev_coords = readable_coords[:]
            real_coords = utils.get_coords(readable_coords)
            self.global_rooms["open"]["main"].append(real_coords)
            self.global_rooms["open"]["all"].append(real_coords)
            readable_coords = utils.next_coordinate(readable_coords, path)
            self.remove_wall(real_coords, path)
            if readable_coords[1] == 18:
                self.write_exit_coords(real_coords)

    def create_branches(self):
        """
        Creates and writes a variable amount of branches until they hit an open room to
        global_base by wall removal and writes coords of open rooms to global_rooms
        """
        branch_amount = 0
        while branch_amount < 4:
            branch_amount += 1
            new_open_rooms = []
            prev_coords = self.global_rooms["closed"][randrange(0,len(self.global_rooms["closed"]))]
            self.global_rooms["closed"].remove(prev_coords)
            new_open_rooms.append(prev_coords)
            prev_coords = utils.get_coords(prev_coords, True)
            readable_coords = prev_coords[:]
            
            finish = False
            # carve out a branch until an open room is hit
            while finish == False:
                branch = utils.get_path_options(prev_coords, readable_coords, False, False)
                prev_coords = readable_coords[:]
                real_coords = utils.get_coords(readable_coords)
                readable_coords = utils.next_coordinate(readable_coords, branch) 
                # next room is on closed room list
                if utils.get_coords(readable_coords) in self.global_rooms["closed"]:
                    self.global_rooms["closed"].remove(utils.get_coords(readable_coords))
                    new_open_rooms.append(utils.get_coords(readable_coords))
                    self.remove_wall(real_coords, branch)
                # next room was on closed room list and already opened up
                elif utils.get_coords(readable_coords) in new_open_rooms:
                    continue
                # next room is on open room list
                elif utils.get_coords(readable_coords) in self.global_rooms["open"]["all"]:
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
        Removes a wall of a given side based off of coordinates and writes to global_base
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

    def create_closed_room_list(self):
        """
        Creates lists of all closed rooms after initial path creation and writes to
        global_rooms
        """
        # for each row
        for i in range(5):
            # for each column
            for j in range(18):
                coords = utils.get_coords([i,j])
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

    def attempt_move(self, entity, instance, direction):
        """
        Checks upon move request if next set of coordinates allow a move
        """
        coords = self.global_entities.get(entity)["instance"][instance]["coords"]
        if direction == "w":
            map = list(self.global_map[coords[0]-1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]-2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            elif map[coords[1]] != " " and map[coords[1]] != "-" and map[coords[1]] != "=":
                result = self.identify_entity(map[coords[1]])
                return result
            else:
                return 0
        elif direction == "s":
            map = list(self.global_map[coords[0]+1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]+2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            elif map[coords[1]] != " " and map[coords[1]] != "-" and map[coords[1]] != "=":
                result = self.identify_entity(map[coords[1]])
                return result
            else:
                return 0
        elif direction == "a":
            map = list(self.global_map[coords[0]])
            if map[coords[1]-2] == " ":
                new_coords = [coords[0], coords[1]-4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            elif map[coords[1]-2] != " " and map[coords[1]-2] != "|":
                result = self.identify_entity(map[coords[1]-2])
                return result
            else:
                return 0
        elif direction == "d":
            map = list(self.global_map[coords[0]])
            if map[coords[1]+2] == " ":
                new_coords = [coords[0], coords[1]+4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
                # level advancement
            elif map[coords[1]+2] != " " and map[coords[1]+2] != "|":
                result = self.identify_entity(map[coords[1]+2])
                return result
            else:
                return 0

    def identify_entity(self, sym):
        """
        Identifies and returns entity based on attempted move towards a direction
        """
        for item in self.global_entities:
            if utils.sym(self.global_entities.get(item)['sym']) == sym:
                return self.global_entities.get(item)
                break


    def write_gold_coords(self):
        """
        Writes the gold loot coords to global_entities       
        """

    def write_loot_coords(self):
        """
        Writes the other loot coords to global_entities 
        """

    def write_enemy_coords(self):
        """
        Writes the enemy coords to global_entities 
        """

    def write_vendor_coords(self):
        """
        Writes the vendor coords to global_entities       
        """

    def place_entities(self):
        """
        Writes all entities from global_entities to newly created global_map
        """
        # copies the base map 
        self.global_map = self.global_base[:]
        # completes the map with entities
        for item in self.global_entities:
            for i in range(len(self.global_entities[item]["instance"])):
                if self.global_entities[item]["instance"][i]["coords"]: #check if to draw it at all
                    draw = list(self.global_map[self.global_entities[item]["instance"][i]["coords"][0]])
                    draw[self.global_entities[item]["instance"][i]["coords"][1]] = utils.sym(self.global_entities[item]["sym"])
                    self.global_map[self.global_entities[item]["instance"][i]["coords"][0]] = "".join(draw)


    def update_entity_coords(self, entity, instance, old_coords, new_coords):
        """
        Updates an entities coordinates in global_entities
        """
        self.global_entities.get(entity)["instance"][instance]["coords"] = new_coords

    def reset_globals(self):
        """
        This clears globals so that information is not kept in between level advancements
        """
        self.global_rooms = {
            "closed":[],
            "open":{
                "all":[],
                "main":[],
                "branches":[]
            }
        }
        self.global_entities = {
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

    def get_map(self):
        """
        Returns global_map as finalized version of the current map including entities
        """
        self.place_entities()
        return self.global_map

    def build_map(self):
        """
        Goes through all necessary methods to create a new map
        """
        self.reset_globals()
        self.create_base_map()
        self.write_entry_coords()
        self.create_path()
        self.create_closed_room_list()
        self.create_branches()
        self.place_entities()