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

    config = open('config.json')
    config_json = json.load(config)
    config.close()

    # This could be 'normal' mode or 'benchmark' mode.
    MODE = config_json['mode']['type']

    FILE_NAME = config_json['image']['file_name']
    PREPROCESS_IMG = config_json['image']['preprocess']
    DISPLAY_IMG = config_json['image']['display']

    img = getImage(FILE_NAME, PREPROCESS_IMG)
    img.loadPixels()
    if img:
        if MODE == 'normal':
            normal_mode(img, img.pixels, DISPLAY_IMG)
        elif MODE == 'benchmark':
            ITERATIONS = config_json['mode']['benchmark_iterations']
            benchmark_mode(img, img.pixels, DISPLAY_IMG, ITERATIONS)
        else:
            print('Error: Invalid mode.')
            exit()
    else:
        print('Failed.')
        exit()

def normal_mode(img, img_pxls, display_img):
    print('Program start.')
    if run(img, img_pxls, display_img):
        print('Success.')
    else:
        print('Failed.')

def benchmark_mode(img, img_pxls, display_img, iterations):
    print('Program start.')
    avg_time = 0.0

    success = True
    for i in range(1, iterations+1):
        start_time = time.time()

        success = run(img, img_pxls, display_img)

        duration = round(time.time() - start_time, 3)
        avg_time += duration
        print('Iteration {} of {}: {} seconds.'
              .format(i, iterations, duration))

        if not success:
            print('Failed at iteration {} of {}'.format(i, iterations))
            avg_time = avg_time / i
            break

    if success:
        print('Success.')
        avg_time = round(avg_time / iterations, 3)
    
    print('Average runtime: {} seconds'.format(avg_time))

def run(img, img_pxls, display_img):
    background(WHITE)
    if img:
        if display_img: image(img, 0, 0)
        GBIPG(img_pxls)
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

    solved_fig_cag = solve_csp_of_cag(
        fig_cag, visualize=True, color_scheme=FIG_COLOR_SCHEME)
    solved_bg_cag = solve_csp_of_cag(
        bg_cag, visualize=True, color_scheme=BG_COLOR_SCHEME)
    

def generate_random_points(img_pxls, visualize=False, color_scheme=RED_COLOR_SCHEME):
    '''
    Return a list of random points in the background and a list of random points in the figure. 
    The random points are generated such that they do not overlap with other points, 
    figure boundary, and the canvas wall.

    Parameters:
        img_pxls: list[color]
        visualize: boolean := If True, the random points will be drawn on the canvas
                              using circles with radius MIN_CIRCLE_RADIUS. Note that 
                              this will draw over the canvas, so if the canvas' pixel 
                              information is needed, don't use this (or transfer the 
                              circles in another image). This is initially set to False.
        color_scheme: list[str] := list of color hex strings that will be used as argument to fill().

    Return Value:
        (fig_random_points, bg_random_points): tuple[list[Point], list[Point]]
    '''
    bg_random_points = []
    fig_random_points = []

    stroke(BLACK)

    for i in range(MAX_NUM_CIRCLES):
        x, y = int(rand.uniform(0, WIDTH)), int(rand.uniform(0, HEIGHT))
        p = Point(x, y, img_pxls)
        overlap = False

        if p.will_overlap_wall() or p.will_overlap_fig_boundary(img_pxls):
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


def build_circles_adjacency_graph(center_points, img_pxls, visualize=False, color_scheme=[RED_COLOR_SCHEME]):
    ''' Build the CirclesAdjacencyGraph from the given center_points.

    Parameters:
        center_points: list[Point]
        img_pxls: list[color]
        visualize: boolean
        color_scheme: list[str] := list of color hex strings that will be used as argument to fill().

    Return Value:
        cag: CirclesAdjacencyGraph
    '''
    cag = CirclesAdjacencyGraph(center_points, img_pxls)

    if visualize:
        cag.visualize(color_scheme)

    return cag


def solve_csp_of_cag(cag, visualize=False, color_scheme=[RED_COLOR_SCHEME]):
    ''' Solve the Constraint Satisfaction Problem of the Circles Adjacency Graph cag.

    Params:
        cag: CirclesAdjacencyGraph
        visualize: boolean
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

    if visualize:
        noStroke()
        for node in solved_cag.nodes:
            fill(rand.choice(color_scheme))
            x, y = node.center.get_coord()
            r = node.radius
            ellipse(x, y, 2*r, 2*r)

    return solved_cag
