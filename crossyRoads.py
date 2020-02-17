"""
Crossy roads
"""
import random
import arcade
import os

screenWidth = 1000
screenHeight = 650
screenTitle = "Crossy Roads"

tileScaling = 0.5
charScaling = tileScaling * 2
spritePixelSize = 32
gridPixelSize = int(spritePixelSize * tileScaling)

playStartX = 500
playStartY = 16

playerMovementSpeed = 5

up = arcade.key.UP

left = arcade.key.LEFT
right = arcade.key.RIGHT

VIEWPORT_MARGIN = 40

def loadTexture(filename):
    return arcade.load_texture(filename)

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        main_path = "./sprites/"

        self.texture = loadTexture(f"{main_path}player32.png")


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(screenWidth, screenHeight, screenTitle)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.wallList = None
        self.enemyList = None
        self.playerList = None

        self.playerSprite = None
        self.physicsEngine = None
        self.game_over = False
        self.view_bottom = 0
        self.view_left = 0

        self.walk = arcade.load_sound("./sounds/walk.wav")

    def setup(self):
        self.wallList = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()
        self.playerList = arcade.SpriteList()

        self.playerSprite = PlayerCharacter()
        self.playerSprite.center_x = playStartX
        self.playerSprite.center_y = playStartY
        self.playerList.append(self.playerSprite)

        player = PlayerCharacter()
        player.boundary_right = 1000
        player.boundary_left = 0
        player.boundary_top = 650

        enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)

        enemy.bottom = 160
        enemy.left = 16

        enemy.boundary_right = 1000
        enemy.boundary_left = 0
        enemy.change_x = 7
        self.enemyList.append(enemy)

        enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)

        enemy.bottom = 288
        enemy.left = 16

        enemy.boundary_right = 1000
        enemy.boundary_left = 0
        enemy.change_x = 8
        self.enemyList.append(enemy)

        enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)

        enemy.bottom = 416
        enemy.left = 16

        enemy.boundary_right = 1000
        enemy.boundary_left = 0
        enemy.change_x = 8
        self.enemyList.append(enemy)

        enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)

        enemy.bottom = 416
        enemy.left = 256

        enemy.boundary_right = 1000
        enemy.boundary_left = 0
        enemy.change_x = 9
        self.enemyList.append(enemy)

        enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)

        enemy.bottom = 544
        enemy.left = 16

        enemy.boundary_right = 1000
        enemy.boundary_left = 0
        enemy.change_x = 9
        self.enemyList.append(enemy)

        enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)

        enemy.bottom = 544
        enemy.left = 256

        enemy.boundary_right = 1000
        enemy.boundary_left = 0
        enemy.change_x = 9
        self.enemyList.append(enemy)

        for y in range(200, 1650, 210):
            for x in range(0, 1000, 70):
                # Randomly skip a box so the player can find a way through
                if random.randrange(5) > 1:
                    wall = arcade.Sprite("./sprites/FINALBOX.png", tileScaling)
                    wall.center_x = x
                    wall.center_y = y
                    self.wallList.append(wall)

    def on_key_press(self, key, modifiers):
        global playerMovementSpeed
        if key == up and (key == right or key == left):
            playerMovementSpeed = 0
            self.playerSprite.change_x = playerMovementSpeed
            self.playerSprite.change_y = playerMovementSpeed
        if key == up:
            self.playerSprite.change_y = playerMovementSpeed
            self.playerSprite.change_x = 0
        elif key == left:
            self.playerSprite.change_x = -playerMovementSpeed
            self.playerSprite.change_y = 0
        elif key == right:
            self.playerSprite.change_x = playerMovementSpeed
            self.playerSprite.change_y = 0



    def on_key_release(self, key, modifiers):
        if key == up:
            self.playerSprite.change_y = 0
        elif key == left:
            self.playerSprite.change_x = 0
        elif key == right:
            self.playerSprite.change_x = 0

        elif key == up and key == right:
            self.playerSprite.change_x = 0
            self.playerSprite.change_y = 0
        elif key == up and key == left:
            self.playerSprite.change_x = 0
            self.playerSprite.change_y = 0


    def on_draw(self):
        arcade.start_render()
        self.playerList.draw()
        self.wallList.draw()
        self.enemyList.draw()

    def on_update(self, delta_time):
        self.playerList.update()

        if not self.game_over:
            self.enemyList.update()

            for enemy in self.enemyList:
                if len(arcade.check_for_collision_with_list(enemy, self.wallList)) > 0:
                    enemy.change_x *= -1
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            if len(arcade.check_for_collision_with_list(self.playerSprite, self.enemyList)) > 0:
                self.game_over = True

        # need to implement else: for if game_over


        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.playerSprite.left < left_boundary:
            self.view_left -= left_boundary - self.playerSprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + screenWidth - VIEWPORT_MARGIN
        if self.playerSprite.right > right_boundary:
            self.view_left += self.playerSprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + screenHeight - VIEWPORT_MARGIN
        if self.playerSprite.top > top_boundary:
            self.view_bottom += self.playerSprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.playerSprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.playerSprite.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                screenWidth + self.view_left - 1,
                                self.view_bottom,
                                screenHeight + self.view_bottom - 1)

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()