import collections

Shape = collections.namedtuple('Shape', 'width height')
Location = collections.namedtuple('Location', 'row column')

class GameBoard:

    def __init__(self, size):
        """
        Constructor: it needs a Shape(width, height) gameboard is based in 3 parameters, two integers: 
        height, width and a matrix: board which represents the gameboard.
        
        Precondition: height and widht > 0
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


    # It makes it in O(w), where w is the board width. I use a vector which is a complete row,
    # to compare directly to the entire rows.
    def full_rows(self):
        """ 
        This method returns a list which contains the full rows.
        """
        size = self.get_shape()
        rows = []
        complete_row = ['\u2b1b']*size.width
        for i in range(size.height):   
            if self.board[i][:] == complete_row:
                rows.append(size.height -i -1) 
        return rows


    # It makes it in O(h), where h is the board height, to do so, 
    # I have to transpose the board in order to get
    # its rows, that's because it isn't possible to acces by columns in a matrix. 
    def full_columns(self):
        """
        This method returns a list which contains the full columns. 
        """
        size = self.get_shape()
        columns = []
        complete_column = ['\u2b1b']*size.height
        board_transposed = list(zip(*self.board))
        for j in range(size.width):            
            if list(board_transposed[j][:]) == complete_column:
                columns.append(j) 
        return columns


    # It searches square by square all the tokens, then it transforms the location,
    # and adds to a list which contains all the squares with token.
    def search_tokens(self):
        """
        This method returns a list which contains the location of all the squares with token.
        """
        tokens_location = []
        size = self.get_shape()
        for i in range (size.height):
            for j in range (size.width):
                if self.__has_token(Location(i,j)):
                    a = (size.height-1-i, j)
                    tokens_location.append(a)
        return tokens_location


    # It uses the remove method in a entire row to erase it, using a for for moving beetwen the given rows,
    # it goes row by row removing without checking if they are full a rectangle with row-shape. 
    def clear_rows(self, rows):
        """ 
        This method erases the tokens of the given rows, rows is a vector which contains
        the rows which are going to be cleared.

        Prec: The rows given are in the gameboard.
        """
        size = self.get_shape()
        number_of_rows = len(rows)
        for i in range (number_of_rows):
            self.remove(Location(rows[i], 0),Shape(size.width, 1), False)
        return self


    # It uses the remove method in a entire column to erase it, using a for for moving beetwen the given columns,
    # it goes column by column removing without checking if they are full a rectangle with column-shape.
    def clear_columns(self, columns):
        """ 
        This method erases the tokens of the given columns, columns 
        is a vector which contains the rows which are going to be cleared.

        Prec: The rows given are in the gameboard.
        """
        size = self.get_shape()
        number_of_columns = len(columns)
        for j in range(number_of_columns):
            self.remove(Location(0, columns[j]), Shape(1, size.height), False)
        return self


    def get_shape(self):
        """This method returns the shape of the gameboard"""
        width = self.width  
        h = self.height
        mesura = Shape(width, h)
        return mesura
   

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


    # First of all it checks if the square is empty and it fits in the location given. If it's true, places the rectangle and fills the squares. 
    def put(self, location, rectangle = Shape(1, 1)):
        """ 
        This method puts, if it's possible, a rectangle of tokens, which has its low-left corner in location
        if the rectangle is not specified, the method will place only one token, in the location.
        """
        try:
            empty = self.is_empty(location, rectangle)   
            assert empty, 'The square is already occupied.'
        except:
            assert 1 == 0, 'The square is out of bounds.'
        size = self.get_shape()
        location = self.__transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):    
                self.board[location.row - i][location.column + j] = '\u2b1b'
        return self


    # First of all it checks if the square is full and fits in the given location, then it erases the squares in the rectangle.
    # It has an extra parametre that default is true, that is because for clear_rows() and clear_columns doesn't matter if they are
    # full or not.
    def remove(self, location,rectangle = Shape(1, 1), must_full = True):
        """ 
        This method erases, if it's possible; that is, if the rectangle is fully occuped and it fits in the board,
        a rectangle of tokens, which has its low-left corner in location if the rectangle is not specified, the 
        method will erase only one token, in the location.
        """
        size = self.get_shape()
        if must_full:
            try:
                full = self.is_full(location, rectangle)
                assert full, 'The rectangle cannot be removed'
            except:
                assert 1 == 0, 'The square is out of bounds'
        location = self.__transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range (rectangle.width):
                self.board[location.row - i][location.column + j] = '\u2b1c'
        return self


    # This method returns false if the rectangle is not empty, and it asserts if it's out of bounds.
    def is_empty(self,location, rectangle=Shape(1,1)):
        """ 
        This method returns wether a rectangle is empty, the rectangle is specified by its shape
        and location is the low-left corner. If the rectangle is not specified, it considers
        only the location of low-left corner.
        """
        size = self.get_shape()
        location = self.__transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):
                try:
                    if self.__has_token(Location(location.row - i, location.column + j)):
                        return False
                except:
                    assert 1 == 0, 'The square is out of bounds.'
        return True


    # This method returns false if the rectangle is not fully occuped, and it asserts if it's out of bounds.
    def is_full(self,location, rectangle=Shape(1,1)):
        """
        This method returns wether a rectangle is full, the rectangle is specified by its shape
        and location is the low-left corner. If the rectangle is not specified, it considers
        only the location of low-left corner.
        """
        size = self.get_shape()
        location = self.__transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):
                try:
                    if not self.__has_token(Location(location.row - i, location.column + j)):
                        return False
                except:
                    assert 1 == 0, 'The square is out of bounds.'
        return True


    # It changes the data shown by the type gameboard, it must be shown the shape, and squares with token,
    # it uses the search_tokens function in order to find the tokens, then it prints it.
    def __repr__(self):
        """
        This method changes the data shown by the type GameBoard, the data that must be shown is,
        the shape, and the squares with token.
        """
        size = self.get_shape()
        tokens = self.search_tokens()
        print(size.width, 'x', size.height, ' board: ', tokens, sep='', end = '')
        return ""


    # It goes row by row counting how many occupied square are, using two fors.
    # The for starts from size.height -1 in order to return the counter from the 0 row to height - 1 row.
    def row_counters(self):
        """
        This method counts how many tokens are in every row, it returns it in a list, in which
        every component of the list represent a row.
        """
        size = self.get_shape()
        row_counter = []        
        for i in range(size.height-1, -1, -1):
            counter = 0
            for j in range(size.width):
                if self.__has_token(Location(i,j)):
                    counter += 1
            row_counter.append(counter)
        return row_counter


    # It goes column by column counting how many occupied square are in each one.
    def column_counters(self):
        """
        This method counts how many tokens are in every column, it returns it in a list,
        in which every component of the list represents a column.
        """
        size = self.get_shape()
        column_counter = []        
        for j in range(size.width):
            counter = 0
            for i in range(size.height):
                if self.__has_token(Location(i,j)):
                    counter += 1
            column_counter.append(counter)
        return column_counter
        

    # Private method, doesn't transform the coordinates, it's used by 
    # a lot of methods which have transformed previously the coordinates.
    def __has_token(self, location):
        """
        This private method returns whether a square has a token or not.
        
        Prec: the location is in the gameboard.
        """
        return self.board[location.row][location.column] == '\u2b1b'


    def __transform_coordinates(self, location, size):
        """ 
        This private method, transform the coordinates of a given location
        to the coordinates that are being used to identify the rows and columns
        most methods use this one. 
        """
        return Location(size.height-location.row - 1,location.column) 