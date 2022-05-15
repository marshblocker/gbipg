def print_rgb(colr):
    print(red(colr), green(colr), blue(colr))
    
def is_greyscale(colr):
    '''
    Returns True if the pixel's color is greyscale.
    '''
    r = red(colr)
    g = green(colr)
    b = blue(colr)
    
    if r != g or g != b:
        return False
        
    return True
