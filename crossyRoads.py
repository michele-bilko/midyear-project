# Michele Bilko, Rhianna D'Silva, Claire Lee, Lujine
# Crossy Roads game
import random
import arcade
import os

# setting variables and other boring stuff
screenWidth = 1000
screenHeight = 650
screenTitle = "Crossy Roads"

tileScaling = 0.5
charScaling = tileScaling * 2
spritePixelSize = 32
gridPixelSize = int(spritePixelSize * tileScaling)

# starts player off at (500, 16)
playStartX = 500
playStartY = 16

# movement variables
playerMovementSpeed = 6
up = arcade.key.UP
left = arcade.key.LEFT
right = arcade.key.RIGHT

# setting viewport margin for future use
VIEWPORT_MARGIN = 200


def loadTexture(filename):
    # loads file textures
    return arcade.load_texture(filename)


class MenuView(arcade.View):
    # creates starting menu
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", screenWidth/2, screenHeight/2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", screenWidth/2, screenHeight/2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        # loads the texture for the player character
        super().__init__()
        main_path = "./sprites/"

        self.texture = loadTexture(f"{main_path}player32.png")


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    # setting variables and creating lists of walls enemies players etc

        self.game_over = False
        self.view_bottom = 0
        self.view_left = 0
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

        # creates enemies with combination of for loops
        i = 16
        for y in range(240, 1650, 320):
            i += 112
            for x in range(16, i + 1, 112):
                enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)
                enemy.bottom = y
                enemy.left = x
                enemy.boundary_right = 1000
                enemy.boundary_left = 0
                enemy.change_x = 7
                self.enemyList.append(enemy)
        c = 16
        for y in range(400, 1650, 320):
            c += 112
            for x in range(16, c + 1, 112):
                enemy = arcade.Sprite("./sprites/enemy.png", tileScaling)
                enemy.bottom = y
                enemy.left = x
                enemy.boundary_right = 1000
                enemy.boundary_left = 0
                enemy.change_x = 7
                self.enemyList.append(enemy)


        for y in range(160, 1650, 160):
            for x in range(0, 1000, 64):
                # creates obstacles for player
                if random.randrange(5) > 0:
                    wall = arcade.Sprite("./sprites/REALBOX.png", tileScaling)
                    wall.center_x = x
                    wall.center_y = y
                    self.wallList.append(wall)


    def on_key_press(self, key, modifiers):
        # checks if key has been pressed so player can move
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
        # checks if key has been released so player can't move forever
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
        # draws everything
        arcade.start_render()
        arcade.set_background_color(arcade.color.BLACK)
        self.playerList.draw()
        self.wallList.draw()
        self.enemyList.draw()

    def on_update(self, delta_time):

        # updates player list and checks if game is over or not
        self.playerList.update()

        if not self.game_over:
            self.enemyList.update()
        # checks for collision with enemy
            for enemy in self.enemyList:
                if len(arcade.check_for_collision_with_list(enemy, self.wallList)) > 0:
                    enemy.change_x *= -1
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            if len(arcade.check_for_collision_with_list(self.playerSprite, self.enemyList)) > 0:
                self.game_over = True

        # brings to losing screen
        elif self.game_over:
            game_over_view = GameOver()
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)


        changed = False

        # scrolls up
        top_boundary = self.view_bottom + screenHeight - VIEWPORT_MARGIN
        if self.playerSprite.top > top_boundary:
            self.view_bottom += self.playerSprite.top - top_boundary
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # updating viewport
        if changed:
            arcade.set_viewport(self.view_left,
                                screenWidth + self.view_left - 1,
                                self.view_bottom,
                                screenHeight + self.view_bottom - 1)
class GameOver(arcade.View):
    # creates game over screen
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)

def main():
    window = arcade.Window(screenWidth, screenHeight, screenTitle)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()



if __name__ == "__main__":
    main()