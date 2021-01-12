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
        if self.state == TetrisState.NewBlock:
            self.init_block_state(key)

        self.change_block_state(key)
        self.generate_block()
             
        if self.tempBlk.anyGreaterThan(1):
            if self.state == TetrisState.NewBlock:
                self.paste_temp_block_to_screen()
                self.state = TetrisState.Finished
                return self.state

            else:
                self.undo_block_state(key)

                if key == ' ' or key == 's':
                    self.iScreen = Matrix(self.oScreen)
                    self.deleteFullLines()
                    self.state = TetrisState.NewBlock

                return self.state

        self.paste_temp_block_to_screen()
 
        self.state = TetrisState.Running
        return self.state

    def init_block_state(self, key):
        self.top = 0
        self.left = self.iScreenDw + self.iScreenDx//2 - 2
        self.rotation = int(key[0])
        self.block_type = int(key[1])

    def generate_block(self):
        self.block = Tetris.setOfBlockObjects[self.block_type][self.rotation]
        self.currBlk = Matrix(self.block)
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

    def paste_temp_block_to_screen(self):
        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)

    def change_block_state(self, key):
        if key == 'a':
            self.left -= 1
        elif key == 'd':
            self.left += 1
        elif key == 's':
            self.top += 1
        elif key == 'w':
            self.rotation -= 1
            if self.rotation < 0:
                self.rotation = 3
        elif key == ' ':
            self.top += 1
            self.generate_block()
            while not self.tempBlk.anyGreaterThan(1):
                self.paste_temp_block_to_screen()
                self.top += 1
                self.generate_block()

    def undo_block_state(self, key):
        if key == 'a':
            self.left += 1
        elif key == 'd':
            self.left -= 1
        elif key == ' ' or key == 's':
            self.top -= 1
        elif key == 'w':
            self.rotation += 1
            if self.rotation > 3:
                self.rotation = 0


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

    def deleteFullLines(self): # To be implemented!!
        j = 0
        for i in range(self.top + self.tempBlk.get_dy() - 1, self.top - 1, -1):
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

class Colors:
    RED = '\033[31m'
    GREEN = '\033[32m' 
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'

class ColorTetris(Tetris):
    def accept(self, key):
        if self.state == TetrisState.NewBlock:
            self.init_block_state(key)

        self.change_block_state(key)
        self.generate_block()
             
        if self.is_block_crash():
            if self.state == TetrisState.NewBlock:
                self.paste_temp_block_to_screen()
                self.state = TetrisState.Finished
                return self.state

            else:
                self.undo_block_state(key)

                if key == ' ' or key == 's':
                    self.iScreen = Matrix(self.oScreen)
                    self.deleteFullLines()
                    self.state = TetrisState.NewBlock

                return self.state

        self.paste_temp_block_to_screen()
 
        self.state = TetrisState.Running
        return self.state

    def is_block_crash(self):
        block = self.block.get_array()
        tempBlk = self.tempBlk.get_array()
        for y in range(self.block._dy):
            for x in range(self.block._dx):
                if block[y][x] == 1 and tempBlk[y][x] > self.color:
                    return True 
        return False

    def init_block_state(self, key):
        super().init_block_state(key)
        self.color = randint(2, 7)

    def generate_block(self):
        self.block = Tetris.setOfBlockObjects[self.block_type][self.rotation]
        self.currBlk = Matrix(self.block)
        self.currBlk.mulc(self.color)
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top + self.currBlk.get_dy(), self.left + self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

    def change_block_state(self, key):
        if key == 'a':
            self.left -= 1
        elif key == 'd':
            self.left += 1
        elif key == 's':
            self.top += 1
        elif key == 'w':
            self.rotation -= 1
            if self.rotation < 0:
                self.rotation = 3
        elif key == ' ':
            self.top += 1
            self.generate_block()
            while not self.is_block_crash():
                self.paste_temp_block_to_screen()
                self.top += 1
                self.generate_block()

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
                elif array[y][x] == 2:
                    print(Colors.RED + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                elif array[y][x] == 3:
                    print(Colors.GREEN + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                elif array[y][x] == 4:
                    print(Colors.YELLOW + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                elif array[y][x] == 5:
                    print(Colors.BLUE + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                elif array[y][x] == 6:
                    print(Colors.MAGENTA + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                elif array[y][x] == 7:
                    print(Colors.CYAN + "■" + Colors.RESET, end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    #continue
            print()

    def deleteFullLines(self): # To be implemented!!
        j = 0
        for i in range(self.top + self.tempBlk.get_dy() - 1, self.top - 1, -1):
            if i >= self.iScreenDy or i < 0:
                continue
            line = self.get_line(i + j)
            if self.count_blocks_in(line) == self.iScreenDx:
                newScreen = self.iScreen.clip(0, self.iScreenDw, i + j, self.iScreenDw + self.iScreenDx)
                newLine = Matrix([[0 for _ in range(self.iScreenDx)]])
                self.iScreen.paste(newScreen, 1, self.iScreenDw)
                self.iScreen.paste(newLine, 0, self.iScreenDw)

                j += 1
                
    def count_blocks_in(self, line):
        line = line.get_array()
        count = 0
        for i in line:
            for j in i:
                if j > 1:
                    count += 1
        return count

### end of class ColorTetris():
    
