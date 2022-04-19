from random import randrange
import numpy.random as np

ROW_INC = 4


def sym(symbol):
    """
    Converts a string into a symbol using unicode characters
    https://unicode-table.com/en/blocks/geometric-shapes/
    """
    switchcase = {
        "square": "\u25a0",
        "tridown": "\u25bc",
        "triright": "\u25ba",
        "disc": "\u25cf",
        "player": "\u1338",
        "sword": "\u2694",
        "clover": "\u2618",
        "fivestar": "\u2605",
        "dir_west": "\u25c1",
        "dir_east": "\u25b7",
        "dir_north": "\u25b3",
        "dir_south": "\u25bd"
    }

    return switchcase.get(symbol, "nothing")


def get_entry_lane(level):
    """
    Chooses the level entry lane based on a probability and level
    """
    lanes = [1, 2, 3]
    level = 11 if level > 11 else level
    probabilities = [
        1 - 0.06 * (level-1),
        0 + 0.04 * (level-1),
        0 + 0.02 * (level-1)
    ]
    lane = np.choice(lanes, 1, p=probabilities)

    return lane


def return_lane(coords):
    """
    Returns the lane (1, 2 or 3) depending on a given coordinate
    """
    if coords[0] == 1 or coords[0] == 9:
        return 0.2
    elif coords[0] == 3 or coords[0] == 7:
        return 0.1
    else:
        return 0


def get_entry_side(lane):
    """
    Decides the lane side for lanes 2 & 3
    """
    rand_num = randrange(1, 3)
    if lane == 2:
        if rand_num > 1:
            side = 3  # lane 2 top
        else:
            side = 7  # lane 2 bottom
    elif lane == 3:
        if rand_num > 1:
            side = 1  # lane 3 top
        else:
            side = 9  # lane 3 bottom
    else:
        side = 5  # lane 1

    return side


def lane_to_xcoord(lane):
    """
    Converts the initial lane (side rather) to the x coordinate
    """
    return int((lane-1)/2)


def get_coords(coords, reverse=False):
    """
    Converts coordinates from/to true/readable coords
    """
    result = [0, 0]

    if not reverse:
        result[0] = coords[0] * 2 + 1
        result[1] = 7 + 4 * coords[1]
    else:
        result[0] = int((coords[0] - 1) / 2)
        result[1] = int((coords[1] - 7) / 4)

    return result


def get_path_options(prev_coords, coords, exclude_left, create_exit):
    """
    Returns a direction based on probabilities with properties to
    exclude left and right for main path creation vs branch creation
    """
    lane = coords[0]
    row = coords[1]
    options = {}

    # probabilities
    if lane == 0:
        options["right"] = 0.3
        options["down"] = 0.4
        options["left"] = 0.3
    elif lane == 1:
        options["up"] = 0.2
        options["right"] = 0.25
        options["down"] = 0.3
        options["left"] = 0.25
    elif lane == 2:
        options["up"] = 0.25
        options["right"] = 0.25
        options["down"] = 0.25
        options["left"] = 0.25
    elif lane == 3:
        options["up"] = 0.3
        options["right"] = 0.25
        options["down"] = 0.2
        options["left"] = 0.25
    else:  # lane == 4
        options["up"] = 0.4
        options["right"] = 0.3
        options["left"] = 0.3

    # option removal
    # going up
    if prev_coords[0] > coords[0] and "down" in options:
        del options["down"]
    # going down
    if prev_coords[0] < coords[0] and "up" in options:
        del options["up"]
    # going left
    if prev_coords[1] > coords[1] and "right" in options:
        del options["right"]
    # going right
    if prev_coords[1] < coords[1] and "left" in options:
        del options["left"]

    # can't go left
    if "left" in options and row == 0:
        del options["left"]
    # can't go right
    if "right" in options and row == 17 and not create_exit:
        del options["right"]
    # can't go up
    if "up" in options and lane == 0:
        del options["up"]
    # can't go down
    if "down" in options and lane == 4:
        del options["down"]

    # for main path generation, to never go left
    if "left" in options and exclude_left:
        del options["left"]

    key_to_list = list(options.keys())
    val_to_list = list(options.values())

    # add probability difference to remaining probabilities
    if len(val_to_list) < 4 and len(val_to_list) != 0:
        diff = (1 - sum(val_to_list)) / len(val_to_list)
        for i in range(len(val_to_list)):
            val_to_list[i] += diff

    if len(val_to_list) != 0:
        result = np.choice(key_to_list, 1, p=val_to_list)
    else:
        result = "none"

    return result


