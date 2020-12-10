from matrix import *

import random

def draw_matrix(m):
    array = m.get_array()
    for y in range(m.get_dy()):
        for x in range(m.get_dx()):
            if array[y][x] == 0:
                print("□", end='')
            elif array[y][x] == 1:
                print("■", end='')
            else:
                print("XX", end='')
        print()


###
### initialize variables
###
I = [ [ [ 0 , 0 , 1 ,0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] ], # 일자
       [ [ 1 , 1 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 0 , 1 , 0] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] ],
       [ [ 1 , 1 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ] ]
L = [ [ [ 1 , 0 , 0 , 0 ] , [ 1 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ], #ㄴ자
       [ [ 1 , 1 , 0 , 0 ] , [ 1 , 0 , 0 , 0 ] , [ 1 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 1 , 1 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] ] ]
H = [ [ [ 0 , 1 , 0 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] ], #H 반쪽
       [ [ 0 , 0 , 1 , 1 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 1 , 0 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 0 , 1 , 1 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ] ]
T = [ [ [ 0 , 0 , 1 , 0 ] , [ 0 , 1 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ], #ㅗ 자
       [ [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 1 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 1 , 1 , 1 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 0 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] ] ]
a = [ [ [ 0 , 0 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 1 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ], #H 반쪽 반대
       [ [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 0 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 1 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ] ]
b = [ [ [ 0 , 0 , 0 , 1 ] , [ 0 , 1 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ], #ㄴ 반대
       [ [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 0 ] , [ 0 , 0 , 1 , 1 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 1 , 1 , 1 ] , [ 0 , 1 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 0 , 1 , 1 ] , [ 0 , 0 , 0 , 1 ] , [ 0 , 0 , 0 , 1 ] , [ 0 , 0 , 0 , 0 ] ] ]
c = [ [ [ 0 , 1 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ], # 정사각형
       [ [ 0 , 1 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 1 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ],
       [ [ 0 , 1 , 1 , 0 ] , [ 0 , 1 , 1 , 0 ] , [ 0 , 0 , 0 , 0 ] , [ 0 , 0 , 0 , 0 ] ] ]

### integer variables: must always be integer!
iScreenDy = 15
iScreenDx = 10
iScreenDw = 4
top = 0
left = iScreenDw + iScreenDx//2 - 2
arrayBlk=[I,L,H,T,a,b,c]
i=random.randint(0, 6)
j=0
newBlockNeeded = False

arrayScreen = [
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ] ]

###
### prepare the initial screen output
###  
iScreen = Matrix(arrayScreen)
oScreen = Matrix(iScreen)
currBlk = Matrix(arrayBlk[i][j])
tempBlk = iScreen.clip(top, left, top+currBlk.get_dy(), left+currBlk.get_dx())
tempBlk = tempBlk + currBlk
oScreen.paste(tempBlk, top, left)
draw_matrix(oScreen); print()

###
### execute the loop
###

while True:
    key = input('Enter a key from [ q (quit), a (left), d (right), s (down), w (rotate), \' \' (drop) ] : ')
    if key == 'q':
        print('Game terminated...')
        break
    elif key == 'a': # move left
        left -= 1
    elif key == 'd': # move right
        left += 1
    elif key == 's': # move down
        top += 1
    elif key == 'w': # rotate the block clockwise
        j += 1
        if j > 3:
            j = 0
    elif key == ' ': # drop the block
        while not tempBlk.anyGreaterThan(1):
            top += 1
            currBlk = Matrix(arrayBlk[i][j])
            tempBlk = iScreen.clip(top, left, top + currBlk.get_dy(), left + currBlk.get_dx())
            tempBlk = tempBlk + currBlk
        top -= 1
        newBlockNeeded = True
    else:
        print('Wrong key!!!')
        continue

    currBlk = Matrix(arrayBlk[i][j])
    tempBlk = iScreen.clip(top, left, top+currBlk.get_dy(), left+currBlk.get_dx())
    tempBlk = tempBlk + currBlk
    if tempBlk.anyGreaterThan(1):
        if key == 'a': # undo: move right
            left += 1
        elif key == 'd': # undo: move left
            left -= 1
        elif key == 's': # undo: move up
            top -= 1
            newBlockNeeded = True
        elif key == 'w': # undo: rotate the block counter-clockwise
            j -= 1
            if j < 0:
                j = 3
        elif key == ' ': # undo: move up
            print('Not implemented')

        currBlk = Matrix(arrayBlk[i][j])
        tempBlk = iScreen.clip(top, left, top+currBlk.get_dy(), left+currBlk.get_dx())
        tempBlk = tempBlk + currBlk

    oScreen = Matrix(iScreen)
    oScreen.paste(tempBlk, top, left)
    draw_matrix(oScreen); print()

    if newBlockNeeded:
        iScreen = Matrix(oScreen)
        top = 0
        left = iScreenDw + iScreenDx//2 - 2
        newBlockNeeded = False
        i = random.randint(0, 6)
        j = 0
        currBlk = Matrix(arrayBlk[i][j])
        tempBlk = iScreen.clip(top, left, top+currBlk.get_dy(), left+currBlk.get_dx())
        tempBlk = tempBlk + currBlk

        if tempBlk.anyGreaterThan(1):
            print('Game Over!!!')
            break
        
        oScreen = Matrix(iScreen)
        oScreen.paste(tempBlk, top, left)
        draw_matrix(oScreen); print()
        
###
### end of the loop
###
