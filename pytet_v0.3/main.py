from tetris import *
from random import *
import threading
import time

def LED_init():
    thread=threading.Thread(target=LMD.main, args=())
    thread.setDaemon(True)
    thread.start()
    return

def rotate(m_array, rot_num):
        N = len(m_array)
        rot_m = [[0] * N for _ in range(N)]

        if rot_num % 4 == 1:
            for i in range(N):
                for j in range(N):
                    rot_m[j][N-1-i] = m_array[i][j]
        elif rot_num % 4 == 2:
            for i in range(N):
                for j in range(N):
                    rot_m[N-1-i][N-1-j] = m_array[i][j]
        elif rot_num % 4 == 3:
            for i in range(N):
                for j in range(N):
                    rot_m[N-1-j][i] = m_array[i][j]
        else:
            for i in range(N):
                for j in range(N):
                    rot_m[i][j] = m_array[i][j]

        return rot_m

def initSetOfBlockArrays():
    arrayBlks = [  [ [ 0, 0, 1, 0 ],     # ㅁ
                    [ 0, 0, 1, 0 ],     # ㅁ
                    [ 0, 0, 1, 0 ],     # ㅁ
                    [ 0, 0, 1, 0 ] ],   # ㅁ
                  [ [0, 1, 0],              
                    [1, 1, 1],          # ㅗ
                    [0, 0, 0] ],
                  [ [1, 0, 0],
                    [1, 1, 1],          # ㄴ
                    [0, 0, 0] ],
                  [ [0, 0, 1],          #    ㅁ
                    [1, 1, 1],          # ㅁㅁㅁ 
                    [0, 0, 0] ],        #
                  [ [1, 1],             # ㅁ
                    [1, 1] ],           
                  [ [0, 1, 1],          #   ㅁㅁ
                    [1, 1, 0],          # ㅁㅁ 
                    [0, 0, 0] ],        #
                  [ [1, 1, 0],          # ㅁㅁ
                    [0, 1, 1],          #   ㅁㅁ
                    [0, 0, 0] ]         #
                ]

    nBlocks = len(arrayBlks)
    setOfBlockArrays = [[0] * 4 for _ in range(nBlocks)]

    for idxBlockType in range(nBlocks):
        for idxBlockDegree in range(4):
            rotate_matrix = rotate(arrayBlks[idxBlockType], idxBlockDegree)
            setOfBlockArrays[idxBlockType][idxBlockDegree] = rotate_matrix

    return setOfBlockArrays
    
if __name__ == "__main__":
    #LED_init()
    setOfBlockArrays = initSetOfBlockArrays()

    Tetris.init(setOfBlockArrays)
    board = Tetris(32, 16)

    idxBlockType = randint(0, 6)
    key = '0' + str(idxBlockType)
    top = 0
    left = board.iScreenDw + board.iScreenDx//2 - 2
    board.accept(key, top, left)
    board.printScreen()
    toBottom = False
      
    while (1):
        if not toBottom:
            key_input = input('Enter a key from [ q (quit), a (left), d (right), s (down), w (rotate), \' \' (drop) ] : ')
        else:
            top += 1

        if key_input != 'q':
          if key_input == 'a': # move left
              left -= 1
          elif key_input == 'd': # move right
              left += 1
          elif key_input == 's': # move down
              top += 1
          elif key_input == 'w': # rotate the block clockwise
              int_key = int(key[0]) + 1
              if int_key > 3:
                  int_key = 0
              key = str(int_key) + key[1]
          elif key_input == ' ':
              toBottom = True

          state = board.accept(key, top, left)
          if(state == TetrisState.Hitwall):
            if key_input == 'a': # undo: move right
                left += 1
            elif key_input == 'd': # undo: move left
                left -= 1
            elif key_input == 's': # undo: move up
                top -= 1
                state = TetrisState.NewBlock
            elif key_input == 'w': # undo: rotate the block counter-clockwise
                int_key = int(key[0]) - 1
                if int_key < 0:
                    int_key = 3
                key = str(int_key) + key[1]
            elif key_input == ' ':
                top -= 1
                toBottom = False
                state = TetrisState.NewBlock 

          board.printScreen()

          if(state == TetrisState.NewBlock):
              board.iScreen = Matrix(board.oScreen)
              idxBlockType = randint(0, 6)
              key = '0' + str(idxBlockType)
              top = 0
              left = board.iScreenDw + board.iScreenDx//2 - 2
              state = board.accept(key, top, left)
              if(state == TetrisState.Hitwall):
                  board.printScreen()
                  print('Game Over!!!')
                  break
              board.printScreen()

        else:
          print('Game aborted...')
          break
    

### end of pytet.py
