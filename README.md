# Simplycooked Environment

> README is still under construction. Updates will be made soon!

Simplycooked is an experimental environment which is inspired by a well-
known co-op game named *Overcooked*. This multi-player game lets two or
more players cooperate in completing a cooking order, from picking up
ingredients, slicing, cooking, and delivering. The reward is awarded
when an order is delivered at a certain point in the map.

## Play the Game
Inside `/simplycooked/`, run the following command
```
python main.py --level levels/CheeseVeggie.txt --num_players 2 --horizon 100
```
Movement keys:
```
w: up
a: left
s: down
d: right
```
To perform an action, one can repeat the movement towards the direction of that action.

## Map Details

TODO: How maps are represented? (visualize(), letter abbrieviation)

TODO: Numpy representation of the map and objects (full_obs_space)

## Customization

TODO

### Add a new map

TODO

### Add a new recipe

TODO

### Add a new ingredient

TODO

### Add custom level or change the layout

TODO

### (Optional) Support new actions

TODO

### Adjust reward

TODO

## Example Usage in RL Environment

Most of the functions are already implemented. Only a few justifications
need to be made. Take a look at [our example](https://gitlab.com/gunsodo/coop_marl/-/blob/simplycooked/coop_marl/envs/gym_cooking.py).
