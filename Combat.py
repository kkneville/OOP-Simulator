import random
from World import earth
from termcolor import colored


class Fight:

    def __init__(self, team_a, team_b):
        self.team_a = team_a
        self.team_b = team_b
        self.team_a.opponent, self.team_b.opponent = self.team_b, self.team_a
        self.participants = self.team_a.members + self.team_b.members
        self.victor = None
        self.loser = None
        self.world = earth
        self.year_fought = self.world.year
        self.name = 'The battle between ' + self.team_a.name + ', led by ' + self.team_a.leader.full_name +', and ' + self.team_b.name + ', led by ' + self.team_b.leader.full_name + ', in the year ' + str(self.year_fought)
        self.battle_results = ""

    def power_balance(self, friendly_side=None, opponent_side=None):
        team_a = friendly_side if friendly_side else self.team_a
        team_b = opponent_side if opponent_side else self.team_b

        team_a_score = sum([(.5 + combatant.strength + combatant.defense + combatant.speed + combatant.eqStrength + combatant.eqDefense + combatant.eqSpeed) * (combatant.health/combatant.max_health) for combatant in team_a.members if combatant.active])
        team_b_score = sum([(.5 + combatant.strength + combatant.defense + combatant.speed + combatant.eqStrength + combatant.eqDefense + combatant.eqSpeed) * (combatant.health/combatant.max_health) for combatant in team_b.members if combatant.active])
        try:
            score = team_a_score / team_b_score
        except ZeroDivisionError:
            score = 99
        return score

    @property
    def combatants(self):
        self.participants = sorted([combatant for combatant in self.participants if combatant.alive], key=lambda x: -(x.speed + x.eqSpeed))
        return self.participants
    
    @property
    def active_combatants(self):
        return [combatant for combatant in self.combatants if combatant.active]

    def pick_targets(self, combatant=None):
        if combatant:
            eligible = [target for target in self.active_combatants if target.team is combatant.team.opponent]
            combatant.target = random.choice(eligible)
        else:
            for combatant in self.active_combatants:
                eligible = [target for target in self.active_combatants if target.team is combatant.team.opponent]
                combatant.target = random.choice(eligible)


    def pick_weapon(self, combatant):
        weapons = combatant.inventory.get_equipped(True)
        if weapons:
            combatant.weapon = random.choice(weapons)
        else:
           combatant.weapon = None

    def attack(self, combatant):
        if combatant.weapon:
            attack_multiplier = 1 + int(.5 * combatant.weapon.strength)
        else:
            attack_multiplier = 1
        defense_multiplier = 1 + combatant.target.eqDefense
        attack_range = int(combatant.strength * (combatant.health / combatant.max_health))
        defense_range = int(combatant.target.defense * (combatant.target.health / combatant.target.max_health))
        attack = random.randint(int(.25 * attack_range), attack_range)
        defense = random.randint(int(.25 * defense_range), defense_range)
        damage = (attack * attack_multiplier) - (defense * defense_multiplier)
        combatant.strength_dealt += attack
        combatant.target.defense_dealt += defense
        if damage > 0:
            combatant.team.damage_dealt += damage
            combatant.target.hurt(damage, combatant, self)
            if not combatant.target.alive:
                combatant.team.opponent.team_casulties += 1
                if combatant.weapon:
                    print(colored("{} ({}/{}) killed {} ({}/{}) with {} {}, dealing {} damage!".format(combatant.full_name, str(combatant.health), str(combatant.max_health), combatant.target.full_name, str(combatant.target.health), str(combatant.target.max_health), combatant.species.gender_pronouns[combatant.gender][0], combatant.weapon.name, str(damage)), 'red'))
                else:
                    print(colored("{} ({}/{}) killed {} ({}/{}), dealing {} damage!".format(combatant.full_name, str(combatant.health), str(combatant.max_health), combatant.target.full_name, str(combatant.target.health), str(combatant.target.max_health), str(damage)), 'red'))
            else:
                if combatant.weapon:
                    print("{} ({}/{}) {} {} ({}/{}) with {} {}, dealing {} damage!".format(combatant.full_name, str(combatant.health), str(combatant.max_health), combatant.weapon.attack_verb, combatant.target.full_name, str(combatant.target.health), str(combatant.target.max_health), combatant.species.gender_pronouns[combatant.gender][0], combatant.weapon.name, str(damage)))
                else:
                    print("{} ({}/{}) struck {} ({}/{}) with {} fists, dealing {} damage!".format(combatant.full_name, str(combatant.health), str(combatant.max_health), combatant.target.full_name, str(combatant.target.health), str(combatant.target.max_health), combatant.species.gender_pronouns[combatant.gender][0], str(damage)))
        else:
            #print(combatant.full_name + "'s ("+ str(combatant.health) + "/"+ str(combatant.max_health) +") attack was blocked by " + combatant.target.full_name + " ("+ str(combatant.target.health) + "/"+ str(combatant.target.max_health) +")!")
            combatant.target.team.blocked_attacks += 1
            
    def fight(self):
        self.pick_targets()
        while not self.victor:
            for combatant in self.active_combatants:
                self.check_victory()
                if self.victor:
                    self.declare_victory()
                    break
                self.check_flee(combatant)
                if combatant.active:
                    if combatant.target not in self.active_combatants:
                        self.pick_targets(combatant)
                    self.pick_weapon(combatant)
                    self.attack(combatant)
                    if random.randint(0, 25) < combatant.speed + combatant.eqSpeed:
                        combatant.speed_dealt += 1
                        self.attack(combatant)
                    else:
                        #print(" ({}/{}) missed {} attack on {} ({}/{})!".format(combatant.full_name, str(combatant.health), str(combatant.max_health), combatant.species.gender_pronouns[combatant.gender][0], combatant.target.full_name, str(combatant.target.health), str(combatant.target.max_health)))
                        combatant.team.missed_attacks += 1

    def declare_victory(self):
        print(colored("{} are victorious over {}!".format(colored(self.victor.name, 'cyan'), self.loser.name)), 'red')
        self.battle_results = "\n{:>30}\t{}   {}".format("Battle Statistics:", self.team_a.name, self.team_b.name)
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Damage Inflicted:", str(self.team_a.damage_dealt), str(self.team_b.damage_dealt), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Casualties:", str(self.team_a.team_casulties), str(self.team_b.team_casulties), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Teammates Fled:", str(self.team_a.members_fled), str(self.team_b.members_fled), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Attacks Missed:", str(self.team_a.missed_attacks), str(self.team_b.missed_attacks), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}\n".format("Attacks Blocked:", str(self.team_a.blocked_attacks), str(self.team_b.blocked_attacks), name=len(self.team_a.name))
        print(self.battle_results)        

    def check_flee(self, combatant):
        opponent_power = self.power_balance(combatant.team.opponent, combatant.team)
        if combatant.health <= .4 * combatant.max_health and opponent_power > 2.5 and random.randint(0, 5) < opponent_power:
            combatant.active = False
            print(colored( "{} ({}/{}) flees from the battle!".format(combatant.full_name, str(combatant.health), str(combatant.max_health)), 'yellow'))
            combatant.team.members_fled += 1
            self.check_victory()

    def check_victory(self):
        if not self.team_a.combatants:
            self.victor = self.team_b
            self.loser = self.team_a
        if not self.team_b.combatants:
            self.victor = self.team_a
            self.loser = self.team_b

    def __repr__(self):
        string = "{} occurred.".format(self.name)
        if self.victor:
            string += "{}, led by {}, was victorious over {}, led by {}.".format(self.victor.name, self.victor.leader.full_name, self.loser.name, self.loser.leader.full_name)
        return string



class Team():

    def __init__(self, name, members, leader=None):
        self.name = name
        self.members = members
        if leader:
            self.leader = leader
        else:
            self.leader = self.members[0]
        for member in self.members:
            member.team = self
            member.active = True

        self.missed_attacks = 0
        self.blocked_attacks = 0
        self.damage_dealt = 0
        self.team_casulties = 0
        self.members_fled = 0

    @property
    def combatants(self):
        return [member for member in self.members if member.alive and member.active]