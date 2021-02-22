from coop_marl.simplycooked.ingredients import *

class Recipe:
    def __init__(self, location):
        self.layers = 0
        self.contains = []
        self.name = 'Recipe'
        self.holded = False
        self.location = location
        self.delivered = False

    def __str__(self):
        return f"{self.name}: {self._str_list(self.contains)}"

    def _str_list(self, item_list):
        item_list = [str(item) for item in item_list]
        return ", ".join(item_list)

    def __eq__(self, other):
        if not isinstance(other, Recipe) or self.layers != other.layers:
            return False
        return self._str_list(self.contains) == self._str_list(other.contains)

    def add(self, obj):
        if self.layers < 7:
            self.contains.append(obj)
            self.layers += 1

    def move_to(self, location):
        self.location = location

class VeggieBurger(Recipe):
    def __init__(self):
        super().__init__(None)
        self.name = 'VeggieBurger'
        self.add(Bread(None))
        self.add(Tomato(None).chop())
        self.add(Lettuce(None).chop())
        self.add(Bread(None))

class DoubleCheeseBurger(Recipe):
    def __init__(self):
        super().__init__(None)
        self.name = 'DoubleCheeseBurger'
        self.add(Bread(None))
        self.add(Cheese(None))
        self.add(Pork(None).grill())
        self.add(Cheese(None))
        self.add(Bread(None))

class ClassicBurger(Recipe):
    def __init__(self):
        super().__init__(None)
        self.name = 'ClassicBurger'
        self.add(Bread(None))
        self.add(Lettuce(None).chop())
        self.add(Pork(None).grill())
        self.add(Tomato(None).chop())
        self.add(Cheese(None))
        self.add(Bread(None))

class JustBread(Recipe):
    def __init__(self):
        super().__init__(None)
        self.name = 'JustBread'
        self.add(Bread(None))
    
    