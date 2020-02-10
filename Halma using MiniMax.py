from math import sqrt


class Halma:
    def __init__(self, black_pawns, white_pawns, matrix, color_of_play, opp_color, depth):
        self.abdepth = depth
        self.my_color = color_of_play
        self.opponent_color = opp_color
        self.matrix = matrix
        self.white_s = white_pawns
        self.black_s = black_pawns
        self.white = {"destination": self.black_s, "pawns": self.white_s}
        self.black = {"destination": self.white, "pawns": self.black_s}
        self.vertical_distance_white = 0
        self.eval_move = (0, 0)
        self.eval_pawn = (0, 0)
        # Destination of White Pawns
        self.w_pawn_dest_1 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        self.w_pawn_dest_2 = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
        self.w_pawn_dest_3 = [(2, 0), (2, 1), (2, 2), (2, 3)]
        self.w_pawn_dest_4 = [(3, 0), (3, 1), (3, 2)]
        self.w_pawn_dest_5 = [(4, 0), (4, 1)]
        # Destination of Black Pawns
        self.b_pawn_dest_1 = [(15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]
        self.b_pawn_dest_2 = [(14, 11), (14, 12), (14, 13), (14, 14), (14, 15)]
        self.b_pawn_dest_3 = [(13, 12), (13, 13), (13, 14), (13, 15)]
        self.b_pawn_dest_4 = [(12, 13), (12, 14), (12, 15)]
        self.b_pawn_dest_5 = [(11, 14), (11, 15)]
        self.destination_assigned_w = {}
        self.destination_assigned_b = {}
        self.already_in_destination = 0
        # Board end pawn position
        self.core = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]
        self.core_b = [(15, 13), (15, 14), (15, 15), (14, 14), (14, 15), (13, 15)]

    # Returns all the adjacent moves, in all 8 directions
    # All the moves for Single Mode version of the game
    def single_move(self, pawn):
        possible_moves = []
        # All 8 directions
        if self.my_color == "WHITE":
            sm_row = [-1, 0, -1, 1, 0, 1, 1, -1]
            sm_col = [-1, -1, 0, 0, 1, -1, 1, 1]
        else:
            sm_row = [1, 0, 1, -1, -1, 1, 0, -1]
            sm_col = [1, 1, 0, 0, -1, -1, -1, 1]
        for index in range(8):
            coordinate_x = pawn[0] + sm_row[index]
            coordinate_y = pawn[1] + sm_col[index]
            if coordinate_x < 0 or coordinate_x > 15 or coordinate_y < 0 or coordinate_y > 15:
                continue
            if (coordinate_x, coordinate_y) not in self.white["pawns"]:
                if (coordinate_x, coordinate_y) not in self.black["pawns"]:
                    possible_moves.append((coordinate_x, coordinate_y))
        # From the same pawn calculate Jumps also
        for each_jump in self.jumps(pawn, [pawn]):
            possible_moves.append(each_jump)
        return possible_moves

    # Multiple jumps
    def jumps(self, pawn, travelled_path):
        possible_moves = []
        if self.my_color == "WHITE":
            sm_row = [-1, 0, -1, 1, 0, 1, 1, -1]
            sm_col = [-1, -1, 0, 0, 1, -1, 1, 1]
        else:
            sm_row = [1, 0, 1, -1, -1, 1, 0, -1]
            sm_col = [1, 1, 0, 0, -1, -1, -1, 1]
        for index in range(8):
            coordinate_x = pawn[0] + 2*sm_row[index]
            coordinate_y = pawn[1] + 2*sm_col[index]
            if coordinate_x < 0 or coordinate_x > 15 or coordinate_y < 0 or coordinate_y > 15:
                continue
            if (coordinate_x, coordinate_y) not in self.white["pawns"]:
                if (coordinate_x, coordinate_y) not in self.black["pawns"]:
                    check_x = pawn[0] + sm_row[index]
                    check_y = pawn[1] + sm_col[index]
                    if check_x < 0 or check_x > 15 or check_y < 0 or check_y > 15:
                        continue
                    if self.matrix[check_x][check_y] != "." or self.matrix[check_x][check_y] in self.white["pawns"] or self.matrix[check_x][check_y] in self.black["pawns"]:
                            if (coordinate_x, coordinate_y) not in travelled_path:
                                travelled_path.append((coordinate_x, coordinate_y))
                                jumps = self.jumps((coordinate_x, coordinate_y), travelled_path)
                                if jumps:
                                    for jump in jumps:
                                        possible_moves.append([(coordinate_x, coordinate_y)]+jump)
                                else:
                                    possible_moves.append([(coordinate_x, coordinate_y)])
        return possible_moves

    # Moves for game mode
    def single_move_game(self, pawn, board):
        current_white_pawns, current_black_pawns = current_pawn_positions(board)
        possible_moves = []
        # All 8 directions
        sm_row = [0, 1, 0, -1, -1, 1, 1, -1]
        sm_col = [-1, 0, 1, 0, -1, -1, 1, 1]
        for index in range(8):
            coordinate_x = pawn[0] + sm_row[index]
            coordinate_y = pawn[1] + sm_col[index]
            if coordinate_x < 0 or coordinate_x > 15 or coordinate_y < 0 or coordinate_y > 15:
                continue
            if (coordinate_x, coordinate_y) not in current_white_pawns:
                if (coordinate_x, coordinate_y) not in current_black_pawns:
                    possible_moves.append((coordinate_x, coordinate_y))
        # From the same pawn calculate Jumps also
        for each_jump in self.jumps_game(pawn, [pawn], board):
            possible_moves.append(each_jump)
        return possible_moves

    def jumps_game(self, pawn, travelled_path, board):
        current_white_pawns, current_black_pawns = current_pawn_positions(board)
        possible_moves = []
        sm_row = [0, 1, 0, -1, -1, 1, 1, -1]
        sm_col = [-1, 0, 1, 0, -1, -1, 1, 1]
        for index in range(8):
            coordinate_x = pawn[0] + 2*sm_row[index]
            coordinate_y = pawn[1] + 2*sm_col[index]
            if coordinate_x < 0 or coordinate_x > 15 or coordinate_y < 0 or coordinate_y > 15:
                continue
            if (coordinate_x, coordinate_y) not in current_white_pawns:
                if (coordinate_x, coordinate_y) not in current_black_pawns:
                    check_x = pawn[0] + sm_row[index]
                    check_y = pawn[1] + sm_col[index]
                    if check_x < 0 or check_x > 15 or check_y < 0 or check_y > 15:
                        continue
                    if self.matrix[check_x][check_y] != "." or self.matrix[check_x][check_y] in current_white_pawns or self.matrix[check_x][check_y] in current_black_pawns:
                            if (coordinate_x, coordinate_y) not in travelled_path:
                                travelled_path.append((coordinate_x, coordinate_y))
                                jumps = self.jumps_game((coordinate_x, coordinate_y), travelled_path, board)
                                if jumps:
                                    for jump in jumps:
                                        possible_moves.append([(coordinate_x, coordinate_y)]+jump)
                                else:
                                    possible_moves.append([(coordinate_x, coordinate_y)])
        return possible_moves

    # Alpha Beta Pruning and selection of the best move using MiniMax
    def alphabeta(self):
        # Initial Board
        self.abdepth -= 1
        alpha = float('-inf')
        beta = float('inf')
        value = float('-inf')
        # Best Move, yet to choose
        move_to_chose = None
        # If the current player's Pawn color is White
        if self.my_color == "WHITE":
            for pawn in self.white_s:
                # Children of the State i,e: List all possible moves
                moves = self.single_move_game(pawn, self.matrix)
                moves = moves[::-1]
                # Loop through the moves
                self.eval_pawn = pawn
                for move in moves:
                    if type(move) is tuple:
                        self.eval_move = move
                        self.matrix = update_board(self.matrix, pawn, move, self.my_color)
                        value = max(value, self.min_val(self.matrix, alpha, beta))
                        self.matrix = reverse_move(self.matrix, pawn, move, self.my_color)
                        if value > alpha:
                            alpha = value
                            move_to_chose = move
                            from_pawn = pawn
                    else:
                        multiple_moves = []
                        for i in range(len(move)):
                            multiple_moves.append(move[:i+1])
                        multiple_moves = multiple_moves[::-1]
                        for m in multiple_moves:
                            self.eval_move = m[-1]
                            self.matrix = update_board(self.matrix, pawn, m[-1], self.my_color)
                            value = max(value, self.min_val(self.matrix, alpha, beta))
                            self.matrix = reverse_move(self.matrix, pawn, m[-1], self.my_color)
                            if value > alpha:
                                alpha = value
                                move_to_chose = m
                                from_pawn = pawn
        # If the current player's Pawn color is Black
        else:
            for pawn in self.black_s:
                # Children of the State i,e: List all possible moves
                moves = self.single_move_game(pawn, self.matrix)
                moves = moves[::-1]
                self.eval_pawn = pawn
                # Loop through the moves
                for move in moves:
                    if type(move) is tuple:
                        self.eval_move = move
                        self.matrix = update_board(self.matrix, pawn, move, self.my_color)
                        value = max(value, self.min_val(self.matrix, alpha, beta))
                        self.matrix = reverse_move(self.matrix, pawn, move, self.my_color)
                        if value > alpha:
                            alpha = value
                            move_to_chose = move
                            from_pawn = pawn
                    else:
                        multiple_moves = []
                        for i in range(len(move)):
                            multiple_moves.append(move[:i+1])
                        multiple_moves = multiple_moves[::-1]
                        for m in multiple_moves:
                            self.eval_move = m[-1]
                            self.matrix = update_board(self.matrix, pawn, m[-1], self.my_color)
                            value = max(value, self.min_val(self.matrix, alpha, beta))
                            self.matrix = reverse_move(self.matrix, pawn, m[-1], self.my_color)
                            if value > alpha:
                                alpha = value
                                move_to_chose = m
                                from_pawn = pawn
        # Write the Moves to a file.
        if type(move_to_chose) is tuple:
            with open("output.txt", 'w+') as close_f:
                output = "E" + " " + str(from_pawn[1]) + "," + str(from_pawn[0]) + " " + str(move_to_chose[1]) + "," + str(move_to_chose[0])
                close_f.write(output)
        else:
            with open("output.txt", 'w+') as close_f:
                output = "J" + " " + str(from_pawn[1]) + "," + str(from_pawn[0]) + " " + str(move_to_chose[0][1]) + "," + str(move_to_chose[0][0]) + "\n"
                for ind in range(1, len(move_to_chose)-1):
                    output += "J" + " " + str(move_to_chose[ind-1][1]) + "," + str(move_to_chose[ind-1][0]) + " " + str(move_to_chose[ind][1]) + "," + str(move_to_chose[ind][0]) + "\n"
                if len(move_to_chose) > 1:
                    output += "J" + " " + str(move_to_chose[-2][1]) + "," + str(move_to_chose[-2][0]) + " " + str(move_to_chose[-1][1]) + "," + str(move_to_chose[-1][0])
                close_f.write(output)
        return True

    # Maximizing the outcome
    def max_val(self, board, alpha, beta):
        self.abdepth -= 1
        if self.abdepth == 0:
            evaluation_val = self.evaluation()
            self.abdepth += 1
            return evaluation_val
        board_w, board_b = current_pawn_positions(board)
        value = float('-inf')
        if self.my_color == "WHITE":
            for pawn in board_w:
                # Children of the State i,e: all possible moves
                moves = self.single_move_game(pawn, self.matrix)
                moves = moves[::-1]
                # Loop through the moves
                for move in moves:
                    if type(move) is tuple:
                        self.matrix = update_board(self.matrix, pawn, move, self.my_color)
                        value = max(value, self.min_val(self.matrix, alpha, beta))
                        self.matrix = reverse_move(self.matrix, pawn, move, self.my_color)
                        if value >= beta:
                            self.abdepth += 1
                            return value
                        alpha = max(alpha, value)
                    else:
                        multiple_moves = []
                        for i in range(len(move)):
                            multiple_moves.append(move[:i+1])
                        multiple_moves = multiple_moves[::-1]
                        for m in multiple_moves:
                            self.matrix = update_board(board, pawn, m[-1], self.my_color)
                            value = max(value, self.min_val(self.matrix, alpha, beta))
                            self.matrix = reverse_move(self.matrix, pawn, m[-1], self.my_color)
                            if value >= beta:
                                self.abdepth += 1
                                return value
                            alpha = max(alpha, value)
        else:
            for pawn in board_b:
                # Children of the State i,e: all possible moves
                moves = self.single_move_game(pawn, self.matrix)
                moves = moves[::-1]
                # Loop through the moves
                for move in moves:
                    if type(move) is tuple:
                        self.matrix = update_board(board, pawn, move, self.my_color)
                        value = max(value, self.min_val(self.matrix, alpha, beta))
                        self.matrix = reverse_move(self.matrix, pawn, move, self.my_color)
                        if value >= beta:
                            self.abdepth += 1
                            return value
                        alpha = max(alpha, value)
                    else:
                        multiple_moves = []
                        for i in range(len(move)):
                            multiple_moves.append(move[:i+1])
                        multiple_moves = multiple_moves[::-1]
                        for m in multiple_moves:
                            self.matrix = update_board(self.matrix, pawn, m[-1], self.my_color)
                            value = max(value, self.min_val(self.matrix, alpha, beta))
                            self.matrix = reverse_move(self.matrix, pawn, m[-1], self.my_color)
                            if value >= beta:
                                self.abdepth += 1
                                return value
                            alpha = max(alpha, value)
        self.abdepth += 1
        return value

    # Minimizing the outcome
    def min_val(self, board, alpha, beta):
        self.abdepth -= 1
        if self.abdepth == 0:
            evaluation_val = self.evaluation()
            self.abdepth += 1
            return evaluation_val
        board_w, board_b = current_pawn_positions(board)
        value = float('inf')
        if self.opponent_color == "BLACK":
            for pawn in board_b:
                # Children of the State i,e: all possible moves
                moves = self.single_move_game(pawn, self.matrix)
                moves = moves[::-1]
                # Loop through the moves
                for move in moves:
                    if type(move) is tuple:
                        self.matrix = update_board(self.matrix, pawn, move, self.opponent_color)
                        value = min(value, self.max_val(self.matrix, alpha, beta))
                        self.matrix = reverse_move(self.matrix, pawn, move, self.opponent_color)
                        if value <= alpha:
                            self.abdepth += 1
                            return value
                        beta = min(beta, value)
                    else:
                        multiple_moves = []
                        for i in range(len(move)):
                            multiple_moves.append(move[:i+1])
                        multiple_moves = multiple_moves[::-1]
                        for m in multiple_moves:
                            self.matrix = update_board(self.matrix, pawn, m[-1], self.opponent_color)
                            value = min(value, self.max_val(self.matrix, alpha, beta))
                            self.matrix = reverse_move(self.matrix, pawn, m[-1], self.opponent_color)
                            if value <= alpha:
                                self.abdepth += 1
                                return value
                            beta = min(beta, value)
        else:
            for pawn in board_w:
                # Children of the State i,e: all possible moves
                moves = self.single_move_game(pawn, self.matrix)
                # Loop through the moves
                moves = moves[::-1]
                for move in moves:
                    if type(move) is tuple:
                        self.matrix = update_board(self.matrix, pawn, move, self.opponent_color)
                        value = min(value, self.max_val(self.matrix, alpha, beta))
                        self.matrix = reverse_move(self.matrix, pawn, move, self.opponent_color)
                        if value <= alpha:
                            self.abdepth += 1
                            return value
                        beta = min(beta, value)
                    else:
                        multiple_moves = []
                        for i in range(len(move)):
                            multiple_moves.append(move[:i+1])
                        multiple_moves = multiple_moves[::-1]
                        for m in multiple_moves:
                            self.matrix = update_board(self.matrix, pawn, m[-1], self.opponent_color)
                            value = min(value, self.max_val(self.matrix, alpha, beta))
                            self.matrix = reverse_move(self.matrix, pawn, m[-1], self.opponent_color)
                            if value <= alpha:
                                self.abdepth += 1
                                return value
                            beta = min(beta, value)
        self.abdepth += 1
        return value

    # Heuristics
    # Board Evaluation for terminal node, when depth is n
    def evaluation(self):
        w_pawn_position, b_pawn_position = current_pawn_positions(self.matrix)
        evaluation_val = 0
        current_pawn = self.eval_pawn
        current_move = self.eval_move
        w_pawn_dest = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
        b_pawn_dest = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]
        if self.my_color == "WHITE":
            if self.already_in_destination <= 17:
                # Assigning certain values based on how far the pawns are.
                if current_pawn in self.w_pawn_dest_1 and (current_move in self.w_pawn_dest_2 or current_move in self.w_pawn_dest_3 or current_move in self.w_pawn_dest_4 or current_move in self.w_pawn_dest_5):
                    evaluation_val -= 7
                if current_pawn in self.w_pawn_dest_2 and (current_move in self.w_pawn_dest_3 or current_move in self.w_pawn_dest_4 or current_move in self.w_pawn_dest_5):
                    evaluation_val -= 7
                if current_pawn in self.w_pawn_dest_3 and (current_move in self.w_pawn_dest_4 or current_move in self.w_pawn_dest_5):
                    evaluation_val -= 7
                if current_pawn in self.w_pawn_dest_4 and current_move in self.w_pawn_dest_5:
                    evaluation_val -= 7
                if current_move in self.core:
                    evaluation_val += 35
                if current_pawn in self.core and current_move not in w_pawn_dest:
                    evaluation_val -= 1500
                if current_pawn in w_pawn_dest and current_move in w_pawn_dest:
                    evaluation_val += 7
                if current_pawn in w_pawn_dest and current_move not in w_pawn_dest:
                    evaluation_val -= 130000
                if current_pawn not in w_pawn_dest and current_move in w_pawn_dest:
                    evaluation_val += 20

                dist = eucledian(self.destination_assigned_w[current_pawn], current_pawn)
                evaluation_val += dist*7
                # check
                if ((15-current_move[0])+(15-current_move[1])) <= ((15-current_pawn[0])+(15-current_pawn[1])):
                    evaluation_val -= 22

                if current_move in self.w_pawn_dest_1:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 12
                if current_move in self.w_pawn_dest_2:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 11
                if current_move in self.w_pawn_dest_3:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 10
                if current_move in self.w_pawn_dest_4:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 9
                if current_move in self.w_pawn_dest_5:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 8
                for pawn in w_pawn_position:
                    distance = (pawn[0]-0) + (pawn[1]-0)
                    if distance == 0:
                        evaluation_val += 200
                    elif distance == 1:
                        evaluation_val += 190
                    elif distance == 2:
                        evaluation_val += 180
                    elif distance == 3:
                        evaluation_val += 170
                    elif distance == 4:
                        evaluation_val += 160
                    elif 5 <= distance <= 11:
                        evaluation_val += 150
                    elif 11 < distance <= 14:
                        evaluation_val += 140
                    elif 14 < distance <= 18:
                        evaluation_val += 120
                    elif 18 < distance <= 21:
                        evaluation_val += 110
                    elif 21 < distance <= 24:
                        evaluation_val += 100
                    elif 24 < distance <= 27:
                        evaluation_val += 90
                    elif 27 < distance <= 30:
                        evaluation_val += 80
            else:
                if current_pawn in w_pawn_dest and current_move not in w_pawn_dest:
                    evaluation_val -= 500000
                if current_pawn not in w_pawn_dest and current_move in w_pawn_dest:
                    evaluation_val += 30
                if current_move in self.w_pawn_dest_1:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 12
                if current_move in self.w_pawn_dest_2:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 11
                if current_move in self.w_pawn_dest_3:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 10
                if current_move in self.w_pawn_dest_4:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 11
                if current_move in self.w_pawn_dest_5:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 12
                # Previous data
                val = ()
                for dest in w_pawn_dest:
                    if self.matrix[dest[0]][dest[1]] == ".":
                        val = (dest[0], dest[1])
                        break
                    else:
                        continue
                # If 0 all pawns in destination
                if len(val) == 0:
                    evaluation_val += 70

                if len(val) != 0:
                    if (abs(current_pawn[0]-val[0]) + abs(current_pawn[1]-val[1])) <= (abs(current_move[0] - val[0]) + abs(current_move[1] - val[1])):
                        evaluation_val -= 50
                    else:
                        evaluation_val += 400

                if current_pawn in w_pawn_dest and current_move not in w_pawn_dest:
                    evaluation_val -= 20000
                if current_pawn not in w_pawn_dest and current_move in w_pawn_dest:
                    evaluation_val += 200
                if current_pawn in w_pawn_dest and current_move in w_pawn_dest:
                    evaluation_val += 15

        if self.my_color == "BLACK":
            if self.already_in_destination <= 17:
                if current_pawn in self.b_pawn_dest_1 and (current_move in self.b_pawn_dest_2 or current_move in self.b_pawn_dest_3 or current_move in self.b_pawn_dest_4 or current_move in self.b_pawn_dest_5):
                    evaluation_val -= 7
                if current_pawn in self.b_pawn_dest_2 and (current_move in self.b_pawn_dest_3 or current_move in self.b_pawn_dest_4 or current_move in self.b_pawn_dest_5):
                    evaluation_val -= 7
                if current_pawn in self.b_pawn_dest_3 and (current_move in self.b_pawn_dest_4 or current_move in self.b_pawn_dest_5):
                    evaluation_val -= 7
                if current_pawn in self.b_pawn_dest_4 and current_move in self.b_pawn_dest_5:
                    evaluation_val -= 7
                # add core
                if current_move in self.core_b:
                    evaluation_val += 35
                if current_pawn in self.core_b and current_move not in w_pawn_dest:
                    evaluation_val -= 1500
                if current_pawn in b_pawn_dest and current_move in b_pawn_dest:
                    evaluation_val += 7
                if current_pawn in b_pawn_dest and current_move not in b_pawn_dest:
                    evaluation_val -= 130000
                if current_pawn not in b_pawn_dest and current_move in b_pawn_dest:
                    evaluation_val += 20

                dist = eucledian(current_pawn, self.destination_assigned_b[current_pawn])
                evaluation_val += dist*7

                # check
                if ((current_move[0]-0)+(current_move[1]-0)) <= ((current_pawn[0]-0)+(current_pawn[1]-0)):
                    evaluation_val -= 22

                if current_move in self.b_pawn_dest_1:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 12
                if current_move in self.b_pawn_dest_2:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 11
                if current_move in self.b_pawn_dest_3:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 10
                if current_move in self.b_pawn_dest_4:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 9
                if current_move in self.b_pawn_dest_5:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 8

                for pawn in b_pawn_position:
                    distance = (15-pawn[0]) + (15-pawn[1])
                    if distance == 0:
                        evaluation_val += 200
                    elif distance == 1:
                        evaluation_val += 190
                    elif distance == 2:
                        evaluation_val += 180
                    elif distance == 3:
                        evaluation_val += 170
                    elif distance == 4:
                        evaluation_val += 160
                    elif 5 <= distance <= 11:
                        evaluation_val += 150
                    elif 11 < distance <= 14:
                        evaluation_val += 140
                    elif 14 < distance <= 18:
                        evaluation_val += 120
                    elif 18 < distance <= 21:
                        evaluation_val += 110
                    elif 21 < distance <= 24:
                        evaluation_val += 100
                    elif 24 < distance <= 27:
                        evaluation_val += 90
                    elif 27 < distance <= 30:
                        evaluation_val += 80
            else:
                if current_pawn in b_pawn_dest and current_move not in b_pawn_dest:
                    evaluation_val -= 500000
                if current_pawn not in b_pawn_dest and current_move in b_pawn_dest:
                    evaluation_val += 30
                if current_move in self.b_pawn_dest_1:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 12
                if current_move in self.b_pawn_dest_2:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 11
                if current_move in self.b_pawn_dest_3:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 10
                if current_move in self.b_pawn_dest_4:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 11
                if current_move in self.b_pawn_dest_5:
                    if self.matrix[current_move[0]][current_move[1]] == ".":
                        evaluation_val += 12

                # checking destination values
                val = ()
                for dest in b_pawn_dest:
                    if self.matrix[dest[0]][dest[1]] == ".":
                        val = (dest[0], dest[1])
                        break
                    else:
                        continue
                # If 0 all pawns in destination
                if len(val) == 0:
                    evaluation_val += 70

                if len(val) != 0:
                    if (abs(val[0]-current_pawn[0]) + abs(val[1]-current_pawn[1])) <= (abs(val[0]-current_move[0]) + abs(val[1]-current_move[1])):
                        evaluation_val -= 50
                    else:
                        evaluation_val += 400
                # print("current pawn", current_pawn, "current move", current_move, "val", val)
                if current_pawn in b_pawn_dest and current_move not in b_pawn_dest:
                    evaluation_val -= 20000
                if current_pawn not in b_pawn_dest and current_move in b_pawn_dest:
                    evaluation_val += 200
                if current_pawn in b_pawn_dest and current_move in b_pawn_dest:
                    evaluation_val += 15
        return evaluation_val


