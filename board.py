#!/bin/python
from cell import Cell

class Board():
    def __init__(self):
        self.board = [Cell(x) for x in range(12*8)]

    def __str__(self):
        text = ""
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
                        if cell.color is 'Red':
                            split += CRED 
                        else:
                            split += CWHITE
                        split += "   "+CEND+"+"
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

            text += split + "\n" + row + "\n" 
        text += "  +---+---+---+---+---+---+---+---+\n"
        text += "  | A | B | C | D | E | F | G | H |"
        return text

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for cell in self.board:
                if other.board[cell.id] != cell:
                    return False
            return True
        return False
    
    def get(self, index):
        return self.board[index]

    
