from if3_game.engine import Game, Sprite, Layer
from pyglet.window import key
from math import radians, cos, sin
from random import randint

RESOLUTION = (800, 600)
CENTER = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)

# Most sprites -- not the life sprites or certain text sprites -- will have a central anchor, 
# which we'll specify individually because the default anchor (0, 0) is on the bottom left corner.

class AsteroidGame(Game):

    def __init__(self):

        super().__init__()

        # Creating the gamestate and setting it to start

        self.gamestate = "start"

        # Creating the player's game element: the ship

        ship_start_position = CENTER[0], CENTER[1] - 20
        self.ship = Ship(ship_start_position)

        # Creating the background layer

        self.background_layer = Layer()
        self.background_layer.add(Sprite("images/pixel_background.png"))

        # Creating the game layer, giving it access to the ship

        self.game_layer = GameLayer(self.ship)

        # Creating the UI layer, giving it access to the ship

        self.ui_layer = UILayer(self.ship)

        # Adding all layers to the game

        self.add(self.background_layer, self.game_layer, self.ui_layer)

    def reset(self):

    # Tells the GameLayer to reset its items -- this is called by the UILayer when the player hits space on controls, victory or gameover screens

        self.game_layer.reset()

class GameLayer(Layer):

    def __init__(self, ship):

        super().__init__()

        # Storing the ship's reference

        self.ship = ship

        # Setting the ship to display on this layer

        self.add(self.ship)

        # Creating a list of asteroids

        self.asteroids = []

        # Creating a list of bullets

        self.bullets = []

        # Creating the first batch of asteroids

        self.generate_first_asteroids()

    def update(self, dt):

        super().update(dt)

        # When there are no more asteroids, victory is declared

        if self.game.gamestate == "play":

            if len(self.asteroids) == 0:
                self.game.gamestate = "victory"
        
    def random_position(self):

    # Creates a random start position away from the center of the screen
        
        position_x = randint(0, 800)
        position_y = randint(0, 600)

        while position_x > 200 and position_x < 600:
            position_x = randint(0, 800)

        while position_y > 200 and position_y < 400:
            position_y = randint(0, 600)

        start_position = position_x, position_y
        return start_position

    def generate_asteroid_batch(self, amount, position = [0, 0], level = 3, tag = ""):

    # Generates a batch of asteroids in a given or random position

        for asteroid in range(amount): 

            if tag == "random_position":
                position = self.random_position()

            # Creating the asteroid sprite

            asteroid = Asteroid(position, level)

            # Adding each asteroid to a list of asteroids

            self.asteroids.append(asteroid)

            # Adding each asteroid to the layer

            self.add(asteroid)

    def generate_first_asteroids(self):

    # Generates the first three asteroids in a random position away from the center of the screen

        self.generate_asteroid_batch(3, tag = "random_position")

    def reset(self):

    # Resets the GameLayer's items

        # Destroying any asteroids on screen -- destroying them removes them from the asteroid list

        for asteroid in self.asteroids[:]:
            asteroid.destroy()

        # Destroying any bullets on screen and clearing the bullet list

        for bullet in self.bullets[:]:
            bullet.destroy()

        self.bullets = []

        # Resetting the ship to default

        self.ship.position = self.ship.default_position
        self.ship.speed = self.ship.default_speed
        self.ship.acceleration = self.ship.default_acceleration
        self.ship.rotation = self.ship.default_rotation
        self.ship.rotation_speed = self.ship.default_rotation_speed
        self.ship.lives = self.ship.default_lives
        self.ship.invincibility = self.ship.default_invincibility
        self.ship.starting_shot_prevention = self.ship.default_starting_shot_prevention
        self.ship.cooldown = self.ship.default_cooldown
        self.ship.opacity = 255

        # Generating the first 3 asteroids

        self.generate_first_asteroids()

        # Setting the gamestate to play

        self.game.gamestate = "play"
        
