import arcade
import random

from Livello2 import Game2

PLAYER_SPEED = 6
PLAYER_HEALT = 10
GRAVITY = 0.7
JUMP_SPEED = 15
DOUBLE_JUMP_SPEED = 15
ENEMY_SPEED = 3
SPAWN_INTERVAL = 4.0
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Game(arcade.View):

    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture("./Immagini/Kingdom_Edge_Background.png")

        self.nemici_uccisi = 0
        self.damage_cooldown = 0
        self.damage_cooldown_max = 60

        # SpriteLists
        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()

        # Player
        self.player = arcade.Sprite("./immagini/Cavaliere_vuoto.png")
        self.player.scale = 0.1
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
        self.dash_speed = 20
        self.dash_cooldown = 10
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
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platforms,
            GRAVITY
        )

        self.total_time = 0

        self.health_text = arcade.Text(
            f"Vita: {self.player.health}",
            20,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

        self.camera = None

    def setup(self):
        self.camera = arcade.Camera2D()

    # INPUT
    def on_key_press(self, key, modifiers):

        # CAMBIO LIVELLO
        if key == arcade.key.N:
            if self.nemici_uccisi >= 10:
                livello2 = Game2()
                livello2.window = self.window
                livello2.setup()
                self.window.show_view(livello2)

        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
            self.player.direction = -1
            self.player.scale_x = -0.1

        if key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED
            self.player.direction = 1
            self.player.scale_x = 0.1

        if key in (arcade.key.SPACE, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
                self.can_double_jump = True
            elif self.can_double_jump:
                self.player.change_y = DOUBLE_JUMP_SPEED
                self.can_double_jump = False

        # DASH
        if key == arcade.key.RSHIFT and self.dash_cooldown == 0:
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = self.dash_cooldown_max

        # ATTACCO
        if key == arcade.key.ENTER and self.attack_cooldown == 0:

            attack = arcade.SpriteSolidColor(50, 30, arcade.color.WHITE)

            attack.center_x = self.player.center_x + self.player.direction * 30
            attack.center_y = self.player.center_y

            self.attack_list.append(attack)
            self.attack_cooldown = 15

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    # UPDATE
    def on_update(self, delta_time):

        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.can_double_jump = True

        # DASH LOGIC
        if self.is_dashing:
            self.player.center_x += self.player.direction * self.dash_speed
            self.dash_timer -= 1

            if self.dash_timer <= 0:
                self.is_dashing = False

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attack_list.clear()

        # SPAWN NEMICI
        self.total_time += delta_time
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.total_time > SPAWN_INTERVAL and self.nemici_uccisi < 10:

            self.total_time = 0

            enemy = arcade.Sprite("./Immagini/B_Vengefly.png")
            enemy.scale = 0.50

            enemy.center_x = random.randint(0, SCREEN_WIDTH)
            enemy.center_y = random.randint(100, SCREEN_HEIGHT - 100)

            self.enemies_list.append(enemy)

        # MOVIMENTO NEMICI
        for enemy in self.enemies_list:

            dx = self.player.center_x - enemy.center_x
            dy = self.player.center_y - enemy.center_y

            if dx != 0:
                enemy.center_x += ENEMY_SPEED * (dx / abs(dx))

            if dy != 0:
                enemy.center_y += (ENEMY_SPEED / 2) * (dy / abs(dy))

                if arcade.check_for_collision(self.player, enemy):
                    if self.damage_cooldown == 0:
                        self.player.health -= 1
                        self.player.center_x -= self.player.direction * 100
                        self.damage_cooldown = self.damage_cooldown_max
                    
        # ATTACCHI
        for atk in self.attack_list:

            hits = arcade.check_for_collision_with_list(atk,self.enemies_list)

            for enemy in hits:
                self.nemici_uccisi += 1
                enemy.remove_from_sprite_lists()

        self.health_text.text = f"Vita: {self.player.health}"

        # GAME OVER SICURO
        if self.player.health <= 0:

            self.player.remove_from_sprite_lists()

            for enemy in self.enemies_list:
                enemy.remove_from_sprite_lists()

            for atk in self.attack_list:
                atk.remove_from_sprite_lists()

    def on_draw(self):

        self.window.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

        self.camera.use()

        self.platforms.draw()
        self.enemies_list.draw()
        self.player_list.draw()
        self.attack_list.draw()

        self.health_text.draw()