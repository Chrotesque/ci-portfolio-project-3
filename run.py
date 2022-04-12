# Import of game specific modules
import random as r
import base_map
import visible_map as vis_map
import entity

def request_input():
  player_input = input("What's next? (type 'help' for a list of possible commands\n")
  validate_input(player_input)

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
      name = names[r.randrange(0,len(names))]
    else:
      name = second_chance
  else:
    name = command

  return name

def validate_input(command):
  try:
    if command == "help":
      print("help requested")
    elif command == "use":
      print("use of item requested")
    elif command == ("W" or "A" or "S" or "D"):
      print(f"movement input detected: {command}")
    else:
      ""
  except:
    ""

def initiate():

  name = validate_name(input("What's your name?\n"))
  player = entity.Player(name, 10, 2)
  print(f"Player: {player.name} / HP: {player.hp} / DMG: {player.dmg}")

  game = base_map.BaseMap(10)
  game.build_map()

  main(game)

def main():
  """
  Runs the game logic
  """
  level = 10
  player = entity.Player("Bobster", 10, 2)

  print(f"Player: {player.name} / HP: {player.hp} / DMG: {player.dmg}")
  print(f"Current Level: {level}")

  test = base_map.BaseMap(level)
  test.build_map()
  player_input = request_input()

initiate()
#main()