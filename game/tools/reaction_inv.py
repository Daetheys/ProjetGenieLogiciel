
from game.tools.conversion import inv_to_msg
from game.campaign.dialogue import Dialogue
from game.campaign.dialoguebubble import Dialogue_Bubble

def reaction_inv(g):
    """ computes the reaction of the inventory button : It is what is triggered
    when one clicks on the bag-shaped button in the top-left hand corner """
    msg_inv = inv_to_msg(g.player.get_inventory())
    dial_inv = Dialogue([Dialogue_Bubble(msg_inv,g.dict_char["narrator"],g.dict_img["img_leaderboard"],300,50,True)])
    dial_inv.show(g)
    return True,False