class UILayer(Layer):

    def __init__(self, ship):

        super().__init__()

        # Storing the ship's reference

        self.ship = ship

        # Creating life sprites to display at the top left of the screen

        self.life_sprites = []
        position = (10, 575)
        for life in range(self.ship.max_lives):
            x, y = position
            x += 19 * life
            life_sprite = Sprite("images/pixel_life.png", (x, y))
            self.life_sprites.append(life_sprite)
            self.add(life_sprite)

        # Creating start, controls, victory and gameover text sprites

        self.start_title = Sprite("images/asteroids.png", (CENTER[0], CENTER[1] + 18), anchor = (138, 22))
        self.start_title.opacity = 0
        self.start_subtitle = Sprite("images/press_space_to_play.png", (CENTER[0], CENTER[1] - 20), anchor = (140, 20))
        self.start_subtitle.opacity = 0

        self.controls1 = Sprite("images/to_accelerate.png", (CENTER[0], CENTER[1] + 26), anchor = (114, 0))
        self.controls1.opacity = 0
        self.controls2 = Sprite("images/to_turn.png", (CENTER[0], CENTER[1] + 0), anchor = (110, 10))
        self.controls2.opacity = 0
        self.controls3 = Sprite("images/space_to_shoot.png", (CENTER[0], CENTER[1] - 26), anchor = (102, 20))
        self.controls3.opacity = 0

        self.victory_subtitle1 = Sprite("images/you_re_safe_now.png", (CENTER[0], CENTER[1] + 38), anchor = (122, 0))
        self.victory_subtitle1.opacity = 0
        self.victory_title = Sprite("images/victory.png", (CENTER[0], CENTER[1]), anchor = (114, 22))
        self.victory_title.opacity = 0
        self.victory_subtitle2 = Sprite("images/press_space_to_play_again.png", (CENTER[0], CENTER[1] - 38), anchor = (178, 20))
        self.victory_subtitle2.opacity = 0

        self.gameover_subtitle1 = Sprite("images/in_space_no_one_can_hear_your_ship_explode.png", (CENTER[0], CENTER[1] + 20), anchor = (166, 0))
        self.gameover_subtitle1.opacity = 0
        self.gameover_title = Sprite("images/gameover.png", (CENTER[0], CENTER[1] - 18), anchor = (152, 22))
        self.gameover_title.opacity = 0
        self.gameover_subtitle2 = Sprite("images/press_space_to_try_again.png", (CENTER[0], CENTER[1] - 56), anchor = (170, 20))
        self.gameover_subtitle2.opacity = 0

        # Setting the sprites to display on this layer

        self.add(self.start_title, self.start_subtitle, 
                 self.controls1, self.controls2, self.controls3,
                 self.victory_subtitle1, self.victory_title, self.victory_subtitle2, 
                 self.gameover_title, self.gameover_subtitle1, self.gameover_subtitle2)

    def update(self, dt):

        super().update(dt)

        # Displaying ship's remaining lives

        for index, _ in enumerate(self.life_sprites):

            if (index < self.ship.lives
                and (self.game.gamestate == "play"
                    or self.game.gamestate == "victory")):
                self.life_sprites[index].opacity = 255
                
            else:
                self.life_sprites[index].opacity = 0

        # Depending on the gamestate, displaying the corresponding text sprites

        if self.game.gamestate == "start":

            self.start_title.opacity = 255
            self.start_subtitle.opacity = 255

        elif self.game.gamestate == "controls":

            self.start_title.opacity = 0
            self.start_subtitle.opacity = 0

            self.controls1.opacity = 255
            self.controls2.opacity = 255
            self.controls3.opacity = 255

        elif self.game.gamestate == "victory":

            self.victory_subtitle1.opacity = 255
            self.victory_title.opacity = 255
            self.victory_subtitle2.opacity = 255

            self.gameover_title.opacity = 0
            self.gameover_subtitle1.opacity = 0
            self.gameover_subtitle2.opacity = 0

        elif self.game.gamestate == "gameover":

            self.victory_subtitle1.opacity = 0
            self.victory_title.opacity = 0
            self.victory_subtitle2.opacity = 0

            self.gameover_title.opacity = 255
            self.gameover_subtitle1.opacity = 255
            self.gameover_subtitle2.opacity = 255

        else:

            self.start_title.opacity = 0
            self.start_subtitle.opacity = 0

            self.controls1.opacity = 0
            self.controls2.opacity = 0
            self.controls3.opacity = 0

            self.victory_subtitle1.opacity = 0
            self.victory_title.opacity = 0
            self.victory_subtitle2.opacity = 0

            self.gameover_title.opacity = 0
            self.gameover_subtitle1.opacity = 0
            self.gameover_subtitle2.opacity = 0

    def on_key_press(self, k, modifiers):

    # Sets up the game to move to the next screen or reset on space bar press

        if k == key.SPACE:

            if self.game.gamestate == "start":
                self.game.gamestate = "controls"

            elif (self.game.gamestate == "controls" 
                or self.game.gamestate == "gameover" 
                or self.game.gamestate == "victory"):
                self.game.reset()

