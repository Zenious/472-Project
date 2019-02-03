#!/bin/python

import sys
import copy 

class Cell():
    def __init__(self, number):
        self.id = number
        self.occupied = False
        self.color = None
        self.symbol = None
        self.link = None
        self.variant = None

    def fill(self, color, symbol, link, variant):
        self.occupied = True
        self.color = color
        self.symbol = symbol
        self.link = link
        self.variant = variant

    def get_symbol(self):
        if self.symbol is None:
            return ' '
        else:
            return self.symbol

    def link_direction(self):
        diff = self.link - self.id
        if diff == 1:
            return 'right'
        if diff == 8:
            return "up"
        if diff == -1:
            return "left"
        if diff == -8:
            return "down"

    def clear(self):
        self.occupied = False
        self.color = None
        self.symbol = None
        self.link = None
        self.variant = None

class DoubleCard():

    def __init__(self):
        self.init_board()
        self.turn = 0
        self.prev_board = []

    def letter_to_int(self, move):
        letter_map = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
        return letter_map[move]
    
    def start(self):
        self.first_load()
        while self.turn <60:
            self.command_parser()
            self.prev_board = copy.deepcopy(self.board)
        print("Game End with Draw")

    def first_load(self):
        print("Welcome Double Card Game!")
        self.print_board()

    def command_parser(self):
        command = input("Place your move: ")
        self.flush()
        parsed_command = command.split(' ')
        if parsed_command[0] is '0':
            print("Regular Move")
            if len(parsed_command) != 4:
                print("Invalid Move!")
            if self.turn >= 24:
                print("Cannot use Regular Moves!")
            else:
                start_cell = self.letter_to_int(parsed_command[2]) + (int(parsed_command[3])-1)*8
                self.place_card(int(parsed_command[1]), start_cell)
        else:
            if len(parsed_command) != 7 or self.turn <24:
                print("Invalid Move!")
            print("Recycling Move")
            start_cell = self.letter_to_int(parsed_command[0]) + (int(parsed_command[1])-1)*8
            neighbour_cell = self.letter_to_int(parsed_command[2]) + (int(parsed_command[3])-1)*8
            new_cell = self.letter_to_int(parsed_command[5]) + (int(parsed_command[6])-1)*8
            self.remove_card(start_cell, neighbour_cell)
            self.place_card(int(parsed_command[4]), new_cell)
            # check if previously occupied cell causing board to be illegal
            for cell in [start_cell, neighbour_cell]:
                if cell+8 < 8*12:
                    if self.board[cell+8].occupied:
                        self.illegal_move()

        print ("Turn {}: Your Move was {}".format(self.turn, command))
        self.print_board()

    def check_win(self, cell_num):
        # won't work for recycling moves
        directions =['down', 'left', 'right', 'diag-left', 'diag-right']
        wins = [0,0,0,0]
        for direction in directions:
            x = self.tabulate(cell_num, direction)
            for y,z in enumerate(x):
                if z == 4 :
                    print("Possible win with {}".format(y))
                    wins[y] = 1
        return wins

    def remove_card(self, start_cell, neighbour_cell):
        # check if cells are linked
        c1 = self.board[start_cell]
        c2 = self.board[neighbour_cell]
        print (c1.id)
        print (c2.id)
        if c1.link == c2.id and c2.link == c1.id:
            c1.clear()
            c2.clear()
        else:
            self.illegal_move()
            return

    def illegal_move(self):
        print("Illegal Move!")
        self.board = copy.deepcopy(self.prev_board)

    def tabulate(self, cell_num, direction):
        # won't work for recycling moves
        red = 0
        white = 0
        cross = 0
        circle = 0
        for x in range(4):
            curr_cell = None
            if direction == 'down':
                curr_cell_num = cell_num-8*x
            elif direction == 'left':
                curr_cell_num = cell_num-x
                if int(curr_cell_num / 8) != int(cell_num / 8):
                    continue
            elif direction == 'right':
                curr_cell_num = cell_num+x
                if int(curr_cell_num / 8) != int(cell_num / 8):
                    continue
            elif direction == 'diag-left':
                break
            elif direction == 'diag-right':
                break

            # check if out of board
            if curr_cell_num >= 0 and curr_cell_num < 8*12:
                curr_cell = self.board[curr_cell_num]
            if curr_cell is None:
                continue
            if curr_cell.color is 'Red':
                red += 1
            elif curr_cell.color is 'White':
                white += 1
            if curr_cell.symbol is 'O':
                circle += 1
            elif curr_cell.symbol is 'X':
                cross += 1 
        print (red, white, circle, cross, direction)
        return [red, white, circle, cross]


    def place_card(self, variant, start_cell):
        neighbour_cell = start_cell+1 if variant%2 == 1 else start_cell+8
        if self.check_illegal(start_cell, neighbour_cell):
            self.illegal_move()
            return
        color = 'Red' if variant in [1,4,5,8] else 'White'
        symbol = 'O' if variant in [2,3,5,8] else 'X'

        def opp_color(color):
            return 'White' if color is 'Red' else 'Red'

        def opp_symbol(symbol):
            return 'X' if symbol is 'O' else 'O'

        self.board[start_cell].fill(color, symbol, neighbour_cell, variant)
        self.board[neighbour_cell].fill(opp_color(color), opp_symbol(symbol), start_cell, variant)
        self.turn += 1
        # if variant is 1:
        #     self.board[start_cell].fill("Red", "X")
        #     self.board[neighbour_cell].fill("White", "O")
        # if variant is 2:
        #     self.board[start_cell].fill("White", "O")
        #     self.board[neighbour_cell].fill("Red", "X")
        # if variant is 3:
        #     self.board[start_cell].fill("White", "O")
        #     self.board[neighbour_cell].fill("Red", "X")
        # if variant is 4:
        #     self.board[start_cell].fill("Red", "X")
        #     self.board[neighbour_cell].fill("White", "O")
        # if variant is 5:
        #     self.board[start_cell].fill("Red", "O")
        #     self.board[neighbour_cell].fill("White", "X")
        # if variant is 6:
        #     self.board[start_cell].fill("White", "X")
        #     self.board[neighbour_cell].fill("Red", "O")
        # if variant is 7:
        #     self.board[start_cell].fill("White", "X")
        #     self.board[neighbour_cell].fill("Red", "O")
        # if variant is 8:
        #     self.board[start_cell].fill("Red", "O")
        #     self.board[neighbour_cell].fill("White", "X")
        wins = self.check_win(start_cell)
        wins.extend(self.check_win(neighbour_cell))
        self.who_win(wins)

    def who_win(self, result):
        player = self.turn % 2
        # player 1 win with Red and X
        # player 2 win with White and O
        print(result)
        player1_win = False
        player2_win = False

        win_cases = [i for i, x in enumerate(result) if x == 1]
        if [i for i in [0,3,4,7] if i in win_cases]:
            player1_win = True
        if [i for i in [1,2,5,6] if i in win_cases]:
            player2_win = True
        if player1_win and player1_win:
            print("Player {} wins".format(player))
        elif player1_win:
            print("Player 1 wins")
        elif player2_win:
            print("Player 2 wins")
        if player2_win or player1_win:
            self.print_board()
            exit()

    def init_board(self):
        # init 12x8 board
        self.board = [Cell(x) for x in range(12*8)] 

    def flush(self):
        print(chr(27) + "[2J")

    def check_illegal(self, start_cell, neighbour_cell):
        # check if out of bound
        def check_in_bound(cell):
            return cell < 8*12 and cell >= 0

        def floating_cell(cell):
            if cell-8 <0:
                return False
            else:
                return self.board[cell-8].occupied == False
        def occupied_cell(cell):
            # print ("cell {}-{}".format(cell, self.board[cell].occupied))
            return self.board[cell].occupied

        if check_in_bound(start_cell) and check_in_bound(neighbour_cell):
            if occupied_cell(start_cell) or occupied_cell(neighbour_cell):
                print("HERE OCCUPIED")
                return True
            if floating_cell(start_cell) or floating_cell(neighbour_cell):
                print("HERE FLOATING")
                return True
            if neighbour_cell - start_cell == 1:
                return int(neighbour_cell/8) != int(start_cell/8)
        else:
            return True

    def print_board(self):
        for y in range(12):
            row = "{:2}|".format(12-y)
            split = "  +"
            for x in range(8):
                CRED = '\033[41m'
                CEND = '\033[0m'
                CWHITE = '\033[107m'
                cell = self.board[8*(11-y)+x]
                if cell.occupied is True:
                    if cell.color is 'Red':
                        row += CRED 
                    else:
                        row += CWHITE
                    row +=" {} ".format(cell.get_symbol())
                    if cell.link_direction() is 'up':
                        split += "   +"
                        row += CEND + '|'
                    elif cell.link_direction() is 'right':
                        split += "---+"
                        row += ' ' + CEND
                    else :
                        split += "---+"
                        row += CEND +'|'
                else:
                    row +="   |"                
                    split += "---+"

            print(split)
            print(row)
        print("  +---+---+---+---+---+---+---+---+")
        print("  | A | B | C | D | E | F | G | H |")

x = DoubleCard()
x.start()
