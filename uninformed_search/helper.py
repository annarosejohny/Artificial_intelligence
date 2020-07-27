#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 01:36:01 2018

@author: Iswariya Manivannan
"""

import sys
import os
import time
from collections import deque
import itertools

class Queue:

    def __init__(self):
        self.queue = deque()
    
    def isEmpty(self):
        return len(self.queue)!=0

    def push(self,x):
        self.queue.append(x)
    
    def get(self):
        return self.queue.popleft()

    def poplast(self):
        return self.queue.pop()
    
    def addFront(self,x):
        self.queue.appendleft(x)

class Maze:
    #Constructor for initializing all variables
    def __init__(self,map):
        
        self.horz_wall = list()
        self.vert_wall = list()
        self.goals = list()
        self.start = tuple()
        self.path = list()
        self.tree = dict()
        self.mazemap = map
        self.w = len(map[0])
        self.h = len(map)
        self.d = self.w*self.h
    
    #Function for finding whether the points are within boundary
    def boundary(self,x):
        
        (j,i) = x
        if (0 <= i <= self.w) and (0 <= j <= self.h):
            return True
        else:
            return False
    
    #Function for finding the neighbors
    def neighbors(self,x):
        (i,j) = x
        results = [(i+1,j),(i,j-1),(i-1,j),(i,j+1)]
        results = filter(self.boundary,results)
        return results
    
    #Function for finding the path from start to goal
    def trace_path(self,goal):
        
        current = goal 
        local_path = list()
        while current !=self.start:
            local_path.append(current)
            current = self.tree[current]
        local_path.append(self.start)
        local_path.reverse()
        return local_path

    #Function for dispalying the output and writing the output in desired file
    def display(self,myFile):
        
        m = open(myFile,"w+")
        s = [['  ']*self.w]*self.h
        for y in range(self.h):
            for x in range(self.w):
                i = (y,x)
                if(i == self.start):
                    s[y][x]="S"
                elif(i in self.goals):
                    s[y][x] ="G"
                elif(i in self.path):
                    parent = self.tree[i]
                    
                    if i[0] == parent[0] + 1: s[y][x] = "v"
                    if i[1] == parent[1] + 1: s[y][x] = ">"
                    if i[1] == parent[1] - 1: s[y][x] = "<" 
                    if i[0] == parent[0] - 1: s[y][x] = "Λ"
                
                elif(i in self.horz_wall):
                    s[y][x] ="="
                
                elif(i in self.vert_wall):
                    s[y][x] ="|"
                else:
                    s[y][x] =" "
                m.write(s[y][x])
            m.write("\n")
        m.close()
    
    #Function that classifies the maze based on symbols as horizontal and vertical walls, start and goal position
    def maze_map_to_tree(self):

        for j in range(self.h):
            for i in range(self.w-1):
                if(self.mazemap[j][i] == "="):
                    self.horz_wall.append((j,i))
                elif(self.mazemap[j][i]=="|"):
                    self.vert_wall.append((j,i))
                elif(self.mazemap[j][i]=="*"):
                    self.goals.append((j,i))
                elif(self.mazemap[j][i]=="s"):
                    self.start = (j,i)
   
    # Method for finding path to each goals and then giving this output to dispaly file
    def write_file(self,myFile):
    
        for i in self.goals:
            if (self.tree.get(i)!=None):
                self.path.append(self.trace_path(i))

        self.path = list(itertools.chain(*self.path))
        self.display(myFile)
    

    # Depth Limited Recursive Method for IDDFS
    def DLS(self,end,depth,queue):

        if not queue.isEmpty():
            return 0
        current = queue.get()

        if(current == end):
            return 1 

        if depth <= 0:
            return 0
        else: 
            for next in self.neighbors(current):
                if next not in self.tree and next not in self.horz_wall and next not in self.vert_wall:
                    self.tree[next] = current 
                    queue.push(next)
            result = self.DLS(end,depth-1,queue)  
            if result ==1:
                return 1  
        return 0       

def maze_map_tree(maze):

    global myMaze
    myMaze = Maze(maze)
    myMaze.maze_map_to_tree()
    return myMaze

def write_to_file(myFile):
    myMaze.write_file(myFile)