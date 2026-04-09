import arcade
import random

from Livello1 import Game
from Livello2 import Game2

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# file MenuView.py
class MenuView(arcade.View): # MenuView è una View... Ricordiamoci delle sottoclassi!
    def on_draw(self):
        self.clear()
        arcade.draw_text("Mini Hollow Knight", 650, 400,
                         arcade.color.BLUE_GRAY, font_size=50, anchor_x="center")
        arcade.draw_text("Premi INVIO per iniziare", 650, 325,
                         arcade.color.LIGHT_GRAY, font_size=30, anchor_x="center")
        arcade.draw_text("Movimento: WASD", 650, 250,
                         arcade.color.YELLOW_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Attacco: INVIO", 650, 200,
                         arcade.color.RED_PURPLE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            # Passiamo alla schermata di gioco
            game = Game()
            game.window = self.window
            game.setup()
            self.window.show_view(game)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Mini Hollow Knight", fullscreen=True)
         # la prima view da mostrare
        menu = MenuView()
        menu.window = self
        self.show_view(menu)

def main():
    window = MyGame()
    arcade.run()

main()