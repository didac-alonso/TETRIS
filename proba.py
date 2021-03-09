from gameboard import *
from myplayer import *

def main():
    b = GameBoard(Shape(4,3))
    shape = b.get_shape()
    b.put(Location(row=1, column=1)).put(Location(2, 0)).put(Location(column=3, row=0)).put(Location(column=5, row = 0)).put(Location(column=3, row = 0)).put(Location(-1,3))
    print("We have created a ", shape.width, "x", shape.height, " board.", sep='')
    print(b)
    print(b.__repr__())
    b
    b.put(Location(1,2), Shape(2,2))
    print(b)
    print(b.put(Location(2, 1)).put(Location(0, 2)).put(Location(0, 3)))
    print(b, "full rows: ", b.full_rows(), "; full columns: ", b.full_columns(), sep='')
    b.remove(Location(0,0),Shape(2,2))
    print(b)
    b.remove(Location(2,2),Shape(3,2))
    print(b)
    print(b.is_empty(Location(0,0), Shape(3,3)))
    

main()