class Entity:

    def __init__(self, name, hp, dmg):
        self.name = name
        self.hp = hp
        self.dmg = dmg

class Player(Entity):

    def __init__(self, name, hp, dmg):
        super().__init__(name, hp, dmg)

class Enemy(Entity):

    def __init__(self, name, hp, dmg):
        super().__init__(name, hp, dmg)