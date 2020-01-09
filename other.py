import arcade
from arcade.gui import *

background = arcade.load_texture("forest_for_hunting.png")


class StopButton(TextButton):
    def __init__(self, x=0, y=0, width=150, height=80, text="Stop", theme=None):
        super().__init__(x, y, width, height, text, theme=theme, font_color=arcade.color.BLACK)
        # self.game = game
        # self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            arcade.unschedule(on_draw)
            self.pressed = False


def draw_background(background):
    # break_point = SCREEN_HEIGHT*(1/3)
    # arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, break_point, arcade.color.SKY_BLUE)
    # arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, break_point, 0, arcade.color.FOREST_GREEN)
    arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, background)
    def set_button_textures():
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        a = Theme()
        button_theme = a.add_button_textures(normal, hover, clicked, locked)
        return button_theme

    button_theme = set_button_textures()    
    button = StopButton(x=100, y=500, theme=button_theme)
    button.draw()


def draw_wagon(x,y):
    break_point = SCREEN_HEIGHT*(1/3)
    arcade.draw_arc_filled((SCREEN_WIDTH-70+x), (break_point-60+y), 30, 30, arcade.color.WHITE, 0, 90)    
    arcade.draw_arc_filled((SCREEN_WIDTH-130+x), (break_point-60+y), 30, 30, arcade.color.WHITE, 90, 180)    
    arcade.draw_lrtb_rectangle_filled((SCREEN_WIDTH-130+x), (SCREEN_WIDTH-70+x), (break_point-30), (break_point-60), arcade.color.WHITE)
    arcade.draw_lrtb_rectangle_filled((SCREEN_WIDTH-175+x), (SCREEN_WIDTH-40+x), (break_point-60), (break_point-95), arcade.color.BROWN)
    arcade.draw_circle_outline((SCREEN_WIDTH-60+x), (break_point-90+y), 17, arcade.color.DARK_BROWN, 5, 5)
    arcade.draw_circle_outline((SCREEN_WIDTH-145+x), (break_point-90+y), 17, arcade.color.DARK_BROWN, 5, 5)
    arcade.draw_arc_outline(SCREEN_WIDTH-100, SCREEN_HEIGHT-60, 20, 20, arcade.color.BLACK, 0, 90)
    arcade.draw_arc_outline(SCREEN_WIDTH-100, SCREEN_HEIGHT-60, 20, 20, arcade.color.BLACK, 90, 180)
    arcade.draw_arc_outline(SCREEN_WIDTH-60, SCREEN_HEIGHT-60, 20, 20, arcade.color.BLACK, 0, 90)
    arcade.draw_arc_outline(SCREEN_WIDTH-60, SCREEN_HEIGHT-60, 20, 20, arcade.color.BLACK, 90, 180)
    



SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

def on_draw(delta_time):
    """
    Use this function to draw everything to the screen.
    """

    arcade.start_render()

    draw_background(background)
    draw_wagon(on_draw.center_x, 0)
    arcade.draw_text("Hello team!", 600, 450, arcade.color.BLACK, 12)

    on_draw.center_x -= on_draw.delta_x * delta_time

    if on_draw.center_x < -900:
        arcade.finish_render()

on_draw.center_x = 100  # type: ignore # dynamic attribute on function obj  # Initial x position
on_draw.center_y = 50   # type: ignore # dynamic attribute on function obj  # Initial y position
on_draw.delta_x = 115   # type: ignore # dynamic attribute on function obj  # Initial change in x
on_draw.delta_y = 130   # type: ignore # dynamic attribute on function obj  # Initial change in y


def main():
    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Testing")
    arcade.set_background_color(arcade.color.WHITE)
    

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(on_draw, 1 / 80)
    # arcade.unschedule(on_draw)

    # Run the program
    arcade.run()


if __name__ == "__main__":
    main()