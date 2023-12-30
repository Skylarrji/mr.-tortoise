# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


### Vicky's Helper functions ###
# this function takes in the coordinates of the snake's head as well as the move direction (e.g. "up") and returns the coordinate of the future head position
def calculate_next_position(head, next_move_direction):
  if next_move_direction == 'up':
    coord = {'x': 0, 'y': 1}
  elif next_move_direction == 'down':
    coord = {'x': 0, 'y': -1}
  elif next_move_direction == 'left':
    coord = {'x': -1, 'y': 0}
  elif next_move_direction == 'right':
    coord = {'x': 1, 'y': 0}

  # calculate the next move position based on the head position
  next_position = {'x': head['x'] + coord['x'], 'y': head['y'] + coord['y']}
  return next_position


def choose_avoid_collision_move(head, body, safe_moves, next_move):

  # since the next_move would cause collision, remove the next_move option
  for move in safe_moves:
    if move == next_move:
      safe_moves.remove(next_move)

  # calculate the next position for each remaining direction inside safe_moves
  for move in safe_moves:
    next_position = calculate_next_position(head, move)

    # check if the next_position would cause self-collision
    if next_position not in body:
      return move

  # no safe move is found
  if len(safe_moves) != 0:
    return random.choice(safe_moves)
  else:
    return "up"


### Skylar's Helper Functions ###
# coord_to_move = {'[-1, 0]': 'left', '[1, 0]': 'right', '[0, 1]': 'up', '[0, -1]': 'down'}

# input: two points in the form of {'x': val, 'y': val}
# returns an integer representing the distance from p1 to p2
def manhattan_distance(p1, p2):
  return abs(p1['x'] - p2['x']) + abs(p1['y'] - p2['y'])


# returns the food coordinate in which my_snake_head is the closest to and can get to it before any other snake
# if no such food is found, the function returns the first food available
def find_closest_food(my_snake_head, other_snakes_heads, food_positions):
  closest_food = None
  my_shortest_dist = 100 

  for food in food_positions:
    my_food_dist = manhattan_distance(my_snake_head, food)
    can_beat_competitors = True # variable to track if the snake can get to the food faster than any other snake
    
    for other_snake_head in other_snakes_heads:
      other_snake_dist = manhattan_distance(other_snake_head, food)

      if other_snake_dist <= my_food_dist:
        can_beat_competitors = False
        break

    if my_food_dist < my_shortest_dist and can_beat_competitors:
      my_shortest_dist = my_food_dist
      closest_food = food
      

  if closest_food == None:
    return food_positions[0]

  else:
    return closest_food


# returns the move (as a word) that causes the snake to navigate the closest to the target food. if not such move is available, the snake moves down
def navigate_towards_closest_food(my_snake_head, safe_moves, target_food):
  shortest_dist = 100
  shortest_move = None
  
  for move in safe_moves:
    dist = manhattan_distance(calculate_next_position(my_snake_head, move), target_food)
    print(move)
    print(dist)
    print()
    if dist < shortest_dist:
      shortest_dist = dist
      shortest_move = move

  print()
  if shortest_move == None: # no safe moves so snake moves down
    return "down"

  else:
    return shortest_move


# this function returns the move that allows the snake to move closer to its tail (i.e. allows the snake to chase its own tail)
def chase_tail(my_snake_head, safe_move_coords, my_snake_tail, game_state):
  print("chasing tail!")
  next_move_left = calculate_next_position(my_snake_head, "left")
  next_move_right = calculate_next_position(my_snake_head, "right") 
  next_move_up = calculate_next_position(my_snake_head, "up")
  next_move_down = calculate_next_position(my_snake_head, "down")
  
  snake_body = game_state["you"]["body"]

  if next_move_left == my_snake_tail and snake_body[-1] != snake_body[-2]:
    return "left"

  elif next_move_right == my_snake_tail and snake_body[-1] != snake_body[-2]:
    return "right"

  elif next_move_up == my_snake_tail and snake_body[-1] != snake_body[-2]:
    return "up"

  elif next_move_down == my_snake_tail and snake_body[-1] != snake_body[-2]:
    return "down"

  else:
    return navigate_towards_closest_food(my_snake_head, safe_move_coords, my_snake_tail)

