""" Module responsible for tour logic
"""

import random
import pygame
import time
from net import Fly, Spider
# import queue
import settings
from utils import get_avaible_moves, get_distance


class Turn():
    # number of players: 2
    # player 0 plays spider
    # player 1 plays fly
    player = 1

    # current state of the game (move1..9)
    state = 1
    net = None

    places = None 


    n = -1

    sel_place1 = None
    sel_place2 = None

    avaible_places = None


    def __init__(self, net) -> None:
        self.net = net
        self.places = net.places
        self.clock = pygame.time.Clock()

    def add_places(self, places):
        self.places = places

    def next_step(self):
        self.state = (self.state + 1) % 8 + 1
    
    def perform_turn(self):
        while True:
            getattr(self, f'move{self.state}')()

    def end_turn(self):
        self.player += 1
        self.player %= 2
        pass
    
    def get_player_name(self):
        if self.player == 0:
            return 'spider'
        if self.player == 1:
            return 'fly'
    
    def find_spider(self):
        return list(filter(lambda x: isinstance(x.figure, Spider), self.places))[0]
    
    def find_any_fly(self):
        return list(filter(lambda x: isinstance(x.figure, Fly), self.places))
    
    def mark_avaible_places(self, is_spider=False):
        self.avaible_places = get_avaible_moves(self.sel_place1, self.n, is_spider=is_spider)
        if is_spider:
            self.avaible_places = list(filter(lambda x: x.c not in range(59, 65),self.avaible_places))
        if not self.avaible_places:
            return
        for place in self.avaible_places:
            place.avaible = True
    
    def unmark_avaible_places(self):
        if not self.avaible_places:
            return
        for place in self.avaible_places:
            place.avaible = False
        self.avaible_places = None
    
    # get random number
    def move1(self):
        self.n = random.randint(1, 6)
        settings.number = self.n
        self.state = 2

    # select a fly
    def move2(self):
        time.sleep(0.1)
        settings.message = 'Select a fly to move'
        while True:
            state = pygame.mouse.get_pressed()
            posx, posy = pygame.mouse.get_pos()
            pygame.time.wait(1)      
            if not state[0]:
                continue
            for place in self.places:
                if isinstance(place.figure, Fly) and abs(place.x - posx) < 10 and abs(place.y - posy) < 10:
                    # place.figure.select()
                    self.sel_place1 = place
                    self.sel_place1.figure_selected = True
                    print("selected a fly!")

                    self.mark_avaible_places()
                    self.state = 3
                    return
            self.clock.tick(60)

    # select a field where fly needs to move    
    def move3(self):
        time.sleep(0.1)
        settings.message = 'Select a place for fly to move'
        while True:
            state = pygame.mouse.get_pressed()
            posx, posy = pygame.mouse.get_pos()
            pygame.time.wait(1)
            if not state[0]:
                continue
            for place in self.avaible_places:
                if not isinstance(place.figure, Fly) and not isinstance(place.figure, Spider) and abs(place.x - posx) < 10 and abs(place.y - posy) < 10:
                    self.unmark_avaible_places()
                    self.sel_place2 = place
                    
                    # fly reached final place
                    if self.sel_place2.final_place:
                        self.net.move_figure(self.sel_place1, self.sel_place2)
                        settings.counter += 1
                        time.sleep(0.5)
                        self.sel_place2.figure = None
                    # common move
                    else:
                        self.net.move_figure(self.sel_place1, self.sel_place2)
                    self.sel_place1.figure_selected = False
                    print("selected empty place!")
                    self.state = 4
                    return
            self.clock.tick(60)

    # if there is more moves then repeat 2 and 3
    def move4(self):
        distance = get_distance(self.places, self.sel_place1, self.sel_place2)
        self.n -= distance
        settings.number = self.n
        if self.n > 0:
            self.state = 2
        else:
            self.state = 5

    # get random number 
    def move5(self):
        self.n = random.randint(1, 6)
        settings.number = self.n
        self.state = 6
        

    # spider moves    
    def move6(self):
        time.sleep(0.1)
        settings.message = 'Select a place for spider to move'

        spider_place = self.find_spider()
        self.sel_place1 = spider_place
        self.sel_place1.figure_selected = True

        self.mark_avaible_places(is_spider=True)

        while True:
            state = pygame.mouse.get_pressed()
            posx, posy = pygame.mouse.get_pos()
            pygame.time.wait(1)
            if not state[0]:
                continue
            for place in self.avaible_places:
                if not isinstance(place.figure, Spider) and not place.final_place and abs(place.x - posx) < 10 and abs(place.y - posy) < 10:
                    self.unmark_avaible_places()

                    self.sel_place2 = place
                    self.net.move_figure(self.sel_place1, self.sel_place2)
                    self.sel_place1.figure_selected = False
                    print("selected empty place for spider and moved!")
                    self.state = 7
                    return
            self.clock.tick(60)

    # if spider has more moves then repeat 6
    def move7(self):
        distance = get_distance(self.places, self.sel_place1, self.sel_place2)
        self.n -= distance
        settings.number = self.n
        if self.n > 0:
            self.state = 6
        else:
            self.state = 8

    # end turn, check game end, go to 1
    def move8(self):
        if not any(self.find_any_fly()):
            settings.message = 'Spider won'
        else:
            self.state = 1




