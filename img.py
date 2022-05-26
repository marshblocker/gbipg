from const import *
import utils

def getImage(file_name, preprocess = True):
    ''' 
    Preprocess (if specified) given image file and return a PImage object.
    If an error occurred during the preprocessing, this returns None.
    
    Parameters:
        file_name: str := Name of the image file. Must be stored in the 'data'
                          folder and must be in PNG format.
        
        preprocess: boolean := If True, preprocessImage() will be called on the 
                               loaded image. Initially set to True.
                               
    Return Value:
        PImage | None
    '''
    if not file_name.endswith('.png'):
        print('Error: Supplied image is not in PNG format.')
        return None
    
    img = loadImage(file_name)
    
    if not img:
        return None
    
    if preprocess: 
        if not preprocessImage(img):
            return None
    
    return img
    
def preprocessImage(img):
    ''' Preprocess the given image. 
    
    This function performs the following on the image:
        - Resize image to the size of the canvas (WIDTH, HEIGHT).
        - Check if there are other colors on the image besides black and white.
        
    If there are pixels that are 'near-black' (greyscale), they will be changed 
    to black. Otherwise, the preprocessing of the image will fail if there are 
    non-greyscale pixels.
    
    Parameter:
        img: PImage := The image to be preprocessed.
        
    Return Value:
        boolean := If the image was preprocessed successfully.
    '''
    img.resize(WIDTH, HEIGHT)
    img.loadPixels()
    
    for i, p_color in enumerate(img.pixels):
        if p_color in [WHITE_RGB, BLACK_RGB]:
            continue
        elif utils.is_greyscale(p_color):
            r, g, b = utils.get_rgb(p_color)
            if r + g + b < GREYSCALE_THRESHOLD * 3:
                img.pixels[i] = BLACK_RGB
            else:
                img.pixels[i] = WHITE_RGB
        else:
            print('Error: The image contains non-greyscale pixel.')
            return False
    
    return True
