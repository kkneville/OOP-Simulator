import inspect
import Equipment

def update_skill_catalog(clas):
    """Updates the dictionary of equipment available for each inventory slot"""
    skill_catalog = []
    def updater(catalog, clas):
        if inspect.isclass(clas):
            if not clas.__subclasses__():
                catalog.append(clas)
            else:
                for skill in clas.__subclasses__():
                    updater(catalog, skill)
        return catalog
    return updater(skill_catalog, clas)

proficiency_ranks = [['Novice', 1], ['Adaquate', 3], ['Competent', 5],['Skilled', 7],['Proficient', 9], ['Talented', 11], ['Adept', 13], ['Professional', 15], ['Great', 17], ['Legendary', 20]]

class Skill:
    primary_eq_skill = True

    def __init__(self, name, tools, skillset):
        self.name = name
        self.level = 0
        self.tools = tools
        self.skillset = skillset
        self.points = 0
        self.max_points = 10
        self.rank_index = 0
        self.learning_rate = 1
        self.proficiency = ''
        self.profession_name = ''
    
    def upgrade(self):
        if self.points >= self.max_points and self.level < 20:
            self.level += self.points // self.max_points
            self.points = self.points % self.max_points
            self.max_points = int(self.level * 20)
            if self.profession_name:
                for rank in proficiency_ranks:
                    if self.level >= rank[1]:
                        self.proficiency = rank[0]
                        if self.proficiency == 'Legendary':
                            print('{} is now known as a {} {}!'.format(self.skillset.learner.full_name, self.proficiency, self.profession_name))
                    else:
                        break


class WeaponSkill(Skill):
    primary_eq_skill = True
    def __init__(self, name, tools, skillset):
        Skill.__init__(self, name, tools, skillset)

class SwordSkill(WeaponSkill):
    profession_name = 'Swords'
    name = 'Swords'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Sword], skillset)

class AxeSkill(WeaponSkill):
    profession_name = 'Axe'
    name = 'Axes'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Axe], skillset)

class HammerSkill(WeaponSkill):
    profession_name = 'Hammer'
    name = 'Hammers'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Hammer], skillset)

class MaceSkill(WeaponSkill):
    profession_name = 'Mace'
    name = 'Maces'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Mace], skillset)

class SpearSkill(WeaponSkill):
    profession_name = 'Spear'
    name = 'Spears'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Spear], skillset)

class HalberdSkill(WeaponSkill):
    profession_name = 'Halberdier'
    name = 'Halberds'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Halberd], skillset)

class BowSkill(WeaponSkill):
    profession_name = 'Bow'
    name = 'Bows'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Bow], skillset)

class CrossbowSkill(WeaponSkill):
    profession_name = 'Crossbow'
    name = 'Crossbows'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Crossbow], skillset)

class AmmoSkill(WeaponSkill):
    name = 'Shooting'
    def __init__(self, skillset):
        WeaponSkill.__init__(self, self.name, [Equipment.Ammunition], skillset)

class ShieldSkill(Skill):
    name = 'Shields'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [Equipment.Shield], skillset)

class ArmorSkill(Skill):
    name = 'Amor'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [Equipment.Helmet, Equipment.Plate, Equipment.Gauntlet, Equipment.Leggings, Equipment.Boot], skillset)

class RidingSkill(Skill):
    name = 'Riding'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [], skillset)

class SmithingSkill(Skill):
    profession_name = 'Blacksmith'
    name = 'Smithing'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [Equipment.Hammer], skillset)

class FarmingSkill(Skill):
    profession_name = 'Farmer'
    name = 'Farming'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [], skillset)

class MiningSkill(Skill):
    profession_name = 'Miner'
    name = 'Mining'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [Equipment.Axe], skillset)

class WoodcuttingSkill(Skill):
    profession_name = 'Woodcutter'
    name = 'Woodcutting'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [Equipment.Axe], skillset)

class BuildingSkill(Skill):
    profession_name = 'Architect'
    name = 'Building'
    def __init__(self, skillset):
        Skill.__init__(self, self.name, [], skillset)

class Skillsets:
    skill_catalog = update_skill_catalog(Skill)
    def __init__(self, learner, skill_specialties):
        self.learner = learner
        self.skill_list = [skill(self) for skill in self.skill_catalog]
        
        for skill in self.skill_list:
            if skill in skill_specialties:
                skill.learning_rate *= 2
        
    def apply_buffs(self, item):
        primary_buffs = []
        secondary_buffs = []
        for skill in self.skill_list:
            tools = tuple(skill.tools)
            if isinstance(item, tools):
                if skill.primary_eq_skill:
                    primary_buffs += [skill.level]
                else:
                    secondary_buffs += [skill.level]
        
        avg_primary, avg_secondary = 0, 0
        if primary_buffs:
            avg_primary = sum(primary_buffs)/len(primary_buffs)
        if secondary_buffs:
            avg_secondary = sum(secondary_buffs)/len(secondary_buffs)
        weighted_avg = (3 * avg_primary + avg_secondary) / 4
        buff_multiplier = ((weighted_avg * 1.5) / 20) + .5
        return [round(item.strength * buff_multiplier), round(item.defense * buff_multiplier), round(item.speed / buff_multiplier)]        

    def __repr__(self):
        string = "{:>30}'s Skills:" .format(self.learner.full_name)
        for skill in self.skill_list:
            skill_string = '+' * 20 * skill.points / skill.max_points 
            string += "\n {:>30} ({}) : {}".format(skill.name, skill.level, skill_string)
        return string