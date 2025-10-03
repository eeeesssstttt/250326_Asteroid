from if3_game.engine import Sprite, Layer, Text
from pyglet.window import key
from math import radians, cos, sin, sqrt
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

    def update(self, dt):
        super().update(dt)

        damage = len(self.life_sprites) - self.ship.hp
        for life_sprite in self.life_sprites[:damage]:
            life_sprite.opacity = 0

        # self.life_text.text = f"Life: {self.ship.hp}"


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

    def __init__(self, image, position, anchor, initial_speed, rotation_speed = 0):
        super().__init__(image, position, anchor, initial_speed, "circle")
        self.rotation_speed = rotation_speed
        self.rotation = 0
        
    def update(self, dt):
        super().update(dt)
        self.rotation += self.rotation_speed * dt

    def on_collision(self, other):
        super().on_collision(other)
        if isinstance(other, Ship):
            other.destroy()


class LargeAsteroid(Asteroid):

    def __init__(self):

        start_position_x = randint(0, 800)
        start_position_y = randint(0, 600)

        while start_position_x > 200 and start_position_x < 600:
            start_position_x = randint(0, 800)

        while start_position_x > 200 and start_position_x < 400:
            start_position_y = randint(0, 600)

        rotation_speed = randint(-15, 15)

        super().__init__("images/asteroid128.png", (randint(0, 800), randint(0, 600)), (64, 64), (randint(-100, 100), randint(-200, 200)), rotation_speed)

    def destroy(self):

        super().destroy()
        for medium_asteroid in range(3):
                medium_asteroid = MediumAsteroid(self.position)
                self.layer.add(medium_asteroid)


class MediumAsteroid(Asteroid):

    def __init__(self, position):
        rotation_speed = randint(-30, 30)
        super().__init__("images/asteroid64.png", position, (32, 32), (randint(-100, 100), randint(-200, 200)), rotation_speed)

    def destroy(self):
        super().destroy()
        for small_asteroid in range(3):
                small_asteroid = SmallAsteroid(self.position)
                self.layer.add(small_asteroid)


class SmallAsteroid(Asteroid):

    def __init__(self, position):
        rotation_speed = randint(-60, 60)
        super().__init__("images/asteroid32.png", position, (16, 16), (randint(-100, 100), randint(-200, 200)), rotation_speed)


class Ship(SpaceElement):

    def __init__(self, position):
        super().__init__("images/ship2.png", position, (32, 64), collision_shape = "circle")
        self.hp = 3
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