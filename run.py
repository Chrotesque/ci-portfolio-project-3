# Import of game specific modules
from random import randrange
from os import system
import math
import colorama as c
import utils
import base_map
import visible_map as vis_map
import entity
import notifications
import items

global_notification = notifications.Notifications()
global_player = entity.Player(name="", hp_cur=100, hp_max=100, dmg=2, gold=0, armor=2, inventory={"Scroll of Obliteration":1})

COMMANDS = {
  "help":["help","halp","hlp","h"],
  "restart":["again", "redo", "restart"],
  "move":{
    "w":f"You moved a room to the north {utils.sym('dir_north')}",
    "s":f"You moved a room to the south {utils.sym('dir_south')}",
    "a":f"You moved a room to the west {utils.sym('dir_west')}",
    "d":f"You moved a room to the east {utils.sym('dir_east')}"
  },
  "use":["use", "item"]
}

def welcome():
    """
    Displays the welcome message at the start of the game
    """
    print(f"{c.Fore.YELLOW}Hey there! Welcome to Endless Dungeons on a Budget{c.Style.RESET_ALL}\n")
    print("Be sure to have a look at the help menu first, before you get started.\n")

def validate_name():
    """
    Validates input for the players name, alternatively assigns a name w/o input
    """   
    name_chosen = False
    i = 0
    while name_chosen == False:
        # initial input
        if i == 0:
            player_input = input("To get started - what's your name?\n> ")

        # no player input
        if not player_input:
            player_input = input("Are you sure you don't want to enter a name? You will get one either way.\n> ")
            if not player_input:
                name = utils.generate_player_name()
                global_notification.modify_note(f"Have it your way, '{name}'!")
                break
            else:
                name = player_input
                global_notification.modify_note("See? Wasn't that hard now, was it?")
                break
        # input too long
        elif len(player_input) > 50:
            player_input = input("That's a tad long, try something with less than 56 characters!\n> ")
            if not player_input:
                i += 1
                continue
            else:
                i += 1
                continue
        # player input valid
        else:
            name = player_input
            global_notification.modify_note(f"Welcome {name}! Off to your death you go ...")
            break

        i += 1
    return name

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
                global_notification.modify_note(f"{COMMANDS['move'].get(command)}")
                entity = game.identify_entity()
                if entity:
                    entity_interaction(entity, game)
            elif move == 0:
                global_notification.modify_note("You can't go there.")
            else: # move == 2
                global_notification.modify_note("Once you descended the stairway, the way closed up behind you. Bummer!")
                return move

        elif not command:
            global_notification.modify_note("Well you have to write something at least!")
        else:
            global_notification.modify_note(f"I'm afraid '{command}' does not compute!")
        return 0
    except:
        global_notification.modify_note("Program error, the developer screwed up! Try restarting the game.")


