'''
json format :

img : {name(str): path(str)}
characters : {name(str): [image(str), color_talk_r(int), color_talk_g(int), color_talk_b(int), inventory]}
dialogue : {name(str): [[name_bubble(str), character(str), image(str), x(int), y(int), is_last(bool)]]}
            = {name(str): [Dialogue_Bubble(list)]}
            = {name(str): talk(list)}
'''

from pygame.image import load
from pygame.font import Font
from character import *
from dialogue import *


def T(cw,txt,x,y,r=0,g=0,b=0,aliasing=1,size=20,center=True):
    """allows the display of text on screen with or without centering
    the text will be displayed in the window 'cw'
    """
    font = Font(None, size)
    text = font.render(txt, aliasing, (r, g, b))
    if center:
        textpos = text.get_rect(centery=y,centerx=x)
    else:
        textpos = (x,y)
    cw.blit(text, textpos)


from dialoguebubble import Dialogue_Bubble

def xyinbounds(mx,my,btn):
    """ tests whether (mx,my) is within the bounds of the button btn """
    b1xmin,b1xmax,b1ymin,b1ymax = btn.boundaries()
    return b1xmin <= mx and mx <= b1xmax and b1ymin <= my and my <= b1ymax

def create_img(dct):
    """ creates the full dictionnary of pictures in dct. Used with dct_img. """
    for img in dct:
        dct[img] = load(dct[img]).convert_alpha()
    return dct

def create_char(dict,dict_img):
    for char in dict:
        dict[char] = Character(char,dict_img[dict[char][0]],(dict[char][1],dict[char][2],dict[char][3]),dict[char][4])
    return dict

def create_bubble(list,dict_str,dict_char,dict_img):
    list_bubble = []
    for bubble in list:
        list_bubble.append(Dialogue_Bubble(dict_str[bubble[0]],dict_char[bubble[1]],dict_img[bubble[2]],bubble[3],bubble[4],bubble[5]))
    return list_bubble

def create_dial(dict,dict_str,dict_char,dict_img):
    for dial in dict:
        dict[dial] = Dialogue(create_bubble(dict[dial],dict_str,dict_char,dict_img))
    return dict
