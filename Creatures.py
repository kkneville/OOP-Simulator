from World import *
from Family import *
from Combat import *

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

    def eat(self, food):
        self.heal(food.healAmount)

    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth

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
                    self.obituary = self.name + " was killed by " + attacker.fullName + " in " + str(self.deathDate) + " at " + reason.name + "."

            else:
                self.obituary = self.name + " died in " + self.species.genderPronouns[self.gender][0]+ " sleep at the age of " + self.age + "."
            
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
            print(self.fullName + " decides to fight " + ", ".join(target.name for target in targets))
            battle.fight()
        else:
            print(self.fullName + " decides not to fight " + ", ".join(target.name for target in targets))

    def reproduce(self, mate):
        if self.age >= 10 and mate.age >= 10 and self.gender == 'Female' and mate.gender == 'Male' and self.species == mate.species and self.world == mate.world:
            child = self.species.create(self, mate)
            self.hasGivenBirth = True
            self.children += [child]
            mate.children += [child]
            print(self.fullName + " and " + mate.fullName + " gave birth to a " + child.species.className.lower() + " " + child.gender.lower() + ", " + child.fullName + ", in year " + str(self.world.year))
            return child

    def create(self):
        gender = ['Female', 'Male'] [int(round(random.random()))]
        maxHealth = genRandom(30, 30)
        lifespan = genRandom(30, 30)
        strength = genRandom(10, 10)
        defense = genRandom(6, 6)
        speed = genRandom(10, 10)
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
        string = ("A " + str(self.age) + " year old " + self.species.className + " " + self.gender.lower() + " known as " + self.fullName + " born in year "  + str(self.birthdate) )
        try:
            if self.father:
                string +=  " to " + self.father.fullName
            if self.mother:
                if self.father:
                    string += " and"
                string +=  " to " + self.mother.fullName
        except AttributeError:
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
            fName = self.species.familyNames.pop(int(random.random() * len(self.species.familyNames)))
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

        self.strengthDealt, self.defenseDealt, self.speedDealt = 0,0,0
        self.kills = []

    @property
    def reputation(self):
        rep = int(self.strength + self.defense + self.speed + self.age + (5 * len(self.kills)) + (.25 * self.family.score))
        rep += 10 if self.family.leader == self else 0
        rep += self.titleIndex
        return rep
        
    def create(mother, father):
        gender = ['Female', 'Male'] [int(round(random.random()))]
        if gender == 'Male':
            names = father.species.maleNames
        else:
            names = mother.species.femaleNames
        eligibleNames = [name for name in names if name not in [child.name for child in father.children + mother.children]]
        name = eligibleNames[int(random.random() * len(eligibleNames))]
        parents = [mother, father]

        maxHealth = genRandom(mother.maxHealth, father.maxHealth)
        lifespan = genRandom(mother.lifespan, father.lifespan)
        strength = genRandom(mother.strength, father.strength)
        defense = genRandom(mother.defense, father.defense)
        speed = genRandom(mother.speed, father.speed)
        creation = father.species(name, gender, parents, maxHealth, lifespan, strength, defense, speed)

        return creation

    def update(self):
        if self.age > self.lifespan:
            self.hurt(self.health)
        
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
        self.updateTitle

    def updateTitle(self):
        if self is self.family.leader:
            titleList = self.species.familyTitles
        else:
            titleList = self.species.combatTitles
        for title in titleList[self.titleIndex:]:
            if title[1](self):
                self.titleIndex = titleList.index(title)
                self.title = title[0]
                print(self.fullName + " will now be known as '" + self.title + "'")
                self.fullName = self.name + " " + self.family.name + " " + self.title
            else:
                break        
    
    def declareWar(self, enemyFamily):
        if self.family.leader == self:
            print(self.fullName + ", leader of " + self.family.fullName + ", has declared war upon " + enemyFamily.fullName + "!")
            self.family.declareWar(enemyFamily)

