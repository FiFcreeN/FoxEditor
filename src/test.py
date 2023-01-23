import pygame

pygame.init()

screen = pygame.display.set_mode((500, 450))

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()

        if i.type == pygame.MOUSEWHEEL:
            print("Mouse wheel movement detected")

            print(i.x, i.y)

    pygame.display.update()