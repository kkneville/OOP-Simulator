from __future__ import division
import pdb
import random
import types

def genRandom(a, b, stdDev = 4):
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)
    return int(random.uniform( mean([a, b]) + stdDev, mean([a, b]) - stdDev))

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
        string = self.name + " (Year: " + str(self.year) +", Population: " + str(self.population) +"): the desolate rock upon which existince hinges."
        print(string)

    def update(self, years):
        self.year += years
        for character in self.alive:
            character.update()

earth = World('Earth', 0)
