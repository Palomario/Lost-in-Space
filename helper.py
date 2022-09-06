import pygame

pygame.init()

size = {"width": 800, "height": 750}
screen = pygame.display.set_mode((size["width"],size["height"]))

pygame.display.set_caption("Helper")
clock = pygame.time.Clock()
while True:
    screen.fill([255,255,255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    


    clock.tick(70)
    pygame.display.update()