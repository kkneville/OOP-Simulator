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
        self.name = 'The battle between ' + self.teamA.name + ', led by ' + self.teamA.leader.fullName +', and ' + self.teamB.name + ', led by ' + self.teamB.leader.fullName + ', in the year ' + str(self.world.year)

    def powerBalance(self, friendlySide = None, opponentSide = None):
        teamA = friendlySide if friendlySide else self.teamA
        teamB = opponentSide if opponentSide else self.teamB

        teamAScore = sum([(.5 + fighter.strength + fighter.defense + fighter.speed) * (fighter.health/fighter.maxHealth) for fighter in teamA.members if fighter.active])
        teamBScore = sum([(.5 + fighter.strength + fighter.defense + fighter.speed) * (fighter.health/fighter.maxHealth) for fighter in teamB.members if fighter.active])
        try:
            score = teamAScore / teamBScore
        except ZeroDivisionError:
            score = 999
        return score
    
    @property
    def combatants(self):
        self.participants = sorted([combatant for combatant in self.participants if combatant.alive], key = lambda x : -x.speed)
        return self.participants
    
    def fight(self):
        def pickTarget(fighter):
            eligible = [target for target in fighter.team.opponent.members if target.alive and target.active]
            fighter.target = eligible[int(random.random() * len(eligible))]

        print(self.name + " begins.")                    
        while not self.victor:
            for fighter in self.combatants:
                if fighter.alive and fighter.active:
                    try:
                        if not fighter.target.alive or not fighter.target.active:
                            pickTarget(fighter)
                    except AttributeError:
                        pickTarget(fighter)

                    attackChance = random.random() * 20
                    if attackChance <= fighter.speed:
                        fighter.speedDealt += int(attackChance)
                        attack = int(random.random() * fighter.strength * (fighter.health / fighter.maxHealth))
                        defense = int(random.random() * fighter.target.defense * (fighter.target.health / fighter.target.maxHealth))
                        damage = 4 * (attack - defense)
                        fighter.strengthDealt += attack
                        fighter.target.defenseDealt += defense
                        if damage <= 0:
                            print(fighter.fullName + "'s ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") attack was blocked by " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +")!")
                            pass
                        else:                           
                            fighter.target.hurt(damage, fighter, self)
                            if not fighter.target.alive:
                                print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") struck down " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +") with " + str(damage) +" damage!")
                                fighter.team.opponent.remove(fighter.target)
                                if fighter.team.opponent.members == []:
                                    self.victor = fighter.team
                                    self.loser = fighter.team.opponent
                                    break
                                pickTarget(fighter)
                            else:
                                print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") dealt " + str(damage) + " damage to " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +")!")

                    else:
                        opponentPower = self.powerBalance(fighter.team.opponent, fighter.team)
                        if opponentPower > 2 and round(random.random() * 4) < opponentPower:
                            fighter.active = False
                            fighter.team.remove(fighter)
                            print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") flees from the battle!" )
                            if fighter.team.members == []:
                                self.victor = fighter.team.opponent
                                self.loser = fighter.team
                                break
                            
                        else:
                            print(fighter.fullName + " ("+ str(fighter.health) + "/"+ str(fighter.maxHealth) +") missed " + fighter.species.genderPronouns[fighter.gender][0] + " attack on " + fighter.target.fullName + " ("+ str(fighter.target.health) + "/"+ str(fighter.target.maxHealth) +")!")

        print(self.victor.name + " are victorious over " + self.loser.name +"!")
           

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

    def remove(self, fighter):
        self.members.remove(fighter)
