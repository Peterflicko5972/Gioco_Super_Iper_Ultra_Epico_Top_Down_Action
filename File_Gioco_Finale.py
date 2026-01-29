import arcade
import random

class MyGame(arcade.Window):
    
    def __init__(self, width, height, title):
        # Ignorare per il momento
        super().__init__(width, height, title, fullscreen=True, )
        self.player_list = None
        self.player_sprite = None
        self.Owlet=None
        
    
    # Chiamato ad ogni frame. delta_time di solito è 1/60 di secondo. 
    # In questo metodo qui "ridisegnamo" lo schermo
    def on_draw(self):
        # Pulisci lo schermo
        self.clear()
        
        # Disegna le scritte
        arcade.draw_text(
            "Premi SPAZIO, e cambierà colore!",
            10, self.height - 30,
            arcade.color.WHITE, 14
        )
        
        arcade.draw_text(
            f"Dim: {self.rect_size}",
            10, self.height - 55,
            arcade.color.WHITE, 14
        )

        

    # Chiamato ad ogni frame. delta_time di solito è 1/60 di secondo  
    # In questa sezione mettiamo la LOGICA del gioco  
    def on_update(self, delta_time):
        # Aumenta la dimensione del rettangolo
        self.rect_size += 0.5
        
        # Resetta la dimensione se è troppo grande
        if self.rect_size > 200:
            self.rect_size = 50
    
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # Velocità del personaggio
        self.velocita = 4


    def on_update(self, delta_time):
        # Movimento del personaggio
        change_x = 0
        change_y = 0

        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita

        # Applica il movimento
        self.Owlet.center_x += change_x
        self.Owlet.center_y += change_y

        
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def setup(self):
        """ Configura il gioco e inizializza gli oggetti """

       
        self.Owlet = arcade.Sprite("Owlet_Monster.png" , scale=1)
        
        
        self.Owlet.center_x = self.width // 2
        self.Owlet.center_y = self.height // 2
        
        
        self.player_list.append(self.Owlet)

    def on_draw(self):
        self.clear()