class SpaceElement(Sprite):

    def __init__(self, image, position, anchor, initial_speed = [0, 0], collision_shape = "rectangle"):

    # Creates the sprite at a given position

        super().__init__(image, position, anchor = anchor, collision_shape = collision_shape)

        self.speed = initial_speed

    def update(self, dt):

    # Updates the sprite's position and keeps it onscreen

        super().update(dt)

        # Generating the sprite's next position according to its speed

        x, y = self.position
        speed_x, speed_y = self.speed

        x += speed_x * dt
        y += speed_y * dt

        # Getting the sprite's bounding box to check its position on the screen

        rect = self.get_rect()

        # Checking whether the sprite is still onscreen
        # If not, setting its position to the opposite side of the screen, just offscreen

        if rect.left > RESOLUTION[0]:
            x = - self.image_anchor_x

        elif rect.right < 0:
            x = RESOLUTION[0] + self.image_anchor_x

        if rect.bottom > RESOLUTION[1]:
            y = - self.image_anchor_y

        elif rect.top < 0:
            y = RESOLUTION[1] + self.image_anchor_y

        # Applying the Sprite's position

        self.position = x, y

class Asteroid(SpaceElement):

    def __init__(self, position, level = 3):

        # Defining the image for the asteroid Sprite depending on its level, with a random rotation speed

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
    
        # Creating the asteroid sprite

        super().__init__(image, position, anchor, initial_speed, "circle")

        self.rotation_speed = self.stats[self.level]["rotation_speed"]
        self.rotation = 0
        
    def update(self, dt):

        # Updating the asteroid's position and rotation

        super().update(dt)

        self.rotation += self.rotation_speed * dt

    def on_collision(self, other):

        super().on_collision(other)

        # Hitting a bullet will destroy the asteroid and generate smaller asteroids, if possible.

        if isinstance(other, Bullet):

            self.generate_smaller_asteroids(3)
            self.destroy()

    def destroy(self):
        
        # Destroying the asteroid sprite

        super().destroy()

        # Removing the asteroid from the asteroid list   

        for asteroid in self.layer.asteroids[:]:
            if self == asteroid:
                self.layer.asteroids.remove(asteroid)

    def generate_smaller_asteroids(self, amount):

    # Creates a batch of smaller asteroids from a destroyed asteroid's position and level

        # Determining the new asteroids' level

        level = self.level - 1

        # No new asteroids if their level is too low

        if level <= 0:
            return
        
        # Creating the batch of new asteroids

        self.layer.generate_asteroid_batch(amount, self.position, level)

