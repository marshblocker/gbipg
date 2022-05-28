import const
import utils

def getImage(file_name, ModelConst, preprocess = True):
    ''' 
    Preprocess (if specified) given image file and return a PImage object.
    If an error occurred during the preprocessing, this returns None.
    
    Parameters:
        file_name: str := Name of the image file. Must be stored in the 'data'
                          folder and must be in PNG format.

        ModelConst: GBIPG_CONST | MC_CONST
        
        preprocess: boolean := If True, preprocessImage() will be called on the 
                               loaded image. Initially set to True.
                               
    Return Value:
        PImage | None
    '''
    img = loadImage(file_name)
    
    if not img:
        return None
    
    if preprocess: 
        if not preprocessImage(img, ModelConst):
            return None
    
    return img
    
def preprocessImage(img, ModelConst):
    ''' Preprocess the given image. 
    
    This function performs the following on the image:
        - Resize image to the size of the canvas (WIDTH, HEIGHT).
        - Turn the image into a pure black-and-white image.
        
    If there are non-black-and-white pixels, they will be converted to greyscale
    and then converted to black or white depending if they are below or greater
    than or equal to GREYSCALE_THRESHOLD.
    
    Parameter:
        img: PImage := The image to be preprocessed.
        ModelConst: GBIPG_CONST | MC_CONST
        
    Return Value:
        None
    '''
    img.resize(ModelConst.WIDTH, ModelConst.HEIGHT)
    img.loadPixels()
    
    for i, p_color in enumerate(img.pixels):
        if p_color in [const.WHITE_RGB, const.BLACK_RGB]:
            continue
        else:
            r, g, b = (0.0, 0.0, 0.0)
            if utils.is_greyscale(p_color):
                r, g, b = utils.get_rgb(p_color)
            else:
                r, g, b = naive_greyscale(p_color)

            if r + g + b < const.GREYSCALE_THRESHOLD * 3:
                img.pixels[i] = const.BLACK_RGB
            else:
                img.pixels[i] = const.WHITE_RGB
    
    return True

def naive_greyscale(colr):
    r, g, b = utils.get_rgb(colr)
    ave = (r + g + b) / 3
    return (ave, ave, ave)
