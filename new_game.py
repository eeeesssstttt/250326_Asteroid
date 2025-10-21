from if3_game.engine import Game, Sprite, Layer, Text
from pyglet.window import key
from math import radians, cos, sin
from random import randint


RESOLUTION = [800, 600]
CENTER = [RESOLUTION[0]/2, RESOLUTION[1]/2]

# Giving asteroids a random start position away from center of screen

def random_asteroid_start_position():
    start_position_x = randint(0, 800)
    start_position_y = randint(0, 600)

    while start_position_x > 200 and start_position_x < 600:
        start_position_x = randint(0, 800)

    while start_position_y > 200 and start_position_y < 400:
        start_position_y = randint(0, 600)

    asteroid_start_position = start_position_x, start_position_y
    return asteroid_start_position

# Giving asteroids an id to remove them from list on destroy()

asteroid_number = -1

def next_asteroid():
    global asteroid_number
    asteroid_number += 1
    return asteroid_number

class AsteroidGame(Game):

    def __init__(self):
        super().__init__()

        # Creating a gamestate variable to control game behavior depending on context

        gamestate = "startscreen"

        # Creating the player's game element: the ship

        self.ship = Ship(CENTER)

        # Creating the background layer

        self.background_layer = Layer()
        self.background_layer.add(Sprite("images/pixel_background.png"))

        # Creating the game layer and adding the ship

        self.game_layer = Layer()
        self.game_layer.add(self.ship)

        # Creating the I layer, giving it access to the ship

        self.ui_layer = UILayer(self.ship)

        # Adding all layers to the game

        self.add(self.background_layer, self.game_layer, self.ui_layer)

        # Creating a list of asteroids

        self.asteroids = []

        # Creating new batch of asteroids and adding them to the game layer

        for asteroid in range(3): 
            asteroid = Asteroid(random_asteroid_start_position())
            self.asteroids.append(asteroid)
            self.game_layer.add(asteroid)

    # Creating reset method to set ship data back to base and remove all remaining asteroids

    def reset(self):
        self.ship.position = CENTER
        self.ship.lives = 3
        self.ship.speed = 0, 0
        self.ship.rotation = 0
        self.ship.rotation_speed = 0
        self.ship.opacity = 255
        for asteroid in self.asteroids:
            asteroid.destroy()
        self.asteroids = []
        for asteroid in range(3): 
            asteroid = Asteroid(random_asteroid_start_position())
            self.asteroids.append(asteroid)
            self.game_layer.add(asteroid)
        print("reset")

class UILayer(Layer):

    def __init__(self, ship):
        super().__init__()

        # Storing the ship's reference

        self.ship = ship

        # Creating life sprites to display at the top left of the screen

        self.life_sprites = []
        position = [10, 575]
        if self.ship.lives < self.ship.max_lives + 1:
            for life in range(self.ship.lives):
                x, y = position
                x += 19 * life
                life_sprite = Sprite("images/pixel_life.png", (x,y))
                self.life_sprites.append(life_sprite)
                self.add(life_sprite)
        else:
            for life in range(self.ship.max_lives):
                x, y = position
                x += 19 * life
                life_sprite = Sprite("images/pixel_life.png", (x,y))
                self.life_sprites.append(life_sprite)
                self.add(life_sprite)


        # Creating gameover text boxes and text

        self.start_title = Sprite("images/asteroids.png", (CENTER[0], CENTER[1] + 30), anchor = (138, 22))
        self.start_title.opacity = 0
        self.start_subtitle = Sprite("images/press_space_to_play.png", (CENTER[0], CENTER[1] -10), anchor = (140, 10))
        self.start_subtitle.opacity = 0
        self.gameover_subtitle1 = Sprite("images/in_space_no_one_can_hear_your_ship_explode.png", (CENTER[0], CENTER[1] + 84), anchor = (166,24))
        self.gameover_subtitle1.opacity = 0
        self.gameover_title = Sprite("images/gameover.png", (CENTER[0], CENTER[1] - 6), anchor = (152, 22))
        self.gameover_title.opacity = 0
        self.gameover_subtitle2 = Sprite("images/press_space_to_try_again.png", (CENTER[0], CENTER[1] - 82), anchor = (170, 10))
        self.gameover_subtitle2.opacity = 0
        self.add(self.start_title, self.start_subtitle, self.gameover_title, self.gameover_subtitle1, self.gameover_subtitle2)

    def update(self, dt):
        super().update(dt)

        # Displaying life sprites corresponding to ship lives

        for n, life_sprite in enumerate(self.life_sprites):
            if n < self.ship.lives:
                self.life_sprites[n].opacity = 255
            else:
                self.life_sprites[n].opacity = 0

        # Checking ship lives to display gameover text

        if self.ship.lives == self.ship.max_lives + 1:
            self.ship.opacity = 0
            self.start_title.opacity = 255
            self.start_subtitle.opacity = 255
            self.gameover_title.opacity = 0
            self.gameover_subtitle1.opacity = 0
            self.gameover_subtitle2.opacity = 0
        elif self.ship.lives == 0:
            self.start_title.opacity = 0
            self.start_subtitle.opacity = 0
            self.gameover_title.opacity = 255
            self.gameover_subtitle1.opacity = 255
            self.gameover_subtitle2.opacity = 255
        else:
            self.start_title.opacity = 0
            self.start_subtitle.opacity = 0
            self.gameover_title.opacity = 0
            self.gameover_subtitle1.opacity = 0
            self.gameover_subtitle2.opacity = 0
        
    # Setting up game restart on space bar press

    def on_key_press(self, k, modifiers):

        if k == key.SPACE:
            if self.ship.lives <= 0:
                self.game.reset()
            if self.ship.lives == self.ship.max_lives + 1:
                self.ship.lives -= 1
                self.game.reset()

