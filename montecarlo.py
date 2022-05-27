import math
import random
import time

from const import *
from img import getImage
from classes import Point
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
        monte_carlo(img.pixels)
        return True
    else:
        return False

def monte_carlo(img_pxls):
    remaining_canvas_area = math.pi * WALL_RADIUS**2
    MIN_UNFILLED_AREA = remaining_canvas_area * 0.4
    MIN_RADIUS = 3
    MAX_RADIUS = 10

    noStroke()
    while remaining_canvas_area > MIN_UNFILLED_AREA:
        loadPixels()
        x, y = random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)
        r = random.randint(MIN_RADIUS, MAX_RADIUS)
        p = Point(x, y, img_pxls)
        
        overlap = False

        if will_overlap_wall((x, y)):
            overlap = True
        
        if will_overlap_something(p, r, pixels):
            overlap = True

        if not overlap:
            color_scheme = FIG_COLOR_SCHEME if p.in_fig() else BG_COLOR_SCHEME
            fill(random.choice(color_scheme))
            ellipse(x, y, 2*r, 2*r)

            circle_area = math.pi * r**2
            remaining_canvas_area -= circle_area
        

def will_overlap_wall(coord):
    px, py = coord

    if utils.distance_squared((px, py), (WIDTH/2, HEIGHT/2)) > WALL_RADIUS**2:
        return True

    return False

def will_overlap_something(p, r, canvas_pxls):
    return opposite_colr_point_in_circle(p, r, canvas_pxls)

def opposite_colr_point_in_circle(p, r, canvas_pxls):
    px, py = p.get_coord()
    p_colr = BLACK_RGB if p.in_fig() else WHITE_RGB
    r_squared = r*r

    y_start = ceil(max(0, py - r))
    x_start = ceil(max(0, px - r))
    y_end = ceil(min(HEIGHT, py + r + 1))
    x_end = ceil(min(WIDTH, px + r + 1))

    for p2y in range(y_start, y_end):
        for p2x in range(x_start, x_end):
            p2_loc = WIDTH*p2y + p2x
            if utils.distance_squared((px, py), (p2x, p2y)) <= r_squared and canvas_pxls[p2_loc] not in [BLACK_RGB, WHITE_RGB]:
                return True

    return False


