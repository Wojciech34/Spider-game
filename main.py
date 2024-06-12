import pygame
import sys
from typing import List
from net import Net, Place, Spider, Fly
from turn import Turn
from itertools import repeat
import threading
# import queue
import settings


IS_ANY_PLACE_SELECTED = False

# Default configuration 1000 x 1000
# when changed need to be scaled
WINDOW_W = 1000
WINDOW_H = 1000


def draw_net(net: Net, surface: pygame.Surface):
    for w in net.places:
        # print circle or figure on the place
        if w.figure:
            surface.blit(w.figure.surf, (w.x - w.figure.size[0] / 2, w.y - w.figure.size[1] / 2))
        elif w.final_place:
            pygame.draw.circle(surface, color='cyan1', center=((w.x, w.y)), radius=20)
        elif w.avaible:
            pygame.draw.circle(surface, color='pink' if not w.color else w.color, center=((w.x, w.y)), radius=15)
        else:
            pygame.draw.circle(surface, color='cornsilk2' if not w.color else w.color, center=((w.x, w.y)), radius=15)
        # print extra circle indicating selected figure
        if w.figure_selected:
            pygame.draw.circle(surface, color='red', center=(w.x, w.y), radius=20, width=5)
        # print edges
        for v in w.conns_map.values():
            # for now each line is drawn 2 times
            pygame.draw.line(surface, color='white', start_pos=((w.x, w.y)), end_pos=((v.x, v.y)), width=5)

def display_places_numbers(net: Net, surface: pygame.Surface):
    for w in net.places:
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(f'{w.c}', True, 'black')
        textRect = text.get_rect()
        textRect.center = (w.x, w.y)
        surface.blit(text, textRect)

def display_buttons(surface: pygame.Surface):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(f'{settings.message}', True, 'black')
    text2 = font.render(f'moves: {settings.number}', True, 'black')
    text3 = font.render(f'rescued flies: {settings.counter}', True, 'black')
    textRect = text.get_rect()
    textRect.center = (860 * WINDOW_W / 1000, 100 * WINDOW_H / 1000)
    textRect2 = text2.get_rect()
    textRect2.center = (860 * WINDOW_W / 1000, 130 * WINDOW_H / 1000)
    textRect3 = text3.get_rect()
    textRect3.center = (860 * WINDOW_W / 1000, 160 * WINDOW_H / 1000)
    surface.blit(text, textRect)
    surface.blit(text2, textRect2)
    surface.blit(text3, textRect3)


def display_main_menu(surface: pygame.Surface):
    font = pygame.font.Font('freesansbold.ttf', 60)
    text = font.render('Start game map 1', True, 'black')
    textRect = text.get_rect()
    textRect.center = (460 * WINDOW_W / 1000, 100 * WINDOW_H / 1000)
    surface.blit(text, textRect)

    text2 = font.render('Start game map 2', True, 'black')
    textRect2 = text2.get_rect()
    textRect2.center = (460 * WINDOW_W / 1000, 300 * WINDOW_H / 1000)
    surface.blit(text2, textRect2)

    text3 = font.render('Start game map 3', True, 'black')
    textRect3 = text2.get_rect()
    textRect3.center = (460 * WINDOW_W / 1000, 500 * WINDOW_H / 1000)
    surface.blit(text3, textRect3)



    return [textRect, textRect2, textRect3]




def catch_cursor(places: List[Place]):
    posx, posy = pygame.mouse.get_pos()
    for place in places:
        if abs(place.x - posx) < 10 and abs(place.y - posy) < 10:
            if not place.color:
                place.set_color('red')
        else:
            place.reset_color()


def set_initial_size():
    global WINDOW_W, WINDOW_H
    infoObject = pygame.display.Info()
    WINDOW_W, WINDOW_H =  infoObject.current_w - 100, infoObject.current_h - 100


pygame.init()
set_initial_size()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

surf2 = pygame.Surface((WINDOW_W, WINDOW_H))
surf2.fill('azure4')

# net = Net(path='positions')
# net.make_conns('connections')
# net.update_places(WINDOW_W / 1000, WINDOW_H / 1000)
# turn = Turn(net)
# thread = threading.Thread(target=turn.perform_turn, daemon=True)


settings.init()


# thread2 = threading.Thread(target=catch_cursor, args=(net.places, ), daemon=True)
started = False
menu_displayed = True

while True:

    if started:
        thread.start()
        # thread2.start()
        started = False
    surf2 = pygame.Surface((WINDOW_W, WINDOW_H))
    surf2.fill('azure4')

    if menu_displayed:
        rects = display_main_menu(surf2)
        posx, posy = pygame.mouse.get_pos()
        state = pygame.mouse.get_pressed()
        for idx, rect in enumerate(rects):
            if state[0] and rect.x < posx < rect.x + rect.w and rect.y < posy < rect.y + rect.h:
                menu_displayed = False
                started = True
                net = Net(path='positions'+str(idx+1), path2='figures'+str(idx+1))
                net.make_conns('connections'+str(idx+1))
                net.update_places(WINDOW_W / 1000, WINDOW_H / 1000)
                turn = Turn(net)
                thread = threading.Thread(target=turn.perform_turn, daemon=True)
                break

    else:
        draw_net(net, surf2)
        display_buttons(surf2)
        # for debug
        display_places_numbers(net, surf2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            WINDOW_W, WINDOW_H = event.w, event.h
            surf2 = pygame.Surface((WINDOW_W, WINDOW_H))
            surf2.fill('azure4')
            if not menu_displayed:
                net.update_places(WINDOW_W / 1000, WINDOW_H / 1000)
                draw_net(net, surf2)
                display_buttons(surf2)
        state = pygame.mouse.get_pressed()

        # left click is being pressed
        # if state[0]:
        #     select_place(net.places)
        # right or middle click
        # if state[1] or state[2]:
        #     reset_places(net.places)
        if not menu_displayed:
            catch_cursor(net.places)

    # draw_net(net, surf2)    
    
    # screen.blit(surf1, (0, 0))
    screen.blit(surf2, (0, 0))
    # pygame.display.flip()

    pygame.display.update()
    clock.tick(60)        
