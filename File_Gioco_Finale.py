import arcade
import random

PLAYER_SPEED = 5
GRAVITY = 1
JUMP_SPEED = 12
DOUBLE_JUMP_SPEED = 12
ENEMY_SPEED = 1.5
SPAWN_INTERVAL = 2.0

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Mini Hollow Knight", fullscreen=True)
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

        # SpriteLists
        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()

        # Player
        self.player = arcade.SpriteSolidColor(40, 50, arcade.color.WHITE)
        self.player.center_x = 100
        self.player.center_y = 300
        self.player.health = 5
        self.player.direction = 1
        self.can_double_jump = True
        self.attack_cooldown = 0
        self.player_list.append(self.player)

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

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platforms, GRAVITY)

        # Timer nemici
        self.total_time = 0

        # Camera
        self.camera = arcade.Camera2D()
        # self.camera.position = (SCREEN_WIDTH/2,
                                # SCREEN_HEIGHT/2)

        # HUD testo
        self.health_text = arcade.Text(
            f"Vita: {self.player.health}",
            20,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

    # Input
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
            self.player.direction = -1
        if key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED
            self.player.direction = 1
        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
                self.can_double_jump = True
            elif self.can_double_jump:
                self.player.change_y = DOUBLE_JUMP_SPEED
                self.can_double_jump = False

        # Attacco
        if key == arcade.key.ENTER and self.attack_cooldown == 0:
            attack = arcade.SpriteSolidColor(30, 20, arcade.color.WHITE)
            if modifiers & arcade.key.UP:
                attack.center_x = self.player.center_x
                attack.center_y = self.player.center_y + 30
            elif modifiers & arcade.key.DOWN:
                attack.center_x = self.player.center_x
                attack.center_y = self.player.center_y - 30
            else:
                attack.center_x = self.player.center_x + self.player.direction * 30
                attack.center_y = self.player.center_y
            self.attack_list.append(attack)
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
        if self.total_time > SPAWN_INTERVAL:
            self.total_time = 0
            e = arcade.SpriteSolidColor(40, 40, arcade.color.RED)
            e.center_x = random.randint(0, SCREEN_WIDTH)
            e.center_y = random.randint(100, SCREEN_HEIGHT - 100)
            self.enemies_list.append(e)

        # Nemici inseguono player
        for enemy in self.enemies_list:
            dx = self.player.center_x - enemy.center_x
            dy = self.player.center_y - enemy.center_y
            if dx != 0:
                enemy.center_x += ENEMY_SPEED * (dx / abs(dx))
            if dy != 0:
                enemy.center_y += (ENEMY_SPEED/2) * (dy / abs(dy))

            if arcade.check_for_collision(self.player, enemy):
                self.player.health -= 1
                self.player.center_x -= self.player.direction * 30

        # Attacchi vs nemici
        for atk in self.attack_list:
            hits = arcade.check_for_collision_with_list(atk, self.enemies_list)
            for en in hits:
                en.remove_from_sprite_lists()

        # Camera segue player
        # self.camera.position = (self.player.center_x - SCREEN_WIDTH/2,
                                # self.player.center_y - SCREEN_HEIGHT/2)

        # Aggiorna HUD
        self.health_text.text = f"Vita: {self.player.health}"

        # Game over
        if self.player.health <= 0:
            arcade.close_window()

        print(self.player.center_x)
        print(self.player.center_y)

    # Draw
    def on_draw(self):
        self.clear()

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