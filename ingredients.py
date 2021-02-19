# class Plate:
#     def __init__(self, location):
#         self.name = 'Plate'
#         self.contains = None
#         self.location = location

#     def __str__(self):
#         return self.name

#     def __eq__(self, other):
#         return self.name == other.name

#     def move_to(self, location):
#         self.location = location

class Ingredient:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.holded = False

        self.chopped = False
        self.grilled = False

    def __str__(self):
        prefix = "Fresh"
        if self.chopped:
            prefix = "Chopped"
        if self.grilled:
            prefix = "Grilled"
        
        if prefix:
            return f"{prefix} {self.name}"
        else:
            return self.name

    def __eq__(self, other):
        return str(self) == str(other)
    
    def move_to(self, location):
        self.location = location
    
    def grill(self):
        pass

    def chop(self):
        pass

    def is_grillable(self):
        return False
    
    def is_choppable(self):
        return False

class Bread(Ingredient):
    def __init__(self, location):
        super().__init__('Bread', location)

class Pork(Ingredient):
    def __init__(self, location):
        super().__init__('Pork', location)

    def grill(self):
        self.grilled = True
        return self

    def is_grillable(self):
        return True
    
class Cheese(Ingredient):
    def __init__(self, location):
        super().__init__('Cheese', location)

class Lettuce(Ingredient):
    def __init__(self, location):
        super().__init__('Lettuce', location)

    def chop(self):
        self.chopped = True
        return self
    
    def is_choppable(self):
        return True

class Tomato(Ingredient):
    def __init__(self, location):
        super().__init__('Tomato', location)

    def chop(self):
        self.chopped = True
        return self
    
    def is_choppable(self):
        return True