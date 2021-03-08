import collections

Shape = collections.namedtuple('Shape', 'width height')
Location = collections.namedtuple('Location', 'row column')

class GameBoard:

    #constructor, gameboard is based in 3 parameters two integers: height, width and a matrix: board which represents the gameboard
    def __init__(self, tamany):
        self.height = tamany.height
        self.width = tamany.width
        matriu =[]
        for i in range (tamany.height):
            fila =[]
            for j in range(tamany.width):
                fila.append('\u2b1c')
            matriu.append(fila)
        self.board = matriu

    # this action returns a list which contains the full rows are the full rows.
    # It makes it in O(w), where w is the board width
    def full_rows(self):
        tamany = self.get_shape()
        rows = []
        complete_row = ['\u2b1b']*tamany.width
        for i in range(tamany.height):   
            if self.board[i][:] == complete_row:
                rows.append(tamany.height -i -1) 
        return rows

    # this action returns a list which contains the full columns. It makes it in O(h),
    # where h is the board height, to do so, i have to transpose the board in order to get
    # its rows, thats because it isn't possible to acces by columns in a matrix 
    def full_columns(self):
        tamany = self.get_shape()
        columns = []
        complete_column = ['\u2b1b']*tamany.height
        board_transposed = list(zip(*self.board))
        for j in range(tamany.width):            
            if list(board_transposed[j][:]) == complete_column:
                columns.append(j) 
        return columns

    #this action returns whether a square has a token
    def has_token(self, location):
        return self.board[location.row][location.column] == '\u2b1b'


    # def has_token(self, location, rectangle=Shape(1,1)):
    #     for i in range(rectangle.height):
    #         for j in range(rectangle.width):
    #             print(location.row - i, location.column + j, self.board[location.row-i][location.column+j])
    #             if self.board[location.row - i][location.column + j] != '\u2b1b':
    #                 return False    
    #     return True

    # this action returns a list which contains all the squares with token
    def search_tokens(self):
        tokens_location = []
        size = self.get_shape()
        for i in range (size.height):
            for j in range (size.width):
                if self.has_token(Location(i,j)):
                    a = (size.height-1-i, j)
                    tokens_location.append(a)
        return tokens_location


    # this action erases the tokens of the given rows, rows is a vector which contains
    # the rows which are going to be cleared
    def clear_rows(self, rows):
        tamany = self.get_shape()
        # if row > tamany.height:
        #     print("The row is out of bounds")
        # else:
        number_of_rows = len(rows)
        for i in range (number_of_rows):
            for j in range(tamany.width):
                self.remove(Location(rows[i], j))
        return self


    # this action erases the tokens of the given columns, columns 
    # is a vector which contains the rows which are going to be cleared
    def clear_columns(self, columns):
        tamany = self.get_shape()
        # if column > tamany.height:
        #     print("The row is out of bounds")
        # else:
        number_of_columns = len(columns)
        for j in range(number_of_columns):
            for i in range (tamany.height):
                self.remove(Location(i, columns[j]))
        return self


    #this actions returns whether a location is out of the gameboard
    def out_bounds(self, location,tamany):
        return location.row >= tamany.height or location.row < 0 or location.column < 0 or location.column >= tamany.width

    #this action returns the shape of the gameboard
    def get_shape(self):
        width = self.width  
        h = self.height
        mesura = Shape(width, h)
        return mesura

    # this private action, transform the coordinates of a given location
    # to the coordinates that are being used to identify the rows and columns
    # most actions use this one 
    def transform_coordinates(self, location, tamany):
        return Location(tamany.height-location.row - 1,location.column)    

    #this action defines how to print the gameboard, it prints the matrix
    def __str__(self):
        size = self.get_shape()
        for i in range(size.height):
            for j in range(size.width):
                print (self.board[i][j],end ="")
            print()
        return ""

    # def put(self, location):
    #     tamany = self.get_shape()
    #     location = self.transform_coordinates(location, tamany)
    #     if self.out_bounds(location,tamany):
    #         print("The square is out of bounds.")
    #     elif self.has_token(location):
    #         print("The square is already occupied.")
    #     else:
    #         self.board[location.row][location.column] = '\u2b1b'
    #     return self

    # this action is used to discard the rectangles which can't be used to put 
    # squares in the board
    def fits_and_no_token(self, tamany, location, rectangle):
        for i in range(rectangle.height):
            for j in range(rectangle.width):    
                if self.out_bounds(Location(location.row - i, location.column + j),tamany):
                    return False
                elif self.has_token(Location(location.row - i, location.column + j)):
                    return False
        return True

    # this action is used to discard the rectangles which can't be used to erase 
    # squares in the board
    def fits_and_fully_occuped(self, tamany, location, rectangle):
        for i in range(rectangle.height):
            for j in range(rectangle.width):    
                if self.out_bounds(Location(location.row - i, location.column + j),tamany):
                    return False
                elif not self.has_token(Location(location.row - i, location.column +j)):
                    return False
        return True

    # this action puts, if it's possible, a rectangle of tokens, which has its low-left corner in location
    # if the rectangle is not specified, the action will place only one token, in the location 
    def put(self, location, rectangle = Shape(1, 1)):
        tamany = self.get_shape()
        location = self.transform_coordinates(location, tamany)
        if rectangle != Shape(1,1) and not self.fits_and_no_token(tamany, location, rectangle):
            print("The rectangle cannot be put on the board.")         
            return self
        for i in range(rectangle.height):
            for j in range(rectangle.width):    
                if self.out_bounds(Location(location.row - i, location.column + j),tamany):
                    print("The square is out of bounds.")
                    return self
                elif self.has_token(Location(location.row - i, location.column + j)):
                    print("The square is already occupied.")
                    return self
                else:
                    self.board[location.row - i][location.column + j] = '\u2b1b'
        return self


    # this action erases, if it's possible; that is, if the rectangle is fully_occuped and it fits in the board,
    # a rectangle of tokens, which has its low-left corner in location
    # if the rectangle is not specified, the action will erase only one token, in the location 
    def remove(self, location,rectangle = Shape(1, 1)):
        tamany = self.get_shape()
        location = self.transform_coordinates(location, tamany)
        if rectangle != Shape(1,1) and not self.fits_and_fully_occuped(tamany, location, rectangle):
            print("The rectangle cannot be removed.")         
            return self
        for i in range(rectangle.height):
            for j in range (rectangle.width):
                self.board[location.row - i][location.column + j] = '\u2b1c'
        return self


    # this action returns wether a rectangle is empty, the rectangle is specified by its shape
    # and location is the low-left corner. If the rectangle is not specified, it considers
    # only the location of low-left corner
    def is_empty(self,location, rectangle=Shape(1,1)):
        size = self.get_shape()
        location = self.transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):
                if self.has_token(Location(location.row - i, location.column + j)):
                    return False
        return True


    # this action returns wether a rectangle is full, the rectangle is specified by its shape
    # and location is the low-left corner. If the rectangle is not specified, it considers
    # only the location of low-left corner
    def is_full(self,location, rectangle=Shape(1,1)):
        size = self.get_shape()
        location = self.transform_coordinates(location, size)
        for i in range(rectangle.height):
            for j in range(rectangle.width):
                if not self.has_token(Location(location.row - i, location.column + j)):
                    return False
        return True


    # this action changes de data shown by the type GameBoard, the data that must be shown is,
    # the shape, and the squares with token
    def __repr__(self):
        tamany = self.get_shape()
        print(tamany.width,end='')
        print("x", end = '')
        print(tamany.height,end='')
        print(" board: ", end='')
        tokens = self.search_tokens()
        print(tokens, end="")
        return ""


    # this action counts how many tokens are in every row, it returns it in a list
    def row_counters(self):
        size = self.get_shape()
        row_counter = []        
        for i in range(size.height-1, -1, -1):
            counter = 0
            for j in range(size.width):
                if self.has_token(Location(i,j)):
                    counter += 1
            row_counter.append(counter)
        return row_counter

    # this action counts how many tokens are in every column, it returns it in a list
    def column_counters(self):
        size = self.get_shape()
        column_counter = []        
        for j in range(size.width):
            counter = 0
            for i in range(size.height):
                if self.has_token(Location(i,j)):
                    counter += 1
            column_counter.append(counter)
        return column_counter
        
