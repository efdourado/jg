import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_house():
    glClearColor(0.6, 0.8, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBegin(GL_QUADS)
    # Parede
    glColor3f(0.6, 0.4, 0.2)
    glVertex2f(200, 100); glVertex2f(600, 100); glVertex2f(600, 350); glVertex2f(200, 350)
    # Porta
    glColor3f(0.4, 0.2, 0.0)
    glVertex2f(350, 100); glVertex2f(450, 100); glVertex2f(450, 250); glVertex2f(350, 250)
    # Janela
    glColor3f(0.8, 0.9, 1.0)
    glVertex2f(480, 200); glVertex2f(560, 200); glVertex2f(560, 280); glVertex2f(480, 280)
    glEnd()

    glBegin(GL_TRIANGLES)
    # Telhado
    glColor3f(0.8, 0.2, 0.1)
    glVertex2f(180, 350); glVertex2f(620, 350); glVertex2f(400, 500)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Casa com OpenGL")

    glOrtho(0, 800, 0, 600, -1, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_house()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()