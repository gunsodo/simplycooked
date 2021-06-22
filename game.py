from world import *
from agent import *
from counter import *
import recipe
from ingredients import *

import random
import copy

REP_TO_CLS = {
    'p': Pork,
    'l': Lettuce,
    't': Tomato,
    'c': Cheese,
    'b': Bread,
    'r': recipe.Recipe,

    '-': PlainCounter,
    'P': PorkCounter,
    'L': LettuceCounter,
    'T': TomatoCounter,
    'C': CheeseCounter,
    'B': BreadCounter,

    'D': DeliverCounter,
    'S': Cutboard,
    'Z': Pan,
}

class Overcooked:
    def __init__(self, num_agents, level, horizon):
        self.num_agents = num_agents
        self.level = level
        self.horizon = horizon

        self._world = None
        self.world = None
        self.missions = []
        self.incomplete = []
        self._deliver_counter = None
        self.deliver_counter = None
        self._spawnable = None
        self.spawnable = []
        self.sim_agents = []
        self.cur_step = 0
    
    def load_level(self, level, init=False):
        x, y = 0, 0
        recipe_index = 0

        if init:
            with open(level, 'r') as file:
                # Mark the phases of reading.
                phase = 0
                for line in file:
                    line = line.strip('\n')
                    if line == '':
                        phase += 1

                    # Phase 0: Instantiate World object
                    elif phase == 0:
                        _x, _y = line.split()
                        self.world = World(int(_x), int(_y), self.num_agents)

                    # Phase 1: Read in kitchen map.
                    elif phase == 1:
                        for x, rep in enumerate(line):
                            # Ingredients/Recipes
                            if rep in 'pltcb':
                                counter = PlainCounter(location=(x, y))
                                obj = REP_TO_CLS[rep](location=(x, y))
                                counter.add(obj)
                                self.world.add(obj)
                                self.world.add(counter)
                            elif rep == 'r':
                                counter = PlainCounter(location=(x, y))
                                obj = REP_TO_CLS[rep](location=(x, y), index=recipe_index)
                                counter.add(obj)
                                self.world.add(obj)
                                self.world.add(counter)
                                recipe_index += 1
                            # Counter
                            elif rep in '-PLTCBSZ':
                                counter = REP_TO_CLS[rep](location=(x, y))
                                self.world.add(counter)
                            elif rep == 'D':
                                self.deliver_counter = REP_TO_CLS[rep](location=(x, y))
                                self._deliver_counter = self.deliver_counter
                                self.world.add(self.deliver_counter)
                            else:
                                self.spawnable.append((x, y))
                        y += 1
                    # Phase 2: Read in recipe list.
                    elif phase == 2:
                        self.missions.append(getattr(recipe, line)())
            
            self._spawnable = self.spawnable[:]
            self.world.missions = self.missions[:]
            self.world.incomplete = self.missions[:]
            self.world.width = x+1
            self.world.height = y
            self._world = copy.deepcopy(self.world)
            self._missions = self.missions[:]
            self.incomplete = self.missions[:]
        else:
            self.deliver_counter = copy.deepcopy(self._deliver_counter)
            self.spawnable = self._spawnable[:]
            self.world = copy.deepcopy(self._world)
            self.missions = self._missions[:]
            self.incomplete = self._missions[:]

        while len(self.sim_agents) < self.num_agents:
            location = random.choice(self.spawnable)
            if len(self.spawnable) <= 0:
                raise ValueError('number of agents exceeds the number of available tiles')
            self.spawnable.remove(location)
            sim_agent = Agent(name='player_'+str(len(self.sim_agents)), location=location)
            self.sim_agents.append(sim_agent)
            self.world.objects[location].append(sim_agent)
            self.world.full_obs_space[len(CLS_LIST)+len(self.sim_agents)-1][location[1]][location[0]] += 1
        
    def reset(self, init=False):
        self.world = None
        self.missions = []
        self.incomplete = []
        self.deliver_counter = None
        self.spawnable = []
        self.sim_agents = []
        self.cur_step = 0

        self.load_level(self.level, init)

    def step(self, joint_action_dict):
        step_flag = [False] * len(joint_action_dict)
        for _ in range(len(joint_action_dict)):
            for i, agent in enumerate(self.sim_agents):
                if not step_flag[i]:
                    step_flag[i] = agent.move(joint_action_dict[agent.name], self.world)
        self.cur_step += 1
        self.incomplete = self.world.incomplete

    def done(self):
        return self.succeed() or self.cur_step >= self.horizon

    def count_completed(self):
        return len(self.deliver_counter.contains)

    def succeed(self):
        return len(self.incomplete) == 0

    def reward_by_progress(self, progress_rwd=5, deliver_rwd=10):
        incomplete = self.incomplete[:]
        incomplete.sort(key=lambda x: x.layers)

        world_recipes = self.world.recipes[:]
        world_recipes.sort(key=lambda x: x.layers, reverse=True)

        reward_dict = dict()

        for recipe in world_recipes:
            if recipe.layers <= 0:
                continue
            reward_dict[recipe.index] = 0
            for i_recipe in incomplete:
                if recipe.layers > i_recipe.layers:
                    continue
                i_recipe_trim = i_recipe.trim(recipe.layers)
                if i_recipe_trim == recipe:
                    reward_dict[recipe.index] = recipe.layers * progress_rwd
                    incomplete.remove(i_recipe)
                    break
        
        for recipe in world_recipes:
            if recipe.delivered:
                reward_dict[recipe.index] = recipe.layers * progress_rwd + deliver_rwd
        
        return reward_dict
    
    @staticmethod
    def compare_reward(r1, r2):
        reward = 0

        # assume that both dicts have the exact same set of keys
        for k, v2 in r2.items():
            try:
                v1 = r1[k]
            except:
                v1 = 0
            if v2 > v1:
                reward += (v2-v1)
        
        return reward

    @staticmethod
    def get_max_reward(r1, r2):
        reward_dict = dict()
        for k, v2 in r2.items():
            try:
                v1 = r1[k]
                reward_dict[k] = v2 if v2 > v1 else v1
            except:
                reward_dict[k] = v2
        
        return reward_dict

