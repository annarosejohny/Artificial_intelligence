#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:15:04 2018

@author: Iswariya Manivannan
"""
import sys
import os
from collections import deque
from helper import Maze,Queue,maze_map_tree, write_to_file
sys.setrecursionlimit(4000)
  
def iterative_deepening_depth_first_search(maze_map):

    grid = maze_map_tree(maze_map) 
    print(len(grid.goals))
    for i in list(grid.goals):
       print("Visiting Goal--->",i)
       for depth in range(0,grid.d+1):
            grid.tree = dict()
            grid.tree[grid.start] = None
            myQueue = Queue()
            myQueue.push(grid.start)
            result = grid.DLS(i,depth,myQueue)
            if result == 1:
                break
 
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
    iterative_deepening_depth_first_search(maze_map_map1)
    write_to_file("results/iddfs_map1")

    maze_map_map2 = []
    with open(file_path_map2) as f2:
        maze_map_map2 = f2.readlines()
    iterative_deepening_depth_first_search(maze_map_map2)
    write_to_file("results/iddfs_map2")

    maze_map_map3 = []
    with open(file_path_map3) as f3:
        maze_map_map3 = f3.readlines()
    iterative_deepening_depth_first_search(maze_map_map3)
    write_to_file("results/iddfs_map3")

    # CALL THESE FUNCTIONS after filling in the necessary implementations
    
    # path_map1 = iterative_deepening_depth_first_search(maze_map_map1, start_pos_map1, goal_pos_map1)
    # write_to_file("iddfs_map1", path_map1)

    # path_map2 = iterative_deepening_depth_first_search(maze_map_map2, start_pos_map2, goal_pos_map2)
    # write_to_file("iddfs_map2", path_map2)

    # path_map3 = iterative_deepening_depth_first_search(maze_map_map3, start_pos_map3, goal_pos_map3)
    # write_to_file("iddfs_map3", path_map3)
