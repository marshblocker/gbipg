from img import displayImage
from classes import Point
from const import *

def setup():        
    size(800, 800)
    background(BLACK)
    
    # Change FILE_NAME if necessary.
    FILE_NAME = "square.png"
    # Set this to False if the loaded image is already properly formatted.
    PREPROCESS = True 
    if displayImage(FILE_NAME, PREPROCESS):
        GBIPG(True)
        # GBIPG(False)
        print('Done')    
    else: print('Failed') 
    
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
    generate_random_points()
    
def generate_random_points():
    random_points = []
    noStroke()
    fill(255, 0, 0)
    
    for _ in range(NUM_CIRCLES):
        x, y = int(random(WIDTH)), int(random(HEIGHT))
        p = Point(x, y)
        
        overlap = False
        for p2 in random_points:
            if p.will_overlap_point(p2) or p.will_overlap_wall():
                overlap = True
                
                break
            
        if not overlap: 
            random_points.append(p)
            r = MIN_CIRCLE_RADIUS
            ellipse(x, y, r, r)
