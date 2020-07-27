import copy
import time

#No use of helper function
human = 1
pc = 3
empty = "_"
width = int(input("Enter the width of the board:"))
height = int(input("Enter the height of the board:"))
max_depth = 0

class Connect4:
    """ Class for creating Connect4 game environment.
    """
    
    #Class constructor for initlaizing the board
    def __init__(self):
        self.board = [["_" for j in range(width)] for i in range(height)]
        self.col = 0
    
    #Method for placing the chosen val "X or O" in the board according the col chosen. Returns val based on the piece is placed or not.
    def play(self, col, player):

        placed = False
        for i in range(height-1, -1, -1):
            if self.board[i][col] == empty:
                if player == pc:
                    self.board[i][col] = "X"
                else:
                    self.board[i][col] = "O"
                placed = True
                return placed
        if not placed:
            placed = False
            return placed
    
    #Method for counting the number of streaks for human to check whether its draw. This method returns a val based on whether the state of board is draw. 
    def is_draw(self):
        consecutivecount = 0
        for i in range(0, height):  # DRAW
            for j in range(0, width):
                if self.board[i][j] != empty:
                    consecutivecount += 1
                if consecutivecount == 42:
                    return True
        return False
    
    #Method for implementing evaluation function. This helps the utility_function to count the points in the board.
    def get_evaluation(self, x_count, o_count):
        if o_count == 3 and x_count == 0:
            return -50
        elif o_count == 2 and x_count == 0:
            return -10
        elif o_count == 1 and x_count == 0:
            return -1
        elif o_count == 0 and x_count == 1:
            return 1
        elif o_count == 0 and x_count == 2:
            return 10
        elif o_count == 0 and x_count == 3:
            return 50
        return 0
    
    #Method used along with "get_evaluation" to ensure that the current board is win or loss.
    #Returns 512 if won, -512 if lost, 0 if draw, sum of evaluation points
    def utility_function(self):
        if self.is_draw():
            return 0
        x_count = 0
        o_count = 0
        sum = 0
        
        #To check horizontal streak.
        for i in range(0, height):  
            for j in range(0, width-3):
                for k in range(j, j+4):
                    if self.board[i][k] == "X":
                        x_count += 1
                    elif self.board[i][k] == "O":
                        o_count += 1      
                if x_count == 4:
                    return 512
                elif o_count == 4:
                    return -512
                sum += self.get_evaluation(x_count, o_count)
                x_count = 0
                o_count = 0
        
        #To check vertical streak.
        for j in range(0, width):  
            for i in range(0, height-3):
                for k in range(i, i+4):
                    if self.board[k][j] == "X":
                        x_count += 1
                    elif self.board[k][j] == "O":
                        o_count += 1      
                if x_count == 4:
                    return 512
                elif o_count == 4:
                    return -512
                sum += self.get_evaluation(x_count, o_count)
                x_count = 0
                o_count = 0
        #To check diagonal right streak.
        for i in range(3, height):  
            z = i
            for j in range(0, width-3):
                for k in range(j, j+4):
                    if self.board[z][k] == "X":
                        x_count += 1
                    elif self.board[z][k] == "O":
                        o_count += 1
                    z -= 1
                z = i
                if x_count == 4:
                    return 512
                elif o_count == 4:
                    return -512
                sum += self.get_evaluation(x_count, o_count)
                x_count = 0
                o_count = 0
        
        #To check diagonal left streak.
        for i in range(3, height):  
            z = i
            for j in range(width-1, width-5, -1):
                for k in range(j, j-4, -1):
                    if self.board[z][k] == "X":
                        x_count += 1
                    elif self.board[z][k] == "O":
                        o_count += 1
                    z -= 1
                z = i
                if x_count == 4:
                    return 512
                elif o_count == 4:
                    return -512
                sum += self.get_evaluation(x_count, o_count)
                x_count = 0
                o_count = 0
        return sum
    
    #Method for printing the board. We need to enter the vals from 0 to (width-1).
    def print_board(self):
        print("Enter the values between 0 and (width-1)")
        for i in range(height):
            str = "|"
            for j in range(width):
                str += " " + self.board[i][j]
            print(str + " |")

#Method just decides whether ai or human won. Returns a statement based on the final results.
def winner(result, player):
    
    if player == human:
        if result == 0:
            print("Draw!")
        elif result == -512:
            print("Human Won!")
        else:
            print("Human Lost!")
    elif player == pc:
        if result == 0:
            print("Draw!")        
        elif result == 512:
            print("AI Won!")
        else:
            print("AI Lost!")
    else:
        if result == 0:
            print("Draw!")

