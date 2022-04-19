from random import randrange
from pyfiglet import Figlet
from os import system
import math
from colorama import (
    Fore as cf,
    Back as cb,
    Style as cs
)
import utils
import base_map
import visible_map as vis_map
import entity
import notifications

custom_fig = Figlet(font="cybermedium")

global_notification = notifications.Notifications()
global_player = entity.Player(
    name="", hp_cur=100, hp_max=100, dmg=2, gold=50, armor=2, inventory={
        "Rations": 1, "Health Potion": 2})

COMMANDS = {
  "help": ["help", "halp", "hlp", "h"],
  "restart": ["again", "redo", "restart"],
  "move": {
    "w": f"You moved a room to the north {utils.sym('dir_north')}",
    "s": f"You moved a room to the south {utils.sym('dir_south')}",
    "a": f"You moved a room to the west {utils.sym('dir_west')}",
    "d": f"You moved a room to the east {utils.sym('dir_east')}"
  },
  "use": ["use", "item", "q", "i", "u"]
}


def welcome():
    """
    Displays the welcome message at the start of the game
    """
    # clearing the screen
    system('cls||clear')
    title = "Endless Dungeons"
    sub_title = "on a budget"
    print(f"""{cf.YELLOW}{custom_fig.renderText(title)}{sub_title : >77}\n

Hey there and welcome!{cs.RESET_ALL}\n
Be sure to have a look at the help menu first, before you get started.\n""")


def validate_name():
    """
    Validates user input for the players name, alternatively assigns a name
    w/o input
    """
    name_chosen = False
    character_limit = 43
    input_msg = "What's your name?\n> "
    i = 0
    while True:

        player_input = str(input(input_msg))
        if player_input is '':
            player_input = input("You should enter a name at this point. "
                                 "Otherwise I will assign you one.\n> ")
            if player_input is '':
                player_input = utils.generate_player_name()
                global_notification.modify_note(
                    f"Have it your way, {player_input}!")
                break
            elif len(player_input) > character_limit:
                input_msg = "That's a tad long, try to keep it to a "\
                    f"maximum of {character_limit} characters.\n> "
                continue
            else:
                global_notification.modify_note(
                        f"Wasn't that hard now, was it?")
                break

        elif len(player_input) > character_limit:
            input_msg = "That's a tad long, try to keep it to a "\
                f"maximum of {character_limit} characters.\n> "
            continue
        else:
            global_notification.modify_note(
                    f"""Welcome "{player_input}"!
     Off to your death you go ...""")
            break

        if i > 0:
            global_notification.modify_note(
                f"See? Wasn't that hard now, was it?")
        i += 1

    return player_input


def validate_input(command, game):
    """
    Validates and sanitizes user input and initiates associated action
    """
    new_command = ""
    new_command = command[:].lower()

    try:
        if command in COMMANDS["help"]:
            help(game)
        elif command in COMMANDS["use"]:
            if len(global_player.inventory) < 1:
                global_notification.modify_note(f"You don't own anything.")
            else:
                use(game)
        elif command in COMMANDS["move"]:
            regen_life()
            move = game.attempt_move("player", 0, command)
            if move == 1:
                global_notification.modify_note(
                    f"{COMMANDS['move'].get(command)}")
                entity = game.identify_entity()
                if entity:
                    entity_interaction(entity, game)
            elif move == 0:
                global_notification.modify_note("You can't go there.")
            else:  # move == 2
                string = "Once you descended the stairway, the way closed up "\
                         "behind you. Bummer!"
                global_notification.modify_note(string)
                return move

        elif not command:
            global_notification.modify_note(
                "Well you have to write something at least!")
        else:
            global_notification.modify_note(
                f"I'm afraid '{command}' does not compute!")
        return 0
    except:
        global_notification.modify_note(
            "Error, the developer screwed up! Try restarting the game.")


