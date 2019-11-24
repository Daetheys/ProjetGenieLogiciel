'''
json format :

img : {name(str): path(str)}
characters : {name(str): [image(str), color_talk_r(int), color_talk_g(int), color_talk_b(int), inventory]}
dialogue : {name(str): [[name_bubble(str), character(str), image(str), x(int), y(int), is_last(bool)]]}
            = {name(str): [Dialogue_Bubble(list)]}
            = {name(str): talk(list)}
items : {name(str): [type(str), args*]}
'''

import os
import sys
path = os.getcwd()
path += "/game/campaign"
sys.path.append(path)

from pygame.image import load
from pygame.font import Font
from collections import defaultdict


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


def xyinbounds(mx,my,btn):
    """ tests whether (mx,my) is within the bounds of the button btn """
    b1xmin,b1xmax,b1ymin,b1ymax = btn.boundaries()
    return b1xmin <= mx and mx <= b1xmax and b1ymin <= my and my <= b1ymax

def create_img(dct):
    """ creates the full dictionnary of pictures in dct. Used with dct_img. """
    for img in dct:
        dct[img] = load(dct[img]).convert_alpha()
    return dct

import character
import dialogue
import items

def create_char(dict,dict_img):
    for char in dict:
        dict[char] = character.Character(char,dict_img[dict[char][0]],(dict[char][1],dict[char][2],dict[char][3]),defaultdict(int))
    return dict

def create_item(dict):
    for item in dict:
        if dict[item][0] == "key":
            dict[item] = items.KeyItem(item)
        elif dict[item][0] == "pas":
            dict[item] = items.Passive(item,dict[item][1])
        elif dict[item][0] == "csm":
            dict[item] = items.Consommable(item,dict[item][1])
    return dict

def insert_score(L,score,name,maxn):
    """ insère score,name dans L, en place et retourne L
    L est une liste leaderboard """
    last = True
    for k in range(len(L)):
        if L[k][1] < score:
            name,L[k][0] = L[k][0],name
            score,L[k][1] = L[k][1],score
            if last:
                L[k][2] = True
                last = False
            else:
                L[k][2] = False
        else:
            L[k][2] = False
    if len(L) < maxn:
        L.append([name,score,last])
    return L
    
def score_to_msg(leaderboard):
    msg="LEADERBOARD\n\n"
    for i,score in enumerate(leaderboard):
        if score[2]:
            msg += str(i+1) + ") " + score[0] + " : " + str(score[1]) + "    *\n"
        else:
            msg += str(i+1) + ") " + score[0] + " : " + str(score[1]) + "\n"
    return msg
    
def inv_to_msg(inv):
    msg="INVENTORY\n\n"
    for item in inv:
        msg += item.name + " : " + str(inv[item]) + "\n"
    return msg
