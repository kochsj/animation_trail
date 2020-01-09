import arcade
from arcade.gui import *
from random_events import random_events, test_input_variable, more_input, MenuButton, return_to_game

class TraverseTheTrail(arcade.Window):
    """ Main application class. """

    def __init__(self, x_coord, pace, landmarks, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate=1/40)
        self.background = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.animal_sprite_list = None

        # Set up the player info
        self.player_sprite = None
        self.miles_traveled = 0
        self.days_traveled = 0
        self.location_at_start_of_day = x_coord or -(15584/2)+SCREEN_WIDTH
        self.image_position = x_coord or -(15584/2)+SCREEN_WIDTH
        #Set up pace
        self.pace = pace or 1
        self.px_per_day = None
        self.increment_miles_by_pace = 1
        # Set up the landmarks
        self.landmarks = landmarks
        self.next_landmark_position = None
        self.next_landmark_name = None
        #default background   
        arcade.set_background_color(arcade.color.AMAZON)
##########################################################################################
# TEST ###################################################################################
    # def set_button_textures(self):
    #     normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
    #     hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
    #     clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
    #     locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
    #     self.theme.add_button_textures(normal, hover, clicked, locked)
    # def setup_theme(self):
    #     self.theme = Theme()
    #     self.theme.set_font(24, arcade.color.WHITE)
    #     self.set_button_textures()

    # def set_buttons(self):
        # self.button_list.append(MenuButton(700, 300, self.props['menu_func']))

    def setup(self):

        """ Set up the game and initialize the variables. """
        self.background = arcade.load_texture("the_trail.png")

        # Sprite lists
        self.player_list = arcade.SpriteList() #stores wagon

        # check if you are past landmarks at setup
        correct_landmarks = []
        for lmrk in self.landmarks:
            lmrk[0] = ((lmrk[0])*(6.4))+(-(15584/2)+SCREEN_WIDTH)
        for lmrk in self.landmarks:
            if lmrk[0] > self.image_position:
                correct_landmarks.append(lmrk)
        self.landmarks = correct_landmarks

        #check what pace we will be moving at
        if self.pace == 0: #STEADY: every 51.2px is a day (8miles/day*6.4px/mile)
            self.px_per_day = -51.2
            self.increment_miles_by_pace = 8
        if self.pace == 1: #STRENUOUS: every 76.8px is a day (12miles/day*6.4px/mile)
            self.px_per_day = -76.8
            self.increment_miles_by_pace = 12
        if self.pace == 2: #GREULING: every 102.4px is a day (16miles/day*6.4px/mile)
            self.px_per_day = -102.4
            self.increment_miles_by_pace = 16

        # Start the view and wagon sprite
        self.current_state = "GAME_RUNNING"
        self.player_sprite = arcade.Sprite("ox_wagon.png",0.5)
        self.player_sprite.center_x = 1200
        self.player_sprite.center_y = 250
        self.player_list.append(self.player_sprite)

        # TESTING############################################################
        # self.button = MenuButton(700, 300, self.props['menu_func'])       
        
    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == "GAME_RUNNING" or self.current_state == "Paused":
            arcade.draw_texture_rectangle(self.image_position, SCREEN_HEIGHT // 2, 15584, SCREEN_HEIGHT, self.background)

            # Draw wagon
            self.player_list.draw()

            # Print test to the window
            miles_traveled = f"Miles traveled: {self.miles_traveled}"
            days_traveled = f"Days on the trail: {self.days_traveled}"
            arcade.draw_text(days_traveled, 0, SCREEN_HEIGHT-100,arcade.color.BLACK, 24)
            arcade.draw_text(miles_traveled, 0, SCREEN_HEIGHT-140,arcade.color.BLACK, 24)
            arcade.draw_text(f"(dev)current px: {self.image_position}", 0, SCREEN_HEIGHT-180,arcade.color.BLACK, 24)
            # arcade.draw_text(self.props['input_var'][0], 0, SCREEN_HEIGHT-220,arcade.color.BLACK, 24)
            # arcade.draw_text(self.props['input_var'][1], 0, SCREEN_HEIGHT-260,arcade.color.BLACK, 24)



            if self.image_position > 6800: # image starts at -6392; after 13000 pixels you reach Oregon City; game over
                self.current_state = "GAME_OVER"

######################################################################################################################
# HANDLE EVENTS (example) ############################################################################################
######################################################################################################################
        elif self.current_state == "LANDMARK":
            arcade.draw_text(f"You reached {self.next_landmark_name}!", 300, 530, arcade.color.BLACK, 40)
        #random event view
        elif self.current_state == "RANDOM_EVENT":
            arcade.draw_text(f"You lost 100 days...", 300, 530, arcade.color.BLACK, 40)
        elif self.current_state == 'RIVER':
            arcade.draw_text(f"You have to now decide HOW to cross this river.", 200, 530, arcade.color.BLACK, 40)
            arcade.draw_text(f"It is 600ft wide and 6ft deep", 200, 450, arcade.color.BLACK, 40)
        elif self.current_state == "RETURN_TO_MENU":
            arcade.draw_text(f"This is the 'main menu'..", 200, 450, arcade.color.BLACK, 40)
            self.button.print_to_screen()
        else:
            arcade.draw_text("Round Over", 450, 530, arcade.color.BLACK, 80)   

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse clicked.
        Handles states of the trail.
        "Transitions" game from running, paused, print_screens, and game over
        Handles functions passed in at setup()
            :Used to return values from animation
        """
        if self.current_state == "GAME_RUNNING": # click to pause wagon when it is moving
            self.current_state = "Paused"
            self.props["done_handler"](self.image_position)

        elif self.current_state == "LANDMARK": # start the game again if you hit a landmark
            if 'River' in self.next_landmark_name:
                self.current_state = "RIVER"
            elif self.landmarks:
                self.next_landmark_position = None
                self.current_state = "GAME_RUNNING"
                self.props["done_handler"](self.image_position)
            else:
                current_state = "GAME_OVER"

        elif self.current_state == "GAME_OVER": # handles end of game
            self.image_position = -(15584/2)+SCREEN_WIDTH
            self.props["done_handler"](self.image_position)
            # self.current_state = "GAME_RUNNING"

        elif self.current_state == "Paused": # when paused, click to start the game again
            self.current_state = "GAME_RUNNING"
        
        elif self.current_state == "RANDOM_EVENT":
            self.current_state = "GAME_RUNNING"
        elif self.current_state == "RIVER":
            self.next_landmark_position = None
            self.current_state = "GAME_RUNNING"
            self.props["done_handler"](self.image_position)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.RETURN:
            self.current_state = "RETURN_TO_MENU"

    def on_update(self, delta_time):
        """ Movement and game logic """

        if self.current_state == "GAME_RUNNING":
            #check if it has been a day / count days
            if (self.location_at_start_of_day - self.image_position) < self.px_per_day:
                self.days_traveled += 1
                # self.props["random_event"](self)
                self.miles_traveled += self.increment_miles_by_pace
                self.location_at_start_of_day = self.image_position

            #make sure game is tracking the next landmark
            if not self.next_landmark_position:
                lmrk_tuple = self.landmarks.pop()
                self.next_landmark_position = lmrk_tuple[0]
                self.next_landmark_name = lmrk_tuple[1]
            # move the map behind wagon 
            self.image_position += (self.pace+1) #moves image position

            # check if you hit a landmark
            if self.image_position > self.next_landmark_position: #when you hit a landmark, stop running, change state to landmark
                self.current_state = "LANDMARK"


if __name__ == "__main__":

    def miles_traveled(val):
        """ Example output from animation """
        print(val)
        return val
    landmark_list = [[2040,"Oregon City"],[1863,"Fort Walla Walla"],[1808,"The Blue Mountains"],[1648,"Fort Boise"],[1543,"the Snake River crossing"],[1395,"Fort Hall"],[1259,"Soda Springs"],[1151,"The Green River Crossing"],[989,"Fort Bridger"],[932,"South Pass [Butte Mtns]"],[830,"Independence Rock"],[640,"Fort Laramie"],[554,"Chimney Rock"],[304,"Fort Kearny"],[185,"the Blue River crossing"],[102, "the Kansas River crossing"]]
    
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800
    SCREEN_TITLE = "OREGON TRAIL"
    game = TraverseTheTrail(0,0, landmark_list, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    props = {"done_handler": miles_traveled, "random_event": random_events, "input_var": (test_input_variable, more_input), "menu_func": return_to_game} # dictionary of a pointer to function in memory
    game.props = props # add the dictionary to the game as attribute 'props'
    game.setup()

    
    arcade.run() 