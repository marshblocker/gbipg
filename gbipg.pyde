import time

from img import displayImage
from classes import Point
from const import *

def setup():        
    size(800, 800)
    background(WHITE)
    
    start_time = time.time()
    
    # Change FILE_NAME if necessary.
    FILE_NAME = "spring.png"
    # Set this to False if the loaded image is already properly formatted.
    PREPROCESS = True 
    if displayImage(FILE_NAME, PREPROCESS):
        fig_random_points, bg_random_points = generate_random_points(True)
        # GBIPG(True)
        # GBIPG(False)
        print('Success')    
    else: 
        print('Failed')
        exit()
    
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
    '''
    Return a list of random points in the background and a list of random points in the figure. 
    The random points are generated such that they do not overlap with other points, 
    figure boundary, and the canvas wall.
    
    Params:
        visualize: boolean := If True, the random points will be drawn on the canvas
        using circles with radius MIN_CIRCLE_RADIUS. Note that this will draw over the
        canvas, so if the canvas' pixel information is needed, don't use this (or transfer
        the circles in another image). This is initially set to False.
        
    Return Value:
        (fig_random_points, bg_random_points): Tuple[List[Point], List[Point]]
    '''
    bg_random_points = []
    fig_random_points = []
    
    noStroke()
    fill(255, 0, 0)
    loadPixels()
    
    for i in range(MAX_NUM_CIRCLES):
        x, y = int(random(WIDTH)), int(random(HEIGHT))
        p = Point(x, y)
        overlap = False
        
        if p.will_overlap_wall() or p.will_overlap_fig(pixels): 
            overlap = True
        
        # If point is located inside the figure.
        in_fig = (pixels[p.get_loc()] == BLACK_RGB)
                                                
        if not overlap:
            # TODO: Don't check all points in random_points, only points near p.
            random_points = fig_random_points if in_fig else bg_random_points
            for p2 in random_points:
                if p.will_overlap_point(p2):
                    overlap = True
                    break
                            
        if not overlap:
            if in_fig:
                fig_random_points.append(p)
            else:
                bg_random_points.append(p)
            
    if visualize:
        r = MIN_CIRCLE_RADIUS
        for p in fig_random_points + bg_random_points:
            x, y = p.get_coord()
            ellipse(x, y, r, r)
            
    return (fig_random_points, bg_random_points)
