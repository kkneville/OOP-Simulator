"""For equipments (weapons and armor) and inventory systems."""

import random
import inspect
import Skills

def update_equipment_catalog(clas):
    """Updates the dictionary of equipment available for each inventory slot"""
    equipment_catalog = {'Head':[], 'Torso':[], 'Arms':[], 'Hands':[], 'Legs':[], 'Feet':[], 'Bag':[]}
    def updater(catalog, clas):
        if inspect.isclass(clas):
            if not clas.__subclasses__():
                catalog[clas.slot_type].append(clas)
            else:
                for equipment in clas.__subclasses__():
                    updater(catalog, equipment)
        return catalog
    return updater(equipment_catalog, clas)

equipment_choices = update_equipment_catalog(Equipment)

class Equipment:
    """
    Equipment Class for all weapons and armor.
    """

    def __init__(self, name, slot_type, slot_quantity, wood, metal, amount, skill, equipper=None):
        self.name = name
        self.slot_type = slot_type
        self.slot_quantity = slot_quantity
        self.wood = wood
        self.metal = metal
        self.equipper = equipper
        if self.equipper:
            self.equipper.inventory.equip(self)
        self.amount = amount
        self.skill = skill

    def __repr__(self):
        return self.name



class Weapon(Equipment):
    slot_type, slot_quantity, amount = 'Hands', 1, 1
    def __init__(self, name, slot_quantity, wood, metal, strength, defense, speed, skill, equipper=None):
        Equipment.__init__(self, name, self.slot_type, slot_quantity, wood, metal, self.amount, skill, equipper)
        self.strength = strength
        self.defense = defense
        self.speed = speed
        self.attackable = True

class Axe(Weapon):
    """
    Common Axe weapon.
    """
    wood = 3
    metal = 4
    name = 'Axe'
    def __init__(self):
        Weapon.__init__(self, self.name, self.slot_quantity, self.wood, self.metal, 3, 1, -1, Skills.AxeSkill)
        self.attack_verb = 'slashed'

class Sword(Weapon):
    """
    Common Sword weapon.
    """
    wood = 3
    metal = 5
    name = 'Sword'
    def __init__(self):
        Weapon.__init__(self, self.name, self.slot_quantity, self.wood, self.metal, 4, 2, -2, Skills.SwordSkill)
        self.attack_verb = 'sliced'

class Spear(Weapon):
    """
    Common Spear weapon.
    """
    wood = 8
    metal = 3
    name = 'Spear'
    def __init__(self):
        Weapon.__init__(self, self.name, self.slot_quantity, self.wood, self.metal, 4, 1, -1, Skills.SpearSkill)
        self.attack_verb = 'stabbed'

class Halberd(Weapon):
    """
    Common Halberd weapon.
    """
    wood = 8
    metal = 6
    name = 'Halberd'
    def __init__(self):
        Weapon.__init__(self, self.name, self.wood, self.metal, 2, 5, 2, -2, Skills.HalberdSkill)
        self.attack_verb = 'stabbed'

class Hammer(Weapon):
    """
    Common Hammer weapon.
    """
    wood = 5
    metal = 4
    name = 'Hammer'
    def __init__(self):
        Weapon.__init__(self, self.name, self.slot_quantity, self.wood, self.metal, 4, 3, -2, Skills.HammerSkill)
        self.attack_verb = 'smashed'

class Mace(Weapon):
    """
    Common Mace weapon.
    """
    wood = 3
    metal = 4
    name = 'Mace'
    def __init__(self):
        Weapon.__init__(self, self.name, self.slot_quantity, self.wood, self.metal, 2, 2, -1, Skills.MaceSkill)
        self.attack_verb = 'smashed'


class RangedWeapon(Weapon):
    """
    Common Ranged weapon.
    """
    def __init__(self, name, slot_quantity, wood, metal, strength, defense, speed, ammo, skill):
        Weapon.__init__(self, name, slot_quantity, wood, metal, strength, defense, speed, skill)
        self.ammo = ammo
    
    def get_ammo(self):
        if self.equipper:
            for item in self.equipper.inventory.equipped['Bag']:
                if isinstance(item, self.ammo):
                    return item
            return None

    def is_prepared(self):
        ammo = self.get_ammo()
        if ammo and ammo.stack_amount >= 1:
            return True
        return False

    @property
    def attack_verb(self):
        if self.is_prepared():
            return 'shot'
        else:
            return 'bashed'

