import pyautogui
pyautogui.FAILSAFE = False
from os import fork,_exit
import os
import signal
from hypothesis import *
from hypothesis.strategies import *
from time import sleep
from game.game import Game

def test_explanation():
    """
    All tests are now deactivated, again. xvfb still fiddles with forks and kills
    Thanks to the Game class, one can launch several displays in one run.
    However, to interact with the python process, one need another process, because
    the Game() enters an infinite event-catching loop. Therefore, we must fork()
    However, this fork interacts on a deep level with pytest+xvfb in a bad way.
    As a consequence, we cannot test automatically the GUI of this project.
    """
    return 0

"""
def test_launching():
    #testing if the game launches correctly, then killing the process
    newpid = fork()
    if newpid == 0:#This first fork is for launching the menu and the killer in parallel
        #we launch the game
        Game()#contains an infinite loop
    else:
        #we kill it
        sleep(4)
        os.kill(newpid,signal.SIGKILL)
        _exit(0)
        sleep(2)
        os.kill(os.getpid(), signal.SIGKILL)
"""

"""
def test_escape():
    #testing if the escape button works at the root of the menu,
    #introducing various easy ways to test efficiently
    newpid = fork()
    if newpid:#This first fork is for launching the menu and pyautogui in parallel
        Game()
        _exit(0)
        sleep(2)
        os.kill(os.getpid(), signal.SIGKILL)
    else:
        #A second thread, for launching the wait and the remaining tests in parallel
        #could be added
        sleep(1)#wait for the menu to initialize
        pyautogui.press('escape')
"""

"""
def test_exit_button():
    #test if the game quits when exit button is touched

    newpid = fork()
    if newpid:
        Game()
        _exit(0)
        sleep(5)
        os.kill(os.getpid(), signal.SIGKILL)
    else:
        sleep(1)
        pyautogui.moveTo(500, 500, duration=0.2, tween=pyautogui.easeInOutQuad)
        pyautogui.doubleClick()
        pyautogui.moveTo(10, 765, duration=0.3, tween=pyautogui.easeInOutQuad)
        pyautogui.doubleClick()
        sleep(1)
"""
"""
@given(text(min_size=40,max_size=200,alphabet=characters(blacklist_categories=('Cs',),blacklist_characters=("|,;"))))
@settings(max_examples=5,deadline=None)
def test_inputs(txt):
    #test if whether game does crash with randomized inputs
    newpid = fork()
    if newpid:#This first fork is for launching the menu and the typer in parallel
        Game()
        _exit(0)
        sleep(5)
        os.kill(os.getpid(), signal.SIGKILL)
    else:
        sleep(2)
        pyautogui.typewrite(txt)
        pyautogui.press('escape')
"""