# this function returns true (safe) or false (unsafe) depending on the future outcomes of the specified move 
def is_head_to_head_safe(my_snake_head, move_coord, food_coords, other_snake_heads, my_snake_length, other_snake_lengths):
  next_move_left = calculate_next_position(move_coord, "left")
  next_move_right = calculate_next_position(move_coord, "right") 
  next_move_up = calculate_next_position(move_coord, "up")
  next_move_down = calculate_next_position(move_coord, "down")
  other_snake_num = len(other_snake_heads)

  closest_food = find_closest_food(my_snake_head, other_snake_heads, food_coords)
  
  for i in range(other_snake_num):
    snake_head = other_snake_heads[i]
    snake_length = other_snake_lengths[i]
    if my_snake_length > snake_length:
      continue
      
    if next_move_left == snake_head:
      return False

    if next_move_right == snake_head:
      return False

    if next_move_up == snake_head:
      return False

    if next_move_down == snake_head:
      return False
      
    # if manhattan_distance(move_coord, closest_food) <= 1:
    #   if next_move_left == snake_head:
    #     return False
  
    #   if next_move_right == snake_head:
    #     return False
  
    #   if next_move_up == snake_head:
    #     return False
  
    #   if next_move_down == snake_head:
    #     return False

  unsafe_move_count = 0
  

  return True

