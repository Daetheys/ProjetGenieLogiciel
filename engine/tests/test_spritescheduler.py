import numpy as np
import json
import sys
import os

path = os.getcwd()
path += "/engine"
sys.path.append(path)
path = os.getcwd()
path += "/error"
sys.path.append(path)
from exception import TransitionUndefined
from automata import *
from spriteScheduler import *
from hypothesis import given
from hypothesis.strategies import integers, lists

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
    assert sps.ata.tt[0,'a'] == 1
    assert sps.ata.tt[1,'a'] == 2
    assert sps.ata.tt[2,'a'] == 2
    #testing a run of the sprite scheduler
    sps.step('a')
    assert sps.ata.cs == 1
    sps.step('a')
    assert sps.ata.cs == 2
    sps.step('a')
    assert sps.ata.cs == 2
    sps.step('i')
    assert sps.ata.cs == 0
    sps.step('i')
    assert sps.ata.cs == 0
    sps.step('a')
    assert sps.ata.cs == 1
    sps.step('i')
    assert sps.ata.cs == 2
    try:#testing the TransitionUndefined Error
        sps.step('b')
        assert False
    except TransitionUndefined:
        pass

@given(text(alphabet=characters(blacklist_categories="|,;")),integers(),integers(),integers(),text(alphabet=characters(blacklist_categories="|,;")))
def test_sps(txt,n,x,y,chrs):
    """ testing the generation of a sprite scheduler on randomly-generated data """
    if n <= 0:
        n = len(chrs) + 1
    data = txt+'|'+str(n)+'|'
    for i in range(min(abs(x+y) + 1 + n*len(chrs),3000)):
        data += str((x+i)%n) + ',' + chrs[i%len(chrs)] + '→' + str((y+i)%n) + ';'
    sps = SpriteScheduler(txt)
    sps.ata = create_automaton(data)
    assert sps.ata.cs == 0
    assert sps.ata.name == txt
    assert sps.ata.states == list(range(n))
    assert len(sps.ata.tt) == min(abs(x+y) + 1 + n*len(chrs),3000)
