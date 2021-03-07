import collections

Shape = collections.namedtuple('Shape', 'width height')
Location = collections.namedtuple('Location', 'row column')

class GameBoard:

    #constructor
    def __init__(self, tamany):
        self.height = tamany.height
        self.width = tamany.width
        matriu =[]
        for i in range (tamany.height):
            fila =[]
            for j in range(tamany.width):
                fila.append('\u2b1c')
            matriu.append(fila)
        self.tauler = matriu

    def full_rows(self):
        tamany = self.get_shape()
        rows = []
        complete_row = ['\u2b1b']*tamany.width
        for i in range(tamany.height):   
            if self.tauler[i][:] == complete_row:
                rows.append(tamany.height -i -1) 
        return rows

    def full_columns(self):
        tamany = self.get_shape()
        columns = []
        complete_column = ['\u2b1b']*tamany.height
        board_transposed = list(zip(*self.tauler))
        for j in range(tamany.width):            
            if list(board_transposed[j][:]) == complete_column:
                columns.append(j) 
        return columns

    def has_token(self, location):
        return self.tauler[location.row][location.column] == '\u2b1b'

    def search_tokens(self):
        tokens_location = []
        size = self.get_shape()
        for i in range (size.height):
            for j in range (size.width):
                if self.has_token(Location(i,j)):
                    a = (size.height-1-i, j)
                    tokens_location.append(a)
        return tokens_location

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

    def out_bounds(self, location,tamany):
        return location.row >= tamany.height or location.row < 0 or location.column < 0 or location.column >= tamany.width

    def get_shape(self):
        width = self.width  
        h = self.height
        mesura = Shape(width, h)
        return mesura

    def transform_coordinates(self, location, tamany):
        return Location(tamany.height-location.row - 1,location.column)    

    def __str__(self):
        size = self.get_shape()
        for i in range(size.height):
            for j in range(size.width):
                print (self.tauler[i][j],end ="")
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
    #         self.tauler[location.row][location.column] = '\u2b1b'
    #     return self

    def fits(self, tamany, location, rectangle):
        for i in range(rectangle.height):
            for j in range(rectangle.width):    
                if self.out_bounds(Location(location.row - i, location.column + j),tamany):
                    return False
                elif self.has_token(Location(location.row - i, location.column + j)):
                    return False
        return True

    def put(self, location, rectangle = Shape(1,1)):
        tamany = self.get_shape()
        location = self.transform_coordinates(location, tamany)
        if rectangle != Shape(1,1) and not self.fits(tamany, location, rectangle):
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
                    self.tauler[location.row - i][location.column + j] = '\u2b1b'
        return self

    def remove(self, location):
        tamany = self.get_shape()
        location = self.transform_coordinates(location, tamany)
        self.tauler[location.row][location.column] = '\u2b1c'
        return self

    def is_empty(self,location):
        return not self.has_token(location)

    def __repr__(self):
        tamany = self.get_shape()
        print(tamany.width,end='')
        print("x", end = '')
        print(tamany.height,end='')
        print(" board: ", end='')
        tokens = self.search_tokens()
        print(tokens, end="")
        return ""

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
        
