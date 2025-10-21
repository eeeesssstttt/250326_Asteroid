from if3_game.engine import Game, Sprite, Layer, Text
from pyglet.window import key
from math import radians, cos, sin
from random import randint


# fix reset
# design ship sprite
# change text font
# game states would be nice

RESOLUTION = [800, 600]
CENTER = [RESOLUTION[0]/2, RESOLUTION[1]/2]

start_position_x = randint(0, 800)
start_position_y = randint(0, 600)

while start_position_x > 200 and start_position_x < 600:
    start_position_x = randint(0, 800)

while start_position_y > 200 and start_position_y < 400:
    start_position_y = randint(0, 600)

asteroid_start_position = start_position_x, start_position_y

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
        self.background_layer.add(Sprite("images/background_test.jpg"))

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
            asteroid = Asteroid(asteroid_start_position)
            self.asteroids.append(asteroid)
            self.game_layer.add(asteroid)

    # Creating reset method to set ship data back to base and remove all remaining asteroids

    def reset(self):
        self.ship.lives = 3
        self.ship.speed = 0, 0
        self.ship.rotation = 0
        self.ship.rotation_speed = 0
        self.ship.opacity = 255
        for asteroid in self.asteroids:
            asteroid.destroy()
        self.asteroids = []
        for asteroid in range(3): 
            asteroid = Asteroid(asteroid_start_position)
            self.asteroids.append(asteroid)
            self.game_layer.add(asteroid)
        self.ui_layer.gameover_title.text = ""
        self.ui_layer.gameover_subtitle.text = ""
        self.ui_layer.gameover_subtitle2.text = ""

class UILayer(Layer):

    def __init__(self, ship):
        super().__init__()

        # Storing the ship's reference

        self.ship = ship

        # Creating life sprites to display at the top left of the screen

        self.life_sprites = []
        position = [10, 575]
        for life in range(self.ship.lives):
            x, y = position
            x += 19 * life
            life_sprite = Sprite("images/pixel_life.png", (x,y))
            self.life_sprites.append(life_sprite)
            self.add(life_sprite)

        # Creating gameover text boxes and text

        self.gameover_title = Text("", (CENTER[0], CENTER[1] + 50), 20, color = (255, 0, 0), anchor = "center")
        self.gameover_subtitle = Text("", (CENTER[0], CENTER[1] - 10), 15, color = (255, 0, 0), anchor = "center")
        self.gameover_subtitle2 = Text("", (CENTER[0], CENTER[1] - 30), 15, color = (255, 0, 0), anchor = "center")
        self.add(self.gameover_title, self.gameover_subtitle, self.gameover_subtitle2)

    def update(self, dt):
        super().update(dt)

        # Displaying life sprites corresponding to ship lives

        for n, life_sprite in enumerate(self.life_sprites):
            if n < self.ship.lives:
                self.life_sprites[n].opacity = 255
            else:
                self.life_sprites[n].opacity = 0

        # Checking ship lives to display gameover text

        if self.ship.lives == 0:
            self.gameover_title.text = "GAME OVER"
            self.gameover_subtitle.text = "IN SPACE NO ONE CAN HEAR YOUR SHIP EXPLODE..."
            self.gameover_subtitle2.text = "PRESS SPACE TO TRY AGAIN"
        else:
            self.gameover_title.text = ""
            self.gameover_subtitle.text = ""
            self.gameover_subtitle2.text = ""
        
    # Setting up game restart on space bar press

    def on_key_press(self, k, modifiers):

        if self.ship.lives <= 0 and k == key.SPACE:
            self.game.reset()
            return


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

        # Removes asteroid from list of asteroids

        for asteroid in self.layer.game.asteroids:
            if self.id == asteroid.id:
                self.layer.game.asteroids.remove(asteroid)


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
        super().__init__("images/handdrawn_ship.png", position, (32, 64), collision_shape = "circle")
        self.lives = 3
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
                self.cooldown = 0.25
                self.shoot()
            else:
                self.cooldown -= dt

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
            self.shooting = True

    def on_key_release(self, k, modifiers):

        if k == key.UP:
            self.acceleration = 0

        if k == key.RIGHT:
            self.rotation_speed -= 200

        if k == key.LEFT:
            self.rotation_speed += 200

        if k == key.SPACE:
            self.shooting = False

    def destroy(self):
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