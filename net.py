import numpy as np
import pygame
from numpy.random import uniform
from itertools import repeat
import pytest
from typing import List


MAX_X = 500
MAX_Y = 500

# def fill(surface, color):
#     """Fill all pixels of the surface with color, preserve transparency."""
#     w, h = surface.get_size()
#     r, g, b, _ = color
#     for x in range(w):
#         for y in range(h):
#             a1 = surface.get_at((x, y))[0]
#             a2 = surface.get_at((x, y))[1]
#             a3 = surface.get_at((x, y))[2]
#             a4 = surface.get_at((x, y))[3]
#             surface.set_at((x, y), pygame.Color(a1, a2, a3, a4))
#     return surface

class Spider():
    surf = pygame.image.load('images/spider.png', 'spider')
    size = (35, 35)
    surf = pygame.transform.scale(surf, size)

    def select(self):


        pass



class Fly():
    surf = pygame.image.load('images/fly.png', 'fly')
    size = (35, 35)
    surf = pygame.transform.scale(surf, size)
    or_surf = pygame.transform.scale(surf, size)


    def select(self):
        
        # self.surf = fill(self.surf, (12, 120, 55, 3))
        # self.surf.set_colorkey([123, 214, 122])
        pass


    def reset_color(self):
        self.surf = self.or_surf


class Place():
    color = None
    selected = False
    show_accesible = False
    figure = None
    final_place = False
    figure_selected = False
    avaible = False

    def __init__(self, x, y, c) -> None:
        self.c = c
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.connections = set()
        self.conns_map :dict[int, Place] = {}
    
    def add_conn(self, n, obj):
        self.connections.add(n)
        self.conns_map[n] = obj
    
    def set_color(self, color):
        self.color = color
    
    def reset_color(self):
        if not any([self.selected, self.show_accesible]):
            self.color = None
    
    def select(self):
        self.selected = True
    
    def unselect(self):
        self.selected = False

    def set_show_accesible(self):
        self.show_accesible =  not self.selected 
    
    def unset_show_accesible(self):
        self.show_accesible =  False 
    
def read_poss(path, places: List[Place]) -> List[Place]:
    counter = 0

    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elems = line.split(' ')
            if len(elems) < 2:
                continue
            places.append(Place(float(elems[0]), float(elems[1]), counter))
            counter += 1
    return places

def read_cons(path, places: List[Place]) -> None:
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            elems = line.split(' ')
            if len(elems) < 2:
                continue
            v, w = int(elems[0]), int(elems[1])
            try:
                places[v].add_conn(w, places[w])
                places[w].add_conn(v, places[v])
            except IndexError:
                pass

class Net():
    places = []
    spider_pos = None
    flies_pos = None
    final_pos = None

    def __init__(self, path=None, path2=None) -> None:
        if path:
            read_poss(path, self.places)
            self.read_figures_places(path2)
            self.add_figures()
        else:
            raise Exception

    
    def add_figures(self):
        for place in self.places:
            if place.c == self.spider_pos:
                place.figure = Spider()
            if place.c in self.flies_pos:
                place.figure = Fly()
            # add also final place
            if place.c == self.final_pos:
                place.final_place = True
    
    def move_figure(self, origin, dest):
        dest.figure = origin.figure
        origin.figure = None

    def make_conns(self, path):
        read_cons(path, self.places)
    
    def update_places(self, scalex, scaley):
        for place in self.places:
            place.x = place.ox * scalex
            place.y = place.oy * scaley
    
    def read_figures_places(self, path):
        # line 0 final pos
        # line 1 spider pos
        # line 2 flies pos
        with open(path) as f:
            lines = f.readlines()
            self.final_pos = int(lines[0])
            self.spider_pos = int(lines[1])
            self.flies_pos = []
            poss = lines[2].split(' ')
            for pos in poss:
                self.flies_pos.append(int(pos))


# for testing purposes
# if __name__ == '__main__':
#     net = Net(path='positions')
#     pytest.set_trace()
