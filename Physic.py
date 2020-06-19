import pygame as pg


class PhysicObject:
    def __init__(self, x, y):
        self.location = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)

    def updateLocation(self):
        self.velocity.x += self.acceleration.x
        self.velocity.y += self.acceleration.y

        self.location.x += self.velocity.x
        self.location.y += self.velocity.y

        self.acceleration.x = 0
        self.acceleration.y = 0

    def applyForce(self, force):
        self.acceleration.x += force.x
        self.acceleration.y += force.y
