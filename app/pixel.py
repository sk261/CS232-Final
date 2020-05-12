import math

class Pixel:
    def __init__(self, x, y, R, G, B):
        self._isMoving = False
        self.ticked = False

        self.staticFriction = 1
        self.kineticFriction = .5
        self.colour = (R,G,B)
        
        self.forces = [0, 0]
        self.velocity = [0, 0]
        self.position = [x, y]
        self.mass = 1

        self._maxBlur = 8
        self.motionBlur = []


    def tick(self):
        # TODO: Perform actions
        force = math.sqrt(self.forces[0]**2 + self.forces[1]**2)
        if force > self.staticFriction and not self._isMoving:
            self._isMoving = True

        if force > self.kineticFriction and self._isMoving:
            # TODO: Correct this formula so the kinetic friction reduces velocity
            # Reduce force by kinetic friction, get Fx and Fy, convert to acceleration, apply to velocity
            Fx = force / (force - self.kineticFriction) * self.forces[0]
            Fy = force / (force - self.kineticFriction) * self.forces[1]
            # a = f/m - m*friction
            self.velocity[0] += Fx / self.mass
            self.velocity[1] += Fy / self.mass

            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]

            self.motionBlur.insert(0, [self.position[0], self.position[1]])

        if len(self.motionBlur) > self._maxBlur:
            self.motionBlur.pop()

        # Check if moving, reset forces.
        if self.velocity[0]**2 + self.velocity[1]**2 == 0:
            self._isMoving = False
        self.forces = [0, 0]
        self.ticked = True

    def applyForce(self, x, y):
        self.forces[0] += x
        self.forces[1] += y