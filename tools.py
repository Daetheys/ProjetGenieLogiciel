from pygame.image import load

def xyinbounds(mx,my,btn):
    """ tests whether (mx,my) is within the bounds of the button btn """
    b1xmin,b1xmax,b1ymin,b1ymax = btn.boundaries()
    return b1xmin <= mx and mx <= b1xmax and b1ymin <= my and my <= b1ymax

def create_img(dct):
    """ creates the full dictionnary of pictures in dct. Used with dct_img. """
    for img in dct:
        dct[img] = load(dct[img]).convert_alpha()
    return dct
