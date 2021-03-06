from counter import *
from recipe import *
from ingredients import *
from agent import _get_instance, _contains_instance, Agent

import numpy as np

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

CLS_LIST = list(CLS_TO_REP.keys())

class World:
    def __init__(self, x, y, num_agents):
        self.width = x
        self.height = y
        self.num_agents = num_agents

        # initialize empty dict for all cells
        locs = [((_x, _y), []) for _y in range(y) for _x in range(x)]
        self.objects = dict(locs)
        self.recipes = []
        self.missions = []
        self.incomplete = []
        self.full_obs_space = np.zeros((len(CLS_LIST)+self.num_agents, self.width, self.height), dtype='float32')

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

            if k[0] >= self.width-1:
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
        
        # update array
        self.full_obs_space[CLS_LIST.index(obj.name)][obj.location[1]][obj.location[0]] += 1
    
    def remove(self, obj):
        if obj in self.objects[obj.location]:
            self.objects[obj.location].remove(obj)
            self.full_obs_space[CLS_LIST.index(obj.name)][obj.location[1]][obj.location[0]] -= 1

    def get(self, location):
        return self.objects[location]

    def update_location(self, obj, new_location):
    # remove
        self.objects[obj.location].remove(obj)
        if isinstance(obj, Agent):
            self.full_obs_space[len(CLS_LIST)+int(obj.name[-1])][obj.location[1]][obj.location[0]] -= 1
        else:
            self.full_obs_space[CLS_LIST.index(obj.name)][obj.location[1]][obj.location[0]] -= 1
            if isinstance(obj, Recipe):
                for item in obj.contains:
                    self.objects[item.location].remove(item)
                    self.full_obs_space[CLS_LIST.index(item.name)][item.location[1]][item.location[0]] -= 1
        
        # add
        self.objects[new_location].append(obj)
        if isinstance(obj, Agent):
            self.full_obs_space[len(CLS_LIST)+int(obj.name[-1])][new_location[1]][new_location[0]] += 1
        else:
            self.full_obs_space[CLS_LIST.index(obj.name)][new_location[1]][new_location[0]] += 1
            if isinstance(obj, Recipe):
                for item in obj.contains:
                    self.objects[new_location].append(item)
                    self.full_obs_space[CLS_LIST.index(item.name)][new_location[1]][new_location[0]] += 1

        # update
        obj.location = new_location
        if isinstance(obj, Recipe):
            for item in obj.contains:
                item.location = new_location
                
    # def to_sparse(self, agent_name):
    #     obj_list = []
    #     agent_locs = []
    #     arrs = np.zeros((len(CLS_LIST)+self.num_agents-1, self.width, self.height))
    #     for k, v in self.objects.items():
    #         for obj in v:
    #             if isinstance(obj, Agent):
    #                 if obj.name == agent_name:
    #                     continue
    #                 agent_locs.append((int(obj.name[-1]), k))
    #             else:
    #                 arrs[CLS_LIST.index(obj.name)][k[1]][k[0]] += 1
        
    #     # agents
    #     agent_locs.sort()
    #     for i, agent_loc in enumerate(agent_locs):
    #         arrs[len(CLS_LIST)+i][agent_loc[1][1]][agent_loc[1][0]] += 1

    #     return arrs.astype('float32')
