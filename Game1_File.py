import arcade
import random

from File_Gioco_Finale import Game

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# file MenuView.py
class MenuView(arcade.View): # MenuView è una View... Ricordiamoci delle sottoclassi!
    def on_draw(self):
        self.clear()
        arcade.draw_text("IL MIO GIOCO", 480, 350,
                         arcade.color.WHITE, font_size=48, anchor_x="center")
        arcade.draw_text("Premi INVIO per iniziare", 480, 250,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RETURN:
            # Passiamo alla schermata di gioco
            game = Game()
            game.window = self.window
            game.setup()
            self.window.show_view(game) 

# file GameView.py
# class GameView(arcade.View):
#     def setup(self):
#         self.player = Player()
#         self.camera = arcade.Camera2D()
#         # ... setup del nnngioco ...

#     def on_draw(self):
#         self.clear()
#         # disegna la scena

#     def on_update(self, delta_time: float):
#         self.player.update()

#     def on_key_press(self, key, modifiers):
#         if key == arcade.key.ESCAPE:
#             pausa = PauseView(self)  # passiamo noi stessi per poter tornare in futuro, allo stato del gioco che avviene in questo momento
#             self.window.show_view(pausa)

# file MyGame.py
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