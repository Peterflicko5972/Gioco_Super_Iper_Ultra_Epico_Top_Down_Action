import arcade
import random

PLAYER_SPEED = 7
PLAYER_HEALT = 5
GRAVITY = 0.7
JUMP_SPEED = 15
DOUBLE_JUMP_SPEED = 15
ENEMY_SPEED = 1.5
SPAWN_INTERVAL = 5.0

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Mini Hollow Knight", fullscreen=True)
        self.background = arcade.load_texture("./Immagini/Kingdom_Edge_Background.png")


        # SpriteLists
        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()

        # Player
        self.player = arcade.Sprite("./immagini/Cavaliere_vuoto.png")
        self.player.scale_x = 0.1
        self.player.scale_y = 0.1
        self.player.center_x = 100
        self.player.center_y = 300
        self.player.health = 5
        self.player.direction = 1
        self.can_double_jump = True
        self.attack_cooldown = 0
        self.player_list.append(self.player)

        # Dash
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_duration = 10
        self.dash_speed = 25
        self.dash_cooldown = 0
        self.dash_cooldown_max = 30

        # Piattaforme
        platforms_data = [
            (960, 20, 1920, 40),
            (400, 200, 200, 20),
            (800, 400, 200, 20),
            (1400, 600, 200, 20),
        ]
        for x, y, w, h in platforms_data:
            plat = arcade.SpriteSolidColor(w, h, arcade.color.GRAY)
            plat.center_x = x
            plat.center_y = y
            self.platforms.append(plat)

        # Gravità
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platforms, GRAVITY)

        # Timer nemici
        self.total_time = 0

        # Camera
        self.camera = arcade.Camera2D()

        # HUD testo
        self.health_text = arcade.Text(
            f"Vita: {self.player.health}",
            20,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )
        arcade.draw_text(f"Vita: {self.player.health}", SCREEN_HEIGHT/2, SCREEN_WIDTH/2)

    # Input
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
            self.player.direction = -1
            self.player.scale_x = -0.1

        if key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED
            self.player.direction = 1
            self.player.scale_x = 0.1

        if key == arcade.key.SPACE or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
                self.can_double_jump = True
            elif self.can_double_jump:
                self.player.change_y = DOUBLE_JUMP_SPEED
                self.can_double_jump = False

        # Dash
        if key == arcade.key.RSHIFT:
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = self.dash_cooldown_max

        # Attacco
        if key == arcade.key.ENTER and self.attack_cooldown == 0:
            self.attack = arcade.SpriteSolidColor(50, 30, arcade.color.WHITE)
            if modifiers & arcade.key.W:
                self.attack.center_x = self.player.center_x
                self.attack.center_y = self.player.center_y + 50
            elif modifiers & arcade.key.S:
                self.attack.center_x = self.player.center_x
                self.attack.center_y = self.player.center_y - 50
            else:
                self.attack.center_x = self.player.center_x + self.player.direction * 30
                self.attack.center_y = self.player.center_y
            self.attack_list.append(self.attack)
            self.attack_cooldown = 15

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.A, arcade.key.D]:
            self.player.change_x = 0

    # Update
    def on_update(self, delta_time):
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.can_double_jump = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attack_list = arcade.SpriteList()

        # Spawn nemici
        self.total_time += delta_time
        if self.total_time > SPAWN_INTERVAL and len(self.enemies_list) < 10:
            self.total_time = 0
            self.enemy = arcade.Sprite("./Immagini/B_Vengefly.png")
            self.enemy.scale = 0.55
            self.enemy.center_x = random.randint(0, SCREEN_WIDTH)
            self.enemy.center_y = random.randint(100, SCREEN_HEIGHT - 100)
            self.enemies_list.append(self.enemy)

        # Nemici inseguono player
        for self.enemy in self.enemies_list:
            dx = self.player.center_x - self.enemy.center_x
            dy = self.player.center_y - self.enemy.center_y
            if dx != 0:
                self.enemy.center_x += ENEMY_SPEED * (dx / abs(dx))
            if dy != 0:
                self.enemy.center_y += (ENEMY_SPEED/2) * (dy / abs(dy))

            if arcade.check_for_collision(self.player, self.enemy):
                self.player.health -= 1
                self.player.center_x -= self.player.direction * 100

        # Attacchi vs nemici
        for atk in self.attack_list:
            hits = arcade.check_for_collision_with_list(atk, self.enemies_list)
            for self.enemy in hits:
                self.enemy.remove_from_sprite_lists()

        #Immunità post danno
        #arcade.check_for_collision_with_lists(self.player_list, self.enemies_list)

        # Aggiorna HUD
        self.health_text.text = f"Vita: {self.player.health}"

        # Game over
        if self.player.health <= 0:
            self.player.remove_from_sprite_lists()
            self.enemy.remove_from_sprite_lists()
            self.attack.remove_from_sprite_lists()

        print(self.player.center_x)
        print(self.player.center_y)

    # Draw
    def on_draw(self):
        self.clear()
        # Disegna lo sfondo
        arcade.draw_texture_rect(self.background, arcade.XYWH(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH,SCREEN_HEIGHT))

        # Disegna mondo con camera

        self.camera.use()

        self.platforms.draw()
        self.enemies_list.draw()
        self.player_list.draw()
        self.attack_list.draw()

        # HUD fisso
        self.health_text.draw()

game = Game()
arcade.run()