def entity_interaction(interacting_entity, game):
    """
    Deals with an entity once engaged
    """
    lane_factor = utils.return_lane(interacting_entity[1])

    # gold
    if interacting_entity[0] == game.global_entities["gold"]["sym"]:

        min_amount = round(5 * (1 + (game.global_level/10)/6))
        max_amount = round(10 * (1 + (game.global_level/10)/3))
        amount = round(randrange(min_amount, max_amount) * (1 + lane_factor))
        global_player.add_attribute_amount("gold", amount)
        global_notification.modify_note(f"You found {amount} gold!")

    # enemies
    if interacting_entity[0] == game.global_entities["enemy"]["sym"]:

        if not hasattr(global_player, "temp_dmg"):
            global_player.temp_dmg = 0
        if not hasattr(global_player, "temp_hp"):
            global_player.temp_hp = 0

        min_amount = round((1 + game.global_level/4)*2)
        max_amount = round((1 + game.global_level/5)*5)
        hp_amount = round(
            randrange(min_amount, min_amount*2) * (1 + lane_factor))
        dmg_amount = round(
            randrange(min_amount, max_amount) * (1 + lane_factor))

        hits = int(math.ceil(hp_amount/(global_player.dmg +
                                        global_player.temp_dmg)))
        dmg_taken = ((hits-1) * (abs(min(0,
                                         global_player.armor -
                                         dmg_amount)))) - global_player.temp_hp
        dmg_dealt_player = global_player.dmg + global_player.temp_dmg

        dmg_dealt_enemy = (hits-1) * dmg_amount
        dmg_after_shield = dmg_dealt_enemy - global_player.temp_hp
        if dmg_after_shield <= 0:
            global_player.temp_hp -= dmg_dealt_enemy
            dmg_after_shield = 0
            dmg_after_mitigation = 0
        else:
            dmg_after_mitigation = dmg_after_shield - ((
                hits-1) * global_player.armor)
            global_player.temp_hp = 0
        if dmg_after_mitigation < 0:
            dmg_after_mitigation = 0

        final_dmg = dmg_after_mitigation
        if dmg_dealt_player >= hp_amount:
            display_enemy = "The enemy was killed before it could react"
        else:
            display_enemy = f"The enemy tried to deal {dmg_dealt_enemy} dmg"
        if final_dmg == 0:
            display_damage = "you took no dmg"
        else:
            display_damage = f"mitigation reduced that to {final_dmg} dmg"

        str_player = f"You dealt {dmg_dealt_player} dmg per hit and killed: "
        str_enemy_name = utils.generate_enemy_name()

        global_notification.modify_note(f"""{str_player}{str_enemy_name}
     {display_enemy}, {display_damage}!""")

        global_player.hp_cur -= final_dmg
        if global_player.hp_cur <= 0:
            game_over(game)

    # vendor
    if interacting_entity[0] == game.global_entities["vendor"]["sym"]:
        vendor(game)

    # loot
    if interacting_entity[0] == game.global_entities["loot"]["sym"]:
        loot = utils.create_loot(game.global_level)
        if loot[0] == "loot":
            string = f"You found some loot: {loot[1]} x{loot[2]}"
            if loot[1] in global_player.inventory.keys():
                global_player.inventory[loot[1]] += loot[2]
            else:
                global_player.inventory[loot[1]] = loot[2]

        elif loot[0] == "weapon":
            if loot[2] > global_player.dmg:
                global_player.dmg = loot[2]
                string = f"You found and equipped the {loot[0]}, {loot[1]}"
                f"(+{loot[2]})"
            else:
                string = f"""You found the {loot[0]}, {loot[1]} (+{loot[2]}) -
                 it was not an upgrade."""

        elif loot[0] == "scroll":
            string = f"You found a {loot[1]}"
            if loot[1] in global_player.inventory.keys():
                global_player.inventory[loot[1]] += loot[2]
            else:
                global_player.inventory[loot[1]] = loot[2]

        else:  # armor
            if loot[2] > global_player.armor:
                global_player.armor = loot[2]
                string = f"""You found and equipped a piece of {loot[0]},
                 {loot[1]} (+{loot[2]})"""
            else:
                string = f"""You found a piece of {loot[0]}, {loot[1]}
                 (+{loot[2]}) - it was not an upgrade."""

        global_notification.modify_note(string)


def print_top_infobar():
    """
    Prints the players health bar at the top right of the map
    """
    max = int(global_player.hp_max/10)
    cur = int(math.ceil(global_player.hp_cur/10))
    name = global_player.name
    health_string = f"Health ({global_player.hp_cur}) "

    front_gap = 5
    screen_length = 78 - front_gap

    player_info = []

    # to align with map borders
    for i in range(front_gap):
        player_info.append(" ")

    # adding the name
    name_to_display = f"{cf.GREEN}Name: {name}{cs.RESET_ALL}"
    player_info.append(name_to_display)

    # adding space between name and health bar
    for i in range(screen_length - len(name)-6 - len(health_string) - max):
        player_info.append(" ")

    player_info.append(health_string)

    # adding full health bar pieces
    for i in range(cur):
        player_info.append(
            cf.RED + utils.sym("square") + cs.RESET_ALL)

    # adding empty health bar pieces
    if cur != max:
        for i in range(max-cur):
            player_info.append(cf.RED + "-" + cs.RESET_ALL)
            cs.RESET_ALL

    print("".join(player_info))


