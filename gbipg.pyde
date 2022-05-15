from img import displayImage, preprocessImage
from const import *

def setup():    
    size(800, 800)
    background(BLACK)
    
    # Change FILE_NAME if necessary.
    FILE_NAME = "square.png"
    # Set this to False if the loaded image is already properly formatted.
    PREPROCESS = True 
    if displayImage(FILE_NAME, PREPROCESS):
        # GBIPG(True)
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
    pass
