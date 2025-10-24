from if3_game.engine import Layer, Sprite, Text, init
from game import RESOLUTION, CENTER, AsteroidGame


init([RESOLUTION[0], RESOLUTION[1]], "ASTEROIDS")


game = AsteroidGame()


game.run()