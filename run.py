# Import of game specific modules
from random import randrange
from os import system
import base_map
import visible_map as vis_map
import entity

COMMANDS = {
  "help":["help","halp","hlp","h"],
  "exit":["exit", "quit", "stop", "restart", "q"],
  "move":["w", "s", "a", "d"],
  "use":["use", "item"]
}

def validate_name(command):
  """
  Validates input for the players name, alternatively assigns a name wo input
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

  if not command:
    second_chance = input("Are you sure you don't want to enter a name?\n")
    if not second_chance:
      name = names[randrange(0,len(names))]
    else:
      name = second_chance
  else:
    name = command

  return name

def request_input(game):
  player_input = input("What's next? (type 'help' for a list of possible commands\n")
  validate_input(player_input, game)

def validate_input(command, game):
  """
  Validates and sanitizes user input and initiates associated action
  """
  command = command.lower()

  try:
    if command in COMMANDS["help"]:
      print("help screen requested")
    elif command in COMMANDS["exit"]:
      exit = input("Are you sure you want to restart the game from scratch?\n")
      if not exit:
        print("no input on restart game")
      else:
        print("game restart requested")
    elif command in COMMANDS["use"]:
      print("use of item requested")
    elif command in COMMANDS["move"]:
      print(f"movement input detected: {command}")
      game.attempt_move("player", 0, command)
    else:
      print("Unknown command")
  except:
    ""

def list_of_commands(key):
  """
  Returns a list of available commands from the COMMANDS constant
  """
  return ", ".join(COMMANDS[key])

def initiate():
  """
  Initiates the game
  """
  name = validate_name(input("What's your name?\n"))
  player = entity.Player(name, 10, 2)
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
    #system('cls||clear')
    print(f"Player: {player.name} / HP: {player.hp} / DMG: {player.dmg}")
    print(f"Current Level: {level}")
    map = game.get_map()
    vis_map.VisibleMap(map).display_map(base_map.BaseMap.ENTITIES["player"]["instance"][0]["coords"])
    player_input = request_input(game)

initiate()