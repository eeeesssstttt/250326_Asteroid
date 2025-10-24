from if3_game.engine import init
from game import RESOLUTION, AsteroidGame


init([RESOLUTION[0], RESOLUTION[1]], "ASTEROIDS")


game = AsteroidGame()


game.run()