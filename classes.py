from const import *
from utils import linear_distance

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._loc = self.set_loc(self)
        
    def get_loc(self):
        return self._loc
        
    def set_loc(self):
        self._loc = WIDTH*self._y + self._x
        
    def get_coord(self):
        return (self._x, self._y)
   
    def set_coord(self, new_coord):
        self._x, self._y = new_coord
        self.set_loc()
       
    def check_collision(self, p2):
        return linear_distance(self, p2) > MIN_CIRCLE_RADIUS
        
    
