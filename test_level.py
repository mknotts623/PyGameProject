import main
import pygame

pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
background = pygame.mixer.Sound("background.wav")
pew = pygame.mixer.Sound("pew.wav")
background.play(-1)

pygame.display.set_caption("Yee")
screen = pygame.display.set_mode((main.screen_width, main.screen_height))

clock =pygame.time.Clock()

player1 = main.Player(30, 30, 1)
player2 = main.Player(900, 30, 2)

wall = main.Wall(100, 100, 20, 120)
wall2 = main.Wall(500, 30, 20, 140)
wall3 = main.Wall(500, 400, 20, 130)
wall4 = main.Wall(275, 375, 20, 75)

laser = main.Laser(480, 0, 2, 600, main.RED)
splitter = main.Splitter(400, 275)
splitter = main.Splitter(600, 120)
top_border = main. Wall(0, 0, main.screen_width, 1, main.BLACK)
bottom_border = main.Wall(0, main.screen_height, main.screen_width, 1, main.BLACK)
left_border = main.Wall(0, 0, 1, main.screen_height, main.BLACK)
right_border = main.Wall(main.screen_width, 0, 10, main.screen_height, main.BLACK)


running = True

pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False
pressed_a = False
pressed_d = False
pressed_w = False
pressed_s = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pressed_a = True
            elif event.key == pygame.K_d:
                pressed_d = True
            elif event.key == pygame.K_w:
                pressed_w = True
            elif event.key == pygame.K_s:
                pressed_s = True
            if event.key == pygame.K_SPACE:
                fire = main.Fire(player1.rect.x + 30, player1.rect.y + 30, main.vel[0], 0, 1)
                pew.play()

            if event.key == pygame.K_LEFT:
                pressed_left = True
            elif event.key == pygame.K_RIGHT:
                pressed_right = True
            elif event.key == pygame.K_UP:
                pressed_up = True
            elif event.key == pygame.K_DOWN:
                pressed_down = True
            if event.key == pygame.K_RCTRL:
                fire = main.Fire(player2.rect.x - 10, player2.rect.y + 20, -main.vel[0], 0, 2)
                pew.play()

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_a:
                pressed_a = False
            elif event.key == pygame.K_d:
                pressed_d = False
            elif event.key == pygame.K_w:
                pressed_w = False
            elif event.key == pygame.K_s:
                pressed_s = False

            if event.key == pygame.K_LEFT:
                pressed_left = False
            elif event.key == pygame.K_RIGHT:
                pressed_right = False
            elif event.key == pygame.K_UP:
                pressed_up = False
            elif event.key == pygame.K_DOWN:
                pressed_down = False

    if pressed_a:
        player1.move(-3, 0)
    elif pressed_d:
        player1.move(3, 0)
    elif pressed_w:
        player1.move(0, -3)
    elif pressed_s:
        player1.move(0, 3)

    if pressed_left:
        player2.move(-3, 0)
    elif pressed_right:
        player2.move(3, 0)
    elif pressed_up:
        player2.move(0, -3)
    elif pressed_down:
        player2.move(0, 3)

    screen.fill(main.BLACK)

    for wall in main.walls:
        pygame.draw.rect(screen, wall.color, wall.rect, 1)

    for fire in main.fires:
        fire.move()
        fire.hitwall()
        fire.hitfire()
        fire.hitplayer()
        pygame.draw.rect(screen, fire.color, fire.rect, 1)

    screen.blit(player1.image, (player1.rect.x, player1.rect.y))
    screen.blit(player2.image, (player2.rect.x, player2.rect.y))
    pygame.display.flip()

    clock.tick(40)
