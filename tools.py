from pygame.image import load

def xyinbounds(mx,my,btn):
    b1xmin,b1xmax,b1ymin,b1ymax = btn.boundaries()
    return b1xmin <= mx and mx <= b1xmax and b1ymin <= my and my <= b1ymax

def no_reaction():
    return True, False

def create_img(dct):
    for img in dct:
        dct[img] = load(dct[img]).convert_alpha()
    return dct
