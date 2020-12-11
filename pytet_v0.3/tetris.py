from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
    Hitwall = 3
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

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
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        return

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
        print()

    def deleteFullLines(self, top): # To be implemented!!
        deleted = 0
        blkY = self.currBlk.get_dy() # 블럭 크기
 
        for y in range(blkY-1,-1,-1):
            currY = top + y + deleted
            line = self.oScreen.clip(currY, 0, currY + 1, self.oScreen.get_dx())

            if (currY < self.iScreenDy and line.sum() == self.oScreen.get_dx()):
                temp = self.oScreen.clip(0, 0, currY, self.oScreen.get_dx())
                lineArr = [[0 for i in range(self.iScreenDx)]]
                newLine = Matrix(lineArr)

                self.oScreen.paste(temp, 1, 0) 
                self.oScreen.paste(newLine, 0, self.iScreenDw)
                deleted += 1
                


        print("line.sum() = {}\noScreen.dx = {}".format(line.sum(), self.oScreen.get_dx())) 
        print("dw = {}".format(self.iScreenDw))

        if line.sum() == self.oScreen.get_dx():
            print("full!")

        #self.oScreen.paste(line, 0, 0)
        

        return

    def accept(self, key, top, left):

        self.currBlk = Matrix(Tetris.setOfBlockObjects[int(key[1])][int(key[0])])
        self.tempBlk = self.iScreen.clip(top, left, top + self.currBlk.get_dy(), left + self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        if self.tempBlk.anyGreaterThan(1):
            self.deleteFullLines(top) 
            self.state = TetrisState.Hitwall
            return self.state
        else:
            self.state = TetrisState.Running


        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, top, left)

        return self.state

### end of class Tetris():
    