# Returns back to the old state of the board
def reverse_move(board, pawn, move, color):
    if color == "WHITE":
        s_x, s_y = move[0], move[1]
        d_x, d_y = pawn[0], pawn[1]
        board[s_x][s_y] = "."
        board[d_x][d_y] = "W"
    else:
        s_x, s_y = move[0], move[1]
        d_x, d_y = pawn[0], pawn[1]
        board[s_x][s_y] = "."
        board[d_x][d_y] = "B"
    return board


# Updates Board Value after pawn is moved
def update_board(board, pawn, move, color):
    if color == "WHITE":
        s_x, s_y = pawn[0], pawn[1]
        d_x, d_y = move[0], move[1]
        board[s_x][s_y] = "."
        board[d_x][d_y] = "W"
    else:
        s_x, s_y = pawn[0], pawn[1]
        d_x, d_y = move[0], move[1]
        board[s_x][s_y] = "."
        board[d_x][d_y] = "B"
    return board


# Returns the Co-ordinates of the board for both Black and White pawns
def current_pawn_positions(matrix):
    w_pawn_position = []
    b_pawn_position = []
    for index_i in range(16):
            for index_j in range(16):
                if matrix[index_i][index_j] == 'W':
                    w_pawn_position.append((index_i, index_j))
                elif matrix[index_i][index_j] == 'B':
                    b_pawn_position.append((index_i, index_j))
                else:
                    continue
    return w_pawn_position, b_pawn_position