def print_bottom_infobar(game):
    """
    Prints the level at the bottom right of the map
    """
    front_gap = 5
    screen_length = 78 - front_gap

    bottom_info = []

    for i in range(front_gap):
        bottom_info.append(" ")

    front_text = f"{cf.YELLOW}"\
        f"{utils.sym(game.global_entities['gold']['sym'])} "\
        f"Gold: {str(global_player.gold)}{cs.RESET_ALL}"
    middle_text = f" | Armor: {global_player.armor}, Damage:"\
        f" {global_player.dmg}"
    back_text = "Level " + str(game.global_level)

    bottom_info.append(front_text)
    bottom_info.append(middle_text)
    len_mt = len(middle_text)
    len_bt = len(back_text)
    for i in range(screen_length - len(front_text)+9 - len_mt - len_bt):
        bottom_info.append(" ")

    bottom_info.append(back_text)

    print("".join(bottom_info))


def help(game):
    """
    Displays the help menu
    """
    # clearing the screen
    system('cls||clear')

    print(f"Welcome to the help screen of {cf.YELLOW}Endless "
          f"Dungeons on a Budget{cs.RESET_ALL}")

    help_text = f"""
    This game is quite simple. You ({
    getattr(cf, game.global_entities["player"]["Fore"])}{
    utils.sym(game.global_entities["player"]["sym"])}{
    cs.RESET_ALL}) venture through a randomly
    generated dungeon. Level by level you try to delve deeper until you
    either give up or get yourself killed. Throughout you will find
    gold {getattr(cf, game.global_entities["gold"]["Fore"])}{
    utils.sym(game.global_entities["gold"]["sym"])}{cs.RESET_ALL}, loot {
    getattr(cf, game.global_entities["loot"]["Fore"])}{
    utils.sym(game.global_entities["loot"]["sym"])}{
    cs.RESET_ALL} , monsters {getattr(
    cf, game.global_entities["enemy"]["Fore"])}{utils.sym(
    game.global_entities["enemy"]["sym"])}{cs.RESET_ALL}  and a vendor {
    getattr(cf, game.global_entities["vendor"]["Fore"])}{utils.sym(
    game.global_entities["vendor"]["sym"])}{
    cs.RESET_ALL}  to trade with.\n
    The dungeon is divided into 3 "lanes", marked L1, L2 or L3.
    L1 is the safest lane, L3 the hardest. It depends on you to choose
    which lanes to stick to. That is if the dungeon gives you a choice.\n
    The following loot {getattr(cf, game.global_entities["loot"]["Fore"])}{
    utils.sym(game.global_entities["loot"]["sym"])}{
    cs.RESET_ALL}  can be found:
    - Health Potion - heals you for 25
    - Rations - heals you per turn for 4, up to 40 in total
    - Scroll of Fireball - increases the strength of your next attack
      > based on level
    - Scroll of Shielding - gives you a shield, not mitigated by armor
      > based on level
    - Scroll of Healing - heals you to full
    - Scroll of Obliteration - destroys all enemies from the level\n
    The following actions are available to you:
    - {cf.CYAN}Move{
    cs.RESET_ALL} around (think north, south, west & east)
        > commands: {cf.CYAN}{list_of_commands('move')}{cs.RESET_ALL}
    - {cf.CYAN}Use{cs.RESET_ALL} an item from your inventory
        > commands: {cf.CYAN}{list_of_commands('use')}{cs.RESET_ALL}
    - This {cf.CYAN}help{cs.RESET_ALL} screen
        > commands: {cf.CYAN}{list_of_commands('help')}{cs.RESET_ALL}
    """

    print(help_text)

    global_notification.modify_note(
        "Now that you're done with the help screen, shall we move on?")

    # to stop the main loop from displaying the map
    input("Press Enter to return to the game ...\n> ")


def list_of_commands(key):
    """
    Returns a list of available commands from the COMMANDS constant
    """
    return f"{cf.WHITE},{cs.RESET_ALL} {cf.CYAN}".join(COMMANDS[key])


