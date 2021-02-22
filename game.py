from coop_marl.simplycooked.world import *
from coop_marl.simplycooked.agent import *
from coop_marl.simplycooked.counter import *
import coop_marl.simplycooked.recipe as recipe
from coop_marl.simplycooked.ingredients import *

from ray.rllib.env.multi_agent_env import MultiAgentEnv
import random

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

class Overcooked(MultiAgentEnv):
    def __init__(self, num_agents, level, horizon):
        self.num_agents = num_agents
        self.level = level
        self.horizon = horizon

        self.world = None
        self.missions = []
        self.incomplete = []
        self.deliver_counter = None
        self.spawnable = []
        self.sim_agents = []
        self.cur_step = 0
    
    def load_level(self, level):
        x, y = 0, 0

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
                        if rep in 'rpltcb':
                            counter = PlainCounter(location=(x, y))
                            obj = REP_TO_CLS[rep](location=(x, y))
                            counter.add(obj)
                            self.world.add(obj)
                            self.world.add(counter)
                        # Counter
                        elif rep in '-PLTCBSZ':
                            counter = REP_TO_CLS[rep](location=(x, y))
                            self.world.add(counter)
                        elif rep == 'D':
                            self.deliver_counter = REP_TO_CLS[rep](location=(x, y))
                            self.world.add(self.deliver_counter)
                        else:
                            self.spawnable.append((x, y))
                    y += 1
                # Phase 2: Read in recipe list.
                elif phase == 2:
                    self.missions.append(getattr(recipe, line)())

        while len(self.sim_agents) < self.num_agents:
            location = random.choice(self.spawnable)
            if len(self.spawnable) <= 0:
                raise ValueError('number of agents exceeds the number of available tiles')
            self.spawnable.remove(location)
            sim_agent = Agent(name='player_'+str(len(self.sim_agents)), location=location)
            self.sim_agents.append(sim_agent)
            self.world.objects[location].append(sim_agent)        

        self.world.missions = self.missions
        self.world.incomplete = self.missions
        self.incomplete = self.missions
        self.world.width = x+1
        self.world.height = y

    def reset(self):
        self.world = None
        self.missions = []
        self.incomplete = []
        self.deliver_counter = None
        self.spawnable = []
        self.sim_agents = []
        self.cur_step = 0

        self.load_level(self.level)

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

        reward = 0
        for recipe in world_recipes:
            if recipe.layers <= 0:
                continue
            for i_recipe in incomplete:
                if recipe.layers > i_recipe.layers:
                    continue
                i_recipe_trim = i_recipe.trim(recipe.layers)
                if i_recipe_trim == recipe:
                    reward += recipe.layers * progress_rwd
                    incomplete.remove(i_recipe)

        reward += deliver_rwd * self.count_completed()
        return reward
    

