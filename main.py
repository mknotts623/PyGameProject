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
vel = [13, 13]
players = []

screen_width = 960
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()

class Player():

    def __init__(self, x, y, player):

        players.append(self)

        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.walls = None

        self.change_x = 0
        self.change_y = 0

        self.player = player


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

    def passable(self):
        return False

class Laser(Wall):

    def __init__(self, x, y, width, height, color=GREEN ):
        Wall.__init__(self, x, y, width, height, color= GREEN)

    def passable(self):
        return True

class Splitter(Wall):

    def __init__(self, x, y, width=30, height=30, color=GRAY):
        Wall.__init__(self, x, y, width, height, color=GRAY)

    def passable(self):
        return False

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
        fires.append(self)

        fires.append(self)
        self.image = pygame.Surface([12, 12])

        self.player = player
        if player == 1:
            self.color = RED
        else:
            self.color = BLUE
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = dx
        self.change_y = dy

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

            pygame.draw.rect(screen, self.color, self.rect, 2)

            self.rect.x += self.change_x
            self.rect.y += self.change_y
