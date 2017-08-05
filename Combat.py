from Creatures import *

class Fight:

    def __init__(self, teamA, teamB):
        self.teamA = teamA
        self.teamB = teamB
        self.teamA.opponent, self.teamB.opponent = self.teamB, self.teamA
        self.participants = self.teamA.members + self.teamB.members
        self.victor = None
        self.loser = None
        self.world = earth
        self.yearFought = self.world.year
        self.name = 'The battle between ' + self.teamA.name + ', led by ' + self.teamA.leader.fullName +', and ' + self.teamB.name + ', led by ' + self.teamB.leader.fullName + ', in the year ' + str(self.yearFought)

    def powerBalance(self, friendlySide = None, opponentSide = None):
        teamA = friendlySide if friendlySide else self.teamA
        teamB = opponentSide if opponentSide else self.teamB

        teamAScore = sum([(.5 + fighter.strength + fighter.defense + fighter.speed + fighter.eqStrength + fighter.eqDefense + fighter.eqSpeed) * (fighter.health/fighter.maxHealth) for fighter in teamA.members if fighter.active])
        teamBScore = sum([(.5 + fighter.strength + fighter.defense + fighter.speed + fighter.eqStrength + fighter.eqDefense + fighter.eqSpeed) * (fighter.health/fighter.maxHealth) for fighter in teamB.members if fighter.active])
        try:
            score = teamAScore / teamBScore
        except ZeroDivisionError:
            score = 999
        return score

    @property
    def combatants(self):
        self.participants = sorted([combatant for combatant in self.participants if combatant.alive], key = lambda x : -(x.speed + x.eqSpeed))
        return self.participants

    def __repr__():
        string += "{} occurred.".format(self.name)
        if self.victor:
            string.repr += "{}, led by {}, was victorious over {}, led by {}.".format(self.victor.name, self.victor.leader.fullName, self.loser.name, self.loser.leader.fullName)

    def fight(self):
        def pickTarget(fighter):
            eligible = [target for target in fighter.team.opponent.members if target.alive and target.active]
            fighter.target = random.choice(eligible)

        print(self.name + " begins.")
        while not self.victor:
            for fighter in self.combatants:
                if fighter.alive and fighter.active:
                    try:
                        if not fighter.target.alive or not fighter.target.active:
                            pickTarget(fighter)
                    except AttributeError:
                        pickTarget(fighter)

                    attackChance = random.randint(0,25)
                    if attackChance <= fighter.speed + fighter.eqSpeed:
                        fighter.speedDealt += 1
                        attack = 3 * random.randint(0, int(fighter.strength * (fighter.target.health / fighter.target.maxHealth) + fighter.eqStrength + 1))
                        defense = 2 * random.randint(0, int(fighter.target.defense * (fighter.target.health / fighter.target.maxHealth) + fighter.target.eqDefense + 1))
                        damage = (attack - defense)
                        fighter.strengthDealt += attack
                        fighter.target.defenseDealt += defense
                        if damage <= 0:
                            #print(fighter.fullName + "'s ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") attack was blocked by " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +")!")
                            fighter.target.team.blockedAttacks += 1
                            pass
                        else:
                            fighter.target.hurt(damage, fighter, self)
                            if not fighter.target.alive:
                                print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") struck down " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +") with " + str(damage) +" damage!")
                                fighter.target.team.teamCasulties += 1
                                fighter.team.opponent.remove(fighter.target)
                                if fighter.team.opponent.members == []:
                                    self.victor = fighter.team
                                    self.loser = fighter.team.opponent
                                    break
                                pickTarget(fighter)
                            else:
                                print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") dealt " + str(damage) + " damage to " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +")!")
                                fighter.team.damageDealt += damage

                    else:
                        opponentPower = self.powerBalance(fighter.team.opponent, fighter.team)
                        if fighter.health <= .4 * fighter.maxHealth and opponentPower > 2.5 and random.randint(0,5) < opponentPower:
                            fighter.active = False
                            fighter.team.remove(fighter)
                            print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") flees from the battle!" )
                            fighter.team.membersFled += 1
                            if fighter.team.members == []:
                                self.victor = fighter.team.opponent
                                self.loser = fighter.team
                                break

                        else:
                            #print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") missed " + fighter.species.genderPronouns[fighter.gender][0] + " attack on " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +")!")
                            fighter.team.missedAttacks += 1

        print(self.victor.name + " are victorious over " + self.loser.name +"!")

        self.battleResults = "\n{:>30}\t{}   {}".format("Battle Statistics:", self.teamA.name, self.teamB.name)
        self.battleResults += "\n{:>30}\t{:<{name}}   {}".format("Damage Inflicted:", str(self.teamA.damageDealt), str(self.teamB.damageDealt), name = len(self.teamA.name))
        self.battleResults += "\n{:>30}\t{:<{name}}   {}".format("Casualties:", str(self.teamA.teamCasulties), str(self.teamB.teamCasulties), name = len(self.teamA.name))
        self.battleResults += "\n{:>30}\t{:<{name}}   {}".format("Teammates Fled:", str(self.teamA.membersFled), str(self.teamB.membersFled), name = len(self.teamA.name))
        self.battleResults += "\n{:>30}\t{:<{name}}   {}".format("Attacks Missed:",str(self.teamA.missedAttacks), str(self.teamB.missedAttacks), name = len(self.teamA.name))
        self.battleResults += "\n{:>30}\t{:<{name}}   {}\n".format("Attacks Blocked:", str(self.teamA.blockedAttacks), str(self.teamB.blockedAttacks), name = len(self.teamA.name))

        print(self.battleResults)

class Team():

    def __init__(self, name, members, leader = None):
        self.name = name
        self.members = members
        if leader:
            self.leader = leader
        else:
            self.leader = self.members[0]
        for member in self.members:
            member.team = self
            member.active = True

        self.missedAttacks = 0
        self.blockedAttacks = 0
        self.damageDealt = 0
        self.teamCasulties = 0
        self.membersFled = 0

    def remove(self, fighter):
        self.members.remove(fighter)