class Human(Humanoid):
    className = 'Human'
    maleNames = ['Adam', 'John', 'Calvin', 'Cain', 'Noah', 'Isaac', 'Argen', 'Alexander', 'Julius', 'Augustus', 'Joseph', 'Dairus', 'Cyrus', 'Xerxes', 'Paris', 'James', 'Jared', 'Ishmael', 'Jonathan', 'Jordan']
    femaleNames = ['Eve', 'Mary', 'Emma', 'Isabella', 'Irene', 'Sophie', 'Caroline', 'Donna', 'Emily', 'Sicily', 'Camille', 'Alexis', 'Margery', 'Cersei', 'Penelope', 'Helen', 'Parthia', 'Julia']
    familyNames = ['Snow', 'Stark', 'Habsburg', 'Xing', 'Nesha', 'Strausburg', 'Zhang', 'Ali', 'Borjinsson', 'Amalis', 'Dawi', 'Esper', 'of the Old Kings', 'Sumarin', 'Renauve', 'Hondari', 'Belesarus', 'Isauros', 'Corinthia', 'Qing', 'Heleviticus', 'Julia', 'Junii', 'Markoff', 'Ulteria', 'Heilbon', 'of Caspia', 'of the Lowborns', 'of Dawnwich']
    numeralTitles = ['', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
    combatTitles = [['the Hunter', lambda x: x.strength > 13], ['the Warrior', lambda x: x.strength > 15 and x.defense > 10], ['the Bear', lambda x: x.strength > 15 and x.defense > 12 or len(x.kills) > 3], ['the Lion', lambda x : x.strength > 17 and x.defense > 14 or len(x.kills) > 5], ['the Dragon', lambda x: x.strength > 20 and x.defense > 15 and x.speed > 13 or len(x.kills) > 7], ['the Kingslayer', lambda x: len([kill for kill in x.kills if kill in kill.family.leaders]) >= 3 and x.strength > 15]]
    familyTitles = [['the Noble', lambda x: x.family.score > 30], ['the Great', lambda x: x.family.score > 50], ['the Legendary', lambda x: x.family.score > 100], ['Kaiser', lambda x: x.family.score > 150], ['Imperator', lambda x: x.family.score > 20]]

    def __init__(self, name, gender, parents = [None, None], maxHealth = 30,
                 lifespan = 30, strength = 10, defense = 10, speed = 10):
        self.species = Human
        Humanoid.__init__(self, name, gender, parents, 'House', maxHealth, lifespan, strength, defense, speed)

class Dwarf(Humanoid):
    className = 'Dwarf'
    maleNames = ['Thorgrim', 'Harsaw', 'Gravden', 'Kaifur', 'Weschen', 'Argen', 'Gorlai', 'Asgor', 'Urist', 'Agseth', 'Darai', 'Gerensei', 'Kazark', 'Karstar', 'Karak', 'Tengrim', 'Zargrim']
    femaleNames = ['Asgora', 'Karazai', 'Thorsai', 'Valkareri', 'Caroline', 'Donna', 'Emily', 'Sicily', 'Camille', 'Alexis', 'Margery', 'Cersei', 'Penelope', 'Helen', 'Parthia', 'Julia']
    familyNames = ['Irondrake', 'Ironhold', 'Grudgebearer', 'Silvermarked', 'Ironblood', 'Lairstone', 'Grudgestone', 'Bronzeslasher', 'Drakehelm', 'Silverhelm', 'Ironhelm', 'BoatMurdered', 'Oakenhelm', 'Shakenfield', 'Gorhammer', 'Ironsurge']
    numeralTitles = ['', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
    combatTitles = [['the Hunter', lambda x: x.strength > 13], ['the Warrior', lambda x: x.strength > 15 and x.defense > 10], ['the Bear', lambda x: x.strength > 15 and x.defense > 12 or len(x.kills) > 3], ['the Lion', lambda x : x.strength > 17 and x.defense > 14 or len(x.kills) > 5], ['the Dragon', lambda x: x.strength > 20 and x.defense > 15 and x.speed > 13 or len(x.kills) > 7], ['the Kingslayer', lambda x: len([kill for kill in x.kills if kill in kill.family.leaders]) >= 3 and x.strength > 15]]
    familyTitles = [['the Noble', lambda x: x.family.score > 30], ['the Great', lambda x: x.family.score > 50], ['the Legendary', lambda x: x.family.score > 100], ['Kaiser', lambda x: x.family.score > 150], ['Imperator', lambda x: x.family.score > 20]]

    def __init__(self, name, gender, parents = [None, None], maxHealth = 40,
                 lifespan = 30, strength = 11, defense = 13, speed = 6):
        self.species = Dwarf
        Humanoid.__init__(self, name, gender, parents, 'Clan', maxHealth, lifespan, strength, defense, speed)


