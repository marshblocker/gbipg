import time

from img import displayImage
from classes import Point
from const import *

def setup():        
    size(800, 800)
    background(WHITE)
    
    start_time = time.time()
    
    # Change FILE_NAME if necessary.
    FILE_NAME = "square.png"
    # Set this to False if the loaded image is already properly formatted.
    PREPROCESS = True 
    if displayImage(FILE_NAME, PREPROCESS):
        random_points = generate_random_points(True)
        # GBIPG(True)
        # GBIPG(False)
        print('Done')    
    else: print('Failed')
    
    print('Program finished execution after {} seconds.'
          .format(round(time.time() - start_time, 3))
    )
    
def GBIPG(onFigure):
    ''' 
    Generate compactly-filled, randomized circles on the background or on the
    figure using the Graph-based Ishihara Plate Generation (GBIPG) Algorithm.
    
    Params:
        onFigure: boolean := If True, perform GBIPG on the figure. Otherwise,
                             perform GBIPG on the background.
                             
    Return Value:
        None
    '''
    pass
        
def generate_random_points(visualize = False):
    random_points = []
    noStroke()
    fill(255, 0, 0)
    loadPixels()
    
    for _ in range(MAX_NUM_CIRCLES):
        x, y = int(random(WIDTH)), int(random(HEIGHT))
        p = Point(x, y)
        overlap = False
        
        if p.will_overlap_wall() or p.will_overlap_fig(pixels): 
            overlap = True
                        
        if not overlap:
            for p2 in random_points:
                if p.will_overlap_point(p2):
                    overlap = True
                    break
            
        if not overlap: 
            random_points.append(p)
            
    if visualize:
        r = MIN_CIRCLE_RADIUS
        for p in random_points:
            x, y = p.get_coord()
            ellipse(x, y, r, r)
            
    return random_points
