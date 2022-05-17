from const import *
import utils

def displayImage(file_name, preprocess = True):
    ''' Preprocess (if specified) and display image on the canvas.
    
    Parameters:
        file_name: str := Name of the image file. Must be stored in the 'data'
                          folder and must be in PNG format.
        
        preprocess: boolean := If True, preprocessImage() will be called on the 
                               loaded image. Initially set to True.
                               
    Return Value:
        boolean := If the image was displayed successfully.
    '''
    if not file_name.endswith('.png'):
        print('Error: Supplied image is not in PNG format.')
        return False
    
    img = loadImage(file_name)
    
    if preprocess: 
        if not preprocessImage(img):
            return False
    
    image(img, 0, 0)
    return True
    
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
        if p_color == WHITE_RGB or p_color == BLACK_RGB:
            continue
        elif utils.is_greyscale(p_color):
            img.pixels[i] = BLACK_RGB
        else:
            print('Error: The image contains non-greyscale pixel.')
            return False
    
    return True
