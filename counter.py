from coop_marl.simplycooked.ingredients import *

class Counter:
    def __init__(self, name, location):
        self.name = name
        self.type = ''
        self.contains = None
        self.location = location

    def __str__(self):
        return f"{self.name} at {self.location} containing {self.contains}"
    
    def add(self, obj):
        self.contains = obj

    def remove(self):
        obj = self.contains
        self.contains = None
        return obj

    def action(self):
        pass

class PlainCounter(Counter):
    def __init__(self, location):
        super().__init__('PlainCounter', location)
        self.type = 'none'
        self.contains = None

class IngredientCounter(Counter):
    def __init__(self, name, location):
        super().__init__(name, location)
        self.type = 'supply'

    def add(self, obj):
        pass

    def remove(self):
        return self.contains

class PorkCounter(IngredientCounter):
    def __init__(self, location):
        super().__init__('PorkCounter', location)
        self.contains = Pork(self.location)

    def remove(self):
        return Pork(self.location)

class CheeseCounter(IngredientCounter):
    def __init__(self, location):
        super().__init__('CheeseCounter', location)
        self.contains = Cheese(self.location)

    def remove(self):
        return Cheese(self.location)

class LettuceCounter(IngredientCounter):
    def __init__(self, location):
        super().__init__('LettuceCounter', location)
        self.contains = Lettuce(self.location)

    def remove(self):
        return Lettuce(self.location)

class TomatoCounter(IngredientCounter):
    def __init__(self, location):
        super().__init__('TomatoCounter', location)
        self.contains = Tomato(self.location)

    def remove(self):
        return Tomato(self.location)

class BreadCounter(IngredientCounter):
    def __init__(self, location):
        super().__init__('BreadCounter', location)
        self.contains = Bread(self.location)

    def remove(self):
        return Bread(self.location)

class ActionCounter(Counter):
    def __init__(self, name, location):
        super().__init__(name, location)
        self.type = 'action'

class Pan(ActionCounter):
    def __init__(self, location):
        super().__init__('Pan', location)
    
    def action(self):
        if self.contains:
            self.contains.grill()

class Cutboard(ActionCounter):
    def __init__(self, location):
        super().__init__('Cutboard', location)
    
    def action(self):
        if self.contains:
            self.contains.chop()

class DeliverCounter(Counter):
    def __init__(self, location):
        super().__init__('DeliverCounter', location)
        self.type = 'action'
        self.contains = []

    def add(self, obj):
        self.contains.append(obj)