# Assigning Destination for the player, based the pawn color
def destination_assignment(matrix):
    w_pawn_with_destination = {}
    b_pawn_with_destination = {}
    dest_black = [(11, 15), (11, 14), (12, 15), (12, 14), (12, 13), (13, 15), (13, 14), (13, 13), (13, 12), (14, 15), (14, 15), (14, 13), (14, 12), (14, 11), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11)]
    dest_white = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    for index_i in range(16):
            for index_j in range(16):
                if matrix[index_i][index_j] == 'W':
                    des = dest_white.pop(0)
                    w_pawn_with_destination[(index_i, index_j)] = des
                elif matrix[index_i][index_j] == 'B':
                    des = dest_black.pop(0)
                    b_pawn_with_destination[(index_i, index_j)] = des
                else:
                    continue
    return w_pawn_with_destination, b_pawn_with_destination


# Function to calculate Eucledian Distance
def eucledian(p1, p2):
    return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)


# Reversing the board pawn position after determining the best moves
def reversing_elements(matrix, color):
    wr_pawns = []
    br_pawns = []
    if color == "WHITE":
        for i in range(15, -1, -1):
            for j in range(16):
                if matrix[i][j] == 'W':
                    wr_pawns.append((i, j))
                elif matrix[i][j] == 'B':
                    br_pawns.append((i, j))
                else:
                    continue
    else:
        for i in range(16):
            for j in range(15, -1, -1):
                if matrix[i][j] == 'W':
                    wr_pawns.append((i, j))
                elif matrix[i][j] == 'B':
                    br_pawns.append((i, j))
                else:
                    continue
    return wr_pawns, br_pawns


