import pygame
import sys
#add comments later


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (67, 139, 211)
RED = (217, 73, 0)
GRAY = (135, 143, 155)
GREEN = (51, 232, 27)

walls = []
fires = []
vel = [20, 20]
players = []

screen_width = 960
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()

class Player():

    def __init__(self, x, y, player):

        self.player = player

        if self.player == 1:
            self.image = pygame.image.load("cowboixcropped.png")
        elif self.player == 2:
            self.image = pygame.image.load("aliencropped.png")

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.walls = None

        self.change_x = 0
        self.change_y = 0

        players.append(self)


    def move(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

class Wall():

    def __init__(self, x, y, width, height, color=BLUE):
        walls.append(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.color = color

class Laser(Wall):

    def __init__(self, x, y, width, height, color=GREEN ):
        Wall.__init__(self, x, y, width, height, color= GREEN)

class Splitter(Wall):

    def __init__(self, x, y, width=30, height=30, color=GRAY):
        Wall.__init__(self, x, y, width, height, color=GRAY)

    def split(self, dx, dy):
        if dx > 0:
            Fire(self.rect.x + 35, self.rect.y, vel[0], vel[1], 1)
            Fire(self.rect.x + 35, self.rect.y, vel[0], 0, 1)
            Fire(self.rect.x + 35, self.rect.y, vel[0], -vel[1], 1)
        if dx < 0:
            Fire(self.rect.x - 35, self.rect.y, -vel[0], vel[1], 2)
            Fire(self.rect.x - 35, self.rect.y, -vel[0], 0, 2)
            Fire(self.rect.x- 35, self.rect.y, -vel[0], -vel[1], 2)


class Fire(pygame.sprite.Sprite):

    def __init__(self, x, y, dx, dy, player):

        self.image = pygame.Surface([15, 15])

        self.player = player
        if player == 1:
            self.color = RED
        else:
            self.color = BLUE

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = dx
        self.change_y = dy

        fires.append(self)

    def hitwall(self):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if type(wall) == Laser:
                    print("Tripped Laser!")
                elif type(wall) == Splitter:
                    wall.split(self.change_x, self.change_y)
                    print("SPLIIIIT!")
                    fires.remove(self)
                elif type(wall) == Wall:
                    fires.remove(self)
                    print("Hit Wall!")


    def hitfire(self):
        for fire in fires:
            if self == fire:
                pass
            else:
                if self.rect.colliderect(fire.rect):
                    fires.remove(self)
                    fires.remove(fire)
                    print("COLLISION!")
        else:
            return False

    def hitplayer(self):
        for player in players:
            if self.rect.colliderect(player.rect):
                print("Player " + str(player.player) + " loses!")
                sys.exit()



    def move(self):

            self.rect.x += self.change_x
            self.rect.y += self.change_y
