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
from hypothesis import *
from hypothesis.strategies import *

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

@given(text(min_size=1,max_size=8,alphabet=characters(blacklist_categories=('Cs',),blacklist_characters=("|,;"))),integers(max_value=30),text(min_size=1,max_size=5,alphabet=characters(blacklist_categories=('Cs',),blacklist_characters=("|,;"))))
@settings(max_examples=100)
def test_sps(txt,n,chrs):
    """ testing the generation of a sprite scheduler on randomly-generated data """
    if n <= 0:
        n = len(chrs) + 1
    data = txt+'|'+str(n)+'|'
    seen = []
    for k in range(len(chrs)):
        if chrs[k] not in seen:#to ensure there is no non-determinism
            seen.append(chrs[k])
            for i in range(n):
                for j in range(n):
                    data += str(i) + ',' + chrs[k] + '→' + str(j) + ';'
    sps = SpriteScheduler(txt)
    sps.ata = create_automaton(data)
    assert sps.ata.cs == 0
    assert sps.ata.name == txt
    assert sps.ata.states == list(range(n))
    #assert len(sps.ata.tt) == len(seen)*n*n will soon be fixed
