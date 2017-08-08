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

        team_a_score = sum([(.5 + fighter.strength + fighter.defense + fighter.speed + fighter.eqStrength + fighter.eqDefense + fighter.eqSpeed) * (fighter.health/fighter.max_health) for fighter in team_a.members if fighter.active])
        team_b_score = sum([(.5 + fighter.strength + fighter.defense + fighter.speed + fighter.eqStrength + fighter.eqDefense + fighter.eqSpeed) * (fighter.health/fighter.max_health) for fighter in team_b.members if fighter.active])
        try:
            score = team_a_score / team_b_score
        except ZeroDivisionError:
            score = 999
        return score

    @property
    def combatants(self):
        self.participants = sorted([combatant for combatant in self.participants if combatant.alive], key=lambda x: -(x.speed + x.eqSpeed))
        return self.participants

    def __repr__(self):
        string = "{} occurred.".format(self.name)
        if self.victor:
            string += "{}, led by {}, was victorious over {}, led by {}.".format(self.victor.name, self.victor.leader.full_name, self.loser.name, self.loser.leader.full_name)
        return string

    def fight(self):
        def pick_target(fighter):
            eligible = [target for target in fighter.team.opponent.members if target.alive and target.active]
            fighter.target = random.choice(eligible)

        print(self.name + " begins.")
        while not self.victor:
            for fighter in self.combatants:
                if fighter.alive and fighter.active:
                    try:
                        if not fighter.target.alive or not fighter.target.active:
                            pick_target(fighter)
                    except AttributeError:
                        pick_target(fighter)

                    attack_chance = random.randint(0, 25)
                    if attack_chance <= fighter.speed + fighter.eqSpeed:
                        fighter.speed_dealt += 1
                        attack = 3 * random.randint(0, int(fighter.strength * (fighter.target.health / fighter.target.max_health) + fighter.eqStrength + 1))
                        defense = 2 * random.randint(0, int(fighter.target.defense * (fighter.target.health / fighter.target.max_health) + fighter.target.eqDefense + 1))
                        damage = (attack - defense)
                        fighter.strength_dealt += attack
                        fighter.target.defense_dealt += defense
                        if damage <= 0:
                            #print(fighter.full_name + "'s ("+ str(fighter.health) + "/"+ str(fighter.max_health) +") attack was blocked by " + fighter.target.full_name + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.max_health) +")!")
                            fighter.target.team.blocked_attacks += 1
                            continue
                        else:
                            fighter.target.hurt(damage, fighter, self)
                            if not fighter.target.alive:
                                print(colored(fighter.full_name + " ("+ str(fighter.health) + "/"+ str(fighter.max_health) +") struck down " + fighter.target.full_name + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.max_health) +") with " + str(damage) +" damage!", 'red'))
                                fighter.target.team.team_casulties += 1
                                fighter.team.opponent.remove(fighter.target)
                                if fighter.team.opponent.members == []:
                                    self.victor = fighter.team
                                    self.loser = fighter.team.opponent
                                    break
                                pick_target(fighter)
                            else:
                                print(fighter.full_name + " ("+ str(fighter.health) + "/"+ str(fighter.max_health) +") dealt " + str(damage) + " damage to " + fighter.target.full_name + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.max_health) +")!")
                                fighter.team.damage_dealt += damage

                    else:
                        opponent_power = self.power_balance(fighter.team.opponent, fighter.team)
                        if fighter.health <= .4 * fighter.max_health and opponent_power > 2.5 and random.randint(0, 5) < opponent_power:
                            fighter.active = False
                            fighter.team.remove(fighter)
                            print(fighter.full_name + " ("+ str(fighter.health) + "/"+ str(fighter.max_health) +") flees from the battle!")
                            fighter.team.members_fled += 1
                            if fighter.team.members == []:
                                self.victor = fighter.team.opponent
                                self.loser = fighter.team
                                break

                        else:
                            #print(fighter.full_name + " ("+ str(fighter.health) + "/"+ str(fighter.max_health) +") missed " + fighter.species.gender_pronouns[fighter.gender][0] + " attack on " + fighter.target.full_name + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.max_health) +")!")
                            fighter.team.missed_attacks += 1

        print(self.victor.name + " are victorious over " + self.loser.name +"!")

        self.battle_results = "\n{:>30}\t{}   {}".format("Battle Statistics:", self.team_a.name, self.team_b.name)
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Damage Inflicted:", str(self.team_a.damage_dealt), str(self.team_b.damage_dealt), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Casualties:", str(self.team_a.team_casulties), str(self.team_b.team_casulties), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Teammates Fled:", str(self.team_a.members_fled), str(self.team_b.members_fled), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}".format("Attacks Missed:", str(self.team_a.missed_attacks), str(self.team_b.missed_attacks), name=len(self.team_a.name))
        self.battle_results += "\n{:>30}\t{:<{name}}   {}\n".format("Attacks Blocked:", str(self.team_a.blocked_attacks), str(self.team_b.blocked_attacks), name=len(self.team_a.name))

        print(self.battle_results)

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

    def remove(self, fighter):
        self.members.remove(fighter)
