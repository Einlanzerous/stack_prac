import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

#Black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 8, 75, "black")
blizzard = Spell("Blizzard", 11, 115, "black")
meteor = Spell("Meteor", 20, 220, "black")
quake = Spell("Quake", 14, 145, "black")

#White magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")
regen = Spell("Regen", 24, 600, "white")

#Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of on party member", 9999)
megaelixir = Item("MegaElixir", "elixir", "Fuly restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2}, {"item": elixir, "quantity": 1},
                {"item": megaelixir, "quantity": 1}, {"item": grenade, "quantity": 5}]

enemy_spells = [fire, meteor, regen]

#People in game
player1 = Person("Ricas", 710,  60, 60, 34, player_magic, player_items)
player2 = Person("Jade",  535,  90, 40, 20, player_magic, player_items)
player3 = Person("Ryuji", 850,  40, 90, 54, player_magic, player_items)

#Enemies in game
enemy1 = Person("Minotaur",  2800, 65, 140, 85, enemy_spells, None)
enemy2 = Person("Lizard",  800, 45,  65, 60, enemy_spells, None)
enemy3 = Person("Lizard",  800, 45,  65, 60, enemy_spells, None)

players = [player1, player2, player3]

enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==============================")

    print("\n\n")
    print("NAME                   HP                                     MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()

        choice = input("Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()

            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print(player.name + " attacked " + enemies[enemy].name + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()

            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]

            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)

                print(bcolors.OKBLUE + "\n" + player.name + "'s " + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + player.name + "'s " + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + player.name + "'s " + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + player.name + "'s " + item.name + " fully restore HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + player.name + "'s " + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    # Check end conditions
    defeated_enemies = 0
    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    elif defeated_players == 2:
        print(bcolors.FAIL + "Your party has perished!" + bcolors.ENDC)
        running = False

    print("\n")

    # Enemy attacks
    for enemy in enemies:
        target = random.randrange(0, 3)
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)

            print(enemy.name + " attacks " + players[target].name + " for " + enemy_dmg + " points of damage.")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()

            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)

                print(bcolors.OKBLUE + enemy.name + " casts " + spell.name + " and heals for", str(magic_dmg), "HP." + bcolors.ENDC)

            elif spell.type == "black":
                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + enemy.name + "'s " + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]
