"""
Creating the random events that occur in the game.
"""
import arcade
from arcade.gui import *
import random

############
test_input_variable = "This came from another module, and was passed in as a property of this instance of this window"
more_input = "Huzzah input!"
############
class MenuButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 300, 40, "Travel the Trail", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        self.action_function()
        super().on_release()
    def print_to_screen(self):
        super.draw()

def return_to_game(self):
  self.current_state = "GAME_RUNNING"

def random_events(game):
  """Determines if a random event happens and handles it.  Has no return"""
  num = random.uniform(0, 1)
  if num > 0.15 : return # events happen on 15% of days

  # List random event functions.
  possible_random_events = [
    # "oxen_dies",
    # "thief_attacks",
    # "wagon_breaks",
    # "find_abandon_wagon",
    # "bad_weather"
    "lose_one_hundred_days"
    ]

# Randomly pick one event to occur.
  random_event = random.choice(possible_random_events)
  globals()[random_event](game)
   
def lose_one_hundred_days(game):
  game.days_traveled += 100
  game.current_state = "RANDOM_EVENT"
  print("you lost 100 days")

# def find_abandon_wagon(game):
#   """player finds an abandoned wagon"""
#   things_to_find=[("Food",30,100),("Clothing",2,8),("Ammunition",100,500),("Wagon Wheel",1,3),("Wagon Axle",1,3),("Wagon Tongue",1,3)]

#   found = {}
#   while not found: # you gotta find SOMETHING
#     for thing in things_to_find:
#       num = random.uniform(0, 1)
#       if num < 0.2 :
#         amount_found = random.randint(thing[1],thing[2])
#         game.inventory[thing[0]] += amount_found
#         found[thing[0]] = amount_found

#   print ("you found:")
#   for i in sorted (found):
#     print("   ", found[i], i)

def oxen_dies(game):
  """
  Removes an oxen from the players inventory.
  """
  oxen_available = game.inventory['Oxen']
  if oxen_available > 1: # In theory, this should always be true, because random events should never trigger if the player doesn't have oxen to move them down the trail.  But just in case...
    input("Alert!!!  An oxen has died")
    game.inventory['Oxen'] -= 1
    input(f'You have {game.inventory["Oxen"]} oxen remaining')

def thief_attacks(game):
  """
  Theif steals and removes a random amount of food from the player's inventory.
  """
  amount = random.randint(10,30)
  food_available = game.inventory['Food']
  if food_available >= amount:
    input(f'Alert!!!  A thief has stolen {amount} pounds of food')
    game.inventory['Food']-= amount
    input(f'You have {game.inventory["Food"]} pounds of food remaining')
  else:
    game.inventory["Food"] = 0
    input('Alert!!! A thief stole all of  your food')


def wagon_breaks(game):
  """
  Random part on wagon breaks.
  """
  wagon_parts = [
      'Wagon Wheel',
      'Wagon Axle',
      'Wagon Tongue'
      ]
  part = random.choice(wagon_parts)
  if game.inventory[part]>0:
    game.inventory[part]-=1
    input(f'Broken Wagon Arert!!! A wagon {part} broke. You have {game.inventory[part]} remaining')


def bad_weather(game):
  """
  Incliment weather attacks!  Beware!
  """

  days = random.randint(2,4)

  snow = game.weather[0] < 32
  rain = game.weather[0]>42 and game.weather[1] < 68
  scorching = game.weather[1] > 95
  windy = 68 < game.weather[1] < 95
  
  ## build array of possible bad weathers.
  events = ["a severe thunderstorm"]
  if snow : events.append("a snowstorm")
  if rain : events.append("torrential downpour")
  if scorching : events.append("danger of heatstroke")
  if windy : events.append("high winds")
  
  # Determine storm.
  event = random.choice(events)
  
  # Inform player, advance time, and consume food for waiting.
  input(f'Bad Weather Alert!!! You have to halt your journey for {days} days due to {event}')

  for _ in range (days):
    game.consume_rations()
    game.increment_day()

