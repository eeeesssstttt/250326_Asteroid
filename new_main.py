from if3_game.engine import Layer, Sprite, Text, init
from new_game import RESOLUTION, CENTER, AsteroidGame


init([RESOLUTION[0], RESOLUTION[1]], "Asteroid")


game = AsteroidGame()


game.run()