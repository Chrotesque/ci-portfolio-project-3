import colorama


symbols = {
  "HT":"-",
  "HH":"=",
  "V":"|",
  "A":" ",
  
}


def colorize(color, char):
  """
  Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
  Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
  Style: DIM, NORMAL, BRIGHT, RESET_ALL
  """
  print(getattr(colorama.Back, color) + char)

def reset_color():
  print(Style.RESET_ALL)

def main():
    """
    Runs the programs functions - https://unicode-table.com/en/blocks/geometric-shapes/
    """
    square = "\u25a0"
    triangle = "\u25bc"
    disc = "\u25cf"
    heart = "\u2665"
    sword = "\u2694"
    death = "\u2620"

    print("12345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print("02       10        20        30        40        50        60        70        80")
    print(f"03+===+===+===+===+===+===+===+===+===+===+")
    print(f"04|   |   |   |   |   |   |   | {triangle} |   |   |")
    print(f"05+---+---+---+---+---+---+---+---+---+---+")
    print(f"06|   |   |   |   |   |   |   |   |   |   |")
    print(f"07+---+---+---+---+---+---+---+---+---+---+")
    print(f"08|   |   |   |   |   |   |   |   |   |   |")
    print(f"09+---+---+---+---+---+---+---+---+---+---+")
    print(f"10|   |   |   |   |   | {death} |   |   |   |   |")
    print(f"11+---+---+---+---+---+---+---+---+---+---+")
    print(f"12|   |   |   | {sword} |   |   |   |   |   |   |")
    print(f"13+===+===+===+===+===+===+===+===+===+===+")
    print("14")
    print("15")
    print("16")
    print("17")
    print("18")
    print("19")
    print("20")
    print("21")
    print("22")
    print("23")
    print("24")
    input("Enter your data here:\n")
    #print(colorize('RED', square))



main()