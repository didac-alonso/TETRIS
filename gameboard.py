import collections

Shape = collections.namedtuple('Shape', 'width height')
Location = collections.namedtuple('Location', 'row column')

class GameBoard:

    def __init__(self, size):
    """
    Constructor, gameboard is based in 3 parameters two integers: 
    height, width and a matrix: board which represents the gameboard
    """
        self.height = size.height
        self.width = size.width
        matriu =[]
        for i in range (size.height):
            fila =[]
            for j in range(size.width):
                fila.append('\u2b1c')
            matriu.append(fila)
        self.board = matriu


    def full_rows(self):
        """ 
        This method returns a list which contains the full rows are the full rows.
        It makes it in O(w), where w is the board width
        """
        size = self.get_shape()
        rows = []
        complete_row = ['\u2b1b']*size.width
        for i in range(size.height):   
            if self.board[i][:] == complete_row:
                rows.append(size.height -i -1) 
        return rows


    def full_columns(self):
        """
        This method returns a list which contains the full columns. It makes it in O(h),
        where h is the board height, to do so, i have to transpose the board in order to get
        its rows, thats because it isn't possible to acces by columns in a matrix 
        """
        size = self.get_shape()
        columns = []
        complete_column = ['\u2b1b']*size.height
        board_transposed = list(zip(*self.board))
        for j in range(size.width):            
            if list(board_transposed[j][:]) == complete_column:
                columns.append(j) 
        return columns

    def has_token(self, location):
    """This method returns whether a square has a token"""
        return self.board[location.row][location.column] == '\u2b1b'


    # def has_token(self, location, rectangle=Shape(1,1)):
    #     for i in range(rectangle.height):
    #         for j in range(rectangle.width):
    #             print(location.row - i, location.column + j, self.board[location.row-i][location.column+j])
    #             if self.board[location.row - i][location.column + j] != '\u2b1b':
    #                 return False    
    #     return True

    def search_tokens(self):
        """This method returns a list which contains all the squares with token"""
        tokens_location = []
        size = self.get_shape()
        for i in range (size.height):
            for j in range (size.width):
                if self.has_token(Location(i,j)):
                    a = (size.height-1-i, j)
                    tokens_location.append(a)
        return tokens_location

    def clear_rows(self, rows):
    """ 
    This method erases the tokens of the given rows, rows is a vector which contains
    the rows which are going to be cleared
    """
        size = self.get_shape()
        # if row > size.height:
        #     print("The row is out of bounds")
        # else:
        number_of_rows = len(rows)
        for i in range (number_of_rows):
            for j in range(size.width):
                self.remove(Location(rows[i], j))
        return self


    def clear_columns(self, columns):
        """ 
        This method erases the tokens of the given columns, columns 
        is a vector which contains the rows which are going to be cleared
        """
        size = self.get_shape()
        # if column > size.height:
        #     print("The row is out of bounds")
        # else:
        number_of_columns = len(columns)
        for j in range(number_of_columns):
            for i in range (size.height):
                self.remove(Location(i, columns[j]))
        return self


    def out_bounds(self, location,size):
    """This methods returns whether a location is out of the gameboard"""
        return location.row >= size.height or location.row < 0 or location.column < 0 or location.column >= size.width

    def get_shape(self):
    """This method returns the shape of the gameboard"""
        width = self.width  
        h = self.height
        mesura = Shape(width, h)
        return mesura

    def transform_coordinates(self, location, size):
    """ 
    This private method, transform the coordinates of a given location
    to the coordinates that are being used to identify the rows and columns
    most methods use this one. 
    """
        return Location(size.height-location.row - 1,location.column)    

    def __str__(self):
    """
    This method defines how to print the gameboard, it prints the matrix.
    """
        size = self.get_shape()
        for i in range(size.height):
            for j in range(size.width):
                print (self.board[i][j],end ="")
            print()
        return ""

    # def put(self, location):
    #     size = self.get_shape()
    #     location = self.transform_coordinates(location, size)
    #     if self.out_bounds(location,size):
    #         print("The square is out of bounds.")
    #     elif self.has_token(location):
    #         print("The square is already occupied.")
    #     else:
    #         self.board[location.row][location.column] = '\u2b1b'
    #     return self

    # def fits_and_no_token(self, size, location, rectangle):
    # """ 
    # This method is used to discard the rectangles which can't be used to put 
    # squares in the board
    # """
    #     for i in range(rectangle.height):
    #         for j in range(rectangle.width):    
    #             if self.out_bounds(Location(location.row - i, location.column + j),size):
    #                 return False
    #             elif self.has_token(Location(location.row - i, location.column + j)):
    #                 return False
    #     return True

    # def fits_and_fully_occuped(self, size, location, rectangle):
    # """ 
    # This method is used to discard the rectangles which can't be used to erase 
    # squares in the board
    # """
    #     for i in range(rectangle.height):
    #         for j in range(rectangle.width):    
    #             if self.out_bounds(Location(location.row - i, location.column + j),size):
    #                 return False
    #             elif not self.has_token(Location(location.row - i, location.column +j)):
    #                 return False
    #     return True

    def put(self, location, rectangle = Shape(1, 1)):
    """ 
    This method puts, if it's possible, a rectangle of tokens, which has its low-left corner in location
    if the rectangle is not specified, the method will place only one token, in the location 
    """
        size = self.get_shape()
        if not self.is_empty(location, rectangle):
            print("The rectangle cannot be put on the board.")         
            return self
        location = self.transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):    
                # if self.out_bounds(Location(location.row - i, location.column + j),size):
                #     print("The square is out of bounds.")
                #     return self
                if self.has_token(Location(location.row - i, location.column + j)):
                    print("The square is already occupied.")
                    return self
                else:
                    self.board[location.row - i][location.column + j] = '\u2b1b'
        return self


    def remove(self, location,rectangle = Shape(1, 1)):
    """ 
    This method erases, if it's possible; that is, if the rectangle is fully occuped and it fits in the board,
    a rectangle of tokens, which has its low-left corner in location
    if the rectangle is not specified, the method will erase only one token, in the location.
    """
        size = self.get_shape()
        if not self.is_full(location, rectangle):
            print("The rectangle cannot be removed.")         
            return self
        location = self.transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range (rectangle.width):
                self.board[location.row - i][location.column + j] = '\u2b1c'
        return self


    def is_empty(self,location, rectangle=Shape(1,1)):
    """ 
    This method returns wether a rectangle is empty, the rectangle is specified by its shape
    and location is the low-left corner. If the rectangle is not specified, it considers
    only the location of low-left corner.
    """
        size = self.get_shape()
        location = self.transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):
                try:
                    if self.has_token(Location(location.row - i, location.column + j)):
                        return False
                except:
                    return False
        return True


    def is_full(self,location, rectangle=Shape(1,1)):
    """
    This method returns wether a rectangle is full, the rectangle is specified by its shape
    and location is the low-left corner. If the rectangle is not specified, it considers
    only the location of low-left corner
    """
        size = self.get_shape()
        location = self.transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):
                try:
                    if not self.has_token(Location(location.row - i, location.column + j)):
                        return False
                except:
                    return False
        return True

    def __repr__(self):
    """
    This method changes de data shown by the type GameBoard, the data that must be shown is,
    the shape, and the squares with token
    """
        size = self.get_shape()
        print(size.width,end='')
        print("x", end = '')
        print(size.height,end='')
        print(" board: ", end='')
        tokens = self.search_tokens()
        print(tokens, end="")
        return ""


    def row_counters(self):
    """
    This method counts how many tokens are in every row, it returns it in a list.
    """
        size = self.get_shape()
        row_counter = []        
        for i in range(size.height-1, -1, -1):
            counter = 0
            for j in range(size.width):
                if self.has_token(Location(i,j)):
                    counter += 1
            row_counter.append(counter)
        return row_counter

    def column_counters(self):
    """
    This method counts how many tokens are in every column, it returns it in a list.
    """
        size = self.get_shape()
        column_counter = []        
        for j in range(size.width):
            counter = 0
            for i in range(size.height):
                if self.has_token(Location(i,j)):
                    counter += 1
            column_counter.append(counter)
        return column_counter
        
