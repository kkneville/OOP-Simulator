from Creatures import *
import random

if __name__ == "__main__":
    aWin = 0
    jWin = 0

    for x in range(1):
        print('World Generated')
        earth.year = 5
        adam = Human('Adam', 'Male')
        eve = Human('Eve', 'Female')
        
        joseph = Human('Joseph', 'Male')
        ana = Human('Ana', 'Female')

        earth.year = 28
        
        adam.strength = 13
        eve.defense = 13
        joseph.strength = 13
        ana.defense = 10
        
        a1 = eve.reproduce(adam)
        a2 = eve.reproduce(adam)
        a3 = eve.reproduce(adam)

        b1 = ana.reproduce(joseph)
        b2 = ana.reproduce(joseph)
        b3 = ana.reproduce(joseph)

        earth.year = 40
        
        adam.declareWar(joseph.family)
        if adam.family.livingMembers:
            aWin += 1
        if joseph.family.livingMembers:
            jWin += 1

print('Adam Wins: ' + str(aWin))
print('Joeseph Wins: ' + str(jWin))
