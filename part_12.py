import arcade
import os

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

TILE_SIZE = 128
SCALED_TILE_SIZE = TILE_SIZE * SPRITE_SCALING
MAP_HEIGHT = 7
BULLET_SPEED = 7

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.5


def get_map(filename):
    """
    This function loads an array based on a map stored as a list of
    numbers separated by commas.
    """

    # Open the file
    map_file = open(filename)

    # Create an empty list of rows that will hold our map
    map_array = []

    # Read in a line from the file
    for line in map_file:

        # Strip the whitespace, and \n at the end
        line = line.strip()

        # This creates a list by splitting line everywhere there is a comma.
        map_row = line.split(",")

        # The list currently has all the numbers stored as text, and we want it
        # as a number. (e.g. We want 1 not "1"). So loop through and convert
        # to an integer.
        for index, item in enumerate(map_row):
            map_row[index] = int(item)

        # Now that we've completed processing the row, add it to our map array.
        map_array.append(map_row)

    # Done, return the map.
    return map_array


class MyWindow(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        # Call the parent class
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Sprite lists
        self.player_list = None
        self.wall_list = None


        # Set up the player
        self.player_sprite = None
        self.player2_sprite = None

        # Physics engine
        self.physics_engine = None

        # Used for scrolling map
        self.view_left = 0
        self.view_bottom = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("character.png", SPRITE_SCALING)
        self.player2_sprite = arcade.Sprite("character_robot_idle.png", SPRITE_SCALING)

        # Starting position of the player
        self.player_sprite.center_x = 90
        self.player_sprite.center_y = 0
        self.player2_sprite.center_x = 180
        self.player2_sprite.center_x = 0
        self.player_list.append(self.player2_sprite)
        self.player_list.append(self.player_sprite)

        # Get a 2D array made of numbers based on the map
        map_array = get_map("newmap1.csv")

        # Now that we've got the map, loop through and create the sprites
        for row_index in range(len(map_array)):
            for column_index in range(len(map_array[row_index])):

                item = map_array[row_index][column_index]

                # For this map, the numbers represent:
                # -1 = empty
                # 0  = box
                # 1  = grass left edge
                # 2  = grass middle
                # 3  = grass right edge
                wall = arcade.Sprite("images/Platformer Tiles/boxCrate_double.png", SPRITE_SCALING)
                if item == 0:
                    wall = arcade.Sprite("images/Platformer Tiles/boxCrate_double.png", SPRITE_SCALING)
                if item == 1:
                    wall = arcade.Sprite("images/Platformer Tiles/grassLeft.png", SPRITE_SCALING)
                if item == 51:
                    wall = arcade.Sprite("images/Platformer Tiles/grassMid.png", SPRITE_SCALING)
                if item == 3:
                    wall = arcade.Sprite("images/Platformer Tiles/grassRight.png", SPRITE_SCALING)
                if item == 49:
                    wall = arcade.Sprite("images/Platformer Tiles/grassHill_right.png", SPRITE_SCALING)
                if item == 43:
                    wall = arcade.Sprite("images/Platformer Tiles/grassCorner_right.png", SPRITE_SCALING)
                if item == 36:
                    wall = arcade.Sprite("images/Platformer Tiles/grassCenter_round.png", SPRITE_SCALING)
                if item == 48:
                    wall = arcade.Sprite("images/Platformer Tiles/grassHill_left.png", SPRITE_SCALING)
                if item == 42:
                    wall = arcade.Sprite("images/Platformer Tiles/grassCorner_left.png", SPRITE_SCALING)
                if item == 52:
                    wall = arcade.Sprite("images/Platformer Tiles/grassRight.png", SPRITE_SCALING)
                if item == 35:
                    wall = arcade.Sprite("images/Platformer Tiles/grass.png", SPRITE_SCALING)
                if item == 9:
                    wall = arcade.Sprite("images/Platformer Tiles/chain.png", SPRITE_SCALING)
                if item == 127:
                    wall = arcade.Sprite("images/Platformer Tiles/spikes.png", SPRITE_SCALING)
                if item == 107:
                    wall = arcade.Sprite("images/Platformer Tiles/signRight.png", SPRITE_SCALING)
                if item == 106:
                    wall = arcade.Sprite("images/Platformer Tiles/signLeft.png", SPRITE_SCALING)


                if item >= 0:
                    # Calculate where the sprite goes

                    wall.left = column_index * SCALED_TILE_SIZE
                    wall.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE

                    # Add the sprite
                    self.wall_list.append(wall)

        # Create out platformer physics engine with gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        self.physics_engine2 = arcade.PhysicsEnginePlatformer(self.player2_sprite,
                                                              self.wall_list,
                                                              gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """

        if key == arcade.key.UP:
            # This line below is new. It checks to make sure there is a platform underneath
            # the player. Because you can't jump if there isn't ground beneath your feet.
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.W:
            # This line below is new. It checks to make sure there is a platform underneath
            # the player. Because you can't jump if there isn't ground beneath your feet.
            if self.physics_engine.can_jump():
                self.player2_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.A:
            self.player2_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player2_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.player2_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine.update()
        self.physics_engine2.update()

        # --- Manage Scrolling ---

        # Track if we need to change the view port

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        # If we need to scroll, go ahead and do it.
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyWindow()
    window.setup()

    arcade.run()


main()
