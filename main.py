# This file contains the main function for the Catan Player project.

from board import CatanBoard

def main():
    myboard = CatanBoard()
    myboard.play()
    #tileList given left->right top->bottom
    #tileList = [('ore', 10), ('wool', 2), ('lumber', 9), ('grain', 12), ('brick', 6), ('wool', 4), ('brick', 10), ('grain', 9), ('lumber', 11), ('desert', 0), ('lumber', 3), ('ore', 8), ('lumber', 8), ('ore', 3), ('grain', 4), ('wool', 5), ('brick', 5), ('grain', 6), ('wool', 11)]
    #myboard.setTerrain(tileList)
    #for node in myboard.nodelist.values():
    #    nears = [nb.returns for nb in node.neighbors.keys()]
    #    print("Node is: {}. Node neighb is: {}".format(node.returns, nears))

if __name__ == "__main__":
    main()
