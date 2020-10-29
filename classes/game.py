import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, attack, defense, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.attack_low = attack - 10
        self.attack_high = attack + 10
        self.enemy_attack_low = attack - 400
        self.enemy_attack_high = attack + 400
        self.defense = defense
        self.magic = magic
        self.actions = ['Attack', 'Magic', 'Items']
        self.items = items

    def generate_damage(self):
        return random.randrange(self.attack_low, self.attack_high)

    def enemy_generate_damage(self):
        return random.randrange(self.enemy_attack_low, self.enemy_attack_high)

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print(bcolors.UNDERLINE + bcolors.BOLD + self.name + '\'s', 'turn' + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD+ "Actions" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ":", item)
            i += 1

    def choose_target(self, enemies):
        i = 1
        print('\n' + bcolors.FAIL + bcolors.BOLD + 'TARGETS:' + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + '.', enemy.name)
                i += 1
        choice = int(input('Choose Target')) - 1

        return choice

    def choose_magic(self):
        i = 1
        print('\n' + bcolors.OKBLUE + 'Spell Book' + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ':', spell.name, '(cost:', str(spell.cost) + ")" + '(dmg: ' + str(spell.dmg) + ')')
            i += 1

    def choose_item(self):
        i = 1
        print('\n' + bcolors.OKBLUE + 'Your Inventory' + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ':', item['item'].name, '(' + str(item['item'].description) + ')',
                  'x' + str(item['quantity']))
            i += 1

    def get_enemy_stats(self):
        hp_bar = ''
        bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += '█'
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += ' '

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ''

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)
            while decreased > 0:
                current_hp += ' '
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("NAME                       HP                                 ")
        print(bcolors.BOLD + self.name + ':   ' + current_hp + bcolors.FAIL +
              '  |' + hp_bar + '|    ' + bcolors.ENDC)

    def get_stats(self):
        hp_bar = ''
        hp_bar_ticks = (self.hp / self.maxhp) * 100 / 4

        mp_bar = ''
        mp_bar_ticks = (self.mp / self.maxmp) * 100 / 10

        while hp_bar_ticks > 0:
            hp_bar += '█'
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += ' '

        while mp_bar_ticks > 0:
            mp_bar += '█'
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += ' '

        # Fix the whitespace of HP bar when HP goes below 1000
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ''

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += ' '
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        #Fix the whitespace of MP bar when it goes below 100
        mp_string = str(self.mp) + '/' + str(self.maxmp)
        current_mp = ''

        if len(mp_string) < 7:
            decreased = 7 -len(mp_string)

            while decreased > 0:
                current_mp += ' '
                decreased -= 1

            current_mp += hp_string
        else:
            current_mp = mp_string


        print("NAME                  HP                                      MP")
        print(bcolors.BOLD + self.name + ':   ' +
              current_hp + bcolors.OKGREEN + '  |' + hp_bar + '|    '
              + bcolors.ENDC + bcolors.BOLD + str(self.mp) + '/' + str(self.maxmp) + '  ' +
              bcolors.OKBLUE + '|' + mp_bar + '|' + bcolors.ENDC)

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.enemy_generate_damage()

        pct = self.mp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == 'white' and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg
