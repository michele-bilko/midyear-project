"""
Crossy roads
"""
import arcade
import os

screenWidth = 1000
screenHeight = 650
screenTitle = "Crossy Roads"

tileScaling = 0.5
charScaling = tileScaling * 2
spritePixelSize = 32
gridPixelSize = (spritePixelSize * tileScaling)

playStartX = 500
playStartY = 16

playerMovementSpeed = 5

up = arcade.key.UP
left = arcade.key.LEFT
right = arcade.key.RIGHT

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

        self.playerSprite = None

        self.walk = arcade.load_sound("./sounds/walk.wav")

    def setup(self):
        self.playerList = arcade.SpriteList()
        self.playerSprite = PlayerCharacter()

        self.playerSprite.center_x = playStartX
        self.playerSprite.center_y = playStartY
        self.playerList.append(self.playerSprite)

    def on_key_press(self, key, modifiers):
        global playerMovementSpeed
        diagonal = 0
        if key == up and (key == right or key == left):
            diagonal = 1
        if diagonal == 1:
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

    def on_update(self, delta_time):
        self.playerList.update()
        self.playerList.update_animation()

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()