from World import earth
from Combat import Team, Fight

class Family:
    familyDict = {}
    def __init__(self, name, kind, **kwargs):
        self.name = name
        self.kind = kind
        self.full_name = self.kind + " " + self.name
        self.world = earth
        self.founding_year = self.world.year
        Family.familyDict[self.name] = self
        self.members = []
        for member in kwargs:
            self.members += [member]
        if self.members:
            self.appoint_leader()
            self.founder = self.leader
        self.score = 0
        self.leaders = []

        self.wood = 0
        self.metal = 0
        self.food = 0
        self.rivals = []

    def add_member(self, member):
        self.members += [member]
        if len(self.members) == 1:
            self.appoint_leader(member)
            self.founder = self.leader

    def appoint_leader(self, candidate=None):
        if candidate and candidate in self.living_members:
            self.leader = candidate
        elif self.living_members == []:
            self.extinction_date = self.world.year
            print("The Great {} of {} has perished in the year {}, with {} as the last of {} kin.".format(self.kind, self.name, str(self.extinction_date), self.leader.full_name, self.leader.species.genderPronouns[self.leader.gender][0]))
        else:
            self.leader = self.heirs[0]
        self.leaders += [self.leader]

    @property
    def heirs(self):
        if self.kind == 'Clan':
            heir_order = sorted(self.members, key=lambda x: -x.age)
        if self.kind == 'House':
            try:
                heir_order = [child for child in self.leader.children if child.alive and child.gender == 'Male'] + [child for child in self.leader.children if child.alive and child.gender == 'Female']
            except AttributeError:
                heir_order = self.living_members
        if self.kind == 'Regents':
            heir_order = sorted(self.living_members, key=lambda x: -x.reputation)
        if self.kind == 'Tribe':
            heir_order = sorted(self.living_members, key=lambda x: -x.strength - x.speed - x.defense)
        else:
            heir_order = self.living_members
        return heir_order

    def family_to_team(self):
        return Team(self.full_name, [member for member in self.living_members if member.age > 8], self.leader)

    def declare_war(self, enemyFamily):
        friendly = self.family_to_team()
        enemy = enemyFamily.family_to_team()
        war = Fight(friendly, enemy)
        warpoints = len(war.combatants)
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

    def update(self):
        print('Updated {}.'.format(self.full_name))


    @property
    def living_members(self):
        return [member for member in self.members if member.alive]

    @property
    def bio(self):
        string = "{} (Founded in year {} by {}) has {} living members.".format(self.full_name, str(self.founding_year), self.founder.full_name, str(len(self.living_members)))
        if not self.living_members:
            string += " All lines of this house are now extinct."
        string += """
  """ + self.leader.full_name + " (" + str(self.leader.strength) + ", "  + str(self.leader.defense) + ", " + str(self.leader.speed) + ")" + ", "

        if self.leader is self.founder:
            string += "Founder"
        else:
            string += "Leader"

        for member in self.living_members:
            if member is not self.leader:
                string += """
  """+ member.full_name + " (" + str(member.strength) + ", " + str(member.defense) + ", " + str(member.speed) + ")"
        print(string)

    def __repr__(self):
        return self.full_name
