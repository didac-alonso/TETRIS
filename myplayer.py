from gameboard import *

class MyPlayer:

    def __init__(self ,width, height, method = "simple"):
        self.board = GameBoard(Shape(width,height))
        self.method = method
    
    def place_block(self, location, block):
        self.board.put(location,block).board
        #print("The block could not be placed. The board has not been modified")
        return self
        
    def __str__(self):
        print(self.board)
        return ""

    def play(self, block):
        size = self.board.get_shape()
        for i in range (size.height):
            for j in range(size.width):    
                if self.board.is_empty(Location(i,j), block):
                    return Location(i, j)
        return None
        