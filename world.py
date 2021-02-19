from counter import *
from agent import *
from recipe import *
from ingredients import *
from agent import _get_instance, _contains_instance

CLS_TO_REP = {
    'Pork': 'p',
    'Lettuce': 'l',
    'Tomato': 't',
    'Cheese': 'c',
    'Bread': 'b',
    'Recipe': 'r',

    'PlainCounter': '-',
    'PorkCounter': 'P',
    'LettuceCounter': 'L',
    'TomatoCounter': 'T', 
    'CheeseCounter': 'C',
    'BreadCounter': 'B',

    'DeliverCounter': 'D',
    'Cutboard': 'S',
    'Pan': 'Z',
}

class World:
    def __init__(self, x, y):
        self.width = x
        self.height = y

        # initialize empty dict for all cells
        locs = [((_x, _y), []) for _y in range(y) for _x in range(x)]
        self.objects = dict(locs)
        self.recipes = []
        self.missions = []
        self.incomplete = []

    def _str_list(self, item_list):
        item_list = [str(item) for item in item_list]
        return ", ".join(item_list)

    def _print_world(self):
        for k, v in self.objects.items():
            print(f"{k}: {self._str_list(v)}")
    
    def visualize(self):
        action_counters = []
        for k, v in self.objects.items():
            c = _get_instance(v, Counter)
            if c == None:
                p = _get_instance(v, Agent)
                if p:
                    print(p.name[-1], end='')
                else:
                    print(' ', end='')
            elif isinstance(c, PlainCounter):
                contain = c.contains
                if isinstance(contain, Recipe):
                    print('r', end='')
                elif contain:
                    print(CLS_TO_REP[contain.name], end='')
                else:
                    print('-', end='')
            elif isinstance(c, ActionCounter):
                if c.contains:
                    action_counters.append(c)
                print(CLS_TO_REP[c.name], end='')
            else:
                print(CLS_TO_REP[c.name], end='')

            if k[0] >= self.width:
                print('')

        print("-"*60)
        print("list of recipes:")
        for recipe in self.recipes:
            if not recipe.delivered:
                print(recipe.location, recipe)
        
        if len(action_counters):
            print("pending items:")
            print(self._str_list(action_counters))
        print("-"*60)

    def add(self, obj):
        assert obj.location <= (self.width, self.height)
        self.objects[obj.location].append(obj)

        if isinstance(obj, Recipe):
            self.recipes.append(obj)
    
    def remove(self, obj):
        if obj in self.objects[obj.location]:
            self.objects[obj.location].remove(obj)

    def get(self, location):
        return self.objects[location]

