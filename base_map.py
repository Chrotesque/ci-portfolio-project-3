from random import randrange
import colorama as c
import utils
import math


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
        self.global_base = ["     +===+===+===+===+===+===+===+===+===+===+==="
                            "+===+===+===+===+===+===+===+",
                            " L3  |   |   |   |   |   |   |   |   |   |   |   "
                            "|   |   |   |   |   |   |   |",
                            "     +---+---+---+---+---+---+---+---+---+---+---"
                            "+---+---+---+---+---+---+---+",
                            " L2  |   |   |   |   |   |   |   |   |   |   |   "
                            "|   |   |   |   |   |   |   |",
                            "     +---+---+---+---+---+---+---+---+---+---+---"
                            "+---+---+---+---+---+---+---+",
                            " L1  |   |   |   |   |   |   |   |   |   |   |   "
                            "|   |   |   |   |   |   |   |",
                            "     +---+---+---+---+---+---+---+---+---+---+---"
                            "+---+---+---+---+---+---+---+",
                            " L2  |   |   |   |   |   |   |   |   |   |   |   "
                            "|   |   |   |   |   |   |   |",
                            "     +---+---+---+---+---+---+---+---+---+---+---"
                            "+---+---+---+---+---+---+---+",
                            " L3  |   |   |   |   |   |   |   |   |   |   |   "
                            "|   |   |   |   |   |   |   |",
                            "     +===+===+===+===+===+===+===+===+===+===+==="
                            "+===+===+===+===+===+===+===+"
                            ]

    def write_entry_coords(self):
        """
        Writes the entry & player coords (always linked) to global_entities
        """
        self.global_entities["entry"]["instance"][0]["coords"] = [self.side, 5]
        self.global_entities[
            "player"]["instance"][0]["coords"] = [self.side, 7]

    def write_exit_coords(self, coords):
        """
        Writes the exit coords into global_entities at the main paths end
        """
        self.global_entities["exit"][
            "instance"][0]["coords"] = [coords[0], coords[1]+2]

    def create_path(self):
        """
        Creates and writes main path to global_base by wall removal and writes
        coords of open rooms to global_rooms
        """
        prev_coords = [utils.lane_to_xcoord(self.side), 0]
        readable_coords = prev_coords[:]

        # loop until path reaches the end of the map
        while readable_coords[1] < 18:
            path = utils.get_path_options(
                prev_coords, readable_coords, True, True)
            prev_coords = readable_coords[:]
            real_coords = utils.get_coords(readable_coords)
            self.global_rooms["open"]["main"].append(real_coords)
            self.global_rooms["open"]["all"].append(real_coords)
            readable_coords = utils.next_coordinate(readable_coords, path)
            self.remove_wall(real_coords, path)
            # place exit at the end of the map
            if readable_coords[1] == 18:
                self.write_exit_coords(real_coords)
                # rem player start pos so entities cant be placed @ same spot
                self.global_rooms["open"]["main"].remove(utils.get_coords(
                    [utils.lane_to_xcoord(self.side), 0]))

    def create_branches(self):
        """
        Creates and writes a variable amount of branches until they hit an open
        room to global_base by wall removal and writes coords of open rooms to
        global_rooms
        """
        branch_num = 0
        branch_max = 4
        while branch_num < branch_max:

            # safeguard against fragmenting the map too much
            if branch_max == 9:
                break

            branch_num += 1
            new_open_rooms = []
            prev_coords = self.global_rooms["closed"][
                randrange(0, len(self.global_rooms["closed"]))]
            self.global_rooms["closed"].remove(prev_coords)
            new_open_rooms.append(prev_coords)
            prev_coords = utils.get_coords(prev_coords, True)
            readable_coords = prev_coords[:]

            # carve out a branch until an open room is hit
            j = 0
            while True:
                branch = utils.get_path_options(
                    prev_coords, readable_coords, False, False)
                prev_coords = readable_coords[:]
                real_coords = utils.get_coords(readable_coords)
                readable_coords = utils.next_coordinate(
                    readable_coords, branch)
                # next room is on closed room list
                if utils.get_coords(readable_coords) in self.global_rooms[
                        "closed"]:
                    self.global_rooms["closed"].remove(
                        utils.get_coords(readable_coords))
                    new_open_rooms.append(utils.get_coords(readable_coords))
                    self.remove_wall(real_coords, branch)
                    j += 1
                # next room was on closed room list and already opened up
                elif utils.get_coords(readable_coords) in new_open_rooms:
                    continue

                # next room is on open room list
                else:
                    self.remove_wall(real_coords, branch)
                    break

            # add newly opened rooms to open room list
            for i in range(len(new_open_rooms)):
                self.global_rooms["open"]["all"].append(new_open_rooms[i])
                self.global_rooms["open"]["branches"].append(new_open_rooms[i])

            # extend the while loop if branch is super short
            if len(new_open_rooms) < 2:
                branch_max += 1

    def remove_wall(self, coords, side, replacer=" "):
        """
        Removes a wall of a given side based off of coordinates and writes to
        global_base
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
        else:  # left
            wall = list(self.global_base[coords[0]])
            wall[coords[1]-2] = replacer
            self.global_base[coords[0]] = "".join(wall)

    def create_closed_room_list(self):
        """
        Creates lists of all closed rooms after initial path creation and
        writes to global_rooms
        """
        # for each row
        for i in range(5):
            # for each column
            for j in range(18):
                coords = utils.get_coords([i, j])
                top = list(self.global_base[coords[0]-1])
                mid = list(self.global_base[coords[0]])
                bot = list(self.global_base[coords[0]+1])

                # check for an opening to a coordinate/room
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

                if not status:
                    self.global_rooms["closed"].append(coords)

    def attempt_move(self, entity, instance, direction):
        """
        Checks upon move request if next set of coordinates allow a move
        """
        coords = self.global_entities.get(entity)[
            "instance"][instance]["coords"]
        # up
        if direction == "w":
            map = list(self.global_map[coords[0]-1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]-2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            else:
                return 0
        # down
        elif direction == "s":
            map = list(self.global_map[coords[0]+1])
            if map[coords[1]] == " ":
                new_coords = [coords[0]+2, coords[1]]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            else:
                return 0
        # left
        elif direction == "a":
            map = list(self.global_map[coords[0]])
            if map[coords[1]-2] == " ":
                new_coords = [coords[0], coords[1]-4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
            else:
                return 0
        # right
        else:
            map = list(self.global_map[coords[0]])
            if map[coords[1]+2] == " ":
                new_coords = [coords[0], coords[1]+4]
                self.update_entity_coords(entity, instance, coords, new_coords)
                return 1
                # next level
            elif map[coords[1]+2] == utils.sym("tridown"):
                return 2
            else:
                return 0

    def identify_entity(self):
        """
        Identifies and returns entity on players position
        """
        # gets coords of players position
        coords = self.global_entities["player"]["instance"][0]["coords"]
        list_map = list(self.global_map[coords[0]])
        sym = list_map[coords[1]]

        # checks all entity kinds for hit
        for item in self.global_entities:
            reference = self.global_entities.get(item)
            if utils.sym(reference['sym']) == sym:

                # change draw to false, so it becomes invisible
                for i in range(len(reference["instance"])):
                    if coords == reference["instance"][i]["coords"]:
                        reference["instance"][i]["draw"] = False

                return [self.global_entities.get(item)['sym'], coords]
                break

    def write_gold_coords(self):
        """
        Writes the gold loot coords to global_entities
        A certain limited amount will be placed on the main path
        The remainder will be placed on the branches
        """
        coords_list = []
        max_num = min(round((self.global_level/25 + 1) * 5), 10)

        cutoff = randrange(1, 4)
        for i in range(randrange(3, max_num)):
            main_amt = len(self.global_rooms["open"]["main"])
            branch_amt = len(self.global_rooms["open"]["branches"])
            if i < cutoff:
                rand_coord = self.global_rooms[
                    "open"]["main"][randrange(0, main_amt)]
                coords_list.append(rand_coord)
                self.global_rooms["open"]["main"].remove(rand_coord)
            else:
                rand_coord = self.global_rooms[
                    "open"]["branches"][randrange(0, branch_amt)]
                coords_list.append(rand_coord)
                self.global_rooms["open"]["branches"].remove(rand_coord)

        # creates entity entries
        for i in range(len(coords_list)):
            entity_to_add = {
                "draw": True,
                "coords": coords_list[i]
            }
            self.global_entities["gold"]["instance"].append(entity_to_add)

    def write_loot_coords(self):
        """
        Writes the other loot coords to global_entities
        """
        coords_list = []

        cutoff = 2
        for i in range(3, 5):
            main_amt = len(self.global_rooms["open"]["main"])
            branch_amt = len(self.global_rooms["open"]["branches"])
            if i < cutoff:
                rand_coord = self.global_rooms[
                    "open"]["main"][randrange(0, main_amt)]
                coords_list.append(rand_coord)
                self.global_rooms["open"]["main"].remove(rand_coord)
            else:
                rand_coord = self.global_rooms[
                    "open"]["branches"][randrange(0, branch_amt)]
                coords_list.append(rand_coord)
                self.global_rooms["open"]["branches"].remove(rand_coord)

        # creates entity entries
        for i in range(len(coords_list)):
            entity_to_add = {
                "draw": True,
                "coords": coords_list[i]
            }
            self.global_entities["loot"]["instance"].append(entity_to_add)

    def write_enemy_coords(self):
        """
        Writes the enemy coords to global_entities
        """
        coords_list = []
        max_num = min(round(((self.global_level/2.5)/6 + 1) * 5), 12)

        cutoff = math.ceil(max_num/2)
        for i in range(randrange(cutoff-1, max_num)):
            main_amt = len(self.global_rooms["open"]["main"])
            branch_amt = len(self.global_rooms["open"]["branches"])
            if i < cutoff:
                rand_coord = self.global_rooms[
                    "open"]["main"][randrange(0, main_amt)]
                coords_list.append(rand_coord)
                self.global_rooms["open"]["main"].remove(rand_coord)
            else:
                rand_coord = self.global_rooms[
                    "open"]["branches"][randrange(0, branch_amt)]
                coords_list.append(rand_coord)
                self.global_rooms["open"]["branches"].remove(rand_coord)

        # creates entity entries
        for i in range(len(coords_list)):
            entity_to_add = {
                "draw": True,
                "coords": coords_list[i]
            }
            self.global_entities["enemy"]["instance"].append(entity_to_add)

    def write_vendor_coords(self):
        """
        Writes the vendor coords to global_entities
        """
        rand_num = randrange(0, len(self.global_rooms["open"]["branches"]))
        coords = self.global_rooms["open"]["branches"][rand_num]
        entity_to_add = {
            "draw": True,
            "coords": coords
        }
        self.global_entities["vendor"]["instance"].append(entity_to_add)

    def place_entities(self):
        """
        Writes all entities from global_entities to newly created global_map
        According to their respective coordinates
        """
        # copies the base map
        self.global_map = self.global_base[:]
        # fills the map with all entities that have coords and should be drawn
        for item in self.global_entities:
            for i in range(len(self.global_entities[item]["instance"])):
                if self.global_entities[item][
                    "instance"][i]["coords"] and self.global_entities[item][
                        "instance"][i]["draw"]:
                    draw = list(self.global_map[self.global_entities[
                        item]["instance"][i]["coords"][0]])
                    draw[self.global_entities[item]["instance"][i][
                        "coords"][1]] = utils.sym(self.global_entities[
                            item]["sym"])
                    self.global_map[self.global_entities[item]["instance"][i][
                        "coords"][0]] = "".join(draw)

    def update_entity_coords(self, entity, instance, old_coords, new_coords):
        """
        Updates an entities coordinates in global_entities
        """
        self.global_entities.get(entity)[
            "instance"][instance]["coords"] = new_coords

    def reset_globals(self):
        """
        This clears globals so that info is not kept in between levels
        """
        self.global_rooms = {
            "closed": [],
            "open": {
                "all": [],
                "main": [],
                "branches": []
            }
        }
        self.global_entities = {
            "entry": {
                "sym": "triright",
                "Fore": "MAGENTA",
                "Back": "RESET",
                "instance": [
                    {
                        "draw": True,
                        "coords": []
                    }
                ]
            },
            "exit": {
                "sym": "tridown",
                "Fore": "MAGENTA",
                "Back": "RESET",
                "instance": [
                    {
                        "draw": True,
                        "coords": []
                    }
                ]
            },
            "player": {
                "sym": "player",
                "Fore": "GREEN",
                "Back": "RESET",
                "instance": [
                    {
                        "draw": True,
                        "coords": []
                    }
                ]
            },
            "vendor": {
                "sym": "clover",
                "Fore": "CYAN",
                "Back": "RESET",
                "instance": [
                    {
                        "draw": True,
                        "coords": []
                    }
                ]
            },
            "enemy": {
                "sym": "sword",
                "Fore": "RED",
                "Back": "RESET",
                "instance": []
            },
            "loot": {
                "sym": "fivestar",
                "Fore": "YELLOW",
                "Back": "RESET",
                "instance": [
                    {
                        "draw": True,
                        "coords": []
                    }
                ]
            },
            "gold": {
                "sym": "disc",
                "Fore": "YELLOW",
                "Back": "RESET",
                "instance": [
                    {
                        "draw": True,
                        "coords": []
                    }
                ]
            }
        }

    def get_map(self):
        """
        Returns global_map as final version of the cur map incl entities
        """
        self.place_entities()
        return self.global_map

    def get_entities(self):
        """
        Returns the global_entities in its current state
        """
        return self.global_entities

    def build_map(self):
        """
        Goes through all necessary methods to create a new map
        """
        # map creation
        self.reset_globals()
        self.create_base_map()
        self.write_entry_coords()
        self.create_path()
        self.create_closed_room_list()
        self.create_branches()

        # entities
        self.write_gold_coords()
        self.write_loot_coords()
        self.write_enemy_coords()
        self.write_vendor_coords()
        self.place_entities()
