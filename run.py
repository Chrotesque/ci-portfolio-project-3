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

        print(f"""{string}{c.Fore.YELLOW}Narrator:{c.Style.RESET_ALL}
     {self.note_to_display}
        """)

note_to_display = Notifications()

COMMANDS = {
  "help":["help","halp","hlp","h"],
  "exit":["exit", "quit", "stop", "restart"],
  "move":{
    "w":f"You moved a room to the north {func.sym('dir_north')}",
    "s":f"You moved a room to the south {func.sym('dir_south')}",
    "a":f"You moved a room to the west {func.sym('dir_west')}",
    "d":f"You moved a room to the east {func.sym('dir_east')}"
  },
  "use":["use", "item"]
}

last_activity = "test"

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

    print(f"""
    
    Hey there! {c.Fore.YELLOW}Welcome to Endless Dungeons on a Budget{c.Style.RESET_ALL}
    
    """)

    player_input = input("To get started - what's your name?\n")

    if not player_input:
        second_chance = input("Are you sure you don't want to enter a name? You will get one either way.\n")
        if not second_chance:
            name = names[randrange(0,len(names))]
            note_to_display.modify_note(f"Have it your way, '{name}'!")
        else:
            name = second_chance
            note_to_display.modify_note("See? Wasn't that hard now, was it?")
    else:
        name = player_input
        note_to_display.modify_note(f"Welcome {name}! Off to your death you go ...")

    return name

def request_input(game):
    player_input = input("What's next? (type 'help' for a list of possible commands)\n")
    validate_input(player_input, game)

def validate_input(command, game):
    """
    Validates and sanitizes user input and initiates associated action
    """
    command = command.lower()

    try:
        if command in COMMANDS["help"]:
            help()
        elif command in COMMANDS["exit"]:
            exit = input("Are you sure you want to restart the game from scratch?\n")
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
            note_to_display.modify_note(f"The command {command} is not recognized.")
    except:
        print("this shouldnt happen")
        note_to_display.modify_note("this shouldn't happen")

def list_of_commands(key):
    """
    Returns a list of available commands from the COMMANDS constant
    """
    return ", ".join(COMMANDS[key])

def show_last_activity(string):
    """

    """
    print(f"""
        ... {str(string)}
    """)

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
    player_info.append(name)

    # adding space between name and health bar
    for i in range(screen_length - len(name) - len(health_string) - max):
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

def print_bottom_infobar(level):
    """
    Prints the level at the bottom right of the map
    """
    empty = ""
    string = "Level " + str(level)

    for i in range(78-len(string)):
        empty += " "
    print(f"{empty}{string}")

def help():
    # clearing the screen
    system('cls||clear')

    print(f"""
    {c.Fore.YELLOW}Welcome to the help screen of Endless Dungeons on a Budget{c.Style.RESET_ALL}

        This game is quite simple. You ({c.Fore.GREEN}{func.sym('disc')}{c.Style.RESET_ALL}) venture through a procedurally generated dungeon.
        Level by level you try to delve deeper until you either give up or get yourself killed. 
        Throughout the way you will find some loot, some monsters and maybe a friendly 
        neighborhood vendor here and there to help you. For a price {c.Fore.YELLOW}{func.sym('star')}{c.Style.RESET_ALL}  of course.
    """)

    # to stop the main loop from displaying the map
    input("Press Enter or type anything (and then press enter) to return to the game\n")

def initiate():
    """
    Initiates the game
    """
    name = validate_name()
    player = entity.Player(name, 5, 10, 2)
    level = 10
    game = base_map.BaseMap(level)
    game.build_map()
    map = game.get_map()
    vis_map.VisibleMap(map).set_mask()

    main(game, player, level)

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
        print_bottom_infobar(level)
        note_to_display.print_note()
        
        player_input = request_input(game)

initiate()