class Ship(SpaceElement):

    def __init__(self, position):

        # Creating the ship sprite

        super().__init__("images/pixel_ship.png", position, (32, 64), collision_shape = "circle")

        # Configuring all the ship's default variable values and some working variables

        self.max_lives = 6

        self.default_lives = 3
        self.lives = self.default_lives
        
        self.default_position = position

        self.default_speed = self.speed

        self.default_acceleration = 10
        self.acceleration = self.default_acceleration

        self.default_rotation = self.rotation

        self.default_rotation_speed = 0
        self.rotation_speed = self.default_rotation_speed

        self.default_starting_shot_prevention = 0.1
        self.starting_shot_prevention = self.default_starting_shot_prevention

        self.bullet_anchor = (8, 8)

        self.shooting = False

        self.default_cooldown = 0.0
        self.cooldown = self.default_cooldown

        self.default_invincibility = 0.0
        self.invincibility = self.default_invincibility

    def update(self, dt):

        # Getting the ship's speed

        speed_x, speed_y = self.speed

        # Getting the ship's angle -- accounting for the fact that, in our engine, angles start at (0, 1) in orthogonal coordinates and increase clockwise,
        # whereas in traditional mathematics, angles start at (0, 0) and increase counterclockwise
        # We're storing it because we also use the angle to determine bullet trajectory

        self.angle = radians(-self.rotation + 90)

        # If the ship accelerates, it accelerates in the direction it is facing and its speed increases accordingly

        accel_x = cos(self.angle) * self.acceleration
        accel_y = sin(self.angle) * self.acceleration

        speed_x += accel_x * dt
        speed_y += accel_y * dt
        self.speed = speed_x, speed_y 

        super().update(dt)

        # Preparing the ship's rotation to update in the next frame 
        # -- to emulate the slight lag between the rotation of a ship and the change in the direction of its acceleration
        
        self.rotation += self.rotation_speed * dt

        # Preventing a byproduct bullet when hitting space to start or reset the game

        if self.layer.game.gamestate == "play":
            self.starting_shot_prevention -= dt

        # Managing the cooldown between shots

        if self.shooting:

            if self.cooldown <= 0.0:
                self.shoot()
                self.cooldown = 0.15

            else:
                self.cooldown -= dt

        # Managing the ship's invincibility and corresponding transparency

        if (self.layer.game.gamestate == "play" 
            or self.layer.game.gamestate == "victory"):

            if self.invincibility > 0.0:
                self.invincibility -= dt
                self.opacity = 125

            else:
                self.opacity = 255

        # On start, controls and gamover screens, the ship is invisible

        if (self.layer.game.gamestate == "start" 
            or self.layer.game.gamestate == "controls"
            or self.layer.game.gamestate == "gameover"):
            self.opacity = 0

    def on_key_press(self, k, modifiers):

        if (self.layer.game.gamestate == "play" 
            or self.layer.game.gamestate == "victory"):

            # Arrow keys trigger forward movement and rotation

            if k == key.UP:
                self.acceleration = 400

            if k == key.RIGHT:
                self.rotation_speed += 200

            if k == key.LEFT:
                self.rotation_speed -= 200

            # Space bar triggers shooting

            if k == key.SPACE:

                self.shoot()
                self.shooting = True

    def on_key_release(self, k, modifiers):
        
        if (self.layer.game.gamestate == "play" 
            or self.layer.game.gamestate == "victory"):

            if k == key.UP:
                self.acceleration = 0

            if k == key.RIGHT:
                self.rotation_speed -= 200

            if k == key.LEFT:
                self.rotation_speed += 200

        if k == key.SPACE:
            self.shooting = False
            self.cooldown = 0.0

    def on_collision(self, other):

        super().on_collision(other)

        if isinstance(other, Asteroid):

            if (self.layer.game.gamestate == "play"):

                if self.invincibility <= 0.0:
                        
                        # When not invincible, hitting an asteroid will cause the ship to lose a life

                        self.lives -= 1

                        if self.lives > 0:

                            # If the ship has any lives left, it will be temporarily invincible

                            self.invincibility = 3

                        else:
                        
                        # When all lives are lost, the game is over

                            self.layer.game.gamestate = "gameover"

    def shoot(self):

    # Creates a bullet that is projected forwards, faster than the ship
        
        if ((self.layer.game.gamestate == "play" 
                or self.layer.game.gamestate == "victory") 
            and self.starting_shot_prevention <= 0.0):

            velocity = 500

            # Determining the bullet's speed based on the ship's angle

            speed_x = cos(self.angle) * velocity
            speed_y = sin(self.angle) * velocity

            # Using the angle and the height of the ship sprite to position the bullet in front of the ship

            bullet_position_x = self.position[0] + (self.image_anchor_y + self.bullet_anchor[1]) * cos(self.angle)
            bullet_position_y = self.position[1] + (self.image_anchor_y + self.bullet_anchor[1]) * sin(self.angle)

            bullet_position = bullet_position_x, bullet_position_y

            # Creating the bullet sprite

            bullet = Bullet(bullet_position, self.bullet_anchor, [speed_x, speed_y], self.rotation)

            # Adding the bullet to the list of bullets

            self.layer.bullets.append(bullet)

            # Adding the bullet to the layer
            
            self.layer.add(bullet)

class Bullet(SpaceElement):

    def __init__(self, position, anchor, initial_speed, rotation):

    # Creates a bullet, with a set lifetime

        super().__init__("images/pixel_bullet.png", position, anchor, initial_speed, collision_shape="circle")
        self.rotation = rotation
        self.lifetime = 3.0

    def update(self, dt):

    # Updates the bullet's position and destroys it once its lifetime has expired

        super().update(dt)
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.destroy()

    def on_collision(self, other):

    # On collision, the bullet is destroyed

        super().on_collision(other)
        if isinstance(other, Asteroid):
            self.destroy()
    
    def destroy(self):

    # Destroys the bullet sprite

        super().destroy()
