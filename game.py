from world import *
from agent import *
from counter import *
import recipe
from ingredients import *

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

class Overcooked:
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

    

