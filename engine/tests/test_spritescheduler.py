import numpy as np
import json
import sys
import os
import pygame

path = os.getcwd()
path += "/engine"
sys.path.append(path)
path = os.getcwd()
path += "/error"
sys.path.append(path)
from exception import TransitionUndefined
from automata import *
from spriteScheduler import *
from hypothesis import *
from hypothesis.strategies import *
from random import randint as rrandint

def assert_well_init(sps,txt):
    assert sps.name == txt
    assert sps.ata is None

@given(text())
@example("")
def test_sps_init(text):
    """ testing the initialization of a SpriteScheduler"""
    sps = SpriteScheduler(text)
    assert_well_init(sps,text)

dict_ata = load_automata()
def test_loaded_sps():
    """ testing the well-functioning of a sprite-scheduler on fixed data """
    sps = SpriteScheduler("ex2")
    assert_well_init(sps,"ex2")
    sps.load_automaton()
    #testing if the right automata has been loaded
    assert sps.name == "ex2"
    assert sps.ata is not None
    assert sps.ata.name == sps.name
    print(sps)
    assert sps.ata.states == [0,1,2]
    assert sps.ata.cs == 0
    #testing the transition table
    assert sps.ata.tt[0,'s'] == 1
    assert sps.ata.tt[1,'s'] == 2
    assert sps.ata.tt[2,'s'] == 2
    #testing a run of the sprite scheduler
    sps.step('s')
    assert sps.ata.cs == 1
    sps.step('s')
    assert sps.ata.cs == 2
    sps.step('s')
    assert sps.ata.cs == 2
    sps.step('i')
    assert sps.ata.cs == 0
    sps.step('i')
    assert sps.ata.cs == 0
    sps.step('s')
    assert sps.ata.cs == 1
    sps.step('i')
    assert sps.ata.cs == 2
    try:#testing the TransitionUndefined Error
        sps.step('b')
        assert False
    except TransitionUndefined:
        pass
    assert sps.ata.qn[sps.ata.cs] == 'data/img/void.png'
    pygame.display.init()
    window = pygame.display.set_mode((10,1))
    sps.load_sprites()
    pygame.display.quit()

@given(text(min_size=1,max_size=8,alphabet=characters(blacklist_categories=('Cs',),blacklist_characters=("|,;"))),integers(max_value=30),text(min_size=1,max_size=5,alphabet=characters(blacklist_categories=('Cs',),blacklist_characters=("|,;"))))
@settings(max_examples=100)
def test_sps(txt,n,chrs):
    """ testing the generation of a sprite scheduler on randomly-generated data """
    if n <= 0:
        n = len(chrs) + 1
    data = txt+'|'+str(n)+'|'
    for i in range(n):
        seen = []
        for k in range(len(chrs)):
            if chrs[k] not in seen:#to ensure there is no non-determinism
                seen.append(chrs[k])
                j = rrandint(0,n - 1)
                data += str(i) + ',' + chrs[k] + '→' + str(j) + ';'
    data += '|0=data/img/void.png,'
    sps = SpriteScheduler(txt)
    sps.ata = create_automaton(data)
    #print(data,seen)
    assert sps.ata.cs == 0
    assert sps.ata.name == txt
    assert sps.ata.states == list(range(n))
    assert len(sps.ata.tt) == len(seen) * n #testing the length of the transition table
    sps.step(chrs[0])
    assert sps.ata.cs == sps.ata.tt[0,chrs[0]]#testing a transition
    try:#testing transitionUndefined
        sps.step(',')#no transition can be defined with this
        assert False
    except TransitionUndefined:
        pass
    for k in range(n*len(chrs)):
        sps.step(chrs[k%len(chrs)])
