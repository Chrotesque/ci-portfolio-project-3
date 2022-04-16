class Entity:

    def __init__(self, name, hp_cur, dmg):
        self.name = name
        self.hp_cur = hp_cur
        self.dmg = dmg

class Player(Entity):

    def __init__(self, name, hp_cur, hp_max, dmg, gold):
        super().__init__(name, hp_cur, dmg)
        self.hp_max = hp_max
        self.gold = gold

    def add_gold(self, amount):
        """
        Adds a certain amount to the players gold
        """
        self.gold += amount

    def remove_gold(self, amount):
        """
        Removes a certain amount to the players gold
        """
        self.gold -= amount


class Enemy(Entity):

    def __init__(self, name, hp_cur, dmg):
        super().__init__(name, hp_cur, dmg)