# Reading and processing the input
def main():
    with open("input.txt", 'r') as f:
        mode = f.readline().strip('\n')
        color_of_play = f.readline().strip('\n')
        if color_of_play == "WHITE":
            opponent_color = "BLACK"
        else:
            opponent_color = "WHITE"
        time_remaining = float(f.readline())
        matrix = []
        for i in range(16):
            line = f.readline()
            row = [char for char in line]
            row = row[:16]
            matrix.append(row)
    # Reading the current board State
    w_pawn_position, b_pawn_position = current_pawn_positions(matrix)
    w_pawn_position = w_pawn_position[::-1]

    # Actually allocated start places
    start_w = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]
    start_b = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    start_w = start_w[::-1]

    # White and black pawn destination
    w_destination = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]
    b_destination = [(11, 14), (11, 15), (12, 13), (12, 14), (12, 15), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)]

    pawn_moves_inside = {}
    pawn_moves_outside = {}
    pawn_outside_to_inside = {}
    pawn_outside_moves = {}

    w_opp_corner = (0, 0)
    b_opp_corner = (15, 15)

    # IF MODE IS SINGLE
    if mode == "SINGLE":
        obj = Halma(b_pawn_position, w_pawn_position, matrix, color_of_play, opponent_color, 3)
        # If our color of play is BLACK
        if color_of_play == "BLACK":
            for b_pawn in obj.black_s:
                pawn_moves_inside_l = []
                pawn_moves_outside_l = []
                pawn_outside_to_inside_l = []
                pawn_outside_moves_l = []
                moves = obj.single_move(b_pawn)
                for move in moves:
                    if type(move) is tuple:
                        if b_pawn in start_b and move in start_b:
                            if (move[0]-0)+(move[1]-0) <= (b_pawn[0]-0)+(b_pawn[1]-0):
                                continue
                            if eucledian(b_pawn, b_opp_corner) <= eucledian(move, b_opp_corner):
                                continue
                            pawn_moves_inside_l.append(move)
                        elif b_pawn in start_b and move not in start_b:
                            pawn_moves_outside_l.append(move)
                        elif b_pawn not in start_b and move in start_b:
                            pawn_outside_to_inside_l.append(move)
                        else:
                            if b_pawn in b_destination and move not in b_destination:
                                continue
                            pawn_outside_moves_l.append(move)
                    else:
                        for index, inner_move in enumerate(move):
                            if b_pawn in start_b and inner_move in start_b:
                                if (inner_move[0]-0)+(inner_move[1]-0) <= (b_pawn[0]-0)+(b_pawn[1]-0):
                                    continue
                                if eucledian(b_pawn, b_opp_corner) <= eucledian(inner_move, b_opp_corner):
                                    continue
                                pawn_moves_inside_l.append(move[:index+1])
                            elif b_pawn in start_b and inner_move not in start_b:
                                pawn_moves_outside_l.append(move[:index+1])
                            elif b_pawn not in start_b and inner_move in start_b:
                                pawn_outside_to_inside_l.append(move[:index+1])
                            else:
                                if b_pawn in b_destination and inner_move not in b_destination:
                                    continue
                                pawn_outside_moves_l.append(move[:index+1])
                if pawn_moves_inside_l:
                    pawn_moves_inside[b_pawn] = pawn_moves_inside_l[::-1]
                if pawn_moves_outside_l:
                    pawn_moves_outside[b_pawn] = pawn_moves_outside_l[::-1]
                if pawn_outside_to_inside_l:
                    pawn_outside_to_inside[b_pawn] = pawn_outside_to_inside_l[::-1]
                if pawn_outside_moves_l:
                    pawn_outside_moves[b_pawn] = pawn_outside_moves_l[::-1]
            # If our color of play is WHITE
        else:
            for w_pawn in obj.white_s:
                moves = obj.single_move(w_pawn)
                pawn_moves_inside_l = []
                pawn_moves_outside_l = []
                pawn_outside_to_inside_l = []
                pawn_outside_moves_l = []
                for move in moves:
                    if type(move) is tuple:
                        if w_pawn in start_w and move in start_w:
                            if (15-move[0])+(15-move[1]) <= (15-w_pawn[0])+(15-w_pawn[1]):
                                continue
                            if eucledian(w_opp_corner, w_pawn) <= eucledian(w_opp_corner, move):
                                continue
                            pawn_moves_inside_l.append(move)
                        elif w_pawn in start_w and move not in start_w:
                            pawn_moves_outside_l.append(move)
                        elif w_pawn not in start_w and move in start_w:
                            pawn_outside_to_inside_l.append(move)
                        else:
                            if w_pawn in w_destination and move not in w_destination:
                                continue
                            pawn_outside_moves_l.append(move)
                    else:
                        for index, inner_move in enumerate(move):
                            if w_pawn in start_w and inner_move in start_w:
                                if (15-inner_move[0])+(15-inner_move[1]) <= (15-w_pawn[0])+(15-w_pawn[1]):
                                    continue
                                if eucledian(w_opp_corner, w_pawn) <= eucledian(w_opp_corner, inner_move):
                                    continue
                                pawn_moves_inside_l.append(move[:index+1])
                            elif w_pawn in start_w and inner_move not in start_w:
                                pawn_moves_outside_l.append(move[:index+1])
                            elif w_pawn not in start_w and inner_move in start_w:
                                pawn_outside_to_inside_l.append(move[:index+1])
                            else:
                                if w_pawn in w_destination and inner_move not in w_destination:
                                    continue
                                pawn_outside_moves_l.append(move[:index+1])
                if pawn_moves_inside_l:
                    pawn_moves_inside[w_pawn] = pawn_moves_inside_l[::-1]
                if pawn_moves_outside_l:
                    pawn_moves_outside[w_pawn] = pawn_moves_outside_l[::-1]
                if pawn_outside_to_inside_l:
                    pawn_outside_to_inside[w_pawn] = pawn_outside_to_inside_l[::-1]
                if pawn_outside_moves_l:
                    pawn_outside_moves[w_pawn] = pawn_outside_moves_l[::-1]
        if pawn_moves_outside:
            key = next(iter(pawn_moves_outside))
            move_list = pawn_moves_outside[key]
            if type(move_list[0]) is tuple:
                with open("output.txt", 'w+') as close_f:
                    output = "E" + " " + str(key[1]) + "," + str(key[0]) + " " + str(move_list[0][1]) + "," + str(move_list[0][0])
                    close_f.write(output)
                    exit(0)
            else:
                m_list = move_list[0]
                with open("output.txt", 'w+') as close_f:
                    output = "J" + " " + str(key[1]) + "," + str(key[0]) + " " + str(m_list[0][1]) + "," + str(m_list[0][0]) + "\n"
                    for ind in range(1, len(m_list)-1):
                        output += "J" + " " + str(m_list[ind-1][1]) + "," + str(m_list[ind-1][0]) + " " + str(m_list[ind][1]) + "," + str(m_list[ind][0]) + "\n"
                    if len(m_list) > 1:
                        output += "J" + " " + str(m_list[-2][1]) + "," + str(m_list[-2][0]) + " " + str(m_list[-1][1]) + "," + str(m_list[-1][0])
                    close_f.write(output)
                    exit(0)

        elif pawn_moves_inside:
            key = next(iter(pawn_moves_inside))
            move_list = pawn_moves_inside[key]
            if type(move_list[0]) is tuple:
                with open("output.txt", 'w+') as close_f:
                    output = "E" + " " + str(key[1]) + "," + str(key[0]) + " " + str(move_list[0][1]) + "," + str(move_list[0][0])
                    close_f.write(output)
                    exit(0)
            else:
                m_list = move_list[0]
                with open("output.txt", 'w+') as close_f:
                    output = "J" + " " + str(key[1]) + "," + str(key[0]) + " " + str(m_list[0][1]) + "," + str(m_list[0][0]) + "\n"
                    for ind in range(1, len(m_list)-1):
                        output += "J" + " " + str(m_list[ind-1][1]) + "," + str(m_list[ind-1][0]) + " " + str(m_list[ind][1]) + "," + str(m_list[ind][0]) + "\n"
                    if len(m_list) > 1:
                        output += "J" + " " + str(m_list[-2][1]) + "," + str(m_list[-2][0]) + " " + str(m_list[-1][1]) + "," + str(m_list[-1][0])
                    close_f.write(output)
                    exit(0)
        elif pawn_outside_moves:
            key = next(iter(pawn_outside_moves))
            move_list = pawn_outside_moves[key]
            if type(move_list[0]) is tuple:
                with open("output.txt", 'w+') as close_f:
                    output = "E" + " " + str(key[1]) + "," + str(key[0]) + " " + str(move_list[0][1]) + "," + str(move_list[0][0])
                    close_f.write(output)
                    exit(0)
            else:
                m_list = move_list[0]
                with open("output.txt", 'w+') as close_f:
                    output = "J" + " " + str(key[1]) + "," + str(key[0]) + " " + str(m_list[0][1]) + "," + str(m_list[0][0]) + "\n"
                    for ind in range(1, len(m_list)-1):
                        output += "J" + " " + str(m_list[ind-1][1]) + "," + str(m_list[ind-1][0]) + " " + str(m_list[ind][1]) + "," + str(m_list[ind][0]) + "\n"
                    if len(m_list) > 1:
                        output += "J" + " " + str(m_list[-2][1]) + "," + str(m_list[-2][0]) + " " + str(m_list[-1][1]) + "," + str(m_list[-1][0])
                    close_f.write(output)
                    exit(0)

    # IF MODE IS GAME
    else:
        # Initialize Board
        obj = Halma(b_pawn_position, w_pawn_position, matrix, color_of_play, opponent_color, 3)
        # Assigning destination
        w_dest, b_dest = destination_assignment(matrix)
        obj.destination_assigned_w = w_dest
        obj.destination_assigned_b = b_dest
        if color_of_play == "BLACK":
            # Number of pawns in Source
            source_count = 0
            for s_bp in start_b:
                if matrix[s_bp[0]][s_bp[1]] == "B":
                    source_count += 1
                else:
                    continue
            move_coded = {0: [(4, 0), (4, 2)], 1: [(4, 1), (4, 3)], 2: [(0, 3), [(2, 5)]], 3: [(1, 4), [(3, 6)]], 4: [(0, 4), (0, 5)]}
            # calculate pawns in destination
            if source_count > 14:
                index = 19-source_count
                pawnAndMove = move_coded[index]
                p = pawnAndMove[0]
                m = pawnAndMove[1]
                if type(m) is tuple:
                    with open("output.txt", 'w+') as close_f:
                        output = "E" + " " + str(p[1]) + "," + str(p[0]) + " " + str(m[1]) + "," + str(m[0])
                        close_f.write(output)
                        exit(0)
                else:
                    with open("output.txt", 'w+') as close_f:
                        output = "J" + " " + str(p[1]) + "," + str(p[0]) + " " + str(m[0][1]) + "," + str(m[0][0])
                        close_f.write(output)
                        exit(0)
            elif source_count <= 14:
                count = 0
                for pawnInDestinationB in b_pawn_position:
                    if pawnInDestinationB in start_w:
                        count += 1
                obj.already_in_destination = count
                wr_pawns, br_pawns = reversing_elements(matrix, color_of_play)
                # print("BLACK REVERSED", br_pawns)
                for b_pawn in br_pawns:
                    pawn_moves_inside_l = []
                    pawn_moves_outside_l = []
                    pawn_outside_to_inside_l = []
                    pawn_outside_moves_l = []
                    moves = obj.single_move(b_pawn)
                    for move in moves:
                        if type(move) is tuple:
                            if b_pawn in start_b and move in start_b:
                                if (move[0]-0)+(move[1]-0) <= (b_pawn[0]-0)+(b_pawn[1]-0):
                                    continue
                                if eucledian(b_pawn, b_opp_corner) <= eucledian(move, b_opp_corner):
                                    continue
                                pawn_moves_inside_l.append(move)
                            elif b_pawn in start_b and move not in start_b:
                                pawn_moves_outside_l.append(move)
                            elif b_pawn not in start_b and move in start_b:
                                pawn_outside_to_inside_l.append(move)
                            else:
                                pawn_outside_moves_l.append(move)
                        else:
                            for index, inner_move in enumerate(move):
                                if b_pawn in start_b and inner_move in start_b:
                                    if (inner_move[0]-0)+(inner_move[1]-0) <= (b_pawn[0]-0)+(b_pawn[1]-0):
                                        continue
                                    if eucledian(b_pawn, b_opp_corner) <= eucledian(inner_move, b_opp_corner):
                                        continue
                                    pawn_moves_inside_l.append(move[:index+1])
                                elif b_pawn in start_b and inner_move not in start_b:
                                    pawn_moves_outside_l.append(move[:index+1])
                                elif b_pawn not in start_b and inner_move in start_b:
                                    pawn_outside_to_inside_l.append(move[:index+1])
                                else:
                                    pawn_outside_moves_l.append(move[:index+1])
                    if pawn_moves_inside_l:
                        pawn_moves_inside[b_pawn] = pawn_moves_inside_l[::-1]
                    if pawn_moves_outside_l:
                        pawn_moves_outside[b_pawn] = pawn_moves_outside_l[::-1]
                    if pawn_outside_to_inside_l:
                        pawn_outside_to_inside[b_pawn] = pawn_outside_to_inside_l[::-1]
                    if pawn_outside_moves_l:
                        pawn_outside_moves[b_pawn] = pawn_outside_moves_l[::-1]
        # If our color of play is WHITE
        else:
            # Number of pawns in source
            source_count = 0
            for s_wp in start_w:
                if matrix[s_wp[0]][s_wp[1]] == "W":
                    source_count += 1
                else:
                    continue
            move_coded = {0: [(11, 15), (11, 13)], 1: [(11, 14), (11, 12)], 2: [(15, 12), [(13, 10)]], 3: [(14, 11), [(12, 9)]], 4: [(15, 11), (15, 10)]}
            # calculate pawns in destination
            if source_count > 14:
                index = 19-source_count
                pawnAndMove = move_coded[index]
                p = pawnAndMove[0]
                m = pawnAndMove[1]
                if type(m) is tuple:
                    with open("output.txt", 'w+') as close_f:
                        output = "E" + " " + str(p[1]) + "," + str(p[0]) + " " + str(m[1]) + "," + str(m[0])
                        close_f.write(output)
                        exit(0)
                else:
                    with open("output.txt", 'w+') as close_f:
                        output = "J" + " " + str(p[1]) + "," + str(p[0]) + " " + str(m[0][1]) + "," + str(m[0][0])
                        close_f.write(output)
                        exit(0)

            elif source_count <= 14:
                count = 0
                for pawnInDestinationW in w_pawn_position:
                    if pawnInDestinationW in start_b:
                        count += 1
                obj.already_in_destination = count
                wr_pawns, br_pawns = reversing_elements(matrix, color_of_play)
                # print("WHITE REVERSED", wr_pawns)
                for w_pawn in wr_pawns:
                    moves = obj.single_move(w_pawn)
                    pawn_moves_inside_l = []
                    pawn_moves_outside_l = []
                    pawn_outside_to_inside_l = []
                    pawn_outside_moves_l = []
                    for move in moves:
                        if type(move) is tuple:
                            if w_pawn in start_w and move in start_w:
                                if (15-move[0])+(15-move[1]) <= (15-w_pawn[0])+(15-w_pawn[1]):
                                        continue
                                if eucledian(w_opp_corner, w_pawn) <= eucledian(w_opp_corner, move):
                                        continue
                                pawn_moves_inside_l.append(move)
                            elif w_pawn in start_w and move not in start_w:
                                pawn_moves_outside_l.append(move)
                            elif w_pawn not in start_w and move in start_w:
                                pawn_outside_to_inside_l.append(move)
                            else:
                                pawn_outside_moves_l.append(move)
                        else:
                            for index, inner_move in enumerate(move):
                                if w_pawn in start_w and inner_move in start_w:
                                    if (15-inner_move[0])+(15-inner_move[1]) <= (15-w_pawn[0])+(15-w_pawn[1]):
                                        continue
                                    if eucledian(w_opp_corner, w_pawn) <= eucledian(w_opp_corner, inner_move):
                                        continue
                                    pawn_moves_inside_l.append(move[:index+1])
                                elif w_pawn in start_w and inner_move not in start_w:
                                    pawn_moves_outside_l.append(move[:index+1])
                                elif w_pawn not in start_w and inner_move in start_w:
                                    pawn_outside_to_inside_l.append(move[:index+1])
                                else:
                                    pawn_outside_moves_l.append(move[:index+1])
                    if pawn_moves_inside_l:
                        pawn_moves_inside[w_pawn] = pawn_moves_inside_l[::-1]
                    if pawn_moves_outside_l:
                        pawn_moves_outside[w_pawn] = pawn_moves_outside_l[::-1]
                    if pawn_outside_to_inside_l:
                        pawn_outside_to_inside[w_pawn] = pawn_outside_to_inside_l[::-1]
                    if pawn_outside_moves_l:
                        pawn_outside_moves[w_pawn] = pawn_outside_moves_l[::-1]
        if pawn_moves_outside:
            key = next(iter(pawn_moves_outside))
            move_list = pawn_moves_outside[key]
            if type(move_list[0]) is tuple:
                with open("output.txt", 'w+') as close_f:
                    output = "E" + " " + str(key[1]) + "," + str(key[0]) + " " + str(move_list[0][1]) + "," + str(move_list[0][0])
                    close_f.write(output)
                    exit(0)
            else:
                m_list = move_list[0]
                with open("output.txt", 'w+') as close_f:
                    output = "J" + " " + str(key[1]) + "," + str(key[0]) + " " + str(m_list[0][1]) + "," + str(m_list[0][0]) + "\n"
                    for ind in range(1, len(m_list)-1):
                        output += "J" + " " + str(m_list[ind-1][1]) + "," + str(m_list[ind-1][0]) + " " + str(m_list[ind][1]) + "," + str(m_list[ind][0]) + "\n"
                    if len(m_list) > 1:
                        output += "J" + " " + str(m_list[-2][1]) + "," + str(m_list[-2][0]) + " " + str(m_list[-1][1]) + "," + str(m_list[-1][0])
                    close_f.write(output)
                    exit(0)

        elif pawn_moves_inside:
            key = next(iter(pawn_moves_inside))
            move_list = pawn_moves_inside[key]
            if type(move_list[0]) is tuple:
                with open("output.txt", 'w+') as close_f:
                    output = "E" + " " + str(key[1]) + "," + str(key[0]) + " " + str(move_list[0][1]) + "," + str(move_list[0][0])
                    close_f.write(output)
                    exit(0)
            else:
                m_list = move_list[0]
                with open("output.txt", 'w+') as close_f:
                    output = "J" + " " + str(key[1]) + "," + str(key[0]) + " " + str(m_list[0][1]) + "," + str(m_list[0][0]) + "\n"
                    for ind in range(1, len(m_list)-1):
                        output += "J" + " " + str(m_list[ind-1][1]) + "," + str(m_list[ind-1][0]) + " " + str(m_list[ind][1]) + "," + str(m_list[ind][0]) + "\n"
                    if len(m_list) > 1:
                        output += "J" + " " + str(m_list[-2][1]) + "," + str(m_list[-2][0]) + " " + str(m_list[-1][1]) + "," + str(m_list[-1][0])
                    close_f.write(output)
                    exit(0)

        x = obj.alphabeta()
        return x


y = main()
# Just for reference, to check the status.
exit(0)


