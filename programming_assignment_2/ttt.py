
import time

class TicTacToe:
    def __init__(self):
        self.initialize_game()
        self.row = 0
        self.col = 0
        self.node_count = 0
        self.current_depth = 0


    def initialize_game(self):
        self.current_state = [['.','.','.'],
                            ['.','.','.'],
                            ['.','.','.']]
        self.pruning = 0
        
    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print(self.current_state[i][j], end=" ")
            print()
        print()
    # Determines if the made move is a legal move
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True


    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and
                self.current_state[0][i] == self.current_state[1][i] and
                self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if (self.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'

        # Main diagonal win
        if (self.current_state[0][0] != '.' and
            self.current_state[0][0] == self.current_state[1][1] and
            self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]

        # Second diagonal win
        if (self.current_state[0][2] != '.' and
            self.current_state[0][2] == self.current_state[1][1] and
            self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]

        # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, continue the game
                if (self.current_state[i][j] == '.'):
                    return None

        # It's a tie!
        return '.'
    # choose action to be played by an A.I
    def choose(self,player):
        self.node_count = 0
        if (player=='X'):
            start = time.time()
            (m, px, py) = self.min_score(0)
            end = time.time()
        elif (player=='O'):
            start = time.time()
            (m,px,py) = self.max_score(0)
            end = time.time()
        self.current_state[px][py] = player
        print('Evaluation time: {}s'.format(round(end - start, 7)))
        print('Nodes count',self.node_count)
    
    # A.I player with alpha beta pruning
    def choose_alpha_beta(self,player):
        self.node_count = 0
        if (player=='X'):
            start = time.time()
            (m,px,py) = self.min_alpha_beta(0,-2,2)
            end = time.time()
        if (player=='O'):
            start = time.time()
            (m,px,py) = self.max_alpha_beta(0,-2,2)
            end = time.time()
        self.current_state[px][py] = player
        print('Evaluation time: {}s'.format(round(end - start, 7)))
        print('Nodes count',self.node_count)

    # function for player to move
    def move(self,player):
        px = self.row
        py = self.col - 1

        (qx, qy) = (px, py)

        if self.is_valid(px, py):
            self.current_state[px][py] = player
        else:
            print('The move is not valid! Try again.')

    # max_score function for minimax
    def max_score(self, depth):
        self.node_count += 1
        # -1 - loss
        # 0  - a tie
        # 1  - win

        maxv = -2

        px = None
        py = None

        result = self.is_end()
    
        if (result == 'X'):
            return (-1 + 0.1 * depth, 0, 0)
        elif (result == 'O'):
            return (1 - 0.1 * depth, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    # On the empty field player 'O' makes a move and calls Min
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min_score(depth+1)
                    if i==0:
                        self.row = 'A'
                    elif i==1:
                        self.row = 'B'
                    elif i==2:
                        self.row = 'C'
                    if (depth==0):
                        print('move',self.row,j+1,'score',m)
                    # Fixing the maxv value if needed
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'
        return (maxv, px, py)

    # min function for minimax
    def min_score(self, depth):
        self.node_count += 1
        # -1 - win
        # 0  - a tie
        # 1  - loss

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if (result == 'X'):
            return (-1 + 0.1 * depth, 0, 0) # win
        elif (result == 'O'):
            return (1 - 0.1 * depth, 0, 0) # loss
        elif result == '.':
            return (0, 0, 0) # tie
        
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_score(depth+1)
                    if i==0:
                        self.row = 'A'
                    elif i==1:
                        self.row = 'B'
                    elif i==2:
                        self.row = 'C'
                    if depth==0:
                        print('move',self.row,j+1,'score',m)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'
        return (minv, qx, qy)

    def max_alpha_beta(self, depth,alpha, beta):
        self.node_count+=1
        maxv = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1 + 0.1 * depth, 0, 0)
        elif result == 'O':
            return (1 - 0.1 * depth, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min_alpha_beta(depth+1,alpha, beta)
                    if i==0:
                        self.row = 'A'
                    elif i==1:
                        self.row = 'B'
                    elif i==2:
                        self.row = 'C'
                    if depth==0:
                        print('move',self.row,j+1,'score',m)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    
                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)

    def min_alpha_beta(self, depth,alpha, beta):
        self.node_count +=1
        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1 + 0.1 * depth, 0, 0)
        elif result == 'O':
            return (1 - 0.1 * depth, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(depth+1,alpha, beta)
                    if i==0:
                        self.row = 'A'
                    elif i==1:
                        self.row = 'B'
                    elif i==2:
                        self.row = 'C'
                    if depth==0:
                        print('move',self.row,j+1,'score',m)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == 'X':
                    print('X is the winning player')
                elif self.result == 'O':
                    print('O is the winning player!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return
            
            # taking user input
            user_input= list(input().split())
            action = user_input[0]
            if (len(user_input)>1):
                player = user_input[1]
                if player != 'X' and player != 'O':
                    print('Invalid player')
                    exit()
            if (len(user_input) > 2):
                row = user_input[2]
                col = user_input[3]
                print()
                if (row=='A'):
                    self.row = 0
                elif(row=='B'):
                    self.row = 1
                elif (row=='C'):
                    self.row = 2
                self.col = int(col)
            
            if (action=='pruning'):
                print('pruning =',self.pruning)
            if (action=='pruning_on'):
                self.pruning = 1
                print('pruninng =',self.pruning)
            if (action=='pruning_off'):
                self.pruning = 0
            if (action =='show'):
                self.draw_board()
            if (action == 'reset'):
                self.initialize_game()
            if (action == 'quit'):
                exit()
            # If it's player's turn
            if (action=='move'):
                self.move(player)
            # If it's AI's turn
            if (action == 'choose' and self.pruning==1):
                self.choose_alpha_beta(player)
            elif (action=='choose' and self.pruning==0):
                self.choose(player)
def main():
    input1 = input()
    if (input1=='ttt'):
        print('Welcome To Tic-Tac-Toe!')
        print('You can turn on Alpha/Beta pruning (pruning_on), and the algorithm will run faster according to the number of nodes + evaluation time')
    else:
        exit()
    g = TicTacToe()
    g.play()

if __name__ == "__main__":
    main()