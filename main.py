"""Starting point: Spanwns a Human 4 v 4"""


from Creatures import Human
from World import earth
from termcolor import colored

if __name__ == "__main__":

    adam_win = 0
    joseph_win = 0
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
            joseph_win += 1
        if war.victor.leader is adam:
            adam_win += 1

print('Adam Wins: ' + str(adam_win))
print('Joeseph Wins: ' + str(joseph_win))
