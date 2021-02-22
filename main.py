from game import Overcooked
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser("SimplyCooked argument parser")
    parser.add_argument("--level", type=str, required=True)
    parser.add_argument("--num_players", type=int, required=True)
    parser.add_argument("--horizon", type=int, required=True)
    return parser.parse_args()

def print_recipes(recipes):
    for recipe in recipes:
        print(str(recipe))

def start(num_agents, level, horizon):
    env = Overcooked(num_agents, level, horizon)
    env.reset()

    print(f"loaded level: {level}")
    print(f"# of players: {num_agents}")
    print(f"     horizon: {horizon}")
    print("-"*60)

    reward = 0

    while not env.done():
        print(f"timestep: {env.cur_step}")
        env.world.visualize()

        for agent in env.sim_agents:
            print(f"{agent.name} is holding {agent.holding}")

        action_dict = dict()
        for i, agent in enumerate(env.sim_agents):
            action = input(f"{agent.name}'s action: ")
            action_dict[agent.name] = action
        
        env.step(action_dict)

        print("-"*60)
        if len(env.incomplete):
            print("remaining subtasks:")
            print_recipes(env.incomplete)

        print("-"*60)
        print(f"# of completed subtasks: {env.count_completed()}")
        print(f"# of incompleted subtasks: {len(env.incomplete)}")
        print(f"new score: {env.reward_by_progress() - reward}")
        reward = env.reward_by_progress()
        print("-"*60)
    
    if env.succeed():
        print("succeeded!")
    else:
        print("failed!")

if __name__ == '__main__':
    arglist = parse_arguments()
    start(arglist.num_players, arglist.level, arglist.horizon)