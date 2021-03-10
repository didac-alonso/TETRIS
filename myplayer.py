from gameboard import *

class MyPlayer:

    def __init__(self ,width, height, method = "simple"):
        self.board = GameBoard(Shape(width,height))
        self.method = method
    
    def place_block(self, location, block):
        self.board.put(location,block).board
        #print("The block could not be placed. The board has not been modified")
        full_row = self.board.full_rows()
        full_column = self.board.full_columns()
        self.board.clear_columns(full_column)
        self.board.clear_rows(full_row)    
        return self
        
    def __str__(self):
        print(self.board)
        return ""

    def play(self, block):
        size = self.board.get_shape()
        if self.method == "simple":
            for i in range (size.height):
                for j in range(size.width):    
                    if self.board.is_empty(Location(i,j), block):
                        return Location(i, j)
            return None
        else:
            provisional_loc = None
            for i in range(size.height):
                for j in range(size.width):
                    if self.board.is_empty(Location(i,j),block):
                        if provisional_loc == None:
                            provisional_loc = Location(i,j)
                        self.board.put(Location(i, j), block)
                        if self.board.full_columns() != [] or self.board.full_rows() != []:
                            self.board.remove(Location(i,j), block)
                            return Location(i,j)
                        self.board.remove(Location(i,j), block)
            return provisional_loc
            
                    
    
    def is_legal(self, block):
        size = self.board.get_shape()
        return block.width <= size.width or block.height <= size.height