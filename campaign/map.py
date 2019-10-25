#!/usr/bin/env python3


class Map():
    
    def __init__(self):
        
        self.levels = []
        self.accessible = False
        self.accessed = False
        self.finished = False