class SpaceElement(Sprite):

    def __init__(self, image, position, anchor, initial_speed = [0, 0], collision_shape = "rectangle"):
        # Creating a Sprite with provided image, position, anchor, speed and collision box shape

        super().__init__(image, position, anchor = anchor, collision_shape = collision_shape)
        self.speed = initial_speed

    def update(self, dt):
        super().update(dt)

        # Generating the sprite's next position according to its speed

        x, y = self.position
        speed_x, speed_y = self.speed

        x += speed_x * dt
        y += speed_y * dt

        # Getting the sprite's bounding box to check its position in the screen

        rect = self.get_rect()

        # Checking whether the sprite is still onscreen. 
        # If not, setting its position to the opposite side of the screen, just offscreen

        if rect.left > RESOLUTION[0]:
            x = -self.anchor[0]
        elif rect.right < 0:
            x = RESOLUTION[0] + self.anchor[0]

        if rect.bottom > RESOLUTION[1]:
            y = -self.anchor[1]
        elif rect.top < 0:
            y = RESOLUTION[1] + self.anchor[1]

        # Applying the Sprite's position

        self.position = x, y

class Asteroid(SpaceElement):

    def __init__(self, position, level = 3):

        # Defining the image for the asteroid Sprite depending on its level, 
        # with a central anchor and a random rotation speed

        self.id = next_asteroid()

        self.stats = {
            3: {
            "image": "images/pixel_asteroid128.png",
            "anchor": (64,64), 
            "rotation_speed": randint(-20, 20)
            }, 
            2: {
            "image": "images/pixel_asteroid64.png",
            "anchor": (32,32),
            "rotation_speed": randint(-40, 40)
            }, 
            1: {
            "image": "images/pixel_asteroid32.png",
            "anchor": (16, 16),
            "rotation_speed": randint(-80, 80)
            }
        }

        self.level = level

        image = self.stats[self.level]["image"]
        anchor = self.stats[self.level]["anchor"]

        # Generating a random initial speed

        initial_speed = randint(-200, 200), randint(-200, 200)
    
        # Creating the asteroid SpaceElement:Sprite with a round collision box 
        # and previously defined initial speed, rotation, image and anchor
        # at the specified position

        super().__init__(image, position, anchor, initial_speed, "circle")
        self.rotation_speed = self.stats[self.level]["rotation_speed"]
        self.rotation = 0
        
    def update(self, dt):
        super().update(dt)

        self.rotation += self.rotation_speed * dt

    def smaller_asteroid_creation(self):
    # Creates a smaller new asteroid from a destroyed asteroid's position and level

        # Defines the new asteroids' level

        level = self.level - 1

        # No new asteroids if their level is <= 0 

        if level <= 0:
            return
        
        # Creates the new smaller asteroid on

        asteroid = Asteroid(self.position, level)
        self.layer.game.asteroids.append(asteroid)
        self.layer.add(asteroid)

    def destroy(self):

        # Destroys this asteroid

        super().destroy()

        # If possible, creates 3 new, smaller asteroids

        for _ in range(3):
            self.smaller_asteroid_creation()        

        self.level -= 1

    def on_collision(self, other):
        super().on_collision(other)
        
        # Hitting an ship will trigger its destruction

        if isinstance(other, Ship):
            other.destroy()

        # Hitting a bullet will trigger destruction and generate smaller asteroids, if possible.

        if isinstance(other, Bullet):

            self.destroy()

class Ship(SpaceElement):

    def __init__(self, position):
        super().__init__("images/pixel_ship.png", position, (32, 64), collision_shape = "circle")
        self.max_lives = 3
        self.lives = self.max_lives + 1
        self.rotation_speed = 0
        self.acceleration = 0
        self.shooting = False
        self.cooldown = 0.0
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

        if self.shooting:
            if self.cooldown <= 0.0:
                self.shoot()
                self.cooldown = 0.15
            else:
                self.cooldown -= dt

        if self.lives == 0:
            self.opacity = 0
        else:
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

        if self.lives < self.max_lives + 1:
            if k == key.UP:
                self.acceleration = 400

            if k == key.RIGHT:
                self.rotation_speed += 200

            if k == key.LEFT:
                self.rotation_speed -= 200

        if k == key.SPACE:
            self.shoot()
            self.shooting = True

    def on_key_release(self, k, modifiers):
        
        if self.lives < self.max_lives + 1:
            if k == key.UP:
                self.acceleration = 0

            if k == key.RIGHT:
                self.rotation_speed -= 200

            if k == key.LEFT:
                self.rotation_speed += 200

            if k == key.SPACE:
                self.shooting = False

    def destroy(self):
        if self.lives < self.max_lives + 1 and self.lives > 0:
            if self.invincible <= 0.0:
                    self.lives -= 1
                    if self.lives < 0:
                        self.opacity = 0
                    else:
                        self.invincible = 3

class Bullet(SpaceElement):

    def __init__(self, position, initial_speed, rotation):
        super().__init__("images/pixel_bullet.png", position, (8, 8), initial_speed, collision_shape="circle")
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