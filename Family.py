from collections import Counter
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

    def declare_war(self, enemy_family):
        friendly = self.family_to_team()
        enemy = enemy_family.family_to_team()
        war = Fight(friendly, enemy)
        warpoints = len(war.combatants)
        power = war.power_balance(friendly, enemy)
        war.fight()
        if war.victor == friendly:
            self.score += int((1/power) * 10 + warpoints)
            enemy_family.score -= warpoints
        if war.victor == enemy:
            enemy_family.score += int((power * 10) + warpoints)
            self.score -= warpoints
        for fighter in war.combatants:
            fighter.updateStats()
        return war

    def update(self):
        most_demand, demand_list = self.craft_priority()
        if most_demand and most_demand.wood <= self.wood and most_demand.metal <= self.metal:
            remaining = most_demand.amount
            equipper = max(demand_list[most_demand], key=lambda x: x.inventory.get_number_unfilled(most_demand.slot_type))
            while remaining > 0:
                crafted = most_demand()
                remaining -= 1
                if equipper.inventory.get_number_unfilled(most_demand.slot_type) == 0:
                    equipper = max(demand_list[most_demand], key=lambda x: x.inventory.get_number_unfilled(most_demand.slot_type))    
                else:
                    equipper.equip(crafted)

            self.wood -= most_demand.wood
            self.metal -= most_demand.metal
            print("{} has crafted a {} for {}".format(self.full_name, crafted.name, demand_list[most_demand][0].full_name))
                

    @property
    def living_members(self):
        return [member for member in self.members if member.alive]

    def craft_priority(self):
        member_demands = {}
        for member in self.members:
            member.inventory.create_demand()
            if member.inventory.demand in member_demands:
                member_demands[member.inventory.demand] += [member]
            else:
                member_demands[member.inventory.demand] = [member]
        return max(member_demands, key=lambda x: len(member_demands[x])), member_demands

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
