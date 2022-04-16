class Entity:

    def __init__(self, hp_cur, dmg):
        self.hp_cur = hp_cur
        self.dmg = dmg

class Player(Entity):

    def __init__(self, name, hp_cur, hp_max, armor, dmg, gold):
        super().__init__(hp_cur, dmg)
        self.name = name
        self.hp_max = hp_max
        self.armor = armor
        self.gold = gold

    def add_attribute_amount(self, attribute, amount):
        """
        Adds a certain amount to a chosen attribute
        """
        setattr(self, attribute, amount)


class Enemy(Entity):

    def __init__(self, hp_cur, dmg):
        super().__init__(hp_cur, dmg)