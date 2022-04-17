import colorama as c

class Notifications:

    global_notification = "..."

    def modify_note(self, note):
        """
        Modifies the global note
        """
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