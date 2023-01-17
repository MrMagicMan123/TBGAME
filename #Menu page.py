import random

class Unit:
    def __init__(self, name, unit_type):
        self.name = name
        self.hp = 100 #based attribute HP at 100
        self.unit_type = unit_type
        self.exp = 0 #EXP starts from 0
        self.rank = 1 #Rank/Level starts from 1
        if self.unit_type == "1": #1 is Warrior
            self.atk = random.randint(5, 20) #attk ranges between 5-20
            self.defn = random.randint(1, 10) #def ranges between 1- 10
        elif self.unit_type == "2": #2 is Tank
            self.atk = random.randint(1, 10) #attk ranges between 1- 10
            self.defn = random.randint(5, 15) #def ranges between 5 - 15
        else:
            return


class Team:
    def __init__(self):
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)


class Game:
    def __init__(self):
        self.player_team = Team()
        self.enemy_team = Team()
        self.unit_types = ["1", "2"] #1 is warrior 2 is tank
        self.unit_chances = {"1": 0.5, "2": 0.5} #weightage, 1 is warrior, 2 is tanker
        self.selected_unit = None #stored variables for print battle report
        self.target_unit = None #stored variables for print battle report
        self.damage = None #stored variables for print battle report
    

    def start(self):
        print("Welcome to the PSB battle game!")
        print("1. Create a character")
        print("2. View your team")
        print("3. Start Battle")
        print("4. Quit Game")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.create_team()
        elif choice == "2":
            self.view_team()
        elif choice == "3":
            self.create_enemy_team()
            self.start_battle()
        elif choice == "4":
            exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            self.start()

    def create_team(self):
        if len(self.player_team.units) >= 3:
         print("3 units is enough to dominate this game, Let's BATTLE!!")
         self.start()
        name = input("Enter unit name: ")
        unit_type = input("Enter unit type (Warrior(1) or Tanker(2)): ")
        if unit_type not in ["1", "2"]:
         print("Invalid unit type.")
         self.start()
        unit = Unit(name, unit_type)
        self.player_team.add_unit(unit)
        print("Unit added to team!")
        self.start()


    def create_enemy_team(self):
      team_size = 3
      for i in range(team_size):
        unit_type = random.choices(
            population=["1", "2"],
            weights=[0.5, 0.5], #weightage, chances of each class spawning is 50% and 50%
            k=1
        )[0]
        unit = Unit("AI"+str(random.randint(10, 99)), unit_type)
        self.enemy_team.add_unit(unit)



    def select_unit_and_attack(self):
        try:
            print("Select a unit from your team:")
            for index, unit in enumerate(self.player_team.units):
                print(f"{index+1}. {unit.name}")
            selected_unit_index = int(input("Enter the number of the unit you want to select: ")) - 1
            selected_unit = self.player_team.units[selected_unit_index]

            print("Select a target from the enemy team:")
            for index, unit in enumerate(self.enemy_team.units):
                print(f"{index+1}. {unit.name}")
            target_unit_index = int(input("Enter the number of the unit you want to attack: ")) - 1
            target_unit = self.enemy_team.units[target_unit_index]

            damage = selected_unit.atk - target_unit.defn + random.randint(-5, 10)
            self.print_battle_report(selected_unit, target_unit, damage)
            target_unit.hp -= damage
            self.selected_unit_enemy = self.enemy_team.units[random.randint(0, len(self.enemy_team.units) - 1)]
            self.target_unit_enemy = self.player_team.units[random.randint(0, len(self.player_team.units) - 1)]
            self.damage_enemy = self.selected_unit_enemy.atk - self.target_unit_enemy.defn + random.randint(-5, 10)
            self.print_battle_report(self.selected_unit_enemy, self.target_unit_enemy, self.damage_enemy)
            self.target_unit_enemy.hp -= self.damage_enemy
            selected_unit.exp += damage
            target_unit.exp += target_unit.defn
            if damage > 10:
                target_unit.exp += 0.2*target_unit.exp #20% Extra EXP
            elif damage <= 0:
                target_unit.exp += 0.5*target_unit.exp #50% Extra EXP
            if target_unit.exp >= 100:
                target_unit.rank += 1
                target_unit.exp = 0
                target_unit.atk += 5 #attk +5 whenever promoted
                target_unit.hp = 100
            if target_unit.hp <= 0:
                self.enemy_team.units.remove(target_unit)
                print(f"{target_unit.name} has been defeated.")
            print(f"{selected_unit.name} attacked {target_unit.name} and dealt {damage} damage.")
            if len(self.enemy_team.units) == 0:
                print("You win!")
                self.start()
            elif len(self.player_team.units) == 0:
                print("You lose!")
                self.start()
        except ValueError:
            print("Invalid input, please enter a number.")
            self.select_unit_and_attack()


    def view_team(self):
        if len(self.player_team.units) == 0:
            print("Create a team first")
            self.start()
            return
        for unit in self.player_team.units:
            print("Name:", unit.name)
            print("HP:", unit.hp)
            print("ATK:", unit.atk)
            print("DEF:", unit.defn)
            print("EXP:", unit.exp)
            print("RANK:", unit.rank)
            print("Type:", unit.unit_type)
        self.start()


    def start_battle(self):
        if len(self.player_team.units) < 3:
            if len(self.player_team.units) < 2:
                print("You need at least 3 units to start a battle.")
            else:
                print("You need at least 1 more unit to start a battle.")
            self.start()
            return
        if len(self.player_team.units) == 0:
            print("Team has not yet been created.")
            self.start()
            return
        while len(self.player_team.units) > 0 and len(self.enemy_team.units) > 0:
            self.select_unit_and_attack()
            self.ai_turn()
            self.check_for_winner()

    def ai_turn(self):
        if len(self.player_team.units) == 0 or len(self.enemy_team.units) == 0:
            return
        ai_unit = random.choice(self.enemy_team.units)
        target_unit = random.choice(self.player_team.units)
        damage = ai_unit.atk - target_unit.defn + random.randint(-5, 10)
        target_unit.hp -= damage
        ai_unit.exp += damage
        target_unit.exp += target_unit.defn
        if damage > 10:
            target_unit.exp += target_unit.exp * 0.2
        if damage <= 0:
            target_unit.exp += target_unit.exp * 0.5
        if ai_unit.exp >= 100:
            ai_unit.rank += 1
            ai_unit.exp -= 100
            ai_unit.atk += 5
            ai_unit.exp = 0
        if target_unit.hp <= 0:
            print(f"{target_unit.name} has been defeated.")
            self.player_team.units.remove(target_unit)
            self.check_for_winner()

    def print_battle_report(self, selected_unit, target_unit, damage):
        print("Player Team:")
        for unit in self.player_team.units:
            print(f"{unit.name}: HP {unit.hp}  EXP {unit.exp}  Rank {unit.rank}")
        print("Enemy Team:")
        for unit in self.enemy_team.units:
            print(f"{unit.name}: HP {unit.hp}  EXP {unit.exp}  Rank {unit.rank}")
        print(f"{selected_unit.name} attacked {target_unit.name} and dealt {damage} damage.")
        selected_unit.exp += damage
        target_unit.exp += target_unit.defn
        if damage>10:
            target_unit.exp += target_unit.exp*0.2
        elif damage<=0:
            target_unit.exp += target_unit.exp*0.5
        if selected_unit.exp>=100:
            selected_unit.rank += 1
            selected_unit.exp -= 100
            selected_unit.atk += 5
        if target_unit.exp>=100:
            target_unit.rank += 1
            target_unit.exp -= 100
            target_unit.atk += 5

    def check_for_winner(self):
        if len(self.player_team.units) == 0:
            print("You lose !! Try harder next time")
            self.play_again()
        elif len(self.enemy_team.units) == 0:
            print("You win !! you are a warrior in PSB acedemy")
            self.play_again()

    def play_again(self):
        choice = input("Challenge yourself again? (Y/N)")
        if choice.upper() == "Y":
            self.start()
        elif choice.upper() == "N":
            print("Thank you for playing!")
            exit()
        else:
            print("Invalid choice. Please enter Y or N.")
            self.play_again()


game = Game()
game.start()

             