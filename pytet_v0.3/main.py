from tetris import *

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

class OnLeft():
    def run(self, t, key):
        t.left -= 1

        updateNeeded = True 
        return t.anyConflict(updateNeeded)


class OnRight():
    def run(self, t, key):
        t.left += 1

        updateNeeded = True
        return t.anyConflict(updateNeeded)

class OnDown():
    def run(self, t, key):
        t.top += 1

        updateNeeded = True
        return t.anyConflict(updateNeeded)

class OnUp():
    def run(self, t, key):
        t.top -= 1

        updateNeeded = True
        return t.anyConflict(updateNeeded)

class OnDrop():
    def run(self, t, key):
        updateNeeded = False
        while True:
            t.top += 1
            if t.anyConflict(updateNeeded):
                updateNeeded = False
                return t.anyConflict(updateNeeded)

class OnCw():
    def run(self, t, key):
        t.idxBlockDegree = (t.idxBlockDegree + 1)  % t.nBlockDegrees
        t.currBlk = t.setOfBlockObjects[t.idxBlockType][t.idxBlockDegree]

        updateNeeded = True
        return t.anyConflict(updateNeeded)

class OnCcw():
    def run(self, t, key):
        t.idxBlockDegree = (t.idxBlockDegree + t.nBlockDegrees - 1)  % t.nBlockDegrees
        t.currBlk = t.setOfBlockObjects[t.idxBlockType][t.idxBlockDegree]
        print(t.idxBlockDegree)

        updateNeeded = True
        return t.anyConflict(updateNeeded)

class OnNewBlock():
    def deleteFullLines(self, screen, blk, top, dy, dx, dw):
        if blk == 0:
            return screen

        j = 0
        tempLine = Matrix([[0 for _ in range(dx)]])
        for i in range(top + blk.get_dy() - 1, top - 1, -1):
            if i >= dy or i < 0:
                continue
            line = screen.clip(i+j, dw, i+j+1, dw + dx)
            if line.sum() == dx:
                tempScreen = screen.clip(0, dw, i+j, dx + dw)
                screen.paste(tempScreen, 1, dw)
                screen.paste(tempLine, 0, dw)

                j += 1

        return screen

    def run(self, t, key):
        t.oScreen = self.deleteFullLines(t.oScreen, t.currBlk, t.top, t.iScreenDy, t.iScreenDx, t.iScreenDw)

        t.iScreen = Matrix(t.oScreen)
        t.idxBlockType = int(key)
        t.idxBlockDegree = 0
        t.currBlk = t.setOfBlockObjects[t.idxBlockType][t.idxBlockDegree]
        t.top = 0
        t.left = t.iScreenDw + t.iScreenDx//2 - t.currBlk.get_dx()//2

        updateNeeded = True
        return t.anyConflict(updateNeeded)

class OnFinished():
    def run(self, t, key):
        print("OnFinished.run() called")

        return False

myOnLeft = OnLeft()
myOnRight = OnRight()
myOnUp = OnUp()
myOnDown = OnDown()
myOnDrop = OnDrop()
myOnCw = OnCw()
myOnCcw = OnCcw()
myOnNewBlock = OnNewBlock()
myOnFinished = OnFinished()

Tetris.setOperation("a", TetrisState.Running, myOnLeft, TetrisState.Running, myOnRight, TetrisState.Running)
Tetris.setOperation("d", TetrisState.Running, myOnRight, TetrisState.Running, myOnLeft, TetrisState.Running)
Tetris.setOperation("s", TetrisState.Running, myOnDown, TetrisState.Running, myOnUp, TetrisState.NewBlock)
Tetris.setOperation("w", TetrisState.Running, myOnCw, TetrisState.Running, myOnCcw, TetrisState.Running)
Tetris.setOperation(" ", TetrisState.Running, myOnDrop, TetrisState.Running, myOnUp, TetrisState.NewBlock)
Tetris.setOperation("0", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation("1", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation("2", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation("3", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation("4", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation("5", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)
Tetris.setOperation("6", TetrisState.NewBlock, myOnNewBlock, TetrisState.Running, myOnFinished, TetrisState.Finished)


if __name__ == "__main__":

    setOfBlockArrays = initSetOfBlockArrays()

    Tetris.init(setOfBlockArrays)

    board = Tetris(10, 8)

    idxBlockType = randint(0, 6)
    key = '0' + str(idxBlockType)
    state = board.accept(key)
    board.printScreen()

    while (1):
        key = input('Enter a key from [ q (quit), a (left), d (right), s (down), w (rotate), \' \' (drop) ] : ')

        if key != 'q':

            state = board.accept(key)
            board.printScreen()

            if(state == TetrisState.NewBlock):
                idxBlockType = randint(0, 6)
                key = '0' + str(idxBlockType)
                state = board.accept(key)
                if(state == TetrisState.Finished):
                    print('Game Over!!!')
                    board.printScreen()
                    break
                print()
                board.printScreen()

        else:
            print('Game aborted...')
            break



