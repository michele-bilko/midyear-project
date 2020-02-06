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
        if key == up:
            self.player_sprite.change_y = playerMovementSpeed
        elif key == left:
            self.player_sprite.change_x = -playerMovementSpeed
        elif key == right:
            self.player_sprite.change_x = playerMovementSpeed

    def on_key_release(self, key, modifiers):
        if key == up:
            self.player_sprite.change_y = 0
        elif key == left:
            self.player_sprite.change_x = 0
        elif key == right:
            self.player_sprite.change_x = 0

    def on_draw(self):
        arcade.start_render()
        self.playerList.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()