import math
import random
import time

from const import MC_CONST
from img import getImage
from classes import Point
import const
import utils

def settings():
    size(MC_CONST.WIDTH, MC_CONST.HEIGHT)

def setup():
    if MC_CONST.is_parameters_valid():
        img = getImage(MC_CONST.FILE_NAME, MC_CONST, MC_CONST.PREPROCESS_IMG)
        if img:
            if MC_CONST.MODE == 'normal':
                normal_mode(img)
            elif MC_CONST.MODE == 'benchmark':
                benchmark_mode(img, MC_CONST.BENCHMARK_ITERATIONS)
            else:
                print('Error: Invalid mode.')
                exit()
        else:
            print('Failed.')
            exit()
    else:
        print('Failed.')
        exit()

def normal_mode(img):
    '''Run the algorithm normally.

    Parameters:
        img: PImage
    '''
    print('Program start.')
    run(img)
    print('Success.')

def benchmark_mode(img, iterations):
    '''Benchmark the algorithm to determine its average runtime and variance.

    Parameters:
        img: PImage
        iterations: int := How many times the algorithm will be run.
    '''
    print('Program start.')
    avg_time = 0.0
    variance = 0.0
    duration_list = []

    for i in range(1, iterations+1):
        start_time = time.time()

        run(img)

        duration = round(time.time() - start_time, 3)
        duration_list.append(duration)
        avg_time += duration
        print('Iteration {} of {}: {} seconds.'
              .format(i, iterations, duration))

    print('Success.')
    avg_time = round(avg_time / iterations, 3)
    variance = round(sum([(duration - avg_time)**2 for duration in duration_list]) / iterations, 3)
    
    print('Average runtime: {} seconds'.format(avg_time))
    print('Variance: {}'.format(variance))

def run(img):
    background(const.WHITE)
    img.loadPixels()
    monte_carlo(img.pixels)

def monte_carlo(img_pxls):
    '''
    Perform the Monte Carlo Algorithm to generate an Ishihara Plate.
    '''
    already_filled_area = 0.0
    total_area = math.pi * MC_CONST.WALL_RADIUS**2
    MAX_FILLED_AREA = total_area * MC_CONST.MAX_FILLED_AREA_RATIO

    start = MC_CONST.WIDTH//2 - MC_CONST.WALL_RADIUS
    end = MC_CONST.WIDTH//2 + MC_CONST.WALL_RADIUS

    noStroke()
    while already_filled_area < MAX_FILLED_AREA:
        loadPixels()
        x, y = random.randint(start, end-1), random.randint(start, end-1)
        r = random.randint(MC_CONST.MIN_CIRCLE_RADIUS, MC_CONST.MAX_CIRCLE_RADIUS)
        p = Point(x, y, img_pxls, MC_CONST)
        
        overlap = False

        if p.will_overlap_wall():
            overlap = True
        
        if p.will_overlap_something(r, pixels):
            overlap = True

        if not overlap:
            color_scheme = MC_CONST.FIG_COLOR_SCHEME if p.in_fig() else MC_CONST.BG_COLOR_SCHEME
            fill(random.choice(color_scheme))
            ellipse(x, y, 2*r, 2*r)

            already_filled_area += math.pi * r**2