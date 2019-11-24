

import dialoguebubble
import dialogue
def create_bubble(list,dict_str,dict_char,dict_img):
    list_bubble = []
    for bubble in list:
        list_bubble.append(dialoguebubble.Dialogue_Bubble(dict_str[bubble[0]],dict_char[bubble[1]],dict_img[bubble[2]],bubble[3],bubble[4],bubble[5]))
    return list_bubble

def create_dial(dict,dict_str,dict_char,dict_img):
    for dial in dict:
        dict[dial] = dialogue.Dialogue(create_bubble(dict[dial],dict_str,dict_char,dict_img))
    return dict
