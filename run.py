# Import of game specific modules
from random import randrange
from os import system
import colorama as c
import utils
import base_map
import visible_map as vis_map
import entity

class Notifications:

    global_notification = "..."

    def modify_note(self, note):
        self.global_notification = note

    def print_note(self):
        """
        Prints the narrator note
        """
        gap = 5
        string = ""
        for i in range(gap):
            string += " "

        print("\n")
        print(f"{string}{c.Fore.YELLOW}Narrator:{c.Style.RESET_ALL}")
        print(f"{string}{self.global_notification}\n")

global_notification = Notifications()
global_player = entity.Player("", 5, 10, 2, 0)

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
    names = [
        "Unknown Adventurer",
        "Very Anonymous Adventurer",
        "Reluctant Adventurer",
        "Privacy Conscious Adventurer",
        "Adventurer of Solitude and Mystery",
        "Mysterious Adventurer",
        "Mr. Confidentiality"
    ]
   
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
                name = names[randrange(0,len(names))]
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
            help()
        elif command in COMMANDS["restart"]:
            exit = input("Are you sure you want to restart the game from scratch?\n> ")
            if not exit:
                print("no input on restart game")
            else:
                print("game restart requested")
        elif command in COMMANDS["use"]:
            print("use of item requested")
        elif command in COMMANDS["move"]:
        
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

def entity_interaction(entity, game):
    """

    """
    lane_factor = utils.return_lane(entity[1])

    if entity[0] == game.global_entities["loot"]["sym"]:
        
        min_amount = round(5 * (1 + (game.global_level/10)/6))
        max_amount = round(10 * (1 + (game.global_level/10)/3))
        amount = round(randrange(min_amount,max_amount) * (1 + lane_factor))
        global_player.add_gold(amount)
        global_notification.modify_note(f"You found {amount} gold!")

    if entity[0] == game.global_entities["enemy"]["sym"]:

        global_notification.modify_note(f"You fought and defeated: {utils.generate_enemy_name()}!")



def print_top_infobar():
    """
    Prints the players health bar at the top right of the map
    """
    max = global_player.hp_max
    cur = global_player.hp_cur
    name = global_player.name
    health_string = "Health "

    front_gap = 5
    screen_length = 78 - front_gap
    
    player_info = []

    # to align with map borders
    for i in range(front_gap):
        player_info.append(" ")

    # adding the name
    player_info.append("Name: " + name)

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
    back_text = "Level " + str(game.global_level)

    bottom_info.append(front_text)
    for i in range(screen_length - len(front_text)+9 - len(back_text)):
        bottom_info.append(" ")

    bottom_info.append(back_text)

    print("".join(bottom_info))

def list_of_commands(key):
    """
    Returns a list of available commands from the COMMANDS constant
    """
    return f"{c.Fore.WHITE},{c.Style.RESET_ALL} {c.Fore.CYAN}".join(COMMANDS[key])

def help():
    # clearing the screen
    system('cls||clear')

    help_text = f"""Welcome to the help screen of {c.Fore.YELLOW}Endless Dungeons on a Budget{c.Style.RESET_ALL}\n
    This game is quite simple. You ({c.Fore.GREEN}{utils.sym('disc')}{c.Style.RESET_ALL}) venture through a randomly 
    generated dungeon. Level by level you try to delve deeper until you 
    either give up or get yourself killed. Throughout you will find loot, 
    monsters, etc.\n
    The dungeon is divided into 3 "lanes", marked L1, L2 or L3. 
    L1 is the safest lane, L3 the hardest. It depends on you to choose
    which lanes to stick to. That is if the dungeon gives you a choice.\n
    The following actions are available to you:
    - {c.Fore.CYAN}Move{c.Style.RESET_ALL} around (think north, south, west & east)
        > commands: {c.Fore.CYAN}{list_of_commands('move')}{c.Style.RESET_ALL}
    - {c.Fore.CYAN}Use{c.Style.RESET_ALL} an item from your inventory
        > commands: {c.Fore.CYAN}{list_of_commands('use')}{c.Style.RESET_ALL}
    - {c.Fore.CYAN}Restart{c.Style.RESET_ALL}, in case you want to begin anew
        > commands: {c.Fore.CYAN}{list_of_commands('restart')}{c.Style.RESET_ALL}
    - This {c.Fore.CYAN}help{c.Style.RESET_ALL} screen
        > commands: {c.Fore.CYAN}{list_of_commands('help')}{c.Style.RESET_ALL}
    """

    print(help_text)

    global_notification.modify_note("Now that you're done with the help screen, shall we move on?")

    # to stop the main loop from displaying the map
    input("Press Enter to return to the game ...\n> ")

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