from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block
    state = 0

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return
		
    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen
		
    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        self.state = TetrisState.NewBlock
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        return

    def accept(self, key):
        self.key = key

        if self.state == TetrisState.NewBlock:
            self.currBlk = self.init_block()

        tempBlk = self.do(self.currBlk)


        if tempBlk.anyGreaterThan(1):
            tempBlk = self.undo(self.currBlk)

            if self.state == TetrisState.NewBlock:
                self.oScreen = Matrix(self.iScreen)
                self.oScreen.paste(tempBlk, self.top, self.left)

                self.state = TetrisState.Finished
            
            elif key == ' ' or key == 's':
                self.iScreen.paste(tempBlk, self.top, self.left)
                self.deleteFullLines(tempBlk)

                self.state = TetrisState.NewBlock

            return self.state

        else: 
            self.state = TetrisState.Running

            return self.state

    def init_block(self):
        if self.state == TetrisState.NewBlock:
            self.top = 0
            self.left = self.iScreenDw + self.iScreenDx//2 - 2
            self.rotation = int(self.key[0])
            self.block_type = int(self.key[1])

        block = Tetris.setOfBlockObjects[self.block_type][self.rotation]
        currBlk = Matrix(block)

        return currBlk

    def do(self, block):
        if self.key == 'a':
            self.left -= 1

        elif self.key == 'd':
            self.left += 1

        elif self.key == 's':
            self.top += 1

        elif self.key == 'w':
            self.rotation -= 1
            if self.rotation < 0:
                self.rotation = 3
            rotatedBlk = Tetris.setOfBlockObjects[self.block_type][self.rotation]
            block = Matrix(rotatedBlk) 
            self.currBlk = block

        elif self.key == ' ':
            while True:
                self.top += 1
                tempBlk = self.iScreen.clip(self.top, self.left, self.top + block.get_dy(), self.left + block.get_dx())
                tempBlk = tempBlk + block
                if tempBlk.anyGreaterThan(1):
                    break
 
        tempBlk = self.iScreen.clip(self.top, self.left, self.top + block.get_dy(), self.left + block.get_dx())
        tempBlk = tempBlk + block

        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(tempBlk, self.top, self.left)

        return tempBlk

    def undo(self, block):
        if self.key == 'a':
            self.left += 1

        elif self.key == 'd':
            self.left -= 1

        elif self.key == ' ' or self.key == 's':
            self.top -= 1

        elif self.key == 'w':
            self.rotation += 1
            if self.rotation > 3:
                self.rotation = 0

            rotatedBlk = Tetris.setOfBlockObjects[self.block_type][self.rotation]
            block = Matrix(rotatedBlk)
            self.currBlk = block

        tempBlk = self.iScreen.clip(self.top, self.left, self.top + block.get_dy(), self.left + block.get_dx())
        tempBlk = tempBlk + block

        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(tempBlk, self.top, self.left)

        return tempBlk

    def deleteFullLines(self, block): # To be implemented!!
        j = 0
        for i in range(self.top + block.get_dy() - 1, self.top - 1, -1):
            if i >= self.iScreenDy or i < 0:
                continue
            line = self.get_line(i + j)
            if line.sum() == self.iScreenDx:
                newScreen = self.iScreen.clip(0, self.iScreenDw, i + j, self.iScreenDw + self.iScreenDx)
                newLine = Matrix([[0 for _ in range(self.iScreenDx)]])
                self.iScreen.paste(newScreen, 1, self.iScreenDw)
                self.iScreen.paste(newLine, 0, self.iScreenDw)

                j += 1


    def get_line(self, index):
        line = self.iScreen.clip(index, self.iScreenDw, index + 1, self.iScreenDw + self.iScreenDx)
        return line

    def printScreen(self):
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print("■", end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    #continue
            print()

    
### end of class Tetris():
