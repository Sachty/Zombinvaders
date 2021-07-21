import pygame
ancho_pantalla = 800
alto_pantalla = 500

screen = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("BOTONES MARCA BRUH")
flechaiz = pygame.image.load("flecha izquierda.jpeg").convert_alpha()
flechaiz = pygame.transform.scale(flechaiz,(50,50))
flechader = pygame.image.load("flecha derecha.jpeg").convert_alpha()
flechader = pygame.transform.scale(flechader,(50,50))
boton_inicio = pygame.image.load("start.jpeg").convert_alpha()
boton_inicio = pygame.transform.scale(boton_inicio,(200,100))
boton_exit = pygame.image.load("exit.jpeg").convert_alpha()
boton_exit = pygame.transform.scale(boton_exit,(200,100))
boton_highscore = pygame.image.load("highscore.jpeg").convert_alpha()
boton_highscore = pygame.transform.scale(boton_highscore,(200,100))
boton_inicio2 = pygame.image.load("start2.jpeg").convert_alpha()
boton_inicio2 = pygame.transform.scale(boton_inicio2,(200,100))
boton_highscore2 = pygame.image.load("highscore2.jpeg").convert_alpha()
boton_highscore2 = pygame.transform.scale(boton_highscore2,(200,100))
boton_exit2 = pygame.image.load("exit2.jpeg").convert_alpha()
boton_exit2 = pygame.transform.scale(boton_exit2,(200,100))
cursor = pygame.mouse.get_pos()

def submenu():
    salir = True
    while salir:
        screen.fill((255,255,255))
        flechaiz.draw()
        flechader.draw()
        if exit1.draw():
            quit()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quit()
        pygame.display.update()

class Boton():
    def __init__(self,x,y,imagen,imagen2):
        self.imagen = imagen
        self.imagen2 = imagen2
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        self.rect2 = self.imagen2.get_rect()
        self.rect2.topleft = (x, y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            screen.blit(self.imagen2,(self.rect2.x,self.rect2.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0 :
                self.clicked = False
        else:
            screen.blit(self.imagen,(self.rect.x, self.rect.y))
        return action
inicio = Boton(300,100,boton_inicio,boton_inicio2)
exit = Boton(300,350,boton_exit,boton_exit2)
highscore = Boton(300,225,boton_highscore,boton_highscore2)
exit1 = Boton(300,350,boton_exit,boton_exit2)
flechaiz = Boton(250,365,flechaiz,flechaiz)
flechader = Boton(495,365,flechader,flechader)
loop = True
while loop:
    screen.fill((202,228,241))
    if inicio.draw():
        submenu()
    if exit.draw():
        quit()
        print("exit")
    highscore.draw()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            loop = False
    pygame.display.update()