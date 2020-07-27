#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:15:04 2018

@author: Iswariya Manivannan
"""
import sys
import os
from collections import deque
from helper import  Maze,Queue,maze_map_tree, write_to_file


def breadth_first_search(map):
    
    grid = maze_map_tree(map)
    myQueue = Queue()
    myQueue.push(grid.start)
    myTree = dict()
    myTree[grid.start] = None
    
    while myQueue.isEmpty():
        current = myQueue.get()
        for next in grid.neighbors(current):
            if next not in myTree and next not in grid.horz_wall and next not in grid.vert_wall:
                myTree[next] = current
                myQueue.push(next)
    grid.tree = myTree


if __name__ == '__main__':

    working_directory = os.getcwd()

    if len(sys.argv) > 1:
        map_directory = sys.argv[1]
    else:
        map_directory = 'maps'

    file_path_map1 = os.path.join(working_directory, map_directory + '/map1.txt')
    file_path_map2 = os.path.join(working_directory, map_directory + '/map2.txt')
    file_path_map3 = os.path.join(working_directory, map_directory + '/map3.txt')

    maze_map_map1 = []
    with open(file_path_map1) as f1:
        maze_map_map1 = f1.readlines()
    breadth_first_search(maze_map_map1)
    write_to_file("results/bfs_map1")

    maze_map_map2 = []
    with open(file_path_map2) as f2:
        maze_map_map2 = f2.readlines()
    breadth_first_search(maze_map_map2)
    write_to_file("results/bfs_map2")

    maze_map_map3 = []
    with open(file_path_map3) as f3:
        maze_map_map3 = f3.readlines()
    breadth_first_search(maze_map_map3)
    write_to_file("results/bfs_map3")


    