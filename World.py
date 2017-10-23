"""For instantiating all world objects and controlling space, time, and population."""

from __future__ import division
from termcolor import colored
import random

class World:
    """Creates one world object.
    Updates Year: advances aging
    Population: add_chars adds characters to world
    alive/dead: returns list of alive and dead characters"""

    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.chars = []
        climate = random.randint(1,4)
        if climate == 1:
            self.climate = "Icey tundra."
        if climate == 2:
            self.climate = "Tropical forest."
        if climate == 3:
            self.climate = "Pine forests and rocky mountainous terrain."

    def add_chars(self, character):
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
    def bio(self):
        string = "{} (Year: {}, Population: {}): the desolate rock upon which existince hinges.".format(self.name, str(self.year), str(self.population))
        print(string)

    def update(self, years):
        for year in range(years):
            self.year += 1
            for character in self.alive:
                character.update()

earth = World('Earth', 0)