def next_coordinate(coords, direction):
    """
    Returns the coords of the room after the next move based on the direction
    """
    if direction == "up":
        coords[0] -= 1
    elif direction == "down":
        coords[0] += 1
    elif direction == "right":
        coords[1] += 1
    else:  # direction == "left"
        coords[1] -= 1
    return coords


def generate_player_name():
    """
    Generates and returns a random player name if the player doesn't choose one
    """
    name_list = [
        "Unknown Adventurer",
        "Very Anonymous Adventurer",
        "Reluctant Adventurer",
        "Privacy Conscious Adventurer",
        "Adventurer of Solitude and Mystery",
        "Mysterious Adventurer",
        "Mr. Confidentiality"
    ]
    rand_num = randrange(0, len(name_list))

    return name_list[rand_num]


def generate_enemy_name():
    """
    Generates and returns a random enemy name & amount
    """
    prefix = [
        "Dirty",
        "Well-groomed",
        "Oozing",
        "Ugly",
        "Brown",
        "Crazed",
        "Shadowy",
        "Awful",
        "Angry",
        "Nasty",
        "Black",
        "Green",
        "Rabid",
        "Gruesome",
        "Grim",
        "Monstrous"

    ]
    enemy = [
        "Goblin",
        "Spider",
        "Cave-Goblin",
        "Oversized Rat",
        "Boneling",
        "Fogling",
        "Murkfiend",
        "Vampire",
        "Bear",
        "Horror",
        "Bat",
        "Lizard",
        "Animated Rock",
        "Mutant",
        "Flayer",
        "Golem",
        "Blob",
        "Serpent",
        "Wraith",
        "Detached Limb",
        "Odd Sheep",
        "Brute"
    ]

    rand_prefix = randrange(0, len(prefix))
    rand_enemy = randrange(0, len(enemy))
    rand_num = randrange(1, 5)
    prefix_str = prefix[rand_prefix]
    enemy_str = enemy[rand_enemy]

    if rand_num > 1:
        prefix_str = f"{str(rand_num)} {prefix_str}"
        enemy_str = f"{enemy_str}s"

    return " ".join([prefix_str, enemy_str])


def generate_vendor_name():
    """
    Generates and returns a random vendor name
    """
    prefix = [
        "Illustrious",
        "Celebrated",
        "Distinguished",
        "Elusive",
        "Eminent",
        "Famous",
        "Almost noteworthy",
        "Noted",
        "Notorious",
        "Renowned",
        "Plain",
        "Chaotic",
        "Cluttered",
        "Disheveled",
        "Disorderly",
        "Ruffled"
    ]
    first_name = [
        "Sir",
        "Alistair",
        "Logan",
        "Quinn",
        "Horace",
        "Chester",
        "Claudette",
        "Antoinette",
        "Doofus",
        "Lord",
        "Dame",
        "Lady"

    ]
    last_name = [
        "Archibald",
        "Marple",
        "Bryton",
        "Cunningham",
        "McLeod",
        "Winterbottom",
        "Fitzgerald",
        "Hampton"
    ]
    suffix = [
        "III",
        "IV",
        "II",
        "3rd Earl of Douglas",
        "2nd Duke of Nothingham",
        "the Plain",
        "of Entitlement",
        "Jr",
        "Sr",
        "I and probably last",
        ""
    ]

    rand_prefix = randrange(0, len(prefix))
    rand_first = randrange(0, len(first_name))
    rand_last = randrange(0, len(last_name))
    rand_suffix = randrange(0, len(suffix))

    first_portion = " ".join([prefix[rand_prefix], first_name[
        rand_first], last_name[rand_last]])
    if not suffix[rand_suffix] == "":
        second_portion = ", ".join([first_portion, suffix[rand_suffix]])
        return "".join(second_portion)
    else:
        return first_portion