def vendor(game):
    """
    Displays up the vendor purchase screen incl random selection of items
    """
    # clearing the screen
    system('cls||clear')
    name = utils.generate_vendor_name()
    coin_col = getattr(cf, game.global_entities['gold']['Fore'])
    coin_sym = utils.sym(game.global_entities['gold']['sym'])
    coins = global_player.gold

    coin = f"{coin_col}{coin_sym} {coins}{cs.RESET_ALL}"

    vendor_text = f"""You may call me the {cf.YELLOW}{name}{cs.RESET_ALL}!
... just like the other peasants.\n
It is quite dangerous around here and I was about to pack up.
Have a look around but hurry, I'll be leaving right after
our little chit-chat and hopefully fruitful transaction.\n
You better have the necessary coin, I do not appreciate common
folk like you wasting my time otherwise.\n
You have {coin} with you.\n"""

    print(vendor_text)

    rand_num = randrange(2, 6)
    item_list = {}
    for i in range(rand_num + 1):
        i += 1
        item = utils.create_loot(game.global_level)

        count = f"{cf.CYAN} {i} {cs.RESET_ALL}"
        if item[0] == "weapon" or item[0] == "armor" or item[0] == "scroll":
            formula = (1+(game.global_level/6)) * 100
            price = randrange(int(round(formula*0.8)), int(round(formula)))
        else:
            formula = (1+(game.global_level/12)) * 50
            price = randrange(int(round(formula*0.8)), int(round(formula)))

        if item[1] in item_list:
            if item[2] >= item_list[item[1]]["value"]:
                item_list[item[1]]["value"] = item[2]
                item_list[item[1]]["price"] = price
        else:
            item_list[item[1]] = {
                "name": item[1],
                "type": item[0],
                "value": item[2],
                "price": price
            }

    i = 0
    d = i + 1
    for item in item_list:
        count = f"{cf.CYAN} {d} {cs.RESET_ALL}"
        coin = f"{coin_col}{coin_sym} {item_list[item]['price']}{cs.RESET_ALL}"

        if item_list[item]["type"] == "loot":
            format = f"x{item_list[item]['value']}"
        else:
            format = f"(+{item_list[item]['value']})"

        print(f"    [{count}] {item_list[item]['name']} {format} {coin}")
        item_list[item]["num"] = d

        i += 1
        d += 1

    global_notification.modify_note(
        "Aaaand gone ... I hope you made this visit count!")

    # continues to show until the player is done
    input_msg = f"\nWhich item would you like to buy?\n> "

    while True:
        try:
            player_input = int(input(input_msg))
            if player_input == 0:
                break
            elif player_input in range(1, d):

                # going through the list to find the right item
                selection = None
                for item in item_list:
                    if item_list[item]["num"] == player_input:
                        selection = item_list[item]
                        break

                if selection["price"] > global_player.gold:
                    input_msg = "You don't have enough gold. Anything else"\
                                " maybe?\n"
                else:
                    type = selection["type"]
                    if type == "weapon" or type == "armor":
                        note = f"You bought: {selection['name']}"\
                                "(+{selection['value']})"
                        global_notification.modify_note(note)
                    else:
                        note = f"You bought: {selection['name']} "\
                                "x{selection['value']}"
                        global_notification.modify_note(note)

                    buy_item(selection)
                    break
            elif player_input > len(item_list)-1:
                input_msg = "There is no such offer.\n"
                continue
            elif isinstance(player_input, str):
                input_msg = "Please type a number like 0, 1, 2, etc.\n"
                continue
            else:
                input_msg = "Please type a number like 0, 1, 2, etc.\n"
                continue
        except ValueError:
            input_msg = "Please type something and it must be a number of an "\
                        "item listed above.\n"
            continue


def buy_item(item):
    """
    Buys an item from the vendor and adds it to the inventory
    """
    global_player.gold -= item["price"]

    if item["type"] == "loot" or item["type"] == "scroll":
        if item["name"] in global_player.inventory.keys():
            global_player.inventory[item["name"]] += item["value"]
        else:
            global_player.inventory[item["name"]] = item["value"]
    elif item["type"] == "weapon":
        global_player.dmg = item["value"]
    else:  # armor
        global_player.armor = item["value"]


