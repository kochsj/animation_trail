"""
Sprite Bullets

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_bullets_aimed
"""

import random
import arcade
import math
import os
from arcade.gui import *

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 2
SPRITE_SCALING_LASER = 0.3
COIN_COUNT = 5

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Sprites and Bullets Aimed Example"

BULLET_SPEED = 25


window = None


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.background = None
        # Variables that will hold sprite lists
        self.player_list = None
        self.animal_sprite_list = None
        self.bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.pounds_of_meat = 0
        self.score_text = None
        self.bullets_used = 0
        self.current_state = "GAME_RUNNING"

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
               
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        """ Set up the game and initialize the variables. """

        self.background = arcade.load_texture("forest_for_hunting.png")

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.animal_sprite_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite("frontiersman_sprite15.png", 3)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 90
        self.player_list.append(self.player_sprite)

        # Create the bears
        for i in range(random.randint(0,3)):
            # Create the bear instance
            # bear image from kenney.nl
            bear = arcade.Sprite("bear_sprite_08.png", SPRITE_SCALING_COIN)
            bear.properties['Bear'] = True
            bear.properties['Sqrl'], bear.properties['Deer'] = False, False
            # Position the bear
            bear.center_x = random.randrange(SCREEN_WIDTH)
            bear.center_y = random.randrange(120, SCREEN_HEIGHT)
            bear.change_x = random.randrange(-9,9)
            bear.change_y = random.randrange(-3,3)
            # Add the bear to the lists
            self.animal_sprite_list.append(bear)

        # Create the sqrls
        for i in range(random.randint(1,10)):
            # Create the sqrl instance
            # sqrl image from kenney.nl
            sqrl = arcade.Sprite("sqrl_sprite_0.png", SPRITE_SCALING_COIN*0.5)
            sqrl.properties['Sqrl'] = True
            sqrl.properties['Bear'], sqrl.properties['Deer'] = False, False
            # Position the sqrl
            sqrl.center_x = random.randrange(SCREEN_WIDTH)
            sqrl.center_y = random.randrange(120, SCREEN_HEIGHT)
            sqrl.change_x = random.randrange(-2,2)
            sqrl.change_y = random.randrange(-1,1)
            # Add the sqrl to the lists
            self.animal_sprite_list.append(sqrl)
            
        # Create the deers
        for i in range(random.randint(0,6)):
            # Create the deer instance
            # deer image from kenney.nl
            female_deer = arcade.Sprite("sprite_06.png", SPRITE_SCALING_COIN*0.8)
            female_deer.properties['Deer'] = True
            female_deer.properties['Sqrl'], female_deer.properties['Bear'] = False, False
            male_deer = arcade.Sprite("deer_sprite_00.png", SPRITE_SCALING_COIN*1.4)
            male_deer.properties['Deer'] = True
            male_deer.properties['Sqrl'], male_deer.properties['Bear'] = False, False
            # Position the deer
            female_deer.center_x, male_deer.center_x = random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_WIDTH)
            female_deer.center_y, male_deer.center_y = random.randrange(120, SCREEN_HEIGHT), random.randrange(120, SCREEN_HEIGHT)
            female_deer.change_x, male_deer.change_x = random.randrange(-9,9), random.randrange(-9,9)
            female_deer.change_y, male_deer.change_y = random.randrange(-3,3), random.randrange(-3,3)
            
            
            # Add the deer to the lists
            self.animal_sprite_list.append(female_deer)
            self.animal_sprite_list.append(male_deer)

        # Set the background color
        # arcade.set_background_color(arcade.color.AMAZON)
                
        
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == "GAME_RUNNING":
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)


            # Draw all the sprites.
            self.animal_sprite_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()

            # Put the text on the screen.
            bullet_output = f"Bullets Used: {self.bullets_used}"
            food_output = f"Food Gathered: {self.pounds_of_meat} pounds"
            arcade.draw_text(bullet_output, 10, 20, arcade.color.WHITE, 14)
            arcade.draw_text(food_output,150,20, arcade.color.WHITE, 14)
            self.test_image_move += 1
        else:
            bullet_output = f"Bullets Used: {self.bullets_used}"
            food_output = f"Food Gathered: {self.pounds_of_meat} pounds" 
            arcade.draw_text("Round Over", 500, 530, arcade.color.BLACK, 60)   
            arcade.draw_text(bullet_output,550, 450, arcade.color.WHITE, 24)
            arcade.draw_text(food_output,550, 375, arcade.color.WHITE, 24)
            arcade.draw_text("Click to hunt again...", 500, 300, arcade.color.BLACK, 24)
            arcade.draw_rectangle_outline(SCREEN_WIDTH // 2, 460, 475, 400, arcade.color.BLACK, 6)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse clicked.
        """
        if self.current_state == "GAME_RUNNING":
            # Create a bullet from https://www.kenney.nl/assets/tanks
            bullet = arcade.Sprite("tank_bulletFly6.png", SPRITE_SCALING_LASER)
            self.bullets_used += 1
            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            dest_x = x
            dest_y = y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.angle = math.degrees(angle)
            # print(f"Bullet angle: {bullet.angle:.2f}")
            # print(f'{self.bullets_used}')

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)
        else:
            self.setup()
            self.current_state = "GAME_RUNNING"

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.bullet_list.update()
        self.animal_sprite_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.animal_sprite_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                print(f'animal(?): {coin.properties}')
                if coin.properties['Bear']:
                    self.pounds_of_meat += 250
                if coin.properties['Deer']:
                    self.pounds_of_meat += random.randint(50,100)
                if coin.properties['Sqrl']:
                    self.pounds_of_meat += random.randint(1,3)
                
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

            #If animal flies off-screen, remove it.
            for animal in self.animal_sprite_list:
                if animal.bottom > self.width or animal.top < 0 or animal.right < 0 or animal.left > self.width:
                    animal.remove_from_sprite_lists()

        #if there are no more animals.. end game?
        if not self.animal_sprite_list.sprite_list:
            self.current_state = "GAME_OVER"
            


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()