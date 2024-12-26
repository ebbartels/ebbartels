# %matplotlib inline


""
import random
import time
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        # Set to True if you would like to run gradescope against the challenge AI!
        # Leave as False if you would like to run the gradescope tests faster for debugging.
        # You can still get full credit with this set to False
        return False

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        
        curr = time.time()
        pieces_on_board = sum(row.count('b') + row.count('r') for row in state)
        
        drop_phase = (pieces_on_board < 8)   # TODO: detect drop phase

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            successors = []
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == self.my_piece:
                        successors.extend(self.succ(state, piece=self.my_piece))
            print("succ " + str(curr - time.time()))

            best_value = float("-inf")
            best_move = None

            for succ_state in successors:
                move_value = self.max_value(succ_state, 0, False, float("-inf"), float("inf"))
                if move_value > best_value:
                    best_value = move_value
                    best_move = succ_state
            print("best move " + str(curr - time.time()))

            # Find the move that leads to the best successor
            for i in range(5):
                for j in range(5):
                    if state[i][j] != best_move[i][j]:
                        if best_move[i][j] == self.my_piece:  # Destination of the move
                            dest = (i, j)
                        elif state[i][j] == self.my_piece:  # Source of the move
                            source = (i, j)

            print("move " + str(curr - time.time()))
            return [dest, source]

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        else:
            successors = self.succ(state)
            print("succ " + str(curr - time.time()))
            best_value = float("-inf")
            best_move = None

            for succ_state in successors:
                move_value = self.max_value(succ_state, 0, False, float("-inf"), float("inf"))
                if move_value > best_value:
                    best_value = move_value
                    best_move = succ_state
            print("best move " + str(curr - time.time()))
            # Find the move that leads to the best successor
            for i in range(5):
                for j in range(5):
                    if state[i][j] != best_move[i][j]:  # Difference indicates the new placement
                        print("move " + str(curr - time.time()))
                        return [(i, j)]  # Drop phase move

        #move = []
        #(row, col) = (random.randint(0,4), random.randint(0,4))
        #while not state[row][col] == ' ':
        #    (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        #move.insert(0, (row, col))
        #return move
    
    def succ(self, state, piece = None):
        return_board_states = []

        if piece is None:
            # Drop Phase: Generate all states by placing the piece on empty spaces
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == " ":
                        current_state = copy.deepcopy(state)
                        current_state[i][j] = self.my_piece  # Assume it's this player's turn
                        return_board_states.append(current_state)
        else:
            # Move Phase: Generate states by moving the specified piece
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == piece:
                        x, y = i, j
                        possible_moves = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]

                        for xi, yi in possible_moves:
                            # Check bounds and if the space is empty
                            if 0 <= xi < 5 and 0 <= yi < 5 and state[xi][yi] == " ":
                                current_state = [row[:] for row in state]
                                current_state[xi][yi] = piece  # Move the piece
                                current_state[i][j] = " "  # Vacate the old spot
                                return_board_states.append(current_state)

        return return_board_states
        
    def heuristic_game_value(self, state):
        # return float between -1 and 1
        terminal_state = self.game_value(state)
        if terminal_state != 0:
            return terminal_state

        me = self.my_piece
        opponent = self.opp

        # Detect imminent wins for me or threats from the opponent
        if self.imminent_win(state, me):
            return 1.0  # Maximize for me
        if self.imminent_win(state, opponent):
            return -1.0  # Avoid letting opponent win

        # Line strength heuristic
        line_strength = self.evaluate_lines(state, me, opponent)

        # Positional score (favor center control)
        center_weights = [
            [1, 2, 3, 2, 1],
            [2, 4, 6, 4, 2],
            [3, 6, 9, 6, 3],
            [2, 4, 6, 4, 2],
            [1, 2, 3, 2, 1],
        ]
        position_score = sum(
            center_weights[i][j] if state[i][j] == me else 0
            for i in range(5)
            for j in range(5)
        )

        # Combine scores with weights
        heuristic_value = (
            0.6 * line_strength +  # Increase weight on line strength
            0.4 * position_score   # Adjust position weight
        )

        return heuristic_value
    
    def imminent_win(self, state, player):
        # Check rows and columns for pairs
        for i in range(5):
            if self.count_pieces(state[i], player) == 2 and state[i].count('.') == 2:
                return True  # Row has two pieces and two empty spaces

            column = [state[x][i] for x in range(5)]
            if self.count_pieces(column, player) == 2 and column.count('.') == 2:
                return True  # Column has two pieces and two empty spaces

        # Check diagonals for pairs
        main_diag = [state[i][i] for i in range(5)]
        anti_diag = [state[i][4 - i] for i in range(5)]
        if self.count_pieces(main_diag, player) == 2 and main_diag.count('.') == 2:
            return True  # Main diagonal has two pieces and two empty spaces
        if self.count_pieces(anti_diag, player) == 2 and anti_diag.count('.') == 2:
            return True  # Anti-diagonal has two pieces and two empty spaces

        return False

            
    def count_pieces(self, line, player):
        return sum(1 for piece in line if piece == player)


        # Check diagonals
        main_diag = [state[i][i] for i in range(5)]
        anti_diag = [state[i][4 - i] for i in range(5)]
        if self.count_pieces(main_diag, player) == 3 and '.' in main_diag:
            return True
        if self.count_pieces(anti_diag, player) == 3 and '.' in anti_diag:
            return True

        return False

    
    def evaluate_lines(self, state, me, opponent):
        score = 0
        for i in range(5):
            # Rows
            score += self.line_score(state[i], me, opponent)
            # Columns
            score += self.line_score([state[x][i] for x in range(5)], me, opponent)

        # Diagonals
        main_diag = [state[i][i] for i in range(5)]
        anti_diag = [state[i][4 - i] for i in range(5)]
        score += self.line_score(main_diag, me, opponent)
        score += self.line_score(anti_diag, me, opponent)

        return score

    def line_score(self, line, me, opponent):
        my_count = self.count_pieces(line, me)
        opp_count = self.count_pieces(line, opponent)

        if opp_count > 0 and my_count > 0:
            return 0  # Blocked line
        elif my_count == 3 and '.' in line:
            return 10  # Near win for me
        elif opp_count == 3 and '.' in line:
            return -10  # Opponent threat
        return my_count - opp_count  # General strength

        
    def max_value(self, state, depth, maxing_player, alpha, beta):
        max_depth = 3
        heuristic = self.heuristic_game_value(state)
        
        if depth == max_depth or heuristic == 1 or heuristic == -1:
            return heuristic
        
        succ_states = self.succ(state)
        if maxing_player:
            # maxing player
            evaluation = float("-inf")
            for state in succ_states:
                evaluation = max(evaluation, self.max_value(state, depth + 1, False, alpha, beta))
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return evaluation
        else:
            # mining player
            evaluation = float("inf")
            for state in succ_states:
                evaluation = min(evaluation, self.max_value(state, depth + 1, True, alpha, beta))
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return evaluation
        
        

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for col in range(2):
            for row in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[i][col]==self.my_piece else -1
                
        # TODO: check / diagonal wins
        for col in range(4,2,-1):
            for row in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[i][col]==self.my_piece else -1
        # TODO: check box wins
        for col in range(4):
            for row in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row][col+1] == state[row+1][col+1]:
                    return 1 if state[i][col]==self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
# ###########################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()

""

