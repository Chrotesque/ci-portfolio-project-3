class Items:

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class Potion(Items):

    def __init__(self, strength):
        super().__init__(name, amount)
        self.strength = strength
    
class Scroll(Items):

    def __init__(self, effect):
        super().__init__(name, amount)
        self.effect = effect