class Bow(RangedWeapon):
    """
    Common Bow weapon.
    """
    wood = 3
    metal = 0
    name = 'Bow'
    skill = Skills.BowSkill
    def __init__(self):
        RangedWeapon.__init__(self, self.name, 2, self.wood, self.metal, 4, 0, -1, Arrow, self.skill)

class Crossbow(RangedWeapon):
    """
    Common Crossbow weapon.
    """
    wood = 3
    metal = 1
    name = 'Crossbow'
    skill = Skills.CrossbowSkill
    def __init__(self):
        RangedWeapon.__init__(self, self.name, 2, self.wood, self.metal, 3, 0, 1, Bolt, self.skill)


class Ammunition(Equipment):
    """
    Common Ammunition class.
    """
    slot_type = 'Bag'
    skill = Skills.AmmoSkill
    attackable = False
    stack_quantity = 10
    slot_quantity = 1
    def __init__(self, name, strength, amount):
        Equipment.__init__(self, name, self.slot_type, self.slot_quantity, self.wood, self.metal, amount, self.skill)
        self.stack_amount = self.stack_quantity
        self.strength = strength
        self.defense = 0
        self.speed = 0

    def merge(self, equipped_stack):
        equipped_stack.stack_amount += self.stack_amount
        del self

class Arrow(Ammunition):
    """
    Common Arrow.
    """
    wood = 1
    metal = 1
    amount = 1
    name = 'Arrows'
    def __init__(self):
        Ammunition.__init__(self, self.name, 2, self.amount)

class Bolt(Ammunition):
    """
    Common Bolt.
    """
    wood = 1
    metal = 1
    amount = 1
    name = 'Bolts'
    def __init__(self):
        Ammunition.__init__(self, self.name, 2, self.amount)

class Armor(Equipment):
    """
    Armor class.
    """
    slot_quantity, amount = 1, 1
    skill = Skills.ArmorSkill
    def __init__(self, name, slot_type, slot_quantity, wood, metal, strength, defense, speed, equipper=None):
        Equipment.__init__(self, name, slot_type, slot_quantity, wood, metal, self.amount, self.skill, equipper)
        self.strength = strength
        self.defense = defense
        self.speed = speed
        self.attackable = False

class Shield(Armor):
    """
    Common Shield.
    """
    wood = 0
    metal = 7
    slot_type = 'Hands'
    name = 'Shield'
    skill = Skills.ShieldSkill
    def __init__(self):
        Armor.__init__(self, self.name, self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 2, -1)
        self.attackable = True
        self.attack_verb = 'struck'

class Helmet(Armor):
    """
    Common Helmet.
    """
    wood = 0
    metal = 5
    slot_type = 'Head'
    name = 'Helmet'
    def __init__(self):
        Armor.__init__(self, self.name, self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 2, -1)

class Plate(Armor):
    """
    Common Plate.
    """
    wood = 0
    metal = 14
    slot_type = 'Torso'
    name = 'Plate'
    def __init__(self):
        Armor.__init__(self, self.name, self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 4, -3)

class Leggings(Armor):
    """
    Common Leggings.
    """
    wood = 0
    metal = 8
    slot_type, slot_quantity = 'Legs', 2
    name = 'Leggings'
    def __init__(self):
        Armor.__init__(self, self.name, self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 3, -2)

class Gauntlet(Armor):
    """
    Common Gauntlet.
    """
    wood = 0
    metal = 4
    amount = 2
    slot_type = 'Arms'
    name = 'Gauntlet'
    def __init__(self):
        Armor.__init__(self, self.name, self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 1, -1)

class Boot(Armor):
    """
    Common Boots.
    """
    wood = 0
    metal = 4
    amount = 2
    slot_type = 'Feet'
    name = 'Boot'
    def __init__(self):
        Armor.__init__(self, self.name, self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 1, 0)


