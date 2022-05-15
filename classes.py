from const import *

class Point:
    ''' 
    Represents the center point of a circle to be generated on the Ishihara Plate.
    '''
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._loc = self._set_loc()
        
    def get_loc(self):
        return self._loc
        
    def _set_loc(self):
        self._loc = WIDTH*self._y + self._x
        
    def get_coord(self):
        return (self._x, self._y)
   
    def set_coord(self, new_coord):
        self._x, self._y = new_coord
        self._set_loc()

    def will_overlap_point(self, p2):
        return self._linear_distance(p2) <= MIN_CIRCLE_RADIUS
    
    def will_overlap_wall(self):
        px, py = self.get_coord()
        
        if px <= MIN_CIRCLE_RADIUS or WIDTH - px <= MIN_CIRCLE_RADIUS:
            return True
        
        if py <= MIN_CIRCLE_RADIUS or HEIGHT - py <= MIN_CIRCLE_RADIUS:
            return True
        
        return False
        
    def _linear_distance(self, p2):
        '''
        Calculates the x-value distance and y-value distance between
        this point and p2, and returns the maximum between the two.
        '''
        p1x, p1y = self.get_coord()
        p2x, p2y = p2.get_coord()
        return max([abs(p2x - p1x), abs(p2y - p1y)])
        
    
