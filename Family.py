from Creatures import *
from Combat import *

class Family:
    familyDict = {}
    def __init__(self, name, kind, **kwargs):
        self.name = name
        self.kind = kind
        self.fullName = self.kind + " " + self.name
        self.world = earth
        self.foundingYear = self.world.year
        Family.familyDict [self.name] = self
        self.members = []
        for member in kwargs:
            self.members += [member]
        if self.members:
            self.appointLeader()
            self.founder = self.leader
        self.score = 0
        self.leaders = []

        self.wood = 0
        self.iron = 0
        self.food = 0

    def addMember(self, member):
        self.members += [member]
        if len(self.members) == 1:
            self.appointLeader(member)
            self.founder = self.leader

    def appointLeader(self, candidate = None):
        if self.livingMembers == []:
            self.extinctionDate = self.world.year
            print("The Great " + self.kind + " of " + self.name + " has perished in the year " + str(self.extinctionDate) +", with " + self.leader.fullName + " as the last of " + self.leader.species.genderPronouns[self.leader.gender][0] + " kin.")
        elif candidate and candidate in self.livingMembers:
            self.leader = candidate
        else:
            self.leader = self.heirs[0]
        self.leaders += [self.leader]

    @property
    def heirs(self):
        if self.kind == 'Clan':
            heirOrder = sorted(self.members, key = lambda x: -x.age)
        if self.kind == 'House':
            try:
                heirOrder = [child for child in self.leader.children if child.alive and child.gender == 'Male'] + [child for child in self.leader.children if child.alive and child.gender == 'Female']
            except AttributeError:
                heirOrder = self.livingMembers
        if self.kind == 'Confederation':
            heirOrder = sorted(self.livingMembers, key = lambda x: -x.reputation)
        if self.kind == 'Tribe':
            heirOrder = sorted(self.livingMembers, key = lambda x: -x.strength - x.speed - x.defense)
        else:
            heirOrder = self.livingMembers
        return heirOrder

    def familyToTeam(self):
        return Team(self.fullName, [member for member in self.livingMembers if member.age > 8], self.leader)

    def declareWar(self, enemyFamily):
        friendly = self.familyToTeam()
        enemy = enemyFamily.familyToTeam()
        war = Fight(friendly, enemy)
        warpoints =  len(war.combatants)
        power = war.powerBalance(friendly, enemy)
        war.fight()
        if war.victor == friendly:
            self.score += int((1/power) * 10 + warpoints)
            enemyFamily.score -= warpoints
        if war.victor == enemy:
            enemyFamily.score += int((power * 10) + warpoints)
            self.score -= warpoints
        for fighter in war.combatants:
            fighter.updateStats()
        return war

    @property
    def livingMembers(self):
        return [member for member in self.members if member.alive]

    @property
    def bio(self):
        string = self.fullName + " (Founded in year "+ str(self.world.year) + " by " + self.founder.fullName +") has " + str(len(self.livingMembers)) + " living members."
        if not self.livingMembers:
            string += " All lines of this house are now extinct."
        string += """
  """ + self.leader.fullName + " (" + str(self.leader.strength) + ", "  + str(self.leader.defense) + ", " + str(self.leader.speed) + ")" + ", "

        if self.leader is self.founder:
            string += "Founder"
        else:
            string += "Leader"

        for member in self.livingMembers:
            if member is not self.leader:
                string += """
  """+ member.fullName + " (" + str(member.strength) + ", " + str(member.defense) + ", " + str(member.speed) + ")"
        print(string)

    def __repr__(self):
        return self.fullName
