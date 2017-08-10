import collections
from Equipment import *

class Skill:
    proficiencyRanks = [['Novice', 1], ['Adaquate', 3], ['Competent', 5],['Skilled', 7],['Proficient', 9], ['Talented', 11], ['Adept', 13], ['Professional', 15], ['Great', 17], ['Legendary', 20]]
    def __init__(self, name, tools, skillset):
        self.name = name
        self.level = 0
        self.tools = tools
        self.skillset = skillset
        self.points = 0
        self.max_points = 10
        self.rank_index = 0
        self.proficiency = ''
    
    def upgrade(self):
        if self.points >= self.max_points:
            self.level += self.points // self.max_points
            self.points = self.points % self.max_points
            if self.profession_name:
                for rank in self.proficiencyRanks:
                    if self.level >= rank[1]:
                        self.proficiency = rank[0]
                        if self.proficiency == 'Legendary':
                            print('{} is now known as a {} {}!'.format(skillset.learner.full_name, self.proficiency, self.profession_name))
                    else:
                        break


class WeaponSkill(Skill):
    def __init__(self, name, tools):
        Skill.__init__(self, name, tools)

class Sword(WeaponSkill):
    profession_name = 'Swords'
    def __init__(self):
        WeaponSkill.__init__(self, 'Swords', [Sword])

class Axe(WeaponSkill):
    profession_name = 'Axe'
    def __init__(self):
        WeaponSkill.__init__(self, 'Axes', [Axe])

class Hammer(WeaponSkill):
    profession_name = 'Hammer'
    def __init__(self):
        WeaponSkill.__init__(self, 'Hammers', [Hammer])

class Mace(WeaponSkill):
    profession_name = 'Mace'
    def __init__(self, 'Maces', [Mace]):
        WeaponSkill.__init__(self, 'Maces', [Mace])

class Spear(WeaponSkill):
    profession_name = 'Spear'
    def __init__(self):
        WeaponSkill.__init__(self, 'Spears', [Spear])

class Halberd(WeaponSkill):
    profession_name = 'Halberdier'
    def __init__(self):
        WeaponSkill.__init__(self, 'Halberds', [Halberd])

class Bow(WeaponSkill):
    profession_name = 'Bow'
    def __init__(self):
        WeaponSkill.__init__(self, 'Bows', [Bow])

class Crossbow(WeaponSkill):
    profession_name = 'Crossbow'
    def __init__(self):
        WeaponSkill.__init__(self, 'Crossbows', [Crossbow])

class Shield(Skill):
    profession_name = ''
    def __init__(self):
        Skill.__init__(self, 'Shields', [Shield])

class Armor(Skill):
    profession_name = ''
    def __init__(self):
        Skill.__init__(self, 'Armor', [Helmet, Plate, Gauntlet, Leggings, Boot])

class Riding(Skill):
    profession_name = ''
    def __init__(self):
        Skill.__init__(self, 'Riding', [])

class Smithing(Skill):
    profession_name = 'Blacksmith'
    def __init__(self):
        Skill.__init__(self, 'Smithing', [Hammer])

class Farming(Skill):
    profession_name = 'Farmer'
    def __init__(self):
        Skill.__init__(self, 'Farming', [Hoe])

class Mining(Skill):
    profession_name = 'Miner'
    def __init__(self):
        Skill.__init__(self, 'Mining', [Pickaxe])

class Woodcutting(Skill):
    profession_name = 'Woodcutter'
    def __init__(self):
        Skill.__init__(self, 'Woodcutting', [Axe])

class Building(Skill):
    profession_name = 'Architect'
    def __init__(self):
        Skill.__init__(self, 'Building', [])


class Skillsets:
    def __init__(self, learner, blocked_skills, skill_specialties):
        self.skills = {}