def generate_gear_name():
    """
    Generates a random gear piece name
    """
    prefix = [
        "Dirty",
        "Bloodsoaked",
        "Pristine",
        "Mithril",
        "Golden",
        "Silver",
        "Wretched",
        "Adamantite",
        "Skeletal",
        "Peacekeeper's",
        "Crazed",
        "Fierce",
        "Bandit's",
        "Trainee's",
        "Bronze"
    ]

    armor = [
        "Greatplate",
        "Cuirass",
        "Trinket",
        "Helm",
        "Bracelet",
        "Dress",
        "Amulet",
        "Shield",
        "Locket",
        "Robes",
        "Greaves",
        "Band",
        "Gloves",
        "Mittens",
        "Pendant",
        "Crown",
        "Leggings",
        "Chestplate",
        "Padded Vest",
        "Vest",
        "Leather Tunic",
        "Jerkin"
    ]

    weapon = [
        "Heartseeker",
        "Skewer",
        "Rapier",
        "Swiftblade",
        "Spellblade",
        "Longsword",
        "Greataxe",
        "Axe",
        "Club",
        "Warhammer",
        "Stick",
        "Blade",
        "Scimitar",
        "Slicer",
        "Chopper",
        "Oathbreaker",
        "Cleaver",
        "Broadaxe",
        "Skullcrusher",
        "Crescent",
        "Javelin",
        "Spear",
        "Halberd",
        "Piercer"
    ]

    suffix = [
        "of the Monkey",
        "of the Whale",
        "of the Whispers",
        "of Hellish Torment",
        "of Broken Bones",
        "of Fire",
        "of Ice",
        "of the Liar",
        "of the Harvest",
        "of Executions",
        "of Traitors"
    ]

    type = "armor" if randrange(0, 2) == 1 else "weapon"
    rand_prefix = randrange(0, len(prefix))
    item = armor if type == "armor" else weapon
    rand_item = randrange(0, len(armor)) if type == "armor" else randrange(
        0, len(weapon))
    rand_suffix = randrange(0, len(suffix))

    suffix_include = 1 if randrange(0, 2) == 1 else 0
    if suffix_include:
        return [" ".join([prefix[rand_prefix], item[rand_item], suffix[
            rand_suffix]]), type]
    else:
        return [" ".join([prefix[rand_prefix], item[rand_item]]), type]


def create_loot(level):
    """
    Decides based on probabilities what loot will drop
    """
    chances = {
        "gear": 0.1,
        "loot": 0.7,
        "scroll": 0.2
    }

    loot = [
        "Health Potion",
        "Rations"
    ]

    scrolls = [
        "Scroll of Fireball",
        "Scroll of Shielding",
        "Scroll of Healing",
        "Scroll of Obliteration"
    ]

    key_to_list = list(chances.keys())
    val_to_list = list(chances.values())

    choice = np.choice(key_to_list, 1, p=val_to_list)
    if choice == "loot":
        name = loot[randrange(0, len(loot))]
        max_amount = int(round((1+level/20) * 2)) + 1
        amount = randrange(1, max_amount)
        type = "".join(choice)
    elif choice == "scroll":
        name = scrolls[randrange(0, len(scrolls))]
        type = "".join(choice)
        amount = 1
    else:  # gear
        gear = generate_gear_name()
        max_amount = int(
            round((
                level/2 + 1) * 8 if gear[1] == "armor" else (level/5 + 1) * 5))
        amount = randrange(int(round(max_amount/2)), max_amount)
        name = gear[0]
        type = gear[1]

    return [type, name, amount]