class Inventory:
    """
    Inventory manager for each creature.
    """

    def __init__(self, owner, blocked_items ,heads=0, torso=0, arms=0, hands=0, legs=0, feet=0):
        self.equipped = {}
        if heads:
            self.equipped['Head'] = [None] * heads
        if torso:
            self.equipped['Torso'] = [None] * torso
        if arms:
            self.equipped['Arms'] = [None] * arms
        if hands:
            self.equipped['Hands'] = [None] * hands
        if legs:
            self.equipped['Legs'] = [None] * legs
        if feet:
            self.equipped['Feet'] = [None] * feet
        self.equipped['Bag'] = [None] * 10
        self.blocked_items = blocked_items

        self.owner = owner
        self.demand = None
        self.owner.eqStrength, self.owner.eqDefense, self.owner.eqSpeed = 0, 0, 0

    def equip(self, item, item_remove=None):
        if isinstance(item, Ammunition) and [bag_item for bag_item in self.equipped['Bag'] if type(bag_item) == type(item)]:
            eligible = [bag_item for bag_item in self.equipped['Bag'] if type(bag_item) == type(item)]
            item.merge(eligible[0])

        else:
            try:
                add_quantity = item.slot_quantity
                slot_type = item.slot_type
            except AttributeError:
                add_quantity = item_remove.slot_quantity
                slot_type = item_remove.slot_type
            slot = self.equipped[slot_type]
            if len([item for item in slot if item is item_remove]) >= add_quantity:
                slots_filled = 0
                for index, element in enumerate(slot):
                    if element is item_remove:
                        slot[index] = item
                        slots_filled += 1
                        if slots_filled == add_quantity:
                            break
                if item:
                    if item.equipper:
                        item.equipper.inventory.unequip(item)
                    item.equipper = self.owner
                    [strength_bonus, defense_bonus, speed_bonus] = self.owner.skills.apply_buffs(item)
                    self.owner.eqStrength += strength_bonus
                    self.owner.eqDefense += defense_bonus
                    self.owner.eqSpeed += speed_bonus


    def unequip(self, item):
        self.equip(None, item)
        item.equipper = None
        self.equipped['Bag'].append(item)
        self.owner.eqStrength -= item.strength
        self.owner.eqDefense -= item.defense
        self.owner.eqSpeed -= item.speed
    
    def has_equipped(self, equipment):
        """returns True if an inventory has the specific equipment or type of equipment equipped"""
        if equipment in self.equipped[equipment.slot_type] or [equip for equip in self.equipped[equipment.slot_type] if isinstance(equip, equipment)]:
            return True
        return False

    def get_equipped(self, attackable=False):
        equip_list = []
        for slot in self.equipped:
            equip_list += [equipment for equipment in self.equipped[slot] if equipment]
        if attackable:
            equip_list = [equipment for equipment in equip_list if equipment.attackable]
        return equip_list

    def get_unfilled_slots(self):
        return [slot for slot in self.equipped if None in self.equipped[slot]]

    def get_number_unfilled(self, slot):
        return len([equipment for equipment in self.equipped[slot] if equipment is None])

    def create_demand(self):
        self.demand = None
        unfilled_slots = self.get_unfilled_slots()
        while not self.demand and unfilled_slots or self.demand.slot_quantity > self.get_number_unfilled(self.demand.slot_type):
            if 'Hands' in unfilled_slots:
                demand = random.choice(equipment_choices['Hands'])
            elif self.has_equipped(RangedWeapon) and not self.equipped['Hands'][0].is_prepared:
                demand = self.equipped['Hands'][0].ammo
            else:
                slot_choice = random.choice(unfilled_slots)
                demand = random.choice(equipment_choices[slot_choice])

            if demand.name in self.blocked_items:
                continue 
            if isinstance(demand, Ammunition) and not self.has_equipped(RangedWeapon):
                continue
            if demand is Shield and self.has_equipped(Shield):
                continue
            if demand.slot_type == 'Bag' or demand.slot_quantity <= self.get_number_unfilled(demand.slot_type):
                self.demand = demand

    def __repr__(self):
        string = "{:>30}'s Inventory:" .format(self.owner.full_name)
        for slot, equip_list in self.equipped.items():
            equip_string = ", ".join([equip.name for equip in equip_list if equip])
            string += "\n {:>30} : {}".format(slot, equip_string)
        return string
        
        

