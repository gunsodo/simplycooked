<<<<<<< HEAD
import coop_marl.simplycooked.world
from coop_marl.simplycooked.counter import *
from coop_marl.simplycooked.recipe import *
=======
import world as w
from counter import *
from recipe import *
>>>>>>> 02b0a9cf23c3288605fb8fe648b9982bf47163b4

class Agent:
    def __init__(self, name, location, facing='S'):
        self.name = name
        self.holding = None
        self.location = location
        self.facing = facing

    def __str__(self):
        return f"{self.name} at {self.location} holding {self.holding}"

    def __eq__(self, other):
        return self.name == other.name
    
    def pick(self, obj):
        self.holding = obj
        self.holding.holded = True

    def drop(self):
        obj = self.holding
        obj.holded = False
        self.holding = None
        return obj

    def move(self, direction, world):
        x, y = self.location
        self.facing = direction
        if direction == 'w':
            y -= 1 # N
        elif direction == 'a':
            x -= 1 # W
        elif direction == 's':
            y += 1 # S
        elif direction == 'd':
            x += 1 # E
        elif direction == 'x':
            return True
        else:
            return True

        # check if a Counter is in the way
        obj_list = world.get((x, y))

        # floor
        if len(obj_list) == 0:
            _update_location(self, (x, y), world)
            if self.holding:
                _update_location(self.holding, (x, y), world)
            return True
        
        elif _contains_instance(obj_list, Agent):
            return False

        # counter
        else:
            c = _get_instance(obj_list, Counter)
            contain = c.contains

            # holding something
            if self.holding:
                if isinstance(c, IngredientCounter):
                    pass                                                # cannot hold other stuff
                elif isinstance(c, ActionCounter):
                    if isinstance(self.holding, Recipe):
                        pass
                    elif contain == None:                                 # if the ActionCounter is available, put it down
                        if isinstance(c, Pan) and not self.holding.is_grillable():
                            pass
                        elif isinstance(c, Cutboard) and not self.holding.is_choppable():
                            pass
                        else:
                            c.add(self.drop())
                            _update_location(c.contains, c.location, world)
                    else:
                        pass
                elif isinstance(c, PlainCounter):
                    if isinstance(contain, Recipe):                     # if there is a Recipe, add to the Recipe
                        if isinstance(self.holding, Recipe):
                            pass
                        else:
                            if not contain.full():
                                dropped = self.drop()
                                contain.add(dropped)
                                _update_location(dropped, c.location, world)
                    elif contain == None:                               # PlainCounter is empty, put it down
                        c.add(self.drop())
                        _update_location(c.contains, c.location, world)
                elif isinstance(c, DeliverCounter):
                    if any(self.holding == mission for mission in world.incomplete):
                        dropped = self.drop()
                        dropped.delivered = True
                        c.add(dropped)
                        _update_location(dropped, c.location, world)
                        world.incomplete.remove(dropped)
                else:
                    pass    
                
            # not holding anything
            else:
                if isinstance(c, IngredientCounter):
                    self.pick(c.remove())
                    world.add(self.holding)
                    _update_location(self.holding, self.location, world)
                elif isinstance(c, ActionCounter):
                    if contain:
                        if contain.grilled or contain.chopped:          # already cooked, so pick it up
                            self.pick(c.remove())
                            _update_location(self.holding, self.location, world)
                        else:
                            c.action()
                elif isinstance(c, PlainCounter):
                    if contain:
                        self.pick(c.remove())
                        _update_location(self.holding, self.location, world)
                elif isinstance(c, DeliverCounter):
                    pass
                else:
                    pass
            return True

def _contains_instance(obj_list, obj_cls):
    return any(isinstance(obj, obj_cls) for obj in obj_list)

def _get_instance(obj_list, obj_cls):
    instance = list(filter(lambda x: isinstance(x, obj_cls), obj_list))
    if len(instance) == 0:
        return None
    else:
        return instance[0]

def _update_location(obj, new_location, world):
    # remove
    world.objects[obj.location].remove(obj)
    if isinstance(obj, Agent):
        world.full_obs_space[len(w.CLS_LIST)+int(obj.name[-1])][obj.location[1]][obj.location[0]] -= 1
    else:
        world.full_obs_space[w.CLS_LIST.index(obj.name)][obj.location[1]][obj.location[0]] -= 1
        if isinstance(obj, Recipe):
            for item in obj.contains:
                world.objects[item.location].remove(item)
                world.full_obs_space[w.CLS_LIST.index(item.name)][item.location[1]][item.location[0]] -= 1
    
    # add
    world.objects[new_location].append(obj)
    if isinstance(obj, Agent):
        world.full_obs_space[len(w.CLS_LIST)+int(obj.name[-1])][new_location[1]][new_location[0]] += 1
    else:
        world.full_obs_space[w.CLS_LIST.index(obj.name)][new_location[1]][new_location[0]] += 1
        if isinstance(obj, Recipe):
            for item in obj.contains:
                world.objects[new_location].append(item)
                world.full_obs_space[w.CLS_LIST.index(item.name)][new_location[1]][new_location[0]] += 1

    # update
    obj.location = new_location
    if isinstance(obj, Recipe):
        for item in obj.contains:
            item.location = new_location
