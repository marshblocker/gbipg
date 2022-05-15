from const import *

def displayImage(file_name, preprocess):
    ''' Preprocess (if specified) and display image on the canvas.
    Params:
        file_name: str := Name of the image file. Must be stored in the 'data'
                          folder and must be in PNG format.
        
        preprocess: boolean := If True, preprocessImage() will be called on the 
                               loaded image.
                               
    Return Value:
        boolean := If the image was displayed successfully.
    '''
    if not file_name.endswith('.png'):
        print('Supplied image is not in PNG format.')
        return False
    
    img = loadImage(file_name)
    
    if preprocess: 
        if not preprocessImage(img):
            return False
    
    image(img, 0, 0)
    return True
    
def preprocessImage(img):
    '''
    Preprocess the image before being displayed on the canvas. This function
    performs the following on the image:
        - Resize image to the size of the canvas.
        - Check if there are other colors on the image besides black and white.
        
    For now, preprocessImage() does not change non-B&W colors to B&W, instead
    this fails to preprocess the given image. Hence, make sure the given image
    is pure B&W.
    
    Params:
        img: PImage := The image to be preprocessed.
        
    Return Value:
        boolean := If the image was preprocessed successfully.
    '''
    img.resize(WIDTH, HEIGHT)
    
    # TODO: Check if there are unnecessary colors inside the plate.
    return True
