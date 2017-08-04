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

        earth.update(10)

        a1 = eve.reproduce(adam)
        a2 = eve.reproduce(adam)
        a3 = eve.reproduce(adam)

        b1 = ana.reproduce(joseph)
        b2 = ana.reproduce(joseph)
        b3 = ana.reproduce(joseph)

        earth.update(10)

        war = adam.declareWar(joseph.family)
        if war.victor.leader is joseph:
            jWin += 1
        if war.victor.leader is adam:
            aWin += 1

print('Adam Wins: ' + str(aWin))
print('Joeseph Wins: ' + str(jWin))
