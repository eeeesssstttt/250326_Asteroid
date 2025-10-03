from if3_game.engine import Game, Sprite, Layer, Text
from pyglet.window import key
from math import radians, cos, sin
from random import randint

RESOLUTION = [800, 600]
CENTER = [RESOLUTION[0]/2, RESOLUTION[1]/2]

start_position_x = randint(0, 800)
start_position_y = randint(0, 600)

while start_position_x > 200 and start_position_x < 600:
    start_position_x = randint(0, 800)

while start_position_y > 200 and start_position_y < 400:
    start_position_y = randint(0, 600)

asteroid_start_position = start_position_x, start_position_y


class AsteroidGame(Game):

    def __init__(self):
        super().__init__()

        self.background_layer = Layer()
        self.background_layer.add(Sprite("images/background_test.jpg"))

        self.game_layer = Layer()

        # for asteroid in range(3): 
        #     asteroid = Asteroid(asteroid_start_position)
        #     self.game_layer.add(asteroid)

        self.ship = Ship(CENTER)

        # self.game_layer.add(self.ship)

        self.ui_layer = UILayer(self.ship)

        self.add(self.background_layer, self.game_layer, self.ui_layer)

        self.asteroids = []

        self.initialize()


    def initialize(self):

        for asteroid in self.asteroids:
            asteroid.level = 1
            asteroid.destroy()

        self.asteroids = []

        self.ship = Ship(CENTER)

        self.game_layer.add(self.ship)
        self.ui_layer.ship = self.ship

        for asteroid in range(3): 
            asteroid = Asteroid(asteroid_start_position)
            self.game_layer.add(asteroid)
            self.asteroids.append(asteroid)




class UILayer(Layer):

    def __init__(self, ship):
        super().__init__()

        self.ship = ship
        position = [10, 575]

        self.life_sprites = []
        for life in range(self.ship.hp):
            x, y = position
            x += 19 * life
            life_sprite = Sprite("images/life.png", (x,y))
            self.add(life_sprite)
            self.life_sprites.append(life_sprite)

        # self.life_text = Text(f"life: {self.ship.hp}", (10, 565), 20)
        # self.add(self.life_text)


        self.game_over = Text("", (CENTER[0], CENTER[1] + 50), 50, color = (255, 255, 255), anchor = "center")
        self.flavor_text = Text("", (CENTER[0], CENTER[1] - 50), 15, color = (255, 255, 255), anchor = "center")
        self.add(self.game_over, self.flavor_text)

    def update(self, dt):
        super().update(dt)

        # for n in range(len(self.life_sprites)):

        for n, life_sprite in enumerate(self.life_sprites):
            if n < self.ship.hp:
                self.life_sprites[n].opacity = 255
            else:
                self.life_sprites[n].opacity = 0

        # self.life_text.text = f"Life: {self.ship.hp}"

        if self.ship.hp == 0:
            self.game_over = Text("GAME OVER", (CENTER[0], CENTER[1] + 50), 50, color = (255, 255, 255), anchor = "center")
            self.flavor_text = Text("In space, no one can hear your ship explode...", (CENTER[0], CENTER[1] - 50), 15, color = (255, 255, 255), anchor = "center")
            self.add(self.game_over, self.flavor_text)
        else:
            self.game_over.text = ""
            self.flavor_text.text = ""
        
    def on_key_press(self, k, modifiers):
        if self.ship.hp <= 0 and k == key.SPACE:
            self.game.initialize()


class SpaceElement(Sprite):

    def __init__(self, image, position, anchor, initial_speed = [0, 0], collision_shape = "rectangle"):
        
        super().__init__(image, position, anchor = anchor, collision_shape = collision_shape)
        self.speed = initial_speed

    def update(self, dt):
        super().update(dt)

        x, y = self.position
        speed_x, speed_y = self.speed

        x += speed_x * dt
        y += speed_y * dt

        rect = self.get_rect()

        if rect.left > RESOLUTION[0]:
            x = -self.anchor[0]
        elif rect.right < 0:
            x = RESOLUTION[0] + self.anchor[0]

        if rect.bottom > RESOLUTION[1]:
            y = -self.anchor[1]
        elif rect.top < 0:
            y = RESOLUTION[1] + self.anchor[1]

        self.position = x, y


