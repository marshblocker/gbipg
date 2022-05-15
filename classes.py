from const import *

class Point:
    ''' 
    Represents the center point of a circle to be generated on the Ishihara Plate.
    '''
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._loc = WIDTH*self._y + self._x
        
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
        p2_coord = p2.get_coord()
        return self._distance_squared(p2_coord) <= MIN_CIRCLE_RADIUS_SQUARED
    
    def will_overlap_wall(self):
        px, py = self.get_coord()
        
        if px <= MIN_CIRCLE_RADIUS or WIDTH - px <= MIN_CIRCLE_RADIUS:
            return True
        
        if py <= MIN_CIRCLE_RADIUS or HEIGHT - py <= MIN_CIRCLE_RADIUS:
            return True
                
        return False
    
    def will_overlap_fig(self, canvas_pxls):
        px, py = self.get_coord()
        center_point_color = canvas_pxls[self.get_loc()]
        min_circle_points = self._get_min_circle_points()
        
        for p_loc in min_circle_points:
            if canvas_pxls[p_loc] != center_point_color:
                return True         
    
        return False
        
    def _distance_squared(self, p2_coord):
        p1x, p1y = self.get_coord()
        p2x, p2y = p2_coord
        
        dx = p2x - p1x
        dy = p2y - p1y
        
        dx_squared = dx * dx
        dy_squared = dy * dy
        
        return dx_squared + dy_squared
    
    def _get_min_circle_points(self):
        '''
        Get all points within the circle with this point as its center
        and its radius is MIN_CIRCLE_RADIUS.
        '''
        min_circle_points = []
        px, py = self.get_coord()
        
        for p2y in range(py - MIN_CIRCLE_RADIUS, py + MIN_CIRCLE_RADIUS + 1):
            for p2x in range(px - MIN_CIRCLE_RADIUS, px + MIN_CIRCLE_RADIUS + 1):
                if self._distance_squared((p2x, p2y)) <= MIN_CIRCLE_RADIUS_SQUARED:
                    p2_loc = WIDTH*p2y + p2x
                    min_circle_points.append(p2_loc)
                    
        return min_circle_points
                
                
        
    
