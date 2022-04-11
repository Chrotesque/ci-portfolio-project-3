# Import of game specific modules
import base_map
import visible_map as vis_map
import entity

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

main()