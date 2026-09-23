import random
import math
import pygame
import colorsys
import tkinter
from tkinter import filedialog

pygame.init()


gridw = 720
gridh = 720

screen = pygame.display.set_mode((gridw, gridh + 320))
pygame.display.set_caption("pixlime")
running = True


pixels = {}

mouse = False
mouse2 = False
current_col = pygame.Color(255,255,255)
curhue = 0
curtrans = 100
cursat = 100
curval = 100
oldmpixel = (-1, -1)

def draw_everything():
    for i in range(gridw // 20):
        for j in range(gridh // 20):
            x = i * 20
            y = j * 20
            if (i,j) not in pixels:
                pixels[i,j] = (0,0,0,0)
            pygame.draw.rect(screen,(220,220,220) if (i + j) % 2 == 0 else (180,180,180),(x, y, 20, 20))
            color = pixels[i,j]
            if color[3] > 0:
                tile = pygame.Surface((20,20), pygame.SRCALPHA)
                tile.fill(color)
                screen.blit(tile, (x, y))

def draw_slider():
    for i in range(640):
        part = i/640
        left = (part * 360)
        c = pygame.Color(0,0,0)
        c.hsva = (left, 100,100,100)
        pygame.draw.rect(screen, c, (i,gridh + 20,1,40))
    for i in range(640):
        part = i/640
        left = part
        rgbada = tuple(round(x * 255) for x in colorsys.hsv_to_rgb(curhue / 360, 1, left))
        pygame.draw.rect(screen, rgbada, (i, gridh + 80, 1, 40))
    pygame.draw.rect(screen, (255,255,255), (10,gridh + 160, 100 ,100))
    pygame.draw.rect(screen, (255,255,255), (140,gridh + 160, 100 ,100))
    font = pygame.font.Font(None, 30)
    text = font.render("export", True, (0, 0, 0))
    screen.blit(text, (27, gridh + 200, 100 ,100))
    font2 = pygame.font.Font(None, 30)
    text2 = font2.render("resize", True, (0, 0, 0))
    screen.blit(text2, (160, gridh + 200, 100 ,100))

def exportata():
    sura = pygame.Surface((gridw//20, gridh//20), pygame.SRCALPHA)
    for i in pixels:
        pygame.draw.rect(sura, pixels[i], (i[0] , i[1], 1, 1))
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Image Files", "*.png"), ("All files", "*.*")],
        title="Save File As"
    )
    if file_path:
        pygame.image.save(sura, file_path)


def set_dima():
    global gridw, gridh, screen
    neww = tkinter.simpledialog.askinteger("canvas resize", "width:")
    if neww == None:
        return
    newh = tkinter.simpledialog.askinteger("canvas resize", "height:")
    if newh == None:
        return
    gridw = neww * 20
    gridh = newh * 20
    if gridw < 640:
        screen = pygame.display.set_mode((640, gridh + 320))
    else:
        screen = pygame.display.set_mode((gridw, gridh + 320))
    pixels.clear()
    

def eventhandler(event):
    global mouse, running, current_col, curhue, curtrans, cursat, oldmpixel, mouse2
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse = True
        elif event.button == 3:
            mouse2 = True
        mousepos = pygame.mouse.get_pos()
        if mousepos[1] > gridh + 160 and mousepos[1] < gridh + 260 and mousepos[0] > 10 and mousepos[0] < 110: 
            exportata()
        elif mousepos[1] > gridh + 160 and mousepos[1] < gridh + 260 and mousepos[0] > 140 and mousepos[0] < 240: 
            set_dima()   
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            mouse = False
        elif event.button == 3:
            mouse2 = True
    elif event.type == pygame.MOUSEMOTION and mouse == True:
        mousepos = pygame.mouse.get_pos()
        mpixel = (mousepos[0] // 20, mousepos[1] // 20)
        if mousepos[1] < gridh and oldmpixel != mpixel:
            current_col.hsva = (curhue, cursat, curval, curtrans)
            new = pygame.Surface((1, 1), pygame.SRCALPHA)
            new.fill(current_col)
            old = pygame.Surface((1, 1), pygame.SRCALPHA)
            old.fill(pixels.get(mpixel, (0, 0, 0, 0)))
            old.blit(new, (0, 0))
            pixels[mpixel] = old.get_at((0, 0))
        elif mousepos[1] > gridh + 20 and mousepos[1] < gridh + 40:
            curhue = (mousepos[0] / 640) * 360
            if curhue < 0: curhue = 0
            elif curhue > 360: curhue = 360
            print(curhue)
        elif mousepos[1] > gridh + 80 and mousepos[1] < gridh + 120:
            curtrans = (mousepos[0] / 640) * 100
            if curtrans < 0: curtrans = 0
            elif curtrans > 100: curtrans = 100
            print(curtrans)
        oldmpixel = mpixel
    elif event.type == pygame.MOUSEMOTION and mouse2 == True:
        mousepos = pygame.mouse.get_pos()
        mpixel = (mousepos[0] // 20, mousepos[1] // 20)
        if mousepos[1] < gridh and oldmpixel != mpixel:
            pixels[mpixel] = (0,0,0,0)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False



while running:
    for event in pygame.event.get():
        eventhandler(event)
    screen.fill((30, 30, 30))
    draw_everything()
    draw_slider()
    pygame.display.flip()

pygame.quit()