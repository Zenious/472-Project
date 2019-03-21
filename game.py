#!/bin/python
import sys
import copy 
from cell import Cell
from board import Board
from minimax import getNextMove
from minimax import interfaceBoard

class DoubleCard():
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.prev_board = copy.deepcopy(self.board)
        self.trace = True
        self.prev_move = []
        self.history = []
        self.player_option = 1
        self.ai_player = 99999

    def start_menu(self):
        print("Welcome to Double Card Game!")
        while (True):
            option = input("""============================
Select Game Mode:
1) Player VS Player
2) Player VS AI

Option: """)
            self.flush()
            if option == '1':
                print("Player VS Player Mode Selected")
                self.win_condition()
                self.flush()
                break
            elif option == '2':
                print("Player VS AI Mode Selected")
                self.ai_condition()
                self.flush()
                self.win_condition()
                self.flush()
                break
            else:
                print("Invalid option selected!")

    def ai_condition(self):
        trace_text = "Do you want to have an output of the trace?(Y/N): "
        choice_text = """Choose AI to start 1st or 2nd:
1) 1st
2) 2nd
Option: """
        while(True):
            choice=input(trace_text)
            if choice in ['Y', 'N']:
                if choice == 'Y':
                    self.trace = True
                else:
                    self.trace = False
                break
            self.flush()

        while(True):
            self.flush()
            choice=input(choice_text)
            if choice in ['1', '2']:
                self.ai_player = int(choice)
                break

    def win_condition(self):
        choice_text = """Choose Player 1 Winning condition:
1) Colors
2) Dots
Option: """
        while(True):
            choice=input(choice_text)
            if choice in ['1', '2']:
                self.player_option = int(choice)
                break
            self.flush()

    def letter_to_int(self, move):
        letter_map = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
        return letter_map.setdefault(move, None)
    
    def start(self):
        self.first_load()
        while True:
            if self.history:
                print ("Turn {}: Move placed is {}".format(self.turn, self.history[-1]))
            print (self.board)
            if self.turn == 40:
                break
            self.command_parser()
            self.prev_board = copy.deepcopy(self.board)
        print("Game End with Draw")

    def first_load(self):
        self.start_menu()

    def print_history(self):
        for x,y in enumerate(self.history):
            print("""Turn {}:
Player {} : {}""".format(x+1,x%2+1,y))

    def same_move(self, parsed_command):
        prev_move = self.prev_move
        if len(prev_move)!= 7:
            return False
        if parsed_command == prev_move:
            return True
        if set(parsed_command[0:4]) == set(prev_move[0:4]):
            print(parsed_command[4])
            if parsed_command[4] == prev_move[4]:
                return True
        return False

    def move_prev_card(self, parsed_command):
        prev_move = self.prev_move
        if len(prev_move)!= 7:
            prev_card = self.prev_move[2:4]
        else:
            prev_card = self.prev_move[5:7]

        c1 = parsed_command[0:2]
        c2 = parsed_command[2:4]

        if prev_card == c1 or prev_card == c2:
            return True
        return False

    def string_to_int(self, commands_list):
        for x,y in enumerate(commands_list):
            if y.isnumeric():
              commands_list[x] = int(y)
        return commands_list

    def validate(self, cmds):
        valid = True
        move_type = len(cmds)
        cmds = self.string_to_int(cmds)
        if move_type == 1:
            if cmds != "history": # View History
                valid = False
        elif move_type == 4: # Regular Move (eg. 0 7 A 1)
            int_letter = self.letter_to_int(cmds[2])
            if cmds[0] != 0:
                valid = False
            elif type(cmds[1]) != int:
                valid = False
            elif type(cmds[3]) != int:
                valid = False
            elif cmds[1] > 8 or cmds[1] <1:
                valid = False
            elif int_letter is None:
                valid = False
            elif cmds[3] > 12 or cmds[3] <1:
                valid = False
        elif move_type == 7: # Recycling move (eg. A 1 A 2 7 A 1)
            int_letter_0 = self.letter_to_int(cmds[0])
            int_letter_2 = self.letter_to_int(cmds[2])
            int_letter_5 = self.letter_to_int(cmds[5])
        
            if int_letter_0 is None:
                valid = False
            elif type(cmds[1]) != int:
                valid = False
            elif type(cmds[3]) != int:
                valid = False
            elif type(cmds[4]) != int:
                valid = False
            elif type(cmds[6]) != int:
                valid = False
            elif cmds[1] > 12 or cmds[1] <1:
                valid = False
            elif int_letter_2 is None:
                valid = False
            elif cmds[3] > 12 or cmds[3] <1:
                valid = False
            elif cmds[4] > 8 or cmds[4] <1:
                valid = False
            elif int_letter_5 is None:
                valid = False
            elif cmds[6] > 12 or cmds[6] <1:
                valid = False
        else:
            valid = False
        return valid
        

    def command_parser(self):
        curr_player = self.turn%2 + 1
        curr_ai = (self.ai_player == curr_player)
        if not curr_ai:
            command = input("[{}'s Turn] Place your move: ".format("Player {}".format(curr_player)))
        else:
            ai_type = 0 if self.player_option == 1 else 1
            if self.turn >= 24:
                command = getNextMove(self.board, ai_type, show_stats=self.trace,recycling=True,prev_move=self.history[-1])
            else:
                command = getNextMove(self.board, ai_type, show_stats=self.trace)
            # command = "0 2 A 1" # TODO place output of minimax algo here
            print("[AI's Turn] Place your move: {}".format(command))
        self.flush()
        print ("{player} Input: {command}".format(player="Player" if not curr_ai else "AI" ,command=command))
        parsed_command = command.split(' ')
       
        if parsed_command[0] == 'history':
            self.print_history()
            return
        if parsed_command[0] == 'export':
            print(interfaceBoard(self.board))
            return
        if not self.validate(parsed_command):
            self.illegal_move("Invalid command!")
            return
        elif parsed_command[0] == 0:
            if len(parsed_command) != 4:
                print("Invalid Move!")
                return

            if self.turn >= 24:
                print("Cannot use Regular Moves!")
                return
            else:
                start_cell = self.letter_to_int(parsed_command[2]) + (parsed_command[3]-1)*8
                self.place_card(parsed_command[1], start_cell)
                self.prev_move = parsed_command
                self.history.append(command)
        else:
            if len(parsed_command) != 7 or self.turn <24:
                print("Invalid Move!")
                return
            if self.same_move(parsed_command):
                self.illegal_move("Same Move")
                return
            if self.move_prev_card(parsed_command):
                self.illegal_move("Moving Same Card as Previous Move")
                return
            start_cell = self.letter_to_int(parsed_command[0]) + (parsed_command[1]-1)*8
            neighbour_cell = self.letter_to_int(parsed_command[2]) + (parsed_command[3]-1)*8
            new_cell = self.letter_to_int(parsed_command[5]) + (parsed_command[6]-1)*8
            if self.remove_card(start_cell, neighbour_cell):
                self.place_card(parsed_command[4], new_cell)

                if self.board == self.prev_board:
                    self.illegal_move("Move did not change to the board")
                    self.turn -= 1
                    return
                self.prev_move = parsed_command
                self.history.append(command)

    def check_win(self, cell_num):

        directions =['vertical', 'horizontal', 'diag-left', 'diag-right']
        wins = [0,0,0,0]
        winning_nums = [2*3*5*7, 3*5*7*11, 5*7*11*13, 7*11*13*17]
        for direction in directions:
            x = self.tabulate(cell_num, direction)
            for y,z in enumerate(x):
                if list(filter(lambda x: z%x==0, winning_nums)):
                    # print("Possible win with {}".format(direction))
                    wins[y] = 1
        return wins

    def remove_card(self, start_cell, neighbour_cell):
        # check if cells are linked
        c1 = self.board.get(start_cell)
        c2 = self.board.get(neighbour_cell)
        def in_bound(cell_num):
            return cell_num >= 0 and cell_num < 8*12

        illegal = False
        if c1.link == c2.id and c2.link == c1.id:
            c1.clear()
            c2.clear()
            for c in [start_cell,neighbour_cell]:
                if in_bound(c+8):
                    if self.board.get(c+8).occupied:
                        illegal = True            
        else:
            illegal = True


        if illegal:
            self.illegal_move("Removal not possible")
            return False
        return True

    def illegal_move(self, reason):
        print("Illegal Move! - {}".format(reason))
        self.board = copy.deepcopy(self.prev_board)

    def tabulate(self, cell_num, direction):
        red = 1
        white = 1
        cross = 1
        circle = 1
        primes = [2,3,5,7,11,13,17]
        if direction == 'horizontal':
            extend_cell_num = cell_num+3
            if int(extend_cell_num / 8) != int(cell_num / 8):
                extend_cell_num = (int(cell_num / 8)+1)*8-1
        if direction == "vertical":
            extend_cell_num = cell_num+3*8
        if direction == 'diag-left':
            extend_cell_num = cell_num+3*8+3
        if direction == 'diag-right':
            extend_cell_num = cell_num+3*8-3
        for x in range(7):
            curr_cell = None
            if direction == 'vertical':
                curr_cell_num = extend_cell_num-8*x
            elif direction == 'horizontal':
                curr_cell_num = extend_cell_num-x
                if int(curr_cell_num / 8) != int(cell_num / 8):
                    continue
            elif direction == 'diag-left':
                curr_cell_num = extend_cell_num-8*x-x
                if int(curr_cell_num / 8) != int(cell_num / 8)+3-x:
                    continue
            elif direction == 'diag-right':
                curr_cell_num = extend_cell_num-8*x+x 
                if int(curr_cell_num / 8) != int(cell_num / 8)+3-x:
                    continue

            # check if out of board
            if curr_cell_num >= 0 and curr_cell_num < 8*12:
                curr_cell = self.board.get(curr_cell_num)
            if curr_cell is None:
                continue
            if curr_cell.color is 'Red':
                red *= primes[x]
            elif curr_cell.color is 'White':
                white *= primes[x]
            if curr_cell.symbol == '\u2022':
                circle *= primes[x]
            elif curr_cell.symbol == '\u25E6':
                cross *= primes[x]
        return [red, white, circle, cross]


    def place_card(self, variant, start_cell):
        neighbour_cell = start_cell+1 if variant%2 == 1 else start_cell+8
        if self.check_illegal(start_cell, neighbour_cell):
            self.illegal_move("Placement not possible")
            return
        color = 'Red' if variant in [1,4,5,8] else 'White'
        symbol = '\u25E6' if variant in [2,3,5,8] else "\u2022"

        def opp_color(color):
            return 'White' if color is 'Red' else 'Red'

        def opp_symbol(symbol):
            return "\u2022" if symbol == '\u25E6' else '\u25E6'

        self.board.get(start_cell).fill(color, symbol, neighbour_cell, variant)
        self.board.get(neighbour_cell).fill(opp_color(color), opp_symbol(symbol), start_cell, variant)
        wins = self.check_win(start_cell)
        wins.extend(self.check_win(neighbour_cell))
        self.who_win(wins)
        self.turn += 1

    def who_win(self, result):
        player = self.turn % 2 + 1
        player1_win = False
        player2_win = False

        win_cases = [i for i, x in enumerate(result) if x == 1]
        if [i for i in [0,1,4,5] if i in win_cases]:
            if self.player_option == 1:
                player1_win = True
            else:
                player2_win = True
        if [i for i in [2,3,6,7] if i in win_cases]:
            if self.player_option == 1:
                player2_win = True
            else:
                player1_win = True
        if player1_win and player2_win:
            print("Player {} wins".format(player))
        elif player1_win:
            print("Player 1 wins")
        elif player2_win:
            print("Player 2 wins")
        if player2_win or player1_win:
            print(self.board)
            exit()

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
                return self.board.get(cell-8).occupied == False
        def occupied_cell(cell):
            return self.board.get(cell).occupied

        if check_in_bound(start_cell) and check_in_bound(neighbour_cell):
            if occupied_cell(start_cell) or occupied_cell(neighbour_cell):
                # print("HERE OCCUPIED")
                return True
            if floating_cell(start_cell) or floating_cell(neighbour_cell):
                if neighbour_cell - start_cell == 8:
                    return floating_cell(start_cell) and floating_cell(neighbour_cell)
                # print("HERE FLOATING")
                return True
            if neighbour_cell - start_cell == 1:
                return int(neighbour_cell/8) != int(start_cell/8)
            return False
        else:
            return True

x = DoubleCard()
x.start()
