from myplayer import *

import urllib.request

def read_file(file, url=True):
    """It reads a file of integers representing shapes. Each pair of consecutive integers represents
    a shape (width and height). It returns a list of shapes. If url is not asserted, file is assumed
    to be the name of a local file.
    """
    if url:
        with urllib.request.urlopen(file) as reader:
            items = reader.read().split()
    else:
        with open(file) as reader:
            items = reader.read().split()
            
    # Check there is an even number of items
    assert len(items) % 2 == 0, "Wrong number of items in " + file
    
    # Convert pairs of items to shapes, checking that the items are correct.
    R = []
    for i in range(0, len(items), 2):
        # Check the items are numbers
        assert items[i].isdigit() and items[i+1].isdigit(), "Some element in the list is not an integer"
        w, h = int(items[i]), int(items[i+1])
        assert w > 0 and h > 0, "Illegal size for a shape"
        R.append(Shape(w, h))
    return R


def play_game(player, blocks, show=True):
    """It plays the blocks puzzle using a pre-defined player. If show is asserted, the state of the player 
    is printed after placing each block. It returns the number of blocks that could be placed.
    """
    if show: print(player)
    count = 0
    for block in blocks:
        assert player.is_legal(block)
        loc = player.play(block)
        if loc is None: break
        player.place_block(loc, block)
        count += 1
        if show: print(player)
    return count

def main():
    url = "https://www.cs.upc.edu/~jordicf/Teaching/AP2/"
    files = ["blocks1.in", "blocks2.in", "blocks3.in", "blocks4.in"]
    %%time
    methods = ["simple", "expert"]
    width = range(10,16)
    for w in width:
        for f in files:
            print(w, 'x', w, ' ', f, ': ', sep='', end='')
            blocks = read_file(url+f, url=True)
            for m in methods:
                player = MyPlayer(w, w, method=m)
                nblocks = play_game(player, blocks, False)
                print(m,' (', nblocks, ' blocks) ', sep='', end='')
            print()
        print("-"*60)

main()