def entity_interaction(interacting_entity, game):
    """
    Deals with an entity once engaged
    """
    lane_factor = utils.return_lane(interacting_entity[1])

    if interacting_entity[0] == game.global_entities["gold"]["sym"]:
        
        min_amount = round(5 * (1 + (game.global_level/10)/6))
        max_amount = round(10 * (1 + (game.global_level/10)/3))
        amount = round(randrange(min_amount,max_amount) * (1 + lane_factor))
        global_player.add_attribute_amount("gold", amount)
        global_notification.modify_note(f"You found {amount} gold!")

    if interacting_entity[0] == game.global_entities["enemy"]["sym"]:

        if not hasattr(global_player, "temp_dmg"):
            global_player.temp_dmg = 0
        if not hasattr(global_player, "temp_hp"):
            global_player.temp_hp = 0
        min_amount = round((1 + game.global_level/4)*2)
        max_amount = round((1 + game.global_level/5)*5)
        hp_amount = round(randrange(min_amount, min_amount*2) * (1 + lane_factor/3))
        dmg_amount = round(randrange(min_amount, max_amount) * (1 + lane_factor/3))
        enemy = entity.Enemy(hp_cur=hp_amount, dmg=dmg_amount)
        hits = int(math.ceil(enemy.hp_cur/(global_player.dmg + global_player.temp_dmg)))
        dmg_taken = ((hits-1) * (abs(min(0, global_player.armor - enemy.dmg)))) - global_player.temp_hp
        dmg_dealt_enemy = (hits-1) * enemy.dmg
        dmg_dealt_player = global_player.dmg + global_player.temp_dmg
        global_player.temp_dmg = 0

        if global_player.temp_hp > 0:
            if dmg_dealt_enemy > global_player.temp_hp:
                global_player.hp_cur -= dmg_dealt_enemy - global_player.temp_hp
                global_player.temp_hp = 0
            else:
                global_player.temp_hp -= dmg_dealt_enemy
        else:
            global_player.hp_cur -= dmg_dealt_enemy

        display_enemy = "The enemy was killed before it could react" if dmg_dealt_player > hp_amount else f"The enemy tried to deal {dmg_dealt_enemy} dmg"
        display_damage = "you took no dmg" if dmg_taken == 0 else f"mitigation reduced that to {str(dmg_taken)} dmg"
        global_notification.modify_note(f"You dealt {dmg_dealt_player} dmg and defeated: {utils.generate_enemy_name()} {hp_amount} {dmg_amount}\n     {display_enemy}, {display_damage}!")

    if interacting_entity[0] == game.global_entities["vendor"]["sym"]:

        vendor()

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
                string = f"You found and equipped the {loot[0]}, {loot[1]} (+{loot[2]})"
            else:
                string = f"You found the {loot[0]}, {loot[1]} (+{loot[2]}) - it was not an upgrade."

        elif loot[0] == "scroll":
            string = f"You found a {loot[1]}"
            if loot[1] in global_player.inventory.keys():
                global_player.inventory[loot[1]] += loot[2]
            else:
                global_player.inventory[loot[1]] = loot[2]

        else: # armor
            if loot[2] > global_player.armor:
                global_player.armor = loot[2]
                string = f"You found and equipped a piece of {loot[0]}, {loot[1]} (+{loot[2]})"
            else:
                string = f"You found a piece of {loot[0]}, {loot[1]} (+{loot[2]}) - it was not an upgrade."

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
    name_to_display = f"{c.Fore.GREEN}Name: {name}{c.Style.RESET_ALL}"
    player_info.append(name_to_display)

    # adding space between name and health bar
    for i in range(screen_length - len(name)-6 - len(health_string) - max):
        player_info.append(" ")

    player_info.append(health_string)

    # adding full health bar pieces
    for i in range(cur):
        player_info.append(c.Fore.RED + utils.sym("square") + c.Style.RESET_ALL)

    # adding empty health bar pieces
    if cur != max:
        for i in range(max-cur):
            player_info.append(c.Fore.RED + "-" + c.Style.RESET_ALL)
            c.Style.RESET_ALL

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

    front_text = f"{c.Fore.YELLOW}{utils.sym(game.global_entities['loot']['sym'])} Gold: {str(global_player.gold)}{c.Style.RESET_ALL}"
    middle_text = f" | Armor: {global_player.armor}, Damage: {global_player.dmg}"
    back_text = "Level " + str(game.global_level)

    bottom_info.append(front_text)
    bottom_info.append(middle_text)
    for i in range(screen_length - len(front_text)+9 - len(middle_text) - len(back_text)):
        bottom_info.append(" ")

    bottom_info.append(back_text)

    print("".join(bottom_info))

def list_of_commands(key):
    """
    Returns a list of available commands from the COMMANDS constant
    """
    return f"{c.Fore.WHITE},{c.Style.RESET_ALL} {c.Fore.CYAN}".join(COMMANDS[key])

def help(game):
    # clearing the screen
    system('cls||clear')

    help_text = f"""Welcome to the help screen of {c.Fore.YELLOW}Endless Dungeons on a Budget{c.Style.RESET_ALL}\n
    This game is quite simple. You ({getattr(c.Fore, game.global_entities["player"]["Fore"])}{utils.sym(game.global_entities["player"]["sym"])}{c.Style.RESET_ALL}) venture through a randomly 
    generated dungeon. Level by level you try to delve deeper until you 
    either give up or get yourself killed. Throughout you will find 
    gold {getattr(c.Fore, game.global_entities["gold"]["Fore"])}{utils.sym(game.global_entities["gold"]["sym"])}{c.Style.RESET_ALL}, loot {getattr(c.Fore, game.global_entities["loot"]["Fore"])}{utils.sym(game.global_entities["loot"]["sym"])}{c.Style.RESET_ALL} , monsters {getattr(c.Fore, game.global_entities["enemy"]["Fore"])}{utils.sym(game.global_entities["enemy"]["sym"])}{c.Style.RESET_ALL}  and a vendor {getattr(c.Fore, game.global_entities["vendor"]["Fore"])}{utils.sym(game.global_entities["vendor"]["sym"])}{c.Style.RESET_ALL}  to trade with.\n
    The dungeon is divided into 3 "lanes", marked L1, L2 or L3. 
    L1 is the safest lane, L3 the hardest. It depends on you to choose
    which lanes to stick to. That is if the dungeon gives you a choice.\n
    The following actions are available to you:
    - {c.Fore.CYAN}Move{c.Style.RESET_ALL} around (think north, south, west & east)
        > commands: {c.Fore.CYAN}{list_of_commands('move')}{c.Style.RESET_ALL}
    - {c.Fore.CYAN}Use{c.Style.RESET_ALL} an item from your inventory
        > commands: {c.Fore.CYAN}{list_of_commands('use')}{c.Style.RESET_ALL}
    - This {c.Fore.CYAN}help{c.Style.RESET_ALL} screen
        > commands: {c.Fore.CYAN}{list_of_commands('help')}{c.Style.RESET_ALL}
    """

    print(help_text)

    global_notification.modify_note("Now that you're done with the help screen, shall we move on?")

    # to stop the main loop from displaying the map
    input("Press Enter to return to the game ...\n> ")