class Asteroid(SpaceElement):

    def __init__(self, position, level = 3):

        self.stats = {
            3: {
            "image": "images/asteroid128.png",
            "anchor": (64,64), 
            "rotation_speed": randint(-20, 20)
            }, 
            2: {
            "image": "images/asteroid64.png",
            "anchor": (32,32),
            "rotation_speed": randint(-40, 40)
            }, 
            1: {
            "image": "images/asteroid32.png",
            "anchor": (16, 16),
            "rotation_speed": randint(-80, 80)
            }
        }

        self.level = level

        image = self.stats[self.level]["image"]
        anchor = self.stats[self.level]["anchor"]

        initial_speed = randint(-200, 200), randint(-200, 200)
    
        super().__init__(image, position, anchor, initial_speed, "circle")
        self.rotation_speed = self.stats[self.level]["rotation_speed"]
        self.rotation = 0
        
    def update(self, dt):
        super().update(dt)

        self.rotation += self.rotation_speed * dt

    def pop_asteroid(self):

        level = self.level - 1

        if level <= 0:
            return
        
        speed_x = randint(-30, 30)
        speed_y = randint(-20, 20)
        initial_speed = speed_x, speed_y

        rotation_speed = randint(-20, 20)

        for _ in range(3):
            asteroid = Asteroid(self.position, level)
            self.layer.add(asteroid)
            self.layer.game.asteroids.append(asteroid)

    def on_collision(self, other):
        super().on_collision(other)
        if isinstance(other, Ship):
            other.destroy()

        if isinstance(other, Bullet):
            self.pop_asteroid()


class Ship(SpaceElement):

    def __init__(self, position):
        super().__init__("images/ship2.png", position, (32, 64), collision_shape = "circle")
        self.hp = 1
        self.rotation_speed = 0
        self.acceleration = 0
        # self.shooting = False
        # self.cooldown = 0.0
        self.invincible = 0.0

    def update(self, dt):

        speed_x, speed_y = self.speed

        angle = radians(-self.rotation + 90)
        accel_x = cos(angle) * self.acceleration
        accel_y = sin(angle) * self.acceleration

        speed_x += accel_x * dt
        speed_y += accel_y * dt
        self.speed = speed_x, speed_y 

        super().update(dt)
        self.rotation += self.rotation_speed * dt

        # if self.shooting:
        #     if self.cooldown <= 0.0:
        #         self.shoot()
        #         self.cooldown = 0.25
        #         self.shoot()
        #     else:
        #         self.cooldown -= dt

        if self.invincible > 0.0:
            self.invincible -= dt
            self.opacity = 125
        else:
            self.opacity = 255


    def shoot(self):

        bullet_speed = 500
        angle = radians(-self.rotation + 90)

        speed_x = cos(angle) * bullet_speed
        speed_y = sin(angle) * bullet_speed

        bullet = Bullet(self.position, [speed_x, speed_y], self.rotation)

        self.layer.add(bullet)

    def on_key_press(self, k, modifiers):

        if k == key.UP:
            self.acceleration = 1000

        if k == key.RIGHT:
            self.rotation_speed += 200

        if k == key.LEFT:
            self.rotation_speed -= 200

        if k == key.SPACE:
            self.shoot()
            # self.shooting = True

    def on_key_release(self, k, modifiers):

        if k == key.UP:
            self.acceleration = 0

        if k == key.RIGHT:
            self.rotation_speed -= 200

        if k == key.LEFT:
            self.rotation_speed += 200

    def destroy(self):
        if self.invincible <= 0.0:
            self.hp -= 1

            if self.hp <= 0:
                super().destroy()
                # self.layer.remove_all_items()
                # game_over = Text("GAME OVER", (CENTER[0], CENTER[1] + 50), 50, color = (255, 255, 255), anchor = "center")
                # flavor_text = Text("In space, no one can hear your ship explode...", (CENTER[0], CENTER[1] - 50), 25, color = (255, 255, 255), anchor = "center")
                # self.layer.add(game_over, flavor_text)

            else:
                self.invincible = 3


class Bullet(SpaceElement):

    def __init__(self, position, initial_speed, rotation):
        super().__init__("images/bullet2.png", position, (8, 8), initial_speed, collision_shape="circle")
        self.rotation = rotation
        self.start_position = position
        self.lifetime = 3.0

    def on_collision(self, other):
        super().on_collision(other)
        if isinstance(other, Asteroid):
            other.destroy()
            self.destroy()


    def update(self, dt):
        super().update(dt)
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.destroy()