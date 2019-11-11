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
    
def create_char(dict,dict_img):
    for char in dict:
        dict[char] = Character(char,dict_img[dict[char][0]],dict[char][1],dict[char][2])
    return dict
    
def create_bubble(list,dict_str,dict_char,dict_img,fen):
    list_bubble = []
    for bubble in list:
        list_bubble.append(Dialogue_Bubble(dict_str[bubble[0]],dict_char[bubble[1]],dict_img[bubble[2]],fen,bubble[3],bubble[4]))
    return list_bubble
    
def create_dial(dict,dict_str,dict_char,dict_img,fen):
    for dial in dict:
        dict[dial] = Dialogue(create_bubble(dict[dial],dict_str,dict_char,dict_img,fen))
    return dict
