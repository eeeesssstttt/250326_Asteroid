import asyncio
import numpy
from engine import init
from game import RESOLUTION, AsteroidGame

# /// script 
# dependencies = [ "numpy", 
#  "asyncio",
#  "cocos",
#  "game.py", 
#  "engine.py",
#  "pyglet",
#  "pathlib",
#  "math",
#  "random",
#  "egl"
# ]
# ///

async def main():

    init([RESOLUTION[0], RESOLUTION[1]], "ASTEROIDS")


    game = AsteroidGame()


    game.run()

    # await game.run_until_complete(asyncio.gather(main()))

    # await asyncio.run(asyncio.gather(main()))

    # return await asyncio.gather(main())

    await asyncio.sleep(0)

asyncio.run(main())