# this function looks ahead 2 moves to prevent the snake from trapping itself and returns true or false to determine whether or not the coordinate is safe
def prevent_trapping(move_coord, game_state):
  num_bad_future_moves = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
  bad_future_moves_count = 0
  
  next_move_left = calculate_next_position(move_coord, "left")
  next_move_right = calculate_next_position(move_coord, "right") 
  next_move_up = calculate_next_position(move_coord, "up")
  next_move_down = calculate_next_position(move_coord, "down")
  
  # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  # avoid colliding with walls
  if next_move_left["x"] < 0 or next_move_left["x"] > board_width - 1 or next_move_left["y"] < 0 or next_move_left["y"] > board_height - 1:
    num_bad_future_moves['left'] += 1
    bad_future_moves_count += 1
    
  if next_move_right["x"] < 0 or next_move_right["x"] > board_width - 1 or next_move_right["y"] < 0 or next_move_right["y"] > board_height - 1:
    num_bad_future_moves['right'] += 1
    bad_future_moves_count += 1

  if next_move_up["x"] < 0 or next_move_up["x"] > board_width - 1 or next_move_up["y"] < 0 or next_move_up["y"] > board_height - 1:
    num_bad_future_moves['up'] += 1
    bad_future_moves_count += 1

  if next_move_down["x"] < 0 or next_move_down["x"] > board_width - 1 or next_move_down["y"] < 0 or next_move_down["y"] > board_height - 1:
    num_bad_future_moves['down'] += 1
    bad_future_moves_count += 1
    
  # Prevent your Battlesnake from colliding with itself and other Battlesnakes
  opponents = game_state['board']['snakes']
  food = game_state['board']['food']

  for snake in opponents:
    snake_body = snake['body']

    if next_move_left in snake_body and next_move_left != snake_body[-1] and num_bad_future_moves['left'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['left'] += 1

    elif move_coord in food and next_move_left == snake_body[-1] and num_bad_future_moves['left'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['left'] += 1

    if next_move_right in snake_body and next_move_right != snake_body[-1] and num_bad_future_moves['right'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['right'] += 1

    elif move_coord in food and next_move_right == snake_body[-1] and num_bad_future_moves['right'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['right'] += 1

    if next_move_up in snake_body and next_move_up != snake_body[-1] and num_bad_future_moves['up'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['up'] += 1

    elif move_coord in food and next_move_up == snake_body[-1] and num_bad_future_moves['up'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['up'] += 1

    if next_move_down in snake_body and next_move_down != snake_body[-1] and num_bad_future_moves['down'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['down'] += 1

    elif move_coord in food and next_move_down == snake_body[-1] and num_bad_future_moves['down'] == 0:
      bad_future_moves_count += 1
      num_bad_future_moves['down'] += 1

  print("prevent trapping")
  print(move_coord)
  if bad_future_moves_count >= 4:
    return False

  else:
    return True
    
    
# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "Mr. Tortoise 🐢",
    "color": "#AFE1AF",
    "head": "beluga",
    "tail": "hook",
  }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print(game_state['board'])
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
  print(game_state['board'])
  is_move_safe = {"up": True, "down": True, "left": True, "right": True}
  is_move_safe_obstacles = {"up": True, "down": True, "left": True, "right": True}

  # We've included code to prevent your Battlesnake from moving backwards
  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
  my_body = game_state["you"]["body"][1:]

  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    is_move_safe["left"] = False
    is_move_safe_obstacles["left"] = False

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    is_move_safe["right"] = False
    is_move_safe_obstacles["right"] = False

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    is_move_safe["down"] = False
    is_move_safe_obstacles["down"] = False

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    is_move_safe["up"] = False
    is_move_safe_obstacles["up"] = False

  # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  # avoid colliding with walls
  if my_head["x"] == 0:
    is_move_safe["left"] = False
    is_move_safe_obstacles["left"] = False
  if my_head["x"] == board_width - 1:
    is_move_safe["right"] = False
    is_move_safe_obstacles["right"] = False
  if my_head["y"] == 0:
    is_move_safe["down"] = False
    is_move_safe_obstacles["down"] = False
  if my_head["y"] == board_height - 1:
    is_move_safe["up"] = False
    is_move_safe_obstacles["up"] = False

  # SKYLAR'S ADDITION FOR STEPS 2 AND 3
  # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
  my_body = game_state['you']['body']
  my_length = game_state['you']['length']
  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  opponents = game_state['board']['snakes']
  food = game_state['board']['food']
  
  other_snakes_heads = []
  other_snakes_lengths = []
  for snake in opponents:
    if snake['name'] == game_state["you"]["name"]:
      continue
      
    other_snakes_heads.append(snake['head'])
    other_snakes_lengths.append(snake['length'])

  
  next_move_left = calculate_next_position(my_head, "left")
  if not is_head_to_head_safe(my_head, next_move_left, food, other_snakes_heads, my_length, other_snakes_lengths) or not prevent_trapping(next_move_left, game_state):
    print("left trapped")
    is_move_safe["left"] = False

  else:
    # if next_move_left in my_body and next_move_left != my_body[-1]:
    #   is_move_safe["left"] = False 
    #   is_move_safe_obstacles["left"] = False         
    
    for snake in opponents:
      print("left opponent")
      if (next_move_left in snake['body'] and next_move_left != snake['body'][-1]) or (next_move_left == snake['body'][-1] and snake['body'][-1] == snake['body'][-2]):
        print("left body is not safe!")
        is_move_safe["left"] = False 
        is_move_safe_obstacles["left"] = False         
        break

  
  next_move_right = calculate_next_position(my_head, "right")
  if not is_head_to_head_safe(my_head, next_move_right, food, other_snakes_heads, my_length, other_snakes_lengths) or not prevent_trapping(next_move_right, game_state):
    print("right trapped")
    is_move_safe["right"] = False

  else:
    # if next_move_right in my_body and next_move_right != my_body[-1]:
    #   is_move_safe["right"] = False 
    #   is_move_safe_obstacles["right"] = False   
    
    for snake in opponents:
      print("right opponent")
      if (next_move_right in snake['body'] and next_move_right != snake['body'][-1]) or (next_move_right == snake['body'][-1] and snake['body'][-1] == snake['body'][-2]):
        print("right body is not safe!")
        is_move_safe["right"] = False
        is_move_safe_obstacles["right"] = False
        break   

  
  next_move_up = calculate_next_position(my_head, "up")
  if not is_head_to_head_safe(my_head, next_move_up, food, other_snakes_heads, my_length, other_snakes_lengths) or not prevent_trapping(next_move_up, game_state):
    print("up trapped")
    is_move_safe["up"] = False

  else:
    # if next_move_up in my_body and next_move_up != my_body[-1]:
    #   is_move_safe["up"] = False 
    #   is_move_safe_obstacles["up"] = False 
    
    for snake in opponents:
      print("up opponent")
      if (next_move_up in snake['body'] and next_move_up != snake['body'][-1]) or (next_move_up == snake['body'][-1] and snake['body'][-1] == snake['body'][-2]):
        print("up body is not safe!")
        is_move_safe["up"] = False
        is_move_safe_obstacles["up"] = False
        break  

  
  next_move_down = calculate_next_position(my_head, "down")
  if not is_head_to_head_safe(my_head, next_move_down, food, other_snakes_heads, my_length, other_snakes_lengths) or not prevent_trapping(next_move_down, game_state):
    print("down trapped")
    is_move_safe["down"] = False

  else:
    # if next_move_down in my_body and next_move_down != my_body[-1]:
    #   is_move_safe["down"] = False 
    #   is_move_safe_obstacles["down"] = False 
    
    for snake in opponents:
      print("down opponent")
      if (next_move_down in snake['body'] and next_move_down != snake['body'][-1]) or (next_move_down == snake['body'][-1] and snake['body'][-1] == snake['body'][-2]):
        print("down body is not safe!")
        is_move_safe["down"] = False 
        is_move_safe_obstacles["down"] = False
        break  

  # Are there any safe moves left?
  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  safe_moves_obstacles = []
  for move, isSafe in is_move_safe_obstacles.items():
    if isSafe:
      safe_moves_obstacles.append(move)

  # # Skylar's ADDITION: generates a set of movable coordinate to calculate the snake head's future position based on the move name in the list of safe moves
  # safe_move_coords = []
  # for move in safe_moves:
  #   if move == 'left':
  #     safe_move_coords.append([-1, 0])

  #   elif move == 'right':
  #     safe_move_coords.append([1, 0])

  #   elif move == 'up':
  #     safe_move_coords.append([0, 1])

  #   else:
  #     safe_move_coords.append([0, -1])


  print("safe moves obstacles:")
  print(safe_moves_obstacles)
  print("safe moves:") 
  print(safe_moves)
  if len(safe_moves_obstacles) == 0:
      print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
      return {"move": "down"}

  # FIND CLOSEST FOOD
  else:
    if len(safe_moves) == 0:
      safe_moves = safe_moves_obstacles
      my_tail = my_body[-1]
      next_move = chase_tail(my_head, safe_moves, my_tail, game_state)


    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # only move towards food if it exists
    else:
      my_length = game_state["you"]["length"]
      my_health = game_state["you"]["health"]
      if len(food) != 0 and (my_length < 7 or my_health < 23):
        closest_food = find_closest_food(my_head, other_snakes_heads, food)
        next_move = navigate_towards_closest_food(my_head, safe_moves, closest_food)
  
      else:
        my_tail = my_body[-1]
        # Chase tail if no food exists
        next_move = chase_tail(my_head, safe_moves, my_tail, game_state)    

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}

  # # TEST: prevent colliding with itself
  # next_position = calculate_next_position(my_head, next_move)

  # # check if the next_position would cause self-collision
  # if next_position in my_body:
  #   # collision detected...
  #   # choose a different direction
  #   avoid_collision_move = choose_avoid_collision_move(my_head, my_body,
  #                                                      safe_moves, next_move)
  #   return {"move": avoid_collision_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
