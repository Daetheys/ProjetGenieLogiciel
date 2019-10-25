#!/usr/bin/env python3

class Map_Point:
    
    def __init__(self):
        
        self.accessible = False
        self.accessed = False
        self.finished = False
        self.start_dialogue = None
        self.end_dialogue = None