def vendor():
    # clearing the screen
    system('cls||clear')
    name = utils.generate_vendor_name()

    vendor_text = f"""The common folk calls me the {c.Fore.YELLOW}{name}{c.Style.RESET_ALL}!\n
    Welcome to my shop! It is quite dangerous around here and I was about 
    to leave. Have a look around but hurry, I'll be leaving right after our 
    little chit-chat and hopefully fruitful transaction.\n
    You better have the necessary coin, I do not appreciate common folk
    like you wasting my time otherwise.\n
    - {c.Fore.CYAN}Move{c.Style.RESET_ALL} around (think north, south, west & east)
        > commands: {c.Fore.CYAN}{list_of_commands('move')}{c.Style.RESET_ALL}
    - {c.Fore.CYAN}Use{c.Style.RESET_ALL} an item from your inventory
        > commands: {c.Fore.CYAN}{list_of_commands('use')}{c.Style.RESET_ALL}
    - {c.Fore.CYAN}Restart{c.Style.RESET_ALL}, in case you want to begin anew
        > commands: {c.Fore.CYAN}{list_of_commands('restart')}{c.Style.RESET_ALL}
    - This {c.Fore.CYAN}help{c.Style.RESET_ALL} screen
        > commands: {c.Fore.CYAN}{list_of_commands('help')}{c.Style.RESET_ALL}
    """

    print(vendor_text)

    global_notification.modify_note("And gone ... I hope you made this visit count!")

    # continues to show until the player is done
    player_input = ""
    while not player_input:
        player_input = input("Press Enter to return to the game ...\n> ")

def use(game):
    # clearing the screen
    system('cls||clear')
    
    print("Your inventory contains:\n")
    i = 1
    item_list = []
    for item in global_player.inventory:
        item_list.append(item)
        print(f"[{i}] {item} x{global_player.inventory.get(item)}")
        i += 1

    global_notification.modify_note("Couldn't quite find what you were looking for?\n> ")

    print("""\nSimply type the corresponding number of the item that you want 
to use followed by enter, or exit this screen by typing 0 and then enter.
    """)
    # continues to show until the player is done
    input_msg = "Which item would you like to use?\n> "
    while True:
        try:
            player_input = int(input(input_msg))
            if player_input == 0:
                break
            elif player_input <= len(item_list):
                global_notification.modify_note(f"You have used: {item_list[player_input-1]}")
                use_item(item_list[player_input-1], game)
                break
            elif player_input > len(item_list)-1:
                input_msg = "You don't own that.\n"
                continue
            elif isinstance(player_input, str):
                input_msg = "Please type a number like 0, 1, 2, etc.\n"
                continue
            else:
                input_msg = "Please type a number like 0, 1, 2, etc.\n"
                continue
        except ValueError:
            input_msg = "The rules are: type something and it must be a number of an item listed above.\n"
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

def next_level(game):
    """
    Increases the level of a running game
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
    name = validate_name()
    global_player.name = name
    game = base_map.BaseMap(15)
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
        #system('cls||clear')
        map = game.get_map()
        entities = game.get_entities()
        print_top_infobar()
        vis_map.VisibleMap(map).display_map(game.global_entities["player"]["instance"][0]["coords"], entities)
        print_bottom_infobar(game)
        global_notification.print_note()
        
        game_status = validate_input(input("What's next? (type 'help' for a list of possible commands)\n> "), game)

    if game_status == 2:
        next_level(game)

    if game_status == 1:
        game_over()

initiate()