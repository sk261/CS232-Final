import math
import random
from app.pixel import Pixel

class WorldManager:
    def __init__(self):
        self.pixels = {} # Dictionary or 3d array, haven't decided which
        self._squareSize = 100
    
    def getView(self, x, y, width, height):
        # Returns the view, all the pixels the player sees on their screen
        blocks = self._getBlocksBetweenCoords(x-width/2, height-width/2, x+width/2, height+width/2)
        ret = []
        for block in blocks:
            for pixel in pixels[block[0]][block[1]]:
                if (pixel.position[0] >= x-width/2 and pixel.position[0] <= x+width/2 and 
                    pixel.position[1] >= y-height/2 and pixel.position[1] <= y+height/2):
                    ret.append([pixel.position[0], pixel.position[1], pixel.colour, pixel.motionBlur])
        return ret

    def tick(self):
        # Ticks all the pixels inside of it and coordinates them proper
        for x in self.pixels.keys():
            for y in self.pixels[x].keys():
                # TODO: fix garbage lines of code
                _i = list(range(len(self.pixels[x][y])))
                _i.reverse()
                for i in _i:
                    pixel = self.pixels[x][y][i]
                    if not pixel.ticked:
                        pixel.tick()
                        # Move pixel to new block if it moved beyond current block
                        _x, _y = self._getBlockByCoords(pixel.position[0], pixel.position[1])
                        if x != _x or y != _y:
                            self.pixels[x][y].pop(i)
                            self.pixels[_x][_y].append(pixel)
                            

    def generate(self, width, height):
        # Set the width and height to blocks
        self.width = math.ceil(width / self._squareSize)
        self.height = math.ceil(height / self._squareSize)

        # Create empty blocks
        for x in range(-math.floor(self.width / 2), math.floor(self.width / 2)):
            for y in range(-math.floor(self.height / 2), math.floor(self.height / 2)):
                if not x in self.pixels:
                    self.pixels[x] = {}
                self.pixels[x][y] = []
        
        # Fill the blocks with Pixels (more pixels as we get farther from the core)

        for x in self.pixels.keys():
            for y in self.pixels[x].keys():
                
                # Set density based on distance from origin
                # > 3 is full (100%), 0 is empty (0%)
                dist = math.sqrt(x**2 + y**2)
                density = min(1, dist/3)
                if density == 0: continue

                # Trend of square (for the sake of simplicity, RGB is either Red, Green, or Blue)
                RGB = random.randint(0, 2)
                if RGB == 0: RGB = [255, 0, 0]
                elif RGB == 1: RGB = [0, 255, 0]
                else: RGB = [0, 0, 255]

                print("Generating pixels")
                # Well, this is disgusting.
                # TODO: Fix this. No need for this many pixels.
                # Maybe just reduce the world size for the sake of testing?
                for _x in range(math.floor((x-.5)*self._squareSize), math.floor((x+.5)*self._squareSize)):
                    for _y in range(math.floor((y-.5)*self._squareSize), math.floor((y+.5)*self._squareSize)):
                        print(str(_x) + ", " + str(_y))
                        if random.randint(0,math.floor(100*density)) > 10: # 10% empty rate? Sure.
                            self.pixels[x][y].append(Pixel(_x, _y, RGB[0], RGB[1], RGB[2]))
                
    def _getBlockByCoords(x, y):
        _x = math.floor(x / self._squareSize + .5)
        _y = math.floor(y / self._squareSize + .5)
        return (_x, _y)
    
    def _getBlocksBetweenCoords(x1, y1, x2, y2):
        ret = []
        _x1, _y1 = self._getBlockByCoords(x1, y1)
        _x2, _y2 = self._getBlockByCoords(x2, y2)
        for x in range(_x1, _x2+1):
            for y in range(_y1, _y2+1):
                if x in self.pixels:
                    if y in self.pixels[x]:
                        ret.append([x, y])
        return ret
        
    # Create a force object, which has mass, and applies the gravitational pull of surrounding objects to it.
    def force(self, x, y, strength):
        # Force = Constant * Mass 1 (strength) * Mass 2 (pixel mass) / (distance^2)
        constant = 10**-10
        # Minimum mass is 1
        # Minimum static friction is 1
        # Maximum distance based on this: d = sqrt(C*S)
        maxDist = math.sqrt(constant*strength)
        bounds = [[x - maxDist, x + maxDist], [y - maxDist, y + maxDist]]
        blocks = _getBlocksBetweenCoords(bounds[0][0], bounds[1][0], bounds[0][1], bounds[1][1])

        # Go into each block and get effect on pixel
        for block in blocks:
            for pixel in self._pixels[block[0], block[1]]:
                # Effect pixel
                _x = pixel.position[0]
                _y = pixel.position[1]
                dist = math.sqrt((x-_x)**2 + (y-_y)**2)
                if dist < maxDist:
                    Fx = pixel.mass * strength * constant / (x-_x)**2
                    Fy = pixel.mass * strength * constant / (x-_x)**2
                    pixel.applyForce(Fx, Fy)



        
