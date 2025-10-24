from if3_game.engine import Game, Layer, Sprite, Text, init
from game import RESOLUTION, CENTER, UILayer, LargeAsteroid, Ship, asteroid_start_position


init([RESOLUTION[0], RESOLUTION[1]], "Asteroid")

background_layer = Layer()
background_layer.add(Sprite("images/background.jpg"))

game_layer = Layer()

for asteroid in range(3): 
    asteroid = LargeAsteroid()
    game_layer.add(asteroid)

ship = Ship(CENTER)
game_layer.add(ship)

ui_layer = UILayer(ship)

# text = Text("Hi Mom", (0, 0), 25)
# game_layer.add(text)

game = Game()
game.add(background_layer, game_layer, ui_layer)

# game.debug = True ## Shows hitboxes

game.run()