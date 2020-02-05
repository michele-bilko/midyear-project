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
spritePixelSize = 64
gridPixelSize = (spritePixelSize * tileScaling)

playStartX = 500
playStartY = 64

def loadTexture(filename):
    return arcade.load_texture(filename)

class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
      #  main_path = ":midyear-project/sprites"

       # self.texture = loadTexture(f"C:/Users/miche/midyear-project/sprites/player.png")
        self.playerSprite = None


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(screenWidth, screenHeight, screenTitle)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):
        self.playerList = arcade.SpriteList()
        self.playerSprite = PlayerCharacter()

        self.playerSprite.center_x = playStartX
        self.playerSprite.center_y = playStartY
        self.playerList.append(self.playerSprite)

    def on_draw(self):
        arcade.start_render()
        self.playerList.draw()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()