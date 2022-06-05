import const
import utils


def getImage(file_name, ModelConst, preprocess=True):
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
        preprocessImage(img, ModelConst)

    return img


def preprocessImage(img, ModelConst):
    ''' Preprocess the given image. 

    This function performs the following on the image:
        - Resize image to the size of the canvas (WIDTH, HEIGHT).
        - Turn the image into a pure black-and-white image.

    If there are non-black-and-white pixels, they will be converted to grayscale
    and then converted to black or white which depends on the GRAYSCALE_THRESHOLD.

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
            if utils.is_grayscale(p_color):
                r, g, b = utils.get_rgb(p_color)
            else:
                r, g, b = naive_grayscale(p_color)

            if r + g + b < const.GRAYSCALE_THRESHOLD * 3:
                img.pixels[i] = const.BLACK_RGB
            else:
                img.pixels[i] = const.WHITE_RGB


def naive_grayscale(colr):
    '''
    Transform an RGB color to its Grayscale version. Note that this is not the
    best way to do this but if it works :B
    '''
    r, g, b = utils.get_rgb(colr)
    ave = (r + g + b) / 3
    return (ave, ave, ave)