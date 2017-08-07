import random
import inspect

def updateEquipmentCatalog(clas):
    equipmentCatalog = {'Head':[],'Torso':[],'Arms':[],'Hands':[],'Legs':[],'Feet':[]}
    if inspect.isclass(clas):
        if not clas.__subclasses__():
            equipmentCatalog[clas.slotType].append(clas)
        else:
            for equipment in clas.__subclasses__():
                updateEquipmentCatalog(equipment)
    return equipmentCatalog

class Equipment:

    def __init__(self, name, slotType, slotQuantity, wood, metal, productionQuantity, equipper = None):
        self.name = name
        self.slotType = slotType
        self.slotQuantity = slotQuantity
        self.wood = wood
        self.metal = metal
        self.equipper = equipper
        self.productionQuantity = productionQuantity



    def __repr__(self):
        return self.name

class Weapon(Equipment):
    slotType, slotQuantity = 'Hands', 1
    def __init__(self, name, slotQuantity, wood, metal, strength, defense, speed, productionQuantity = 1, equipper = None):
        Equipment.__init__(self, name, self.slotType, slotQuantity, wood, metal, productionQuantity, equipper)
        self.strength = strength
        self.defense = defense
        self.speed = speed

class Axe(Weapon):
    def __init__(self):
        Weapon.__init__(self, 'Axe', self.slotQuantity, 1, 1, 3, 1, -1)

class Sword(Weapon):
    def __init__(self):
        Weapon.__init__(self, 'Sword', self.slotQuantity, 1, 2, 4, 2, -2)

class Spear(Weapon):
    def __init__(self):
        Weapon.__init__(self, 'Spear', self.slotQuantity, 2, 1, 4, 1, -1)

class Halberd(Weapon):
    slotQuantity = 2
    def __init__(self):
        Weapon.__init__(self, 'Halberd', self.slotQuantity, 2, 2, 5, 2, -2)

class Hammer(Weapon):
    def __init__(self):
        Weapon.__init__(self, 'Hammer', self.slotQuantity, 2, 2, 4, 3, -2)

class Mace(Weapon):
    def __init__(self):
        Weapon.__init__(self, 'Mace', self.slotQuantity, 1, 1, 2, 2, -1)

class Armor(Equipment):
    slotQuantity = 1
    def __init__(self, name, slotType, slotQuantity, wood, metal, strength, defense, speed, productionQuantity = 1, equipper = None):
        Equipment.__init__(self, name, slotType, slotQuantity, wood, metal, productionQuantity, equipper)
        self.strength = strength
        self.defense = defense
        self.speed = speed

class Shield(Armor):
    slotType = 'Hands'
    def __init__(self):
        Armor.__init__(self, 'Shield', self.slotType, self.slotQuantity, 0, 1, 0, 2, -1)

class Helmet(Armor):
    slotType = 'Head'
    def __init__(self):
        Armor.__init__(self, 'Helmet', self.slotType, self.slotQuantity, 0, 1, 0, 2, -1)

class Plate(Armor):
    slotType = 'Torso'
    def __init__(self):
        Armor.__init__(self, 'Plate', self.slotType, self.slotQuantity, 0, 2, 0, 4, -3)

class Leggings(Armor):
    slotType, slotQuantity = 'Legs', 2
    def __init__(self):
        Armor.__init__(self, 'Leggings', self.slotType, self.slotQuantity, 0, 2, 0, 3, -2)

class Gauntlet(Armor):
    slotType = 'Arms'
    def __init__(self):
        Armor.__init__(self, 'Gauntlet', self.slotType, self.slotQuantity, 0, 1, 0, 1, -1, 2)

class Boot(Armor):
    slotType = 'Feet'
    def __init__(self):
        Armor.__init__(self, 'Boot', self.slotType, self.slotQuantity, 0, 1, 0, 1, -1, 2)


class Inventory:

    equipmentChoices = updateEquipmentCatalog(Equipment)

    def __init__(self, owner, heads = 0, torso = 0, arms = 0, hands = 0, legs = 0, feet = 0):
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

    def equip(self, item, item_remove = None):
        if item in self.bag:
            self.bag.remove(item)
        try:
            addQuantity = item.slotQuantity
            slotType = item.slotType
        except AttributeError:
            addQuantity = item_remove.slotQuantity
            slotType = item_remove.slotType
        slot = self.equipped[slotType]
        if len([item for item in slot if item is item_remove]) >= addQuantity:
            slotsFilled = 0
            for index in range(len(slot)):
                if slot[index] is item_remove:
                    slot[index] = item
                    slotsFilled += 1
                    if slotsFilled == addQuantity:
                        break
            if item:
                item.equipper = self.owner
                self.owner.eqStrength += item.strength
                self.owner.eqDefense += item.defense
                self.owner.eqSpeed += item.speed

    def hasEquipped(self, equipment):
        if equipment in self.equipped[equipment.slotType] or [equip for equip in self.equipped[equipment.slotType] if isinstance(equip , equipment)]:
            return True
        return False

    def unequip(self, item):
        self.equip(None, item)
        item.equipper = None
        self.bag.append(item)
        self.owner.eqStrength -= item.strength
        self.owner.eqDefense -= item.defense
        self.owner.eqSpeed -= item.speed

    def getUnfilledSlots(self):
        return [slot for slot in self.equipped if None in self.equipped[slot]]

    def getNumberUnfilled(self, slot):
        return len([equipment for equipment in self.equipped[slot] if equipment is None])

    def makeDemand(self):
        while not self.demand:
            slotChoice = random.choice(self.getUnfilledSlots())
            demand = random.choice(self.equipmentChoices[slotChoice])
            if demand is Shield and self.hasEquipped(Shield):
                continue
            if demand.slotQuantity <= self.getNumberUnfilled(slotChoice):
                self.demand = demand

# class RangedWeapon(Weapon):
#     def __init__(self, name, slotQuantity, wood, metal, strength, defense, speed, ammo, equipper = None):
#         Weapon.__init__(self, name, slotQuantity, wood, metal, strength, defense, speed, equipper = None)
#         self.ammo = ammo
#
# class Longbow(RangedWeapon):
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
