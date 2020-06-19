import pygame as pg
import math
import random

pg.init()

WIDTH = 400
HEIGHT = 600

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# image
eggImg = pg.image.load("egg-outline.png")
nestImg = pg.image.load("nest.png")

# var
gravity = pg.math.Vector2(0, 0.1)

# -------------------CLASSES-------------------------------------------------

# Egg class
class Egg:
    def __init__(self):
        self.location = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)

        self.jumpForce = pg.math.Vector2(0, -6)

        self.sticking = False
        self.jumping = True

    def draw(self):
        # pg.draw.rect(window, WHITE, (self.location.x - 10, self.location.y - 15, 20, 30), 2)
        window.blit(eggImg, (self.location.x - 10, self.location.y - 10))
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

    def jump(self):

        self.applyForce(self.jumpForce)
        self.sticking = False
        self.jumping = True

    def checkIfLose(self):
        if self.location.y > 600 - 15:
            global running
            running = False

    def stickTo(self, that):
        self.location.x = that.location.x
        self.location.y = that.location.y - 8

        self.velocity.xy = 0, 0

        self.sticking = True
        self.jumping = False


# Nest class
class Nest:
    def __init__(self, x, y, vel):
        self.location = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2(-vel, 0)

        self.haveEgg = False

    def draw(self):
        # pg.draw.rect(window, WHITE, (self.location.x - self.width / 2, self.location.y - self.height / 2, self.width, self.height), 2)
        window.blit(nestImg, (self.location.x - 15, self.location.y - 15))
    def updateLocation(self):
        self.location.x += self.velocity.x
        self.location.y += self.velocity.y

    def checkBoundBack(self):
        if self.location.x > WIDTH - 15:
            self.location.x = WIDTH - 15
            self.velocity.x *= -1

        elif self.location.x < 15:
            self.location.x = 15
            self.velocity.x *= -1


# All nest class
class NestSystem:
    def __init__(self):
        self.nestList = [Nest(WIDTH / 2, HEIGHT / 2, 1), Nest(WIDTH/2, HEIGHT / 4, 2)]

    def addNest(self):
        lastNest = self.nestList[len(self.nestList) - 1]

        newNest = Nest(random.randrange(20, WIDTH - 20), lastNest.location.y - HEIGHT / 4, random.randrange(-4, 4))
        # newNest = Nest(WIDTH / 2, lastNest.location.y - HEIGHT / 4, 0)

        self.nestList.append(newNest)

    def removeNest(self, limit):
        if len(self.nestList) > limit:
            self.nestList.pop(0)

    def moveDownAll(self):
        for nest in self.nestList:
            nest.location.y += HEIGHT/4

    def updateAll(self):
        for nest in self.nestList:
            nest.updateLocation()

    def drawAll(self):
        for nest in self.nestList:
            nest.draw()

    def checkBoundAll(self):
        for nest in self.nestList:
            nest.checkBoundBack()

# --------------------------------------------------------------------------

# calculate distance between 2 vector
def dist(thing1, thing2):
    return math.sqrt((thing1.x - thing2.x) ** 2 + (thing1.y - thing2.y) ** 2)

# display score
score = -2
# font = pg.font.Font("/Users/anhkhoa/PycharmProjects/Egg_game/rainyhearts.tff", 32)
# text = font.render(score, True, BLACK, WHITE)
# textRect = text.get_rect()
# textRect.center = (0, 0)

# setup game
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Egg Launch")

egg = Egg()
nestSystem = NestSystem()

# the main loop
running = True
while running:

    window.fill(WHITE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and egg.sticking:
                egg.jump()

    # window.blit(text, textRect)

    nestSystem.updateAll()
    nestSystem.checkBoundAll()

    # apply location

    for nest in nestSystem.nestList:
        if dist(egg.location, nest.location) <= 20 and not nest.haveEgg:
            egg.stickTo(nest)

            # global score
            score += 1
            print(score)

            nestSystem.addNest()
            nestSystem.moveDownAll()
            nestSystem.removeNest(5)

            nest.haveEgg = True

        elif nest.haveEgg:
            if egg.sticking:
                egg.stickTo(nest)
        # i dont think this work anymore
            elif egg.jumping:
                egg.applyForce(gravity)
                egg.updateLocation()
                egg.checkIfLose()

    # draw
    nestSystem.drawAll()
    egg.draw()

    pg.display.update()

print("Your score is : ", score)