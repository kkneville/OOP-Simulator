import random
import math
from Combat import Team, Fight
from Family import Family
from World import earth
from Equipment import Inventory


def gen_random(first, second, standard_dev=5):
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)
    return random.randint(mean([first, second]) - standard_dev, mean([first, second]) + standard_dev)

class Animal:
    gender_pronouns = {'Male': ['his', 'he'], 'Female': ['her', 'she']}
    class_name = 'Animal'
    char_id = 1000

    def __init__(self, gender, max_health=30, lifespan=30, strength=10, defense=6, speed=10):
        self.gender = gender
        self.health = max_health
        self.max_health = max_health
        self.lifespan = lifespan
        self.name = 'A wild Animal'
        self.full_name = self.name
        self.species = self.species

        self.strength = strength
        self.defense = defense
        self.speed = speed

        self.world = earth
        self.birth_date = self.world.year
        self.char_id = self.gen_char_id()
        self.alive = True
        self.family = None
        self.children = []
        self.father = None
        self.mother = None
        self.kills = []
        self.death_date = None
        self.killer = None
        self.obituary = None

        self.world.add_chars(self)

    def heal(self, amount):
        if self.health + amount > self.max_health:
            amount = self.max_health - self.health
        if self.family:
            if int(math.ceil(amount // 5)) > self.family.food:
                amount = self.family.food * 5
            self.family.food -= math.ceil(amount // 5)

        self.health += amount

    def hurt(self, amount, attacker=None, reason=None):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.death_date = self.world.year
            if attacker:
                self.killer = attacker
                attacker.kills += [self]
            if reason:
                if isinstance(reason, Fight):
                    self.obituary = "{} was killed by {} in {} at {}.".format(self.name, attacker.full_name, str(self.death_date), reason.name)

            else:
                self.obituary = "{} died in {} sleep at the age of {}.".format(self.name, self.species.gender_pronouns[self.gender][0], str(self.age))

            try:
                if self.family.leader == self:
                    self.family.appointLeader()
            except AttributeError:
                pass

    def decide_fight(self, targets, allies=None):
        if not isinstance(targets, list):
            targets = [targets]
        if allies is None:
            allies = []
        friends = Team(self.full_name, [self] + allies, self)

        enemies = Team(targets[0].full_name, targets)
        battle = Fight(friends, enemies)
        power_balance = battle.power_balance(friends, enemies)
        if power_balance > 1.1:
            print("{} decides to fight {}".format(self.full_name, ", ".join(target.name for target in targets)))
            battle.fight()
        else:
            print(self.full_name + "{} decides not to fight {}".format(self.full_name, ", ".join(target.name for target in targets)))

    def reproduce(self, mate):
        if self.age >= 10 and mate.age >= 10 and self.gender == 'Female' and mate.gender == 'Male' and self.species == mate.species:
            child = self.species.create(self, mate)
            self.children += [child]
            mate.children += [child]
            print("{} and {} gave birth to the {} {} {} in the year {}".format(self.full_name, mate.full_name, child.species.className.lower(), child.gender.lower(), child.full_name, str(self.world.year)))
            return child

    def create(self, mate):
        gender = random.choice(['Female', 'Male'])
        max_health = gen_random(30, 30)
        lifespan = gen_random(30, 30)
        strength = gen_random(10, 10)
        defense = gen_random(6, 6)
        speed = gen_random(70, 70, 10)
        creation = Animal(gender, max_health, lifespan, strength, defense, speed)
        return creation

    def gen_char_id(self):
        Animal.char_id += 1
        return Animal.char_id

    def __repr__(self):
        return self.full_name

    @property
    def age(self):
        if self.alive:
            return self.world.year - self.birth_date
        return self.death_date - self.birth_date


    @property
    def bio(self):
        string = "A {} year old {} {} known as {} born in year {}".format(str(self.age), self.species.className, self.gender.lower(), self.full_name, str(self.birth_date))
        if self.father:
            string += " to " + self.father.full_name
        if self.mother:
            if self.father:
                string += " and"
            string += " to " + self.mother.full_name
        else:
            string += " from unknown forces"
        string += ". "
        if not self.alive:
            string += self.obituary

        string += ("\n\n\tStrength: "+ str(self.strength) + "\n\tDefense: " + str(self.defense) + "\n\tSpeed: " + str(self.speed))
        if self.kills:
            string += "\n\n\t" + str(len(self.kills)) + " Kills:"
            for kill in self.kills:
                string += "\n\t" + kill.full_name + " (Year "+ str(kill.death_date) + ")"

        string += "\n"

        print(string)

class Humanoid(Animal):
    className = 'Humanoid'
    numeralTitles = ['', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
    combatQualifications = [lambda x: x.defense > 20, lambda x: x.strength > 20, lambda x: x.strength > 20 and x.defense > 20 and len(x.kills) > 0, lambda x: len(x.kills) > 3, lambda x: (x.strength > 23 and x.defense > 20) or len(x.kills) > 5, lambda x: (x.strength > 25 and x.defense > 23) or len(x.kills) > 7, lambda x: (x.strength > 27 and x.defense > 30 and x.speed > 18) or len(x.kills) > 9, lambda x: len([kill for kill in x.kills if kill in kill.family.leaders]) >= 3 and x.strength > 23]
    familyQualifications = [lambda x: x.family.score > 40, lambda x: x.family.score > 70, lambda x: x.family.score > 100, lambda x: x.family.score > 150, lambda x: x.family.score > 200]

    def __init__(self, name, gender, parents, familyKind, max_health,
                 lifespan, strength, defense, speed):
        Animal.__init__(self, gender, max_health, lifespan, strength, defense, speed)
        self.name = name
        self.mother = parents[0]
        self.father = parents[1]
        if self.father:
            self.family = self.father.family
        elif self.mother:
            self.family = self.mother.family
        else:
            family_name = self.species.familyNames.pop(random.randint(0, len(self.species.familyNames) - 1))
            if family_name in Family.familyDict:
                self.family = Family.familyDict[family_name]
            else:
                self.family = Family(family_name, familyKind)
        self.family.add_member(self)
        self.full_name = self.name + " " + self.family.name

        self.title = self.species.numeralTitles[len([member for member in self.family.members if member.name == self.name and member is not self])]
        self.title_index = 0
        if self.title:
            self.full_name += " " + self.title

        self._strength, self._defense, self._speed = self.strength, self.defense, self.speed
        self.strength, self.defense, self.speed = 3, 3, 3
        self.strength_dealt, self.defense_dealt, self.speed_dealt = 0, 0, 0
        self.kills = []

        # Equipment format: [1 head, 1 torso, 2 arms, 2 hands, 2 legs, 2 feet]
        self.equipment = Inventory(self, 1, 1, 2, 2, 2, 2)

    @property
    def reputation(self):
        rep = int(self.strength + self.defense + self.speed + self.age + (5 * len(self.kills)) + (.25 * self.family.score))
        rep += 10 if self.family.leader == self else 0
        rep += self.title_index
        return rep

    def create(self, mate):
        gender = random.choice(['Female', 'Male'])
        if gender == 'Male':
            names = mate.species.maleNames
        else:
            names = self.species.femaleNames
        eligible_names = [name for name in names if name not in [child.name for child in mate.children + self.children]]
        name = random.choice(eligible_names)
        parents = [self, mate]

        max_health = gen_random(self.max_health, mate.max_health, 10)
        lifespan = gen_random(self.lifespan, mate.lifespan)
        strength = gen_random(self.strength, mate.strength)
        defense = gen_random(self.defense, mate.defense)
        speed = gen_random(self.speed, mate.speed)
        creation = mate.species(name, gender, parents, max_health, lifespan, strength, defense, speed)

        return creation

    def equip(self, item):
        self.equipment.equip(item)

    def update(self, wood, metal, food):
        if self.family.leader is self:
            self.family.update()

        puberty_age = .2 * self.lifespan
        elder_age = .8 * self.lifespan
        if self.age < puberty_age:
            self.strength += (self._strength - self.strength) // (puberty_age - self.age)
        if self.age > elder_age:
            if self.age > self.lifespan:
                self.hurt(self.health)
            self.max_health -= 3
            if self.health > self.max_health:
                self.health = self.max_health
            if random.random() < self.age / self.lifespan:
                self.strength -= 1
                self.defense -= 1
                self.speed -= 1
        else:
            self.strength, self.defense, self.speed = self._strength, self._defense, self._speed

        self.family.wood += wood
        self.family.metal += metal
        self.family.food += food
        if self.health < self.max_health:
            self.heal(10)


    def updateStats(self):
        if self.strength_dealt >= 50:
            self.strength += self.strength_dealt // 50
            print(self.full_name + "'s strength increased by " + str(self.strength_dealt // 50) + " points to " + str(self.strength) + "!")
            self.strength_dealt = self.strength_dealt % 50
        if self.defense_dealt >= 50:
            self.defense += self.defense_dealt // 50
            print(self.full_name + "'s defense increased by " + str(self.defense_dealt // 50) + " points to " + str(self.defense) + "!")
            self.defense_dealt = self.defense_dealt % 50
        if self.speed_dealt >= 50:
            self.speed += int(self.speed_dealt // 50)
            print(self.full_name + "'s speed increased by " + str(self.speed_dealt // 50) + " points to " + str(self.speed) + "!")
            self.speed_dealt = self.speed_dealt % 50
        self.updateTitle()

    def updateTitle(self):
        if self is self.family.leader:
            qualifications = self.species.familyQualifications
            titles = self.species.familyTitles
        else:
            qualifications = self.species.combatQualifications
            titles = self.species.combatTitles
        for qual in qualifications[self.title_index:]:
            if qual(self):
                self.title_index = qualifications.index(qual)
                self.title = titles[self.title_index]
                print("{} will now be known as '{}'".format(self.full_name, self.title))
                self.full_name = self.name + " " + self.family.name + " " + self.title
            else:
                break

    def declareWar(self, enemyFamily):
        if self.family.leader == self:
            print(self.full_name + ", leader of " + self.family.full_name + ", has declared war upon " + enemyFamily.full_name + "!")
            return self.family.declare_war(enemyFamily)

class Human(Humanoid):
    className = 'Human'
    data_file = open('./Data/Human.txt', 'r')
    maleNames = data_file.readline().split(', ') [:-1]
    femaleNames = data_file.readline().split(', ') [:-1]
    familyNames = data_file.readline().split(', ') [:-1]
    combatTitles = data_file.readline().split(', ') [:-1]
    familyTitles = data_file.readline().split(', ') [:-1]

    def __init__(self, name, gender, parents=[None, None], max_health=100,
                 lifespan=30, strength=14, defense=10, speed=13):
        self.species = Human
        Humanoid.__init__(self, name, gender, parents, 'House', max_health, lifespan, strength, defense, speed)

    def update(self):
        Humanoid.update(self, 6, 6, 10)

class Dwarf(Humanoid):
    className = 'Dwarf'
    data_file = open('./Data/Human.txt', 'r')
    maleNames = data_file.readline().split(', ') [:-1]
    femaleNames = data_file.readline().split(', ') [:-1]
    familyNames = data_file.readline().split(', ') [:-1]
    combatTitles = data_file.readline().split(', ') [:-1]
    familyTitles = data_file.readline().split(', ') [:-1]

    def __init__(self, name, gender, parents=[None, None], max_health=115,
                 lifespan=30, strength=13, defense=14, speed=10):
        self.species = Dwarf
        Humanoid.__init__(self, name, gender, parents, 'Clan', max_health, lifespan, strength, defense, speed)

    def update(self):
        Humanoid.update(self, 5, 10, 7)

class Elf(Humanoid):
    className = 'Elf'
    data_file = open('./Data/Human.txt', 'r')
    maleNames = data_file.readline().split(', ') [:-1]
    femaleNames = data_file.readline().split(', ') [:-1]
    familyNames = data_file.readline().split(', ') [:-1]
    combatTitles = data_file.readline().split(', ') [:-1]
    familyTitles = data_file.readline().split(', ') [:-1]

    def __init__(self, name, gender, parents=[None, None], max_health=75,
                 lifespan=30, strength=13, defense=10, speed=14):
        self.species = Elf
        Humanoid.__init__(self, name, gender, parents, 'Regents', max_health, lifespan, strength, defense, speed)

    def update(self):
        Humanoid.update(self, 8, 7, 7)
