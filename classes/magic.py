import random

class Spell:
    def __init__(self, name, cost, dmg, type):
         self.name = name
         self.cost = cost
         self.dmg = dmg
         self.type = type

    def generate_damage(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)

    def enemy_generate_damage(self):
        low = self.dmg - 400
        high = self.dmg + 400
        return random.randrange(low, high)