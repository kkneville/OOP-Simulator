"""Starting point: Spanwns a Human 4 v 4"""


from Creatures import Human
from World import earth
import Equipment

if __name__ == "__main__":
    ADAM_WIN = 0
    JOSEPH_WIN = 0

    for x in range(1):
        print('World Generated')
        earth.update(5)
        adam = Human('Adam', 'Male')
        eve = Human('Eve', 'Female')

        joseph = Human('Joseph', 'Male')
        ana = Human('Ana', 'Female')

        earth.update(2)
        earth.update(4)
        earth.update(6)

        a1 = eve.reproduce(adam)
        a2 = eve.reproduce(adam)
        a3 = eve.reproduce(adam)

        b1 = ana.reproduce(joseph)
        b2 = ana.reproduce(joseph)
        b3 = ana.reproduce(joseph)

        earth.update(10)

        c1 = Equipment.Spear()
        c1r = Equipment.Shield()
        c2 = Equipment.Sword()
        c3 = Equipment.Sword()
        c4 = Equipment.Sword()

        adam.equip(c1)
        adam.equip(c1r)

        war = adam.declareWar(joseph.family)
        if war.victor.leader is joseph:
            JOSEPH_WIN += 1
        if war.victor.leader is adam:
            ADAM_WIN += 1

print('Adam Wins: ' + str(ADAM_WIN))
print('Joeseph Wins: ' + str(JOSEPH_WIN))