def use(game):
    # clearing the screen
    system('cls||clear')

    print("Your inventory contains:\n")
    i = 1
    item_list = []
    for item in global_player.inventory:
        item_list.append(item)
        print(
            f"    [ {cf.CYAN}{i}{cs.RESET_ALL} ] {item}"
            f" x{global_player.inventory.get(item)}")
        i += 1

    global_notification.modify_note(
        "Couldn't quite find what you were looking for?\n> ")

    print(f"""
Simply type the corresponding number of the item that you want to use
followed by enter, or exit this screen by typing 0 and then enter.\n""")
    # continues to show until the player is done
    input_msg = "Which item would you like to use?\n> "
    while True:
        try:
            player_input = int(input(input_msg))
            if player_input == 0:
                break
            elif player_input <= len(item_list):
                global_notification.modify_note(
                    f"You have used: {item_list[player_input-1]}")
                use_item(item_list[player_input-1], game)
                break
            elif player_input > len(item_list)-1:
                input_msg = "You don't have more than what's listed.\n"
                continue
            elif isinstance(player_input, str):
                input_msg = "Please type a number like 0, 1, 2, etc.\n"
                continue
            else:
                input_msg = "Please type a number like 0, 1, 2, etc.\n"
                continue
        except ValueError:
            input_msg = "Please type something and it must be a number of an"\
                        "item listed above.\n"
            continue


def use_item(item, game):
    """
    Executes certain actions depending on what items was used
    """
    amount = global_player.inventory.get(item)

    if item == "Health Potion":
        if global_player.hp_cur >= 75:
            health = 100
        else:
            health = global_player.hp_cur + 25
        global_player.hp_cur = health

    if item == "Rations":
        global_player.hot = 40

    if item == "Scroll of Fireball":
        if not hasattr(global_player, "temp_dmg"):
            global_player.temp_dmg = 0
        global_player.temp_dmg = game.global_level*2

    if item == "Scroll of Shielding":
        if not hasattr(global_player, "temp_hp"):
            global_player.temp_hp = 0
        global_player.temp_hp = game.global_level*3

    if item == "Scroll of Healing":
        global_player.hp_cur = 100

    if item == "Scroll of Obliteration":
        enemies = game.global_entities["enemy"]["instance"]
        enemy_amount = len(enemies)
        for i in range(enemy_amount):
            enemies[i]["draw"] = False

    if amount > 1:
        global_player.inventory[item] -= 1
    else:
        del global_player.inventory[item]


def regen_life():
    """
    Regenerates health after usage of rations
    """
    amount = 4
    if not hasattr(global_player, "hot"):
        global_player.hot = 0
    if global_player.hp_cur < 100:
        if global_player.hp_cur > 96:
            amount = 100-global_player.hp_cur
        if global_player.hot > 0:
            remain = global_player.hot
            global_player.hp_cur += amount
            global_player.hot -= amount
    else:
        global_player.hot = 0


def game_over(game):
    """
    End of game screen once health pool reached 0 or less, leading to a restart
    """
    # clearing the screen
    system('cls||clear')
    title = "YOU DIED"
    print(f"""{cf.YELLOW}{custom_fig.renderText(title)}{cs.RESET_ALL}
You reached level {game.global_level} and had {getattr(
cf, game.global_entities["gold"]["Fore"])}{utils.sym(game.global_entities[
"gold"]["sym"])}{cs.RESET_ALL} {global_player.gold}.
You could have dealt {global_player.dmg} dmg and mitigate {
global_player.armor} dmg through your armor!
If you weren't dead, that is.\n
    """)
    global_player.hp_cur = 100
    global_player.dmg = 2
    global_player.gold = 50
    global_player.armor = 2
    global_player.inventory = inventory = {"Rations": 1, "Health Potion": 2}
    global_notification.modify_note("Welcome back!? Better luck this time!")
    input("Restart?\n")

    game.global_level = 0
    next_level(game)


def next_level(game):
    """
    Increments the level of a running game
    """
    new_level = game.global_level + 1
    game = base_map.BaseMap(new_level)
    game.build_map()
    map = game.get_map()
    vis_map.VisibleMap(map).set_mask()

    main(game)


def initiate():
    """
    Initiates the game
    """
    welcome()
    player_name = validate_name()
    global_player.name = player_name
    game = base_map.BaseMap(1)
    game.build_map()
    map = game.get_map()
    vis_map.VisibleMap(map).set_mask()

    main(game)


def main(game):
    """
    Game Logic Loop
    """
    game_status = 0

    while game_status == 0:
        system('cls||clear')
        map = game.get_map()
        entities = game.get_entities()
        print_top_infobar()
        vis_map.VisibleMap(map).display_map(game.global_entities["player"][
            "instance"][0]["coords"], entities)
        print_bottom_infobar(game)
        global_notification.print_note()
        string = "What's next? (type 'help' for a list of possible "\
                 "commands)\n> "
        game_status = validate_input(input(string), game)

    if game_status == 2:
        next_level(game)

initiate()
