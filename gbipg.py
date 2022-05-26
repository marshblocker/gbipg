import time
import random as rand
import json

from img import getImage
from classes import Point, CirclesAdjacencyGraph
from const import *
import utils

def setup():        
    size(800, 800)
    background(WHITE)
    
    start_time = time.time()
    
    config = open('config.json')
    config_json = json.load(config)
    config.close()

    file_name = config_json['image']['file_name']
    preprocess = config_json['image']['preprocess']
    display_img = config_json['image']['display']

    img = getImage(file_name, preprocess)
    if img:
        if display_img:
            image(img, 0, 0)
        GBIPG(True)
        print('Success')    
    else: 
        print('Failed')
        exit()
    
    print('Program finished execution after {} seconds.'
          .format(round(time.time() - start_time, 3))
    )
    
def GBIPG(overlap_output = False):
    ''' 
    Generate compactly-filled, randomized circles on the background or on the
    figure using the Graph-based Ishihara Plate Generation (GBIPG) Algorithm.
    
    Parameters:
        overlap_output: boolean := If True, overlap the output of this function to the current canvas. Otherwise,
                        clear the background and display the output. This is initially set to False.
    '''
    loadPixels()
    fig_random_points, bg_random_points = generate_random_points(pixels)

    fig_cag = build_circles_adjacency_graph(fig_random_points, pixels)
    bg_cag = build_circles_adjacency_graph(bg_random_points, pixels)
    
    if not overlap_output: background(WHITE)
    
    solved_fig_cag = solve_csp_of_cag(fig_cag, visualize = True, color_scheme = FIG_COLOR_SCHEME)
    solved_bg_cag = solve_csp_of_cag(bg_cag, visualize = True, color_scheme = BG_COLOR_SCHEME)
        
def generate_random_points(canvas_pxls, visualize = False, color_scheme = RED_COLOR_SCHEME):
    '''
    Return a list of random points in the background and a list of random points in the figure. 
    The random points are generated such that they do not overlap with other points, 
    figure boundary, and the canvas wall.
    
    Parameters:
        canvas_pxls: List[color]
        visualize: boolean := If True, the random points will be drawn on the canvas
                              using circles with radius MIN_CIRCLE_RADIUS. Note that 
                              this will draw over the canvas, so if the canvas' pixel 
                              information is needed, don't use this (or transfer the 
                              circles in another image). This is initially set to False.
        color_scheme: List[str] := List of color hex strings that will be used as argument to fill().
        
    Return Value:
        (fig_random_points, bg_random_points): Tuple[List[Point], List[Point]]
    '''
    bg_random_points = []
    fig_random_points = []
    
    stroke(BLACK)
    
    for i in range(MAX_NUM_CIRCLES):
        x, y = int(rand.uniform(0, WIDTH)), int(rand.uniform(0, HEIGHT))
        p = Point(x, y, canvas_pxls)
        overlap = False
                
        if p.will_overlap_wall() or p.will_overlap_fig_boundary(canvas_pxls):
            overlap = True
                                                                            
        if not overlap:
            # TODO: Don't check all points in random_points, only points near p.
            random_points = fig_random_points if p.in_fig() else bg_random_points
            for p2 in random_points:
                if p.will_overlap_point(p2):
                    overlap = True
                    break
                                                    
        if not overlap:
            if p.in_fig():
                fig_random_points.append(p)
            else:
                bg_random_points.append(p)
    
    if visualize:
        r = MIN_CIRCLE_RADIUS
        for p in fig_random_points + bg_random_points:
            fill(rand.choice(color_scheme))
            x, y = p.get_coord()
            ellipse(x, y, 2*r, 2*r)
            
    return (fig_random_points, bg_random_points)

def build_circles_adjacency_graph(center_points, canvas_pxls, visualize = False, color_scheme = [RED_COLOR_SCHEME]):
    ''' Build the CirclesAdjacencyGraph from the given center_points.
    
    Parameters:
        center_points: List[Point]
        canvas_pxls: List[color]
        visualize: boolean
        color_scheme: List[str] := List of color hex strings that will be used as argument to fill().
        
    Return Value:
        cag: CirclesAdjacencyGraph
    '''
    cag = CirclesAdjacencyGraph(center_points, canvas_pxls)
    
    if visualize:
        cag.visualize(color_scheme)
        
    return cag

def solve_csp_of_cag(cag, visualize = False, color_scheme = [RED_COLOR_SCHEME]):
    ''' Solve the Constraint Satisfaction Problem of the Circles Adjacency Graph cag.
    
    Params:
        cag: CirclesAdjacencyGraph
        visualize: boolean
        color_scheme: List[str] := List of color hex strings that will be used as argument to fill().
        
    Return Value:
        solved_cag: CirclesAdjacencyGraph := This is cag but with the radius of each of its node
                                             satisfying the CSP of cag.
    '''
    for i in range(len(cag.nodes)):
        cag.nodes[i].radius = cag.nodes[i].max_radius
        cx, cy = cag.nodes[i].center.get_coord()
        for indx in cag.nodes[i].adj_nodes:
            cx2, cy2 = cag.nodes[indx].center.get_coord()
            other_node_new_max_radius = utils.distance((cx, cy), (cx2, cy2)) - cag.nodes[i].radius
            if other_node_new_max_radius < cag.nodes[indx].max_radius:
                cag.nodes[indx].max_radius = other_node_new_max_radius
                cag.nodes[indx].adj_nodes.remove(i)
                
    solved_cag = cag
    
    if visualize:
        noStroke()
        for node in solved_cag.nodes:
            fill(rand.choice(color_scheme))
            x, y = node.center.get_coord()
            r = node.radius
            ellipse(x, y, 2*r, 2*r)
    
    return solved_cag
            
            
        
        
        
