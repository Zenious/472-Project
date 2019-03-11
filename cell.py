#!/bin/python

class Cell():
    def __init__(self, number):
        self.id = number
        self.occupied = False
        self.color = None
        self.symbol = None
        self.link = float("-inf")
        self.variant = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.color == other.color and self.id == other.id\
            and self.symbol == other.symbol and self.occupied == other.occupied\
            and self.link == other.link and self.variant == other.variant
        return False

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

    def get_color(self):
        if self.color is None:
            return " "
        else:
            return self.color

    def get_id(self):
        return self.id

    def get_variant(self):
        return self.variant
        
    def link_direction(self):
        diff = self.link - self.id
        if diff == 1:
            return 'right'
        elif diff == 8:
            return "up"
        elif diff == -1:
            return "left"
        elif diff == -8:
            return "down"
        else:
            return "no link"

    def clear(self):
        self.occupied = False
        self.color = None
        self.symbol = None
        self.link = None
        self.variant = None