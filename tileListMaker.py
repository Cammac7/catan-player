#quick-type to generate the initialized board list in python.
#Just type each tile as the number followed by the first letter of the resource
#left->right, top-bottom
#0d for the desert
tList = []
lMap = {'g':'grain','b':'brick','o':'ore','l':'lumber','w':'wool','d':'desert'}
while True:
    com = input('Next Tile:')
    if com == "build":
        print(tList)
        break
    if com == "undo":
        tList.pop()
    else:
        resource = lMap[com[-1:]]
        number = int(com[0:-1])
        tList.append((resource,number))


