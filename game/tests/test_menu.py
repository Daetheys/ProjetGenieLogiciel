import pyautogui
pyautogui.FAILSAFE = False
from os import fork,_exit
import os
import signal
from hypothesis import *
from hypothesis.strategies import *
from time import sleep


"""
All tests are now deactivated, again. xvfb still fiddles with forks and kills
Thanks to the launcher class, one can launch several displays in one run.
"""

def test_escape():
    #testing if the escape button works at the root of the menu,
    #introducing various easy ways to test efficiently
    pass
    """
    newpid = fork()
    if newpid:#This first fork is for launching the menu and pyautogui in parallel
        #pass
        Launcher()
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
        Launcher()
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
        Launcher()
        _exit(0)
        sleep(5)
        os.kill(os.getpid(), signal.SIGKILL)
    else:
        sleep(2)
        pyautogui.typewrite(txt)
        pyautogui.press('escape')
"""
