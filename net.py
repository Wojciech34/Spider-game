import numpy as np
from numpy.random import uniform
from itertools import repeat
import pytest
from typing import List


MAX_X = 500
MAX_Y = 500


class Place():
    color = None
    selected = False
    show_accesible = False

    def __init__(self, x, y, c) -> None:
        self.c = c
        self.x = x
        self.y = y
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
            elems = line.split(' ')
            places.append(Place(float(elems[0]), float(elems[1]), counter))
            counter += 1
    return places

def read_cons(path, places: List[Place]) -> None:

    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            elems = line.split(' ')
            v, w = int(elems[0]), int(elems[1])
            places[v].add_conn(w, places[w])
            places[w].add_conn(v, places[v])

class Net():
    places = []

    def __init__(self, n=0, random = False, path=None) -> None:
        if path:
            read_poss(path, self.places)
        # dont use them for now
        elif random:
            self.places.extend(repeat(Place(uniform(high=MAX_X), uniform(high=MAX_Y)), n))
        else:
            self.places.extend(repeat(Place(0, 0), n))
    
    def make_conns(self, path):
        read_cons(path, self.places)
    
    def update_places(self, scalex, scaley):
        for place in self.places:
            place.x *= scalex
            place.y *= scaley
    
    def find_path(self, dest):
        return
        start = list(filter(lambda x: x.selected, self.places))[0]



# for testing purposes
if __name__ == '__main__':
    net = Net(path='positions')
    pytest.set_trace()