#Method creates all possible moves the human can make in the  board. 
def succ(board, player):
    temp_board = copy.deepcopy(board)
    child_list = list()
    for i in range(0, width):
        temp_board.play(i, player)
        temp_board.col = i
        child_list.append(temp_board)
        temp_board = copy.deepcopy(board)
    return child_list

#Method for implemeting minimax algorithm. 
def minimax(board, depth):
    #Evaluvating maximizing player
    val = float("-inf")
    col = 0
    for s in succ(board, pc):  # maximizer player
        v = min_minimax(s, depth - 1)
        if v >= val:
            val = v
            col = s.col
    return col
 
#Method for minimizing human, returns the best move.
def min_minimax(board, depth):
    val = board.utility_function()
    if depth == 0 or val in [-512, 512] or board.is_draw():
        return val
    #Evaluting minimzing player
    v = float("inf")
    for s in succ(board, human):
        v = min(v, max_minimax(s, depth - 1))
    return v
    
#Method for maximizing human, returns the best move
def max_minimax(board, depth):
    val = board.utility_function()
    if depth == 0 or val in [-512, 512] or board.is_draw():
        return val
    #Evaluating maximizing player
    v = float("-inf")
    for s in succ(board, pc):
        v = max(v, min_minimax(s, depth - 1))
    return v
    
#Method for implementing alpha-beta pruning.
def alpha_beta(board, depth, alpha, beta):
    val = float("-inf")
    col = 0
    for s in succ(board, pc):
        v = min_alpha_beta(s, depth - 1, alpha, beta)
        if v >= val:
            val = v
            col = s.col
            if val >= beta:
                break
    return col
 
#Method for minimizing human player for alpha-beta, returns best move.
def min_alpha_beta(board, depth, alpha, beta):
    val = board.utility_function()
    if depth == 0 or val in [-512, 512] or board.is_draw():
        return val
    v = float("inf")
    for s in succ(board, human):
        v = min(v, max_alpha_beta(s, depth - 1, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
    
#Method for maximizing human player for alpha-beta, returns the best move.
def max_alpha_beta(board, depth, alpha, beta):
    val = board.utility_function()
    if depth == 0 or val in [-512, 512] or board.is_draw():
        return val
    v = float("-inf")
    for s in succ(board, pc):
        v = max(v, min_alpha_beta(s, depth - 1, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

#Method for choosing among human and ai player. 
def human_ai(board):
    global max_depth
    print("1: Min - max algorithm")
    print("2: Min - max algorithm with alpha-beta pruning")
    ai = input("Option: ")
    depth = 5
    max_depth = depth
    plays_first = input("Do you want to play first? [y/n]: ")
    pc_turn = True

    if plays_first == "y" or plays_first == "yes":
        pc_turn = False

    board.print_board()
    print("Human is 'O' and AI is 'X'")
    print("Press ? if you want the best move.")
    while True:
        if not pc_turn:
            print("Your turn.")
            col = input("Choose the column: ")
            if col == "":
                print("Please enter the column for proceeding!")
            elif col == "?":
                c = alpha_beta(board, depth, float("-inf"), float("+inf"))
                print("Best move: col %d" % c)
            else:
                col = int(col)
                if col == -1:
                    print("Game over")
                    break
                if col > 6 or col < 0:
                    print("Column is not valid!")
                else:
                    if board.play(col, human):
                        board.print_board()
                        if board.is_draw():
                            winner(0, human)
                            break
                        result = board.utility_function()
                        if result in [-512, 512]:
                            winner(result, human)
                            break
                        pc_turn = True
                    else:
                        print("Column %d is full!" % col)
        else:
            print("AI turn.")
            start = time.time()
            if pc == "1":
                b = minimax(board, depth)
            else:
                b = alpha_beta(board, depth, float("-inf"), float("+inf"))
            if board.play(b, pc):
                board.print_board()
                if board.is_draw():
                    winner(0, pc)
                    break
                result = board.utility_function()
                if result in [-512, 512]:
                    winner(result, pc)
                    break
                pc_turn = False
            else:
                print("ERROR!")
                print("Col %d is full!" % b)
                print("AI has no possible moves.")
                break
            end = time.time()
            print("Time taken: %f s" % (end - start))

def start_game():
    board = Connect4()
    human_ai(board)
        
def main():
    print("Connect Four:")
    start_game()

if __name__ == '__main__':
    main()