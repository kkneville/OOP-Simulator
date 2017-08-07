from World import *
from Family import *
from Equipment import *
from Combat import *
import math

def genRandom(a, b, stdDev = 5):
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)
    return random.randint(mean([a, b]) - stdDev, mean([a, b]) + stdDev)

class Animal:
    genderPronouns = {'Male': ['his', 'he'], 'Female': ['her', 'she']}
    className = 'Animal'
    charID = 1000

    def __init__(self, gender, maxHealth = 30, lifespan = 30, strength = 10, defense = 6, speed = 10):
        self.gender = gender
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.lifespan = lifespan

        self.strength = strength
        self.defense = defense
        self.speed = speed

        self.world = earth
        self.birthdate = self.world.year
        self.charID = self.genCharID()
        self.alive = True

        self.children = []

        self.world.addChars(self)

    def heal(self, amount):
        if self.health + amount > self.maxHealth:
            amount = self.maxHealth - self.health
        if int(math.ceil(amount // 5)) > self.family.food:
            amount = self.family.food * 5
        self.health += amount
        self.family.food -= math.ceil(amount // 5)

    def hurt(self, amount, attacker = None, reason = None):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.deathDate = self.world.year
            if attacker:
                self.killer = attacker
                attacker.kills += [self]
            if reason:
                if isinstance(reason, Fight):
                    self.obituary = "{} was killed by {} in {} at {}.".format(self.name, attacker.fullName,str(self.deathDate), reason.name)

            else:
                self.obituary = "{} died in {} sleep at the age of {}.".format(self.name, self.species.genderPronouns[self.gender][0], str(self.age))

            try:
                if self.family.leader == self:
                    self.family.appointLeader()
            except AttributeError:
                pass

    def decideFight(self, targets, allies = None):
        if not isinstance(targets, list):
            targets = [targets]
        if allies is None:
            allies = []
        friends = Team(self.fullName, [self] + allies, self)

        enemies = Team(targets[0].fullName, targets)
        battle = Fight(friends, enemies)
        powerBalance = battle.powerBalance(friends, enemies)
        if powerBalance > 1.1:
            print("{} decides to fight {}".format(self.fullName, ", ".join(target.name for target in targets)))
            battle.fight()
        else:
            print(self.fullName + "{} decides not to fight {}".format(self.fullName, ", ".join(target.name for target in targets)))

    def reproduce(self, mate):
        if self.age >= 10 and mate.age >= 10 and self.gender == 'Female' and mate.gender == 'Male' and self.species == mate.species and self.world == mate.world:
            child = self.species.create(self, mate)
            self.hasGivenBirth = True
            self.children += [child]
            mate.children += [child]
            print("{} and {} gave birth to the {} {} {} in the year {}".format(self.fullName, mate.fullName, child.species.className.lower(), child.gender.lower(), child.fullName, str(self.world.year)))
            return child

    def create(self):
        gender = ['Female', 'Male'] [int(round(random.random()))]
        maxHealth = genRandom(30, 30)
        lifespan = genRandom(30, 30)
        strength = genRandom(10, 10)
        defense = genRandom(6, 6)
        speed = genRandom(70, 70, 10)
        creation = Animal(gender, maxHealth, lifespan, strength, defense, speed)
        return creation

    def genCharID(self):
        Animal.charID += 1
        return Animal.charID

    def __repr__(self):
        return self.fullName

    @property
    def age(self):
        if self.alive:
            return self.world.year - self.birthdate
        self._age = self.deathDate - self.birthdate
        return self._age


    @property
    def bio(self):
        string = "A {} year old {} {} known as {} born in year {}.".format(str(self.age), self.species.className, self.gender.lower(),self.fullName,str(self.birthdate))
        if self.father:
            string +=  " to " + self.father.fullName
        if self.mother:
            if self.father:
                string += " and"
            string +=  " to " + self.mother.fullName
        else:
            string += " from unknown forces"
        string += ". "
        if not self.alive:
            string += self.obituary

        string += ("\n\n\tStrength: "+ str(self.strength) + "\n\tDefense: " + str(self.defense) + "\n\tSpeed: " + str(self.speed))
        if not self.kills == []:
            string += "\n\n\t" + str(len(self.kills)) + " Kills:"
            for kill in self.kills:
                string += "\n\t" + kill.fullName + " (Year "+ str(kill.deathDate) + ")"

        string += "\n"

        print(string)

class Humanoid(Animal):
    className = 'Humanoid'
    numeralTitles = ['', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
    combatQualifications = [lambda x: x.defense > 20, lambda x: x.strength > 20, lambda x: x.strength > 20 and x.defense > 20 and len(x.kills) > 0, lambda x: len(x.kills) > 3, lambda x: (x.strength > 23 and x.defense > 20) or len(x.kills) > 5, lambda x : (x.strength > 25 and x.defense > 23) or len(x.kills) > 7, lambda x: (x.strength > 27 and x.defense > 30 and x.speed > 18) or len(x.kills) > 9, lambda x: len([kill for kill in x.kills if kill in kill.family.leaders]) >= 3 and x.strength > 23]
    familyQualifications = [lambda x: x.family.score > 40, lambda x: x.family.score > 70, lambda x: x.family.score > 100, lambda x: x.family.score > 150, lambda x: x.family.score > 200]

    def __init__(self, name, gender, parents, familyKind, maxHealth,
                 lifespan, strength, defense, speed):
        Animal.__init__(self, gender, maxHealth, lifespan, strength, defense, speed)
        self.name = name
        self.mother = parents[0]
        self.father = parents[1]
        if self.father:
            self.family = self.father.family
        elif self.mother:
            self.family = self.mother.family
        else:
            fName = self.species.familyNames.pop(random.randint(0, len(self.species.familyNames) - 1))
            if fName in Family.familyDict:
                self.family = Family.familyDict[fName]
            else:
                self.family = Family(fName, familyKind)
        self.family.addMember(self)
        self.fullName = self.name + " " + self.family.name

        self.title = self.species.numeralTitles[len([member for member in self.family.members if member.name == self.name and member is not self])]
        self.titleIndex = 0
        if self.title:
            self.fullName += " " + self.title

        self._strength, self._defense, self._speed = self.strength, self.defense, self.speed
        self.strength, self.defense, self.speed = 3, 3, 3
        self.strengthDealt, self.defenseDealt, self.speedDealt = 0,0,0
        self.kills = []

        # Equipment format: [1 head, 1 torso, 2 arms, 2 hands, 2 legs, 2 feet]
        self.equipment = Inventory(self, 1, 1, 2, 2, 2, 2)

    @property
    def reputation(self):
        rep = int(self.strength + self.defense + self.speed + self.age + (5 * len(self.kills)) + (.25 * self.family.score))
        rep += 10 if self.family.leader == self else 0
        rep += self.titleIndex
        return rep

    def create(mother, father):
        gender = ['Female', 'Male'] [random.randint(0,1)]
        if gender == 'Male':
            names = father.species.maleNames
        else:
            names = mother.species.femaleNames
        eligibleNames = [name for name in names if name not in [child.name for child in father.children + mother.children]]
        name = random.choice(eligibleNames)
        parents = [mother, father]

        maxHealth = genRandom(mother.maxHealth, father.maxHealth, 10)
        lifespan = genRandom(mother.lifespan, father.lifespan)
        strength = genRandom(mother.strength, father.strength)
        defense = genRandom(mother.defense, father.defense)
        speed = genRandom(mother.speed, father.speed)
        creation = father.species(name, gender, parents, maxHealth, lifespan, strength, defense, speed)

        return creation

    def equip(self, item):
        self.equipment.equip(item)

    def update(self, wood, metal, food):
        if self.family.leader is self:
            self.family.update()

        pubertyPoint = .2 * self.lifespan
        elderPoint = .8 * self.lifespan
        if self.age < pubertyPoint:
            self.strength +=  (self._strength - self.strength) // (pubertyPoint - self.age)
        if self.age > elderPoint:
            if self.age > self.lifespan:
                self.hurt(self.health)
            self.maxHealth -= 3
            if self.health > self.maxHealth:
                self.health = self.maxHealth
            if random.random() < self.age / self.lifespan:
                self.strength -= 1
                self.defense -= 1
                self.speed -= 1
        else:
            self.strength, self.defense, self.speed = self._strength, self._defense, self._speed

        self.family.wood += wood
        self.family.metal += metal
        self.family.food += food
        if self.health < self.maxHealth:
            self.heal(10)


    def updateStats(self):
        if self.strengthDealt >= 50:
            self.strength += self.strengthDealt // 50
            print(self.fullName + "'s strength increased by " + str(self.strengthDealt // 50) + " points to " + str(self.strength) + "!")
            self.strengthDealt = self.strengthDealt % 50
        if self.defenseDealt >= 50:
            self.defense += self.defenseDealt // 50
            print(self.fullName + "'s defense increased by " + str(self.defenseDealt // 50) + " points to " + str(self.defense) + "!")
            self.defenseDealt = self.defenseDealt % 50
        if self.speedDealt >= 50:
            self.speed += int(self.speedDealt // 50)
            print(self.fullName + "'s speed increased by " + str(self.speedDealt // 50) + " points to " + str(self.speed) + "!")
            self.speedDealt = self.speedDealt % 50
        self.updateTitle()

    def updateTitle(self):
        if self is self.family.leader:
            qualifications = self.species.familyQualifications
            titles = self.species.familyTitles
        else:
            qualifications = self.species.combatQualifications
            titles = self.species.combatTitles
        for qual in qualifications[self.titleIndex:]:
            if qual(self):
                self.titleIndex = qualifications.index(qual)
                self.title = titles[self.titleIndex]
                print("{} will now be known as '{}'".format(self.fullName, self.title))
                self.fullName = self.name + " " + self.family.name + " " + self.title
            else:
                break

    def declareWar(self, enemyFamily):
        if self.family.leader == self:
            print(self.fullName + ", leader of " + self.family.fullName + ", has declared war upon " + enemyFamily.fullName + "!")
            return self.family.declareWar(enemyFamily)

class Human(Humanoid):
    className = 'Human'
    data_file = open('./Data/Human.txt', 'r')
    maleNames = data_file.readline().split(', ') [:-1]
    femaleNames = data_file.readline().split(', ') [:-1]
    familyNames = data_file.readline().split(', ') [:-1]
    combatTitles = data_file.readline().split(', ') [:-1]
    familyTitles = data_file.readline().split(', ') [:-1]

    def __init__(self, name, gender, parents = [None, None], maxHealth = 100,
                 lifespan = 30, strength = 14, defense = 10, speed = 13):
        self.species = Human
        Humanoid.__init__(self, name, gender, parents, 'House', maxHealth, lifespan, strength, defense, speed)

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

    def __init__(self, name, gender, parents = [None, None], maxHealth = 115,
                 lifespan = 30, strength = 13, defense = 14, speed = 10):
        self.species = Dwarf
        Humanoid.__init__(self, name, gender, parents, 'Clan', maxHealth, lifespan, strength, defense, speed)

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

    def __init__(self, name, gender, parents = [None, None], maxHealth = 75,
                 lifespan = 30, strength = 13, defense = 10, speed = 14):
        self.species = Elf
        Humanoid.__init__(self, name, gender, parents, 'Regents', maxHealth, lifespan, strength, defense, speed)

    def update(self):
        Humanoid.update(self, 8, 7, 7)
