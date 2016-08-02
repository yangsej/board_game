from tkinter import *

class Unit:
    def __init__(self, name='Unnamed', player=None, x=-1, y=-1,
                 action=0, speed=0, attack=0, defence=0,
                 range=0, accuracy=0, image=None):
        
        self.name = name

        self.player = player

        self.stat = {
            'attack'    : attack,
            'defence'   : defence,
            'range'     : range,
            'accuracy'  : accuracy,
            'action'    : action,
            'speed'     : speed,

            }

        self.x = x
        self.y = y

        self.image = image

    def __str__(self):
        return self.name

    def move(self, x, y):
        self.x += x
        self.y += y
        

핫산 = Unit('핫산',action=2, speed=5, attack=3, defence=1,
          range=7, accuracy=70, image='C:/Users/ysj/Desktop/python/판/hot.png')
