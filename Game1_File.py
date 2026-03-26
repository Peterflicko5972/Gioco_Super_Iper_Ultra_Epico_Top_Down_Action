import arcade
import random

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
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

# file GameView.py
class GameView(arcade.View):
    def setup(self):
        self.player = Player()
        self.camera = arcade.Camera2D()
        # ... setup del gioco ...

    def on_draw(self):
        self.clear()
        # disegna la scena

    def on_update(self, delta_time: float):
        self.player.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            pausa = PauseView(self)  # passiamo noi stessi per poter tornare in futuro, allo stato del gioco che avviene in questo momento
            self.window.show_view(pausa)

# file MyGame.py
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(960, 540, "Giochino bellino")
        menu = MenuView()
        self.show_view(menu)  # la prima view da mostrare


def main():
    window = MyGame()
    arcade.run()

main()
