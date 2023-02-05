from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random


# Create black Magic
fire = Spell(name="Fire", cost=25, dmg=600, type="black")
thunder = Spell(name="Thunder", cost=25, dmg=500, type="black")
blizzard = Spell(name="Blizzard", cost=25, dmg=550, type="black")
meteor = Spell(name="Meteor", cost=40, dmg=1200, type="black")
quake = Spell(name="Quake", cost=35, dmg=900, type="black")

# Create white magic
cure = Spell(name="Heal", cost=25, dmg=600, type="white")
cura = Spell(name="Cure", cost=35, dmg=1500, type="white")
curaga = Spell(name="Curaga", cost=50, dmg=6000, type="white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
megaelixer = Item("MegaElixer", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grendae", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15},{"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": megaelixer, "quantity": 2},{"item": grenade, "quantity": 5}]
# Create Players
player1 = Person("Valos:", 3260, 174, 300, 34, player_magic, player_items)
player2 = Person("Dovi: ", 4160, 188, 311, 34, player_magic, player_items)
player3 = Person("Zakk: ", 3089, 132, 280, 34, player_magic, player_items)

players = [player1, player2, player3]

# Create Enemy
enemy1 = Person("Imp  ", 1250, 130, 560, 325, [enemy_spells], [])
enemy2 = Person("Magus", 18200, 221, 525, 25, [enemy_spells], [])
enemy3 = Person("Imp  ", 1250, 130, 560, 325, [enemy_spells], [])

enemies = [enemy1, enemy2, enemy3]


running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + " An Enemy Attacks!" + bcolors.ENDC)

while running:

    print("============================================================")
    print("\n\n")
    print("Name                HP                                          MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose Action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked ",enemies[enemy].name.replace(" ", ""), dmg, "points of damage.")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_dmg()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n" + " Not enough MagicPoints!" + bcolors.ENDC)
                continue

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " restores " + str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                          "points of damage to", enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                player.reduce_mp(spell.cost)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item:")) - 1

            if item_choice == -1:
                continue
            item = player_items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + " None left...." + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", item.prop + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                print(bcolors.OKGREEN + "\n" + item.name + "Restores full HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + str(item.name), "deals", str(item.prop), "points of damage to",
                      enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]
    # check if battle is over
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for players in player:
        if player.get_hp() == 0:
            defeated_players += 1
# check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "YOU WIN!" + bcolors.ENDC)
        running = False
# check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have has defeated you!" + bcolors.ENDC)
        running = False
    print("\n")
# Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.random(0, 2)

        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", ""), "attacks" + player[target].name.replace(" ", "") + " for", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + "for", str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemies[enemy].name.replace(" ", "") + "'s", spell.name + " deals",
                      str(magic_dmg), "points of damage to", players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died")
                    del players[player]
                enemy.reduce_mp(spell.cost)
            print(enemies[enemy].name.replace(" ", ""), "chose", spell.name, "damage is", magic_dmg)

