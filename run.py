# Import of game specific modules
from random import randrange
from os import system
import colorama as c
import func
import base_map
import visible_map as vis_map
import entity

class Notifications:

    note_to_display = "..."

    def modify_note(self, note):
        self.note_to_display = note

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
        print(f"{string}{self.note_to_display}\n")

note_to_display = Notifications()

COMMANDS = {
  "help":["help","halp","hlp","h"],
  "restart":["again", "redo", "restart"],
  "move":{
    "w":f"You moved a room to the north {func.sym('dir_north')}",
    "s":f"You moved a room to the south {func.sym('dir_south')}",
    "a":f"You moved a room to the west {func.sym('dir_west')}",
    "d":f"You moved a room to the east {func.sym('dir_east')}"
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
                note_to_display.modify_note(f"Have it your way, '{name}'!")
                break
            else:
                name = player_input
                note_to_display.modify_note("See? Wasn't that hard now, was it?")
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
            note_to_display.modify_note(f"Welcome {name}! Off to your death you go ...")
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
            if move:
                note_to_display.modify_note(f"{COMMANDS['move'].get(command)}")
            else:
                note_to_display.modify_note("You can't go there.")

        else:
            note_to_display.modify_note(f"I'm afraid '{command}' does not compute!")
    except:
        note_to_display.modify_note("Program error, the developer screwed up! Try restarting the game.")

def print_top_infobar(player):
    """
    Prints the players health bar at the top right of the map
    """
    max = player.hp_max
    cur = player.hp_cur
    name = player.name
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
        i += 1

    player_info.append(health_string)

    # adding full health bar pieces
    for i in range(cur):
        player_info.append(c.Fore.RED + func.sym("square") + c.Style.RESET_ALL)
        i += 1

    # adding empty health bar pieces
    if cur != max:
        for i in range(max-cur):
            player_info.append(c.Fore.RED + "-" + c.Style.RESET_ALL)
            c.Style.RESET_ALL
            i += 1

    print("".join(player_info))

def print_bottom_infobar(player, level):
    """
    Prints the level at the bottom right of the map
    """
    front_gap = 5
    screen_length = 78 - front_gap

    bottom_info = []

    for i in range(front_gap):
        bottom_info.append(" ")

    front_text = f"{c.Fore.YELLOW}{func.sym('star')} Gold: {str(player.gold)}{c.Style.RESET_ALL}"
    back_text = "Level " + str(level)

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

    help_text = f"""Welcome to the help screen of {c.Fore.YELLOW}Endless Dungeons on a Budget{c.Style.RESET_ALL}
    This game is quite simple. You ({c.Fore.GREEN}{func.sym('disc')}{c.Style.RESET_ALL}) venture through a randomly 
    generated dungeon. Level by level you try to delve deeper until you 
    either give up or get yourself killed. Throughout you will find loot, 
    monsters, etc.

    The dungeon is divided into 3 "lanes", marked L1, L2 or L3. 
    L1 is the safest lane, L3 the hardest. It depends on you to choose
    which lanes to stick to. That is if the dungeon gives you a choice.

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

    note_to_display.modify_note("Now that you're done with the help screen, shall we move on?")

    # to stop the main loop from displaying the map
    input("Press Enter to return to the game ...\n> ")

def initiate():
    """
    Initiates the game
    """
    welcome()
    name = validate_name()
    player = entity.Player(name, 5, 10, 2, 0)
    level = 10
    game = base_map.BaseMap(level)
    game.build_map()
    map = game.get_map()
    vis_map.VisibleMap(map).set_mask()

    main(game, player, level)

def new_level(level):
    """
    Increases the level of a running game
    """
    new_level = level+1

def main(game, player, level):
    """
    Game Logic Loop
    """

    game_over = False

    while game_over == False:
        system('cls||clear')
        map = game.get_map()

        print_top_infobar(player)
        vis_map.VisibleMap(map).display_map(base_map.BaseMap.ENTITIES["player"]["instance"][0]["coords"])
        print_bottom_infobar(player, level)
        note_to_display.print_note()
        
        validate_input(input("What's next? (type 'help' for a list of possible commands)\n> "), game)


initiate()