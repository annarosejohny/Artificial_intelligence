from copy import deepcopy
import timeit

#Program for implementing astar algorithm
#Helper function not used

class puzzle:
    # Constructor for initilaizing variables
    def __init__ (self, starting, parent):
        self.board = starting
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0
    
    # Method for calculating manhattan distance
    def manhattan(self):
        h = 0
        # search through the numbers in puzzle
        for i in range(3):
            for j in range(3):
                x, y = divmod(self.board[i][j], 3)
                #calculate manhattan distance based on the points
                h += abs(x-i) + abs(y-j)
        return h
	
    # Method for obtaining mmisplaced tiles heuristics
    def misplaced_tiles(self):
        h = 0
        goal = [[0,1,2],[3,4,5],[6,7,8]]
        # search through the numbers in puzzle
        for i in range(3):
            for j in range(3):
                # make sure we don't check blank tiles
                if (self.board[i][j]!=0):
                    #If it is not in proper place then it is misplaced tile
                    if (self.board[i][j]!=goal):
                        h+=1
        return h
	

    #Method for providing goal state
    def goal(self):
        #Returns True if current board is goal state
        inc = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != inc:
                    return False
                inc += 1
        return True


    def __eq__(self, other):
        return self.board == other.board

#This method will return moves for each node in every iteration till it reaches the goal state and returns total no of nodes with it
def move_function(curr):
    curr = curr.board
    totalnodes=0
    #Finding empty tile '0' from the puzzle board
    for i in range(3):
        for j in range(3):
            if curr[i][j] == 0:
                x, y = i, j
                break
    q = []
    
    #The following codes are used for moving the empty tile in left,right, down and up direction
    #for Left Direction
    if x-1 >= 0:
        b = deepcopy(curr)
        b[x][y]=b[x-1][y]
        b[x-1][y]=0
        succ = puzzle(b, curr)
        q.append(succ)
    
    #For right direction 
    if x+1 < 3:
        b = deepcopy(curr)
        b[x][y]=b[x+1][y]
        b[x+1][y]=0
        succ = puzzle(b, curr)
        q.append(succ)
    
    #for down direction
    if y-1 >= 0:
        b = deepcopy(curr)
        b[x][y]=b[x][y-1]
        b[x][y-1]=0
        succ = puzzle(b, curr)
        q.append(succ)

    #for up direction
    if y+1 < 3:
        b = deepcopy(curr)
        b[x][y]=b[x][y+1]
        b[x][y+1]=0
        succ = puzzle(b, curr)
        q.append(succ)

    return q

#Method for obtaining best f value
def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0: 
            continue
        if(item.f < f):
            f = item.f
            index  = i

    return openList[index], index

#Method to implement A star  search algorithm --> f(n) = g(n)+h(n)
def AStar(start):
    openList = []
    closedList = []
    openList.append(start)

    while openList:
        current, index = best_fvalue(openList)
        if current.goal():
            return current
        openList.pop(index)
        closedList.append(current)

        X = move_function(current)
        for move in X:
            ok = False   #checking in closedList
            for i, item in enumerate(closedList):
                if item == move:
                    ok = True
                    break
            if not ok:              #not in closed list
                newG = current.g + 1 
                present = False

                #openList includes move
                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            openList[j].f = openList[j].g + openList[j].h
                            openList[j].parent = current
                if not present:
                    move.g = newG
                    move.h = move.manhattan()
                    #Use this line for "misplaced tiles heuristics"
                    #move.h = move.misplaced_tiles()
                    move.f = move.g+move.h
                    move.parent = current
                    openList.append(move)

    return nodes

#Method to write the output to output file and print it
def writetofile(start,time,filname,result):
    #This method prints goal state, initial state, time taken and number of moves from initial state to goal state
    noofMoves = 0
    fileoutput=open(filname,'w')
    if(not result):
        print ("No solution")
    else:
        fileoutput.write("Goal State: "+str(result.board)+'\n')
        t=result.parent
    while t:
        noofMoves += 1
        fileoutput.write(str(t.board)+'\n')
        t=t.parent
    fileoutput.write("Initial State: "+str(start)+'\n')
    fileoutput.write("\nTime taken: "+str(time)+'\n')
    fileoutput.write("\nMoves from initial state to goal state: "+str(noofMoves)+'\n')

#Setting up three initial states
start_state1 = [[0, 1, 2],[3, 4, 5],[8, 6, 7]]
start_state2 = [[8, 7, 6],[5, 1, 4],[2, 0, 3]]
start_state3 = [[1, 5, 7],[3, 6, 2],[0, 4, 8]] 
start1 = puzzle(start_state1,None) # Initial Configuration for testing
start2 = puzzle(start_state2,None)# Second Configuration for testing
start3 = puzzle(start_state3,None)# Final Configuration for testing

#for initial state 1
start_time1 = timeit.default_timer()
result1 = AStar(start1)
end_time1 = timeit.default_timer()
time1 = end_time1-start_time1
noofMoves1 = 0
writetofile(start_state1,time1,"a_star_state1.txt",result1)
if(not result1):
    print ("No solution")
else:
    print("Goal State:",result1.board)
    t = result1.parent
    while t:
        noofMoves1 += 1
        print(t.board)
        t = t.parent
print("Start state1:",start_state1)
print("\nMoves from initial state to final state: " + str(noofMoves1))
print("\nTime taken: ",time1)

#for initial state 2
start_time2 = timeit.default_timer()
result2 = AStar(start2)
end_time2 = timeit.default_timer()
time2 = end_time2-start_time2
noofMoves2 = 0
writetofile(start_state2,time2,"a_star_state2.txt",result2)
if(not result2):
    print ("No solution")
else:
    print("Goal State:",result2.board)
    t=result2.parent
    while t:
        noofMoves2 += 1
        print(t.board)
        t=t.parent
print("Start state2:",start_state2)
print("\n Moves from initial state to final state: " + str(noofMoves2))
print("\n Time taken: ",time2)


# For initial state 3
start_time3 = timeit.default_timer()
result3 = AStar(start3)
end_time3 = timeit.default_timer()
time3 = end_time3-start_time3
noofMoves3 = 0
writetofile(start_state3,time3,"a_star_state3.txt",result3)
if(not result3):
    print ("No solution")
else:
    print("Goal State:",result3.board)
    t=result3.parent
    while t:
        noofMoves3 += 1
        print(t.board)
        t=t.parent
print("Start state1:",start_state3)
print("\nMoves from initial state to final state: " + str(noofMoves3))
print("\nTime taken: ",time3)
