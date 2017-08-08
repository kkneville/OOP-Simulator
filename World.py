from __future__ import division

class World:

    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.chars = []

    def addChars(self, character):
        self.chars.append(character)

    @property
    def alive(self):
        return [char for char in self.chars if char.alive]

    @property
    def dead(self):
        return [char for char in self.chars if not char.alive]

    @property
    def population(self):
        return len(self.alive)

    @property
    def bio (self):
        string = "{} (Year: {}, Population: {}): the desolate rock upon which existince hinges.".format(self.name, str(self.year), str(self.population))
        print(string)

    def update(self, years):
        self.year += years
        for character in self.alive:
            character.update()

earth = World('Earth', 0)
