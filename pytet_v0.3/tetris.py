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

#class Block(Matrix):
#    def generate_block(self):
#        block = Tetris.setOfBlockObjects[self.block_type][self.rotation]
#        super().__init__(block)
#        
#
#    def __init__(self, top, left, rotation, block_type):
#        self.top = top
#        self.left = left
#        self.rotation = rotation
#        self.block_type = block_type
#        
#        self.generate_block()
#
#        return
#
#    def rotate(self):
#        self.generate_block()
#        return
#
#### end of class Block():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0  
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
            currBlk = self.init_block()

        else: 
            currBlk = self.update(self.pastBlk)
        
        tempBlk = self.clip_and_paste(self.iScreen, currBlk)
 
        if tempBlk.anyGreaterThan(1):
            if self.state == TetrisState.NewBlock:
                self.oScreen = Matrix(self.iScreen)
                self.paste_block_to_screen(tempBlk, self.oScreen)

                self.state = TetrisState.Finished


            else:
                currBlk = self.undo(currBlk)

                if key == ' ' or key == 's':   
                    tempBlk = self.clip_and_paste(self.iScreen, currBlk)
                    self.paste_block_to_screen(tempBlk, self.iScreen)
                    self.deleteFullLines(tempBlk)

                    self.state = TetrisState.NewBlock

            return self.state

        self.oScreen = Matrix(self.iScreen)
        self.paste_block_to_screen(tempBlk, self.oScreen)

        self.pastBlk = currBlk
        self.state = TetrisState.Running

        return self.state
    
    def init_block(self):
        top = 0
        left = self.iScreenDw + self.iScreenDx//2 - 2
        rotation = int(self.key[0])
        block_type = int(self.key[1])

        block = Tetris.setOfBlockObjects[block_type][rotation]
        block = Block(block, top, left, block_type, rotation)

        return block


    def update(self, block):
        if self.key == 'a':
            block.left -= 1

        elif self.key == 'd':
            block.left += 1

        elif self.key == 's':
            block.top += 1

        elif self.key == 'w':
            block.rotation -= 1
            if block.rotation < 0:
                block.rotation = 3

            block = self.rotate(block)

        elif self.key == ' ':
            block.top += 1
            tempBlk = self.clip_and_paste(self.iScreen, block) 

            while not tempBlk.anyGreaterThan(1):
                block.top += 1
                tempBlk = self.clip_and_paste(self.iScreen, block)  
       
        return block

    def rotate(self, block):
        rotatedBlk = Tetris.setOfBlockObjects[block.block_type][block.rotation]
        return Block(rotatedBlk, block.top, block.left, block.block_type, block.rotation)


    def clip_and_paste(self, screen, block): 
        tempBlk = screen.clip(block.top, block.left, block.top + block.get_dy(), block.left + block.get_dx())
        tempBlk = tempBlk + block
        tempBlk = Block(tempBlk, block.top, block.left, block.block_type, block.rotation)

        return tempBlk


    def undo(self, block):
        if self.key == 'a':
            block.left += 1
        elif self.key == 'd':
            block.left -= 1
        elif self.key == 's':
            block.top -= 1
        elif self.key == ' ':
            block.top -= 1
        elif self.key == 'w':
            block.rotation += 1
            if block.rotation > 3:
                block.rotation = 0

            block = self.rotate(block)
          
        return block

    def paste_block_to_screen(self, block, screen):
        screen.paste(block, block.top, block.left)

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
        

    def deleteFullLines(self, block): # To be implemented!!
        j = 0
        for i in range(block.top + block.get_dy() - 1, block.top - 1, -1):
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



### end of class Tetris():
    
