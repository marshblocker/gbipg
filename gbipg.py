import time
import random as rand
import json

from img import getImage
from classes import Point, CirclesAdjacencyGraph
from const import *
import utils

def settings():
    size(WIDTH, HEIGHT)

def setup():
    config = open('config.json')
    config_json = json.load(config)
    config.close()

    # This could be 'normal' mode or 'benchmark' mode.
    MODE = config_json['run']['mode']

    FILE_NAME = config_json['image']['file_name']
    PREPROCESS_IMG = config_json['image']['preprocess']

    img = getImage(FILE_NAME, PREPROCESS_IMG)
    if img:
        if MODE == 'normal':
            normal_mode(img)
        elif MODE == 'benchmark':
            ITERATIONS = config_json['run']['benchmark_iterations']
            benchmark_mode(img, ITERATIONS)
        else:
            print('Error: Invalid mode.')
            exit()
    else:
        print('Failed.')
        exit()

def normal_mode(img):
    print('Program start.')
    if run(img):
        print('Success.')
    else:
        print('Failed.')

def benchmark_mode(img, iterations):
    print('Program start.')
    avg_time = 0.0
    variance = 0.0
    duration_list = []

    success = True
    for i in range(1, iterations+1):
        start_time = time.time()

        success = run(img)

        duration = round(time.time() - start_time, 3)
        duration_list.append(duration)
        avg_time += duration
        print('Iteration {} of {}: {} seconds.'
              .format(i, iterations, duration))

        if not success:
            print('Failed at iteration {} of {}'.format(i, iterations))
            avg_time = avg_time / i
            variance = sum([(duration - avg_time)**2 for duration in duration_list]) / (iterations - 1)
            break

    if success:
        print('Success.')
        avg_time = round(avg_time / iterations, 3)
        variance = round(sum([(duration - avg_time)**2 for duration in duration_list]) / (iterations - 1), 3)
    
    print('Average runtime: {} seconds'.format(avg_time))
    print('Variance: {}'.format(variance))

def run(img):
    background(WHITE)
    if img:
        img.loadPixels()
        GBIPG(img.pixels)
        return True
    else:
        return False


def GBIPG(img_pxls):
    ''' 
    Generate compactly-filled, randomized circles on the background and the 
    figure using the Graph-based Ishihara Plate Generation (GBIPG) Algorithm.

    Parameters:
        img_pxls: list[color] := The pixels of the image reference.

    Return Value:
        None
    '''
    fig_random_points, bg_random_points = generate_random_points(img_pxls)

    fig_cag = build_circles_adjacency_graph(fig_random_points, img_pxls)
    bg_cag = build_circles_adjacency_graph(bg_random_points, img_pxls)

    solved_fig_cag = solve_csp_of_cag(fig_cag, FIG_COLOR_SCHEME)
    solved_bg_cag = solve_csp_of_cag(bg_cag, BG_COLOR_SCHEME)

    fill_up_crevices(img_pxls)
    

def generate_random_points(img_pxls):
    '''
    Return a list of random points in the background and a list of random points in the figure. 
    The random points are generated such that they do not overlap with other points, 
    figure boundary, and the canvas wall.

    Parameters:
        img_pxls: list[color]

    Return Value:
        (fig_random_points, bg_random_points): tuple[list[Point], list[Point]]
    '''
    bg_random_points = []
    fig_random_points = []

    stroke(BLACK)

    start = WIDTH/2 - WALL_RADIUS
    end = WIDTH/2 + WALL_RADIUS
    
    # How distributed the points are in the canvas.
    box_size = BOX_SIZE

    for i in range(start, end, box_size):
        for j in range(start, end, box_size):
            x = int(rand.uniform(i + MIN_CIRCLE_RADIUS, i + box_size - MIN_CIRCLE_RADIUS))
            y = int(rand.uniform(j + MIN_CIRCLE_RADIUS, j + box_size - MIN_CIRCLE_RADIUS))
            p = Point(x, y, img_pxls)
            overlap = False

            if p.will_overlap_wall() or p.will_overlap_fig_boundary(img_pxls):
                overlap = True

            if not overlap:
                if p.in_fig():
                    fig_random_points.append(p)
                else:
                    bg_random_points.append(p)

    return (fig_random_points, bg_random_points)


def build_circles_adjacency_graph(center_points, img_pxls):
    ''' Build the CirclesAdjacencyGraph from the given center_points.

    Parameters:
        center_points: list[Point]
        img_pxls: list[color]

    Return Value:
        cag: CirclesAdjacencyGraph
    '''
    cag = CirclesAdjacencyGraph(center_points, img_pxls)

    return cag


def solve_csp_of_cag(cag, color_scheme):
    ''' Solve the Constraint Satisfaction Problem of the Circles Adjacency Graph cag.

    Params:
        cag: CirclesAdjacencyGraph
        color_scheme: list[str] := list of color hex strings that will be used as argument to fill().

    Return Value:
        solved_cag: CirclesAdjacencyGraph := This is cag but with the radius of each of its node
                                             satisfying the CSP of cag.
    '''
    for i in range(len(cag.nodes)):
        cag.nodes[i].radius = cag.nodes[i].max_radius
        cx, cy = cag.nodes[i].center.get_coord()
        for indx in cag.nodes[i].adj_nodes:
            cx2, cy2 = cag.nodes[indx].center.get_coord()
            other_node_new_max_radius = utils.distance(
                (cx, cy), (cx2, cy2)) - cag.nodes[i].radius
            if other_node_new_max_radius < cag.nodes[indx].max_radius:
                cag.nodes[indx].max_radius = other_node_new_max_radius
                cag.nodes[indx].adj_nodes.remove(i)

    solved_cag = cag

    noStroke()
    for node in solved_cag.nodes:
        fill(rand.choice(color_scheme))
        x, y = node.center.get_coord()
        r = node.radius
        ellipse(x, y, 2*r, 2*r)

    return solved_cag

def fill_up_crevices(img_pxls):
    '''Fill up remaining crevices using Monte Carlo algorithm.
    
    Parameter:
        img_pxls: list[color]

    Return Value:
        None
    '''
    start = WIDTH/2 - WALL_RADIUS
    end = WIDTH/2 + WALL_RADIUS
    for i in range(20000):
        loadPixels()
        x, y = int(rand.uniform(start, end-1)), int(rand.uniform(start, end-1))
        p = Point(x, y, img_pxls)
        r = rand.randint(2, MIN_CIRCLE_RADIUS)
        overlap = False

        if p.will_overlap_wall():
            overlap = True
        
        if p.will_overlap_something(r, pixels):
            overlap = True

        if not overlap:
            color_scheme = FIG_COLOR_SCHEME if p.in_fig() else BG_COLOR_SCHEME
            fill(rand.choice(color_scheme))
            ellipse(x, y, 2*r, 2*r)

