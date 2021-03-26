from gameboard import *

class MyPlayer:


    # Constructor, it uses the gameboard class to use all its methods, and a string which contains the skill of the bot.
    def __init__(self ,width, height, method = "simple"):
        """
        This is the constructor, it, creates a gameboard, which needs a Shape, and you can define wether is an expert AI or the simple one.
            """
        self.board = GameBoard(Shape(width,height))
        self.method = method
    

    # It uses the put, method in order to use all the methods of the GameBoard class.
    def place_block(self, location, block):
        """This method puts a block if it's possible in a given location, it uses the put method from gameboard"""
        try:
            self.board.put(location,block).board
        except:
            assert 1 == 0, 'The block could not be placed'
        full_row = self.board.full_rows()
        full_column = self.board.full_columns()
        self.board.clear_columns(full_column)
        self.board.clear_rows(full_row)    
        return self
        

    # It uses the print method from the GameBoard class.
    def __str__(self):
        """
        This method uses the __str__ method of GameBoard.
        """
        print(self.board)
        return ""


    # This method have the instructions which the AI follows, the simple places the block as bottom-left is possible, and the
    # expert does the same, but if puting one block it completes a row or column, it takes that location, to do so it puts
    # the block in the location, then it checks if it makes a column or row be full, it removes the block and if the block makes
    # a column or row be full, returns the location.
    def play(self, block):
        """
        This method defines playing method, the simple one places the block as bottom-left is possible. 
        The expert does the same, but if puting one block it completes a row or column, it places that one.
        """
        size = self.board.get_shape()
        if self.method == "simple":
            for i in range (size.height):
                for j in range(size.width):
                    try:    
                        if self.board.is_empty(Location(i,j), block):
                            return Location(i, j)
                    except:
                        pass
            return None
        
        else:
            provisional_loc = None
            for i in range(size.height):
                for j in range(size.width):
                    try:
                        if self.board.is_empty(Location(i,j),block):
                            if provisional_loc == None:
                                provisional_loc = Location(i,j)
                            self.board.put(Location(i, j), block)
                            if self.board.full_columns() != [] or self.board.full_rows() != []:
                                self.board.remove(Location(i,j), block)
                                return Location(i,j)
                            self.board.remove(Location(i,j), block)
                    except:
                        pass
            return provisional_loc
            
                    
    # This is a control method, it uses logic conditions to determine wether a block is legal or not, that is
    # if the block is a Shape type, if it's not bigger than the board and if its width and height > 0.
    def is_legal(self, block):
        """
        This method returns a boolean which is true if the block fits the board, empty or not, the block is a Shape, and if it has heigth and width > 0.
        """
        
        size = self.board.get_shape()
        try:
            return (block.width <= size.width or block.height <= size.height) and (block.width > 0 and block.height > 0)
        except:
            return False