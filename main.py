import pygame
import sys
from typing import List
from net import Net, Place
from itertools import repeat

# IS_ANY_PLACE_SELECTED = False
WINDOW_H = 1000
WINDOW_W = 1000


def draw_net(net: Net, surface: pygame.Surface):
    for w in net.places:
        pygame.draw.circle(surface, color="cornsilk2" if not w.color else w.color, center=((w.x, w.y)), radius=15)
        for v in w.conns_map.values():
            # for now each line is drawn 2 times
            pygame.draw.line(surface, color="black", start_pos=((w.x, w.y)), end_pos=((v.x, v.y)), width=5)

# def update_places(places: List[Place], surface: pygame.Surface):
#     for place in places:
#         if place.color:
            

def catch_cursor(places: List[Place]):
    posx, posy = pygame.mouse.get_pos()
    for place in places:
        if abs(place.x - posx) < 10 and abs(place.y - posy) < 10:
            if not place.color:
                place.set_color("red")
        else:
            place.reset_color()

def select_place(places: List[Place]):
        # if IS_ANY_PLACE_SELECTED:
        #     pass
        posx, posy = pygame.mouse.get_pos()
        for place in places:
            if abs(place.x - posx) < 10 and abs(place.y - posy) < 10:
                place.select()
                place.set_color("blue")
                show_neighbours(1, place)
                return

def reset_places(places: List[Place]):
    for place in places:
        place.unselect()
        place.unset_show_accesible()

def show_neighbours(n: int, place: Place):
    for v in place.conns_map.values():
        v.set_show_accesible()
        v.set_color('pink')
        if n - 1 > 0:
            show_neighbours(n - 1, v)

def reset_showed_neighbours(places: List[Place]):
    for place in places:
        place.set_show_accesible()

# def select_next_place(place: Place):


pygame.init()
# infoObject = pygame.display.Info()
# print(infoObject)
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# init surfaces
# surf1 = pygame.Surface((1000, 900))
# surf1.fill('azure4')
surf2 = pygame.Surface((WINDOW_W, WINDOW_H))
surf2.fill('azure4')

net = Net(path='positions')
net.make_conns('connections')
# draw_net(net, surf2)

while True:

    draw_net(net, surf2)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            WINDOW_W, WINDOW_H = event.w, event.h
            surf2 = pygame.Surface((WINDOW_W, WINDOW_H))
            surf2.fill('azure4')
            net.update_places(WINDOW_W / 1000, WINDOW_H / 1000)
            draw_net(net, surf2)
        state = pygame.mouse.get_pressed()
        # left click is being pressed
        if state[0]:
            select_place(net.places)
        # right or middle click
        if state[1] or state[2]:
            reset_places(net.places)

        # print(state)
        catch_cursor(net.places)

    # draw_net(net, surf2)    
    
    # screen.blit(surf1, (0, 0))
    screen.blit(surf2, (0, 0))
    # pygame.display.flip()

    pygame.display.update()
    clock.tick(60)        
