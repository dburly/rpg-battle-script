from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random



print('\n\n')

print('\n\n')
#Create Black Magic
fire = Spell('Fireball', 7, 300, 'black')
thunder = Spell('Thunderstrike', 11, 450, 'black')
blizzard = Spell('Icebolt', 4, 215, 'black')
meteor = Spell('Meteor', 19, 999, 'black')
quake = Spell('Earthquake', 14, 850, 'black')

infest = Spell('Infest', 0, 1000, 'black')
remorseless_winter = Spell('Remorseless Winter', 15, 800, 'black')
defile = Spell('Defile', 0, 1200, 'black')


#Create White Magic
cure = Spell('Renewing Mist', 1, 300, 'white')
cura = Spell('Enveloping Mist', 3, 550, 'white')

#Create some items
healing_potion = Item('Healing Potion', 'potion', 'Heals 150 HP', 150)
greater_healing_potion = Item('Greater Healing Potion', 'potion', 'Heals for 350 HP', 350)
mega_healing_potion = Item('Mega Healing Potion', 'potion', 'Heals for 1000 HP', 1000)
elixer = Item('Elixer', 'elixer', 'Fully restores the HP and MP of one party member', 9999)
greater_elixer = Item('Greater Elixer', 'elixer', 'Fully restores the HP and MP of all party members', 9999)

grenade = Item('Grenade', 'attack', 'Deals 500 damage', 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
lk_spells = [infest, remorseless_winter, defile]
player_items = [{'item': healing_potion, 'quantity': 7}, {'item': greater_healing_potion, 'quantity': 5},
                {'item': mega_healing_potion, 'quantity': 1}, {'item': elixer, 'quantity': 2},
                {'item': greater_elixer, 'quantity': 2}, {'item': grenade, 'quantity': 2}]

    #[healing_potion, greater_healing_potion, mega_healing_potion, elixer, greater_elixer, grenade]

#Instantiate People
player1 = Person('Gromm', 6000, 100, 450, 100, player_spells, player_items)
player2 = Person('Defit', 6000, 200, 320, 34, player_spells, player_items)
player3 = Person('Mokna', 6000, 180, 340, 34, player_spells, player_items)

enemy2 = Person('Professor Putricide', 7000, 130, 600, 325, lk_spells, [])
enemy1 = Person('The Lich King      ', 20000, 65, 800, 25, lk_spells, [])
enemy3 = Person('Lord Marrowgar     ', 7000, 130, 600, 325, lk_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

def removed_defeated_enemy(list, target):
    if list[target].get_hp() == 0:
        print(list[target].name + ' has died')
        del list[target]

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

print('========================')
for enemy in enemies:
    enemy.get_enemy_stats()
print('========================')

while running:
    print('\n\n')

    print(bcolors.OKGREEN + 'Our Worthy Adevnturers' + bcolors.ENDC)
    for player in players:
        player.get_stats()

    print('\n')

    for player in players:
        player.choose_action()
        choice = input('Choose Action: ')

        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.OKGREEN + player.name, 'hit', enemies[enemy].name.strip(), 'for', dmg, bcolors.ENDC)

            removed_defeated_enemy(enemies, enemy)

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input('Choose Spell:')) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + '\nYou do not have enough MP\n' + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + ' heals for', str(magic_dmg), 'HP' + bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + '\n' + player.name + "'s " + spell.name + ' deals', str(magic_dmg),
                      'points of dmg to', enemies[enemy].name.strip() + bcolors.ENDC)
                removed_defeated_enemy(enemies, enemy)
        elif index == 2:
            player.choose_item()
            item_choice = int(input('Choose Item: ')) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]['item']

            if player_items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + '\n' + 'None left' + bcolors.ENDC)
                continue

            player.items[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name, "heals for ", str(item.prop), 'HP' + bcolors.ENDC)
            elif item.type == 'elixer':
                if item.name == 'Greater Elixer':
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print('All player\'s HP and MP have been restored to full')
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + 'Your HP and MP have been restored to full' + bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + '\n' + item.name, 'dealt', str(item.prop), 'damage' + bcolors.ENDC)
                removed_defeated_enemy(enemies, enemy)

    defeated_enemies = 0

    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 3:
        print(bcolors.OKGREEN + 'YOU WIN' + bcolors.ENDC)
        running = False
    elif defeated_players == 3:
        print(bcolors.FAIL + 'YOU LOST' + bcolors.ENDC)
        running = False

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.enemy_generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name.strip(), 'hits', players[target].name, 'for', enemy_dmg, bcolors.ENDC)
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + '\n' + spell.name + ' heals', enemy.name + str(magic_dmg), 'for HP' + bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + '\n' + enemy.name.strip() + "'s " + spell.name + ' deals', str(magic_dmg),
                      'points of dmg to', players[target].name.strip() + bcolors.ENDC)
                removed_defeated_enemy(players, target)

    for enemy in enemies:
        enemy.get_enemy_stats()
