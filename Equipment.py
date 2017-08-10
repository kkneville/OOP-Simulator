"""For equipments (weapons and armor) and inventory systems."""

import random
import inspect

def update_equipment_catalog(clas):
    """Updates the dictionary of equipment available for each inventory slot"""
    equipment_catalog = {'Head':[], 'Torso':[], 'Arms':[], 'Hands':[], 'Legs':[], 'Feet':[]}
    def updater(catalog, clas):
        if inspect.isclass(clas):
            if not clas.__subclasses__():
                catalog[clas.slot_type].append(clas)
            else:
                for equipment in clas.__subclasses__():
                    updater(catalog, equipment)
        return catalog
    return updater(equipment_catalog, clas)

class Equipment:
    """
    Equipment Class for all weapons and armor.
    """

    def __init__(self, name, slot_type, slot_quantity, wood, metal, amount, equipper=None):
        self.name = name
        self.slot_type = slot_type
        self.slot_quantity = slot_quantity
        self.wood = wood
        self.metal = metal
        self.equipper = equipper
        self.amount = amount

    def __repr__(self):
        return self.name

class Weapon(Equipment):
    slot_type, slot_quantity, amount = 'Hands', 1, 1
    def __init__(self, name, slot_quantity, wood, metal, strength, defense, speed, equipper=None):
        Equipment.__init__(self, name, self.slot_type, slot_quantity, wood, metal, self.amount, equipper)
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
    def __init__(self):
        Weapon.__init__(self, 'Axe', self.slot_quantity, self.wood, self.metal, 3, 1, -1)
        self.attack_verb = 'slashed'

class Sword(Weapon):
    """
    Common Sword weapon.
    """
    wood = 3
    metal = 5
    def __init__(self):
        Weapon.__init__(self, 'Sword', self.slot_quantity, self.wood, self.metal, 4, 2, -2)
        self.attack_verb = 'sliced'

class Spear(Weapon):
    """
    Common Spear weapon.
    """
    wood = 8
    metal = 3
    def __init__(self):
        Weapon.__init__(self, 'Spear', self.slot_quantity, self.wood, self.metal, 4, 1, -1)
        self.attack_verb = 'stabbed'

class Halberd(Weapon):
    """
    Common Halberd weapon.
    """
    wood = 8
    metal = 6
    def __init__(self):
        Weapon.__init__(self, 'Halberd', self.wood, self.metal, 2, 5, 2, -2)
        self.attack_verb = 'stabbed'

class Hammer(Weapon):
    """
    Common Hammer weapon.
    """
    wood = 5
    metal = 4
    def __init__(self):
        Weapon.__init__(self, 'Hammer', self.slot_quantity, self.wood, self.metal, 4, 3, -2)
        self.attack_verb = 'smashed'

class Mace(Weapon):
    """
    Common Mace weapon.
    """
    wood = 3
    metal = 4
    def __init__(self):
        Weapon.__init__(self, 'Mace', self.slot_quantity, self.wood, self.metal, 2, 2, -1)
        self.attack_verb = 'smashed'

class Armor(Equipment):
    """
    Armor class.
    """
    slot_quantity, amount = 1, 1
    def __init__(self, name, slot_type, slot_quantity, wood, metal, strength, defense, speed, equipper=None):
        Equipment.__init__(self, name, slot_type, slot_quantity, wood, metal, self.amount, equipper)
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
    def __init__(self):
        Armor.__init__(self, 'Shield', self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 2, -1)
        self.attackable = True
        self.attack_verb = 'struck'

class Helmet(Armor):
    """
    Common Helmet.
    """
    wood = 0
    metal = 5
    slot_type = 'Head'
    def __init__(self):
        Armor.__init__(self, 'Helmet', self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 2, -1)

class Plate(Armor):
    """
    Common Plate.
    """
    wood = 0
    metal = 14
    slot_type = 'Torso'
    def __init__(self):
        Armor.__init__(self, 'Plate', self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 4, -3)

class Leggings(Armor):
    """
    Common Leggings.
    """
    wood = 0
    metal = 8
    slot_type, slot_quantity = 'Legs', 2
    def __init__(self):
        Armor.__init__(self, 'Leggings', self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 3, -2)

class Gauntlet(Armor):
    """
    Common Gauntlet.
    """
    wood = 0
    metal = 4
    amount = 2
    slot_type = 'Arms'
    def __init__(self):
        Armor.__init__(self, 'Gauntlet', self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 1, -1)

class Boot(Armor):
    """
    Common Boots.
    """
    wood = 0
    metal = 4
    amount = 2
    slot_type = 'Feet'
    def __init__(self):
        Armor.__init__(self, 'Boot', self.slot_type, self.slot_quantity, self.wood, self.metal, 0, 1, 0)


# class RangedWeapon(Weapon):
#     def __init__(self, name, slotQuantity, wood, metal, strength, defense, speed, ammo, equipper = None):
#         Weapon.__init__(self, name, slotQuantity, wood, metal, strength, defense, speed, equipper = None)
#         self.ammo = ammo
#
# class Bow(RangedWeapon):
# ma    def __init__(self):
#         RangedWeapon.__init__(self, 'Longbow', 2, 2, 0, 4, 0, 0, Arrow, equipper = None)
#
# class Crossbow(RangedWeapon):
#     def __init__(self):
#         RangedWeapon.__init__(self, 'Crossbow', 2, 3, 0, 4, 0, 1, Bolt, equipper = None)
#
# class Ammunition(Equipment):
#     def __init__(self, name, slotQuantity):
#         Equipment.__init__(self, name, 'Bag', slotQuantity, wood, metal, equipper = None)



class Inventory:
    """
    Inventory manager for each creature.
    """

    equipment_choices = update_equipment_catalog(Equipment)

    def __init__(self, owner, heads=0, torso=0, arms=0, hands=0, legs=0, feet=0):
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

        self.bag = []
        self.owner = owner
        self.demand = None
        self.owner.eqStrength, self.owner.eqDefense, self.owner.eqSpeed = 0, 0, 0

    def equip(self, item, item_remove=None):
        if item in self.bag:
            self.bag.remove(item)
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
                self.owner.eqStrength += item.strength
                self.owner.eqDefense += item.defense
                self.owner.eqSpeed += item.speed

    def unequip(self, item):
        self.equip(None, item)
        item.equipper = None
        self.bag.append(item)
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
        while not self.demand and unfilled_slots:
            if 'Hands' in unfilled_slots:
                demand = random.choice(self.equipment_choices['Hands'])
            else:
                slot_choice = random.choice(unfilled_slots)
                demand = random.choice(self.equipment_choices[slot_choice])
            if demand is Shield and self.has_equipped(Shield):
                continue
            if demand.slot_quantity <= self.get_number_unfilled(demand.slot_type):
                self.demand = demand

    def __repr__(self):
        string = "{:>30}'s Inventory:" .format(self.owner.full_name)
        for slot, equip_list in self.equipped.items():
            equip_string = ", ".join([equip.name for equip in equip_list if equip])
            string += "\n {:>30} : {}".format(slot, equip_string)
        return string
        
        

