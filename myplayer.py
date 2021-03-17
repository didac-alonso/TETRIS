from gameboard import *

class MyPlayer:

    def __init__(self ,width, height, method = "simple"):
        """This is the constructor, it, creates a gameboard, which needs a Shape, and you can define wether is
            an expert AI or the simple one."""
        self.board = GameBoard(Shape(width,height))
        self.method = method
    
    def place_block(self, location, block):
        """This method puts a block if it's possible in a given location, it uses the put method from gameboard"""
        self.board.put(location,block).board
        #print("The block could not be placed. The board has not been modified")
        full_row = self.board.full_rows()
        full_column = self.board.full_columns()
        self.board.clear_columns(full_column)
        self.board.clear_rows(full_row)    
        return self
        
    def __str__(self):
        """
        This method uses the __str__ method of gameboard.
        """
        print(self.board)
        return ""

    def play(self, block):
        """
        This method defines playing method, the simple one places the block as bottom-left is possible. 
        The expert does the same, but if puting one block it completes a row or column, it places that one.
        """
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
        """
        This method returns a boolean which is true if
        the block doesn't fit the board, empty or not.
        """
        size = self.board.get_shape()
        return block.width <= size.width or block.height <= size.height