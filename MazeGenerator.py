from random import randint
from MazeIndex import MazeIndex
from PIL import Image, ImageDraw

WALL_AROUND = 15
WALL_TOP = TOP = 1
WALL_RIGHT = RIGHT = 2
WALL_BOTTOM = BOTTOM = 4
WALL_LEFT = LEFT = 8
CELL_VISITED = 16

PEN_WIDTH = 1


class MazeGenerator:
    def __init__(self, cols=30, rows=15, size=30, offset=10):
        self.cols = cols
        self.rows = rows
        self.width = int(cols * size + offset * 1.5)  # image width
        self.height = int(rows * size + offset * 1.5)  # image height
        self.mazeMap = None
        self.path = None
        self.offset = offset
        self.size = size
        self.unsolved = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        self.solved = self.unsolved.copy()
        self.newMaze()

    def save(self, fileName='maze'):
        self.unsolved.save(fileName + ".png", "PNG")
        self.solved.save(fileName + "__solved.png", "PNG")

    def newMaze(self):
        self.mazeMap = [[WALL_AROUND for i in range(self.cols)] for i in range(self.rows)]
        self.unsolved.close()
        self.unsolved = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        self.solved.close()
        self.createMaze()
        self.path = self.findPath(MazeIndex(0, 0), MazeIndex(self.rows - 1, self.cols - 1), self.mazeMap)
        self.printMaze()
        self.printPath()

    def createMaze(self):
        stack = []
        self.mazeMap[0][0] |= CELL_VISITED
        unvisitedCount = self.rows * self.cols - 1
        currentCell = MazeIndex(0, 0)  # start from 0,0
        stack.append(currentCell)
        while unvisitedCount > 0:
            unvisitedNeighbours = MazeGenerator.getNeighbours(currentCell, self.mazeMap)
            if len(unvisitedNeighbours) > 0:
                targetCell = unvisitedNeighbours[randint(0, len(unvisitedNeighbours) - 1)]
                stack.append(currentCell)
                self.mazeMap[targetCell.x][targetCell.y] |= CELL_VISITED
                unvisitedCount -= 1
                MazeGenerator.removeWall(currentCell, targetCell, self.mazeMap)
                currentCell = targetCell
            else:
                currentCell = stack.pop()

    @staticmethod
    def getNeighbours(pos, mazeMap):
        x = pos.x
        y = pos.y
        cols = len(mazeMap[0])
        rows = len(mazeMap)
        result = []
        if x - 1 < 0:
            if y - 1 < 0:
                if mazeMap[x + 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x + 1, y))
                if mazeMap[x][y + 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y + 1))
            elif y + 1 > cols - 1:
                if mazeMap[x + 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x + 1, y))
                if mazeMap[x][y - 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y - 1))
            else:
                if mazeMap[x][y + 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y + 1))
                if mazeMap[x + 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x + 1, y))
                if mazeMap[x][y - 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y - 1))
        elif x + 1 > rows - 1:
            if y - 1 < 0:
                if mazeMap[x - 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x - 1, y))
                if mazeMap[x][y + 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y + 1))
            elif y + 1 > cols - 1:
                if mazeMap[x - 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x - 1, y))
                if mazeMap[x][y - 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y - 1))
            else:
                if mazeMap[x - 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x - 1, y))
                if mazeMap[x][y + 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y + 1))
                if mazeMap[x][y - 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y - 1))
        else:
            if y - 1 < 0:
                if mazeMap[x - 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x - 1, y))
                if mazeMap[x + 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x + 1, y))
                if mazeMap[x][y + 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y + 1))
            elif y + 1 > cols - 1:
                if mazeMap[x - 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x - 1, y))
                if mazeMap[x + 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x + 1, y))
                if mazeMap[x][y - 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y - 1))
            else:
                if mazeMap[x - 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x - 1, y))
                if mazeMap[x + 1][y] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x + 1, y))
                if mazeMap[x][y + 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y + 1))
                if mazeMap[x][y - 1] & CELL_VISITED != CELL_VISITED:
                    result.append(MazeIndex(x, y - 1))
        return result

    @staticmethod
    def getAvailable(targetCell, neighbours, mazeMap):  # find neighbour cells which have no wall
        result = []
        for cell in neighbours:
            if mazeMap[cell.x][cell.y] & CELL_VISITED != CELL_VISITED:
                xDiff = targetCell.x - cell.x
                yDiff = targetCell.y - cell.y
                if xDiff == 1 and mazeMap[targetCell.x][targetCell.y] & WALL_TOP != WALL_TOP:
                    result.append(cell)
                if xDiff == -1 and mazeMap[targetCell.x][targetCell.y] & WALL_BOTTOM != WALL_BOTTOM:
                    result.append(cell)
                if yDiff == 1 and mazeMap[targetCell.x][targetCell.y] & WALL_LEFT != WALL_LEFT:
                    result.append(cell)
                if yDiff == -1 and mazeMap[targetCell.x][targetCell.y] & WALL_RIGHT != WALL_RIGHT:
                    result.append(cell)
        return result

    @staticmethod
    def findPath(fromCell, toCell, mazeMap):  # find path from cell to cell
        src = [[cell & ~CELL_VISITED for cell in row] for row in mazeMap]
        path = []
        current = fromCell
        while current.x != toCell.x or current.y != toCell.y:
            neighs = MazeGenerator.getAvailable(current, MazeGenerator.getNeighbours(current, src), src)
            if len(neighs) > 0:
                prev = current
                current = neighs[randint(0, len(neighs) - 1)]
                prev.direction = MazeGenerator.getDirection(prev, current)
                path.append(prev)
                src[current.x][current.y] |= CELL_VISITED
            else:
                current = path.pop()
        return path

    @staticmethod
    def getDirection(fromCell, toCell):  # get direction of way from cell to cell
        xDiff = fromCell.x - toCell.x
        yDiff = fromCell.y - toCell.y
        if xDiff == 1:
            return TOP
        if xDiff == -1:
            return BOTTOM
        if yDiff == 1:
            return LEFT
        if yDiff == -1:
            return RIGHT

    @staticmethod
    def removeWall(c1, c2, mazeMap):  # c1, c2 - the cells in map between which need to remove the wall
        xDiff = c1.x - c2.x
        yDiff = c1.y - c2.y
        if xDiff == 1:
            mazeMap[c1.x][c1.y] &= ~WALL_TOP
            mazeMap[c2.x][c2.y] &= ~WALL_BOTTOM
        elif xDiff == -1:
            mazeMap[c2.x][c2.y] &= ~WALL_TOP
            mazeMap[c1.x][c1.y] &= ~WALL_BOTTOM
        elif yDiff == 1:
            mazeMap[c1.x][c1.y] &= ~WALL_LEFT
            mazeMap[c2.x][c2.y] &= ~WALL_RIGHT
        elif yDiff == -1:
            mazeMap[c2.x][c2.y] &= ~WALL_LEFT
            mazeMap[c1.x][c1.y] &= ~WALL_RIGHT

    def printMaze(self):
        # Открываем вход и выход в лабиринт
        self.mazeMap[0][0] &= ~WALL_TOP
        self.mazeMap[self.rows - 1][self.cols - 1] &= ~WALL_BOTTOM
        # //
        size = self.size
        offset = self.offset
        draw = ImageDraw.Draw(self.unsolved)
        for i, row in enumerate(self.mazeMap):
            for j, coll in enumerate(row):
                x = j * size + offset
                y = i * size + offset
                if coll & WALL_LEFT == WALL_LEFT:
                    draw.line((x, y, x, y + size), fill='black', width=PEN_WIDTH)
                if coll & WALL_BOTTOM == WALL_BOTTOM:
                    draw.line((x, y + size, x + size, y + size), fill='black', width=PEN_WIDTH)
                if coll & WALL_RIGHT == WALL_RIGHT:
                    draw.line((x + size, y, x + size, y + size), fill='black', width=PEN_WIDTH)
                if coll & WALL_TOP == WALL_TOP:
                    draw.line((x, y, x + size, y), fill='black', width=PEN_WIDTH)
        draw.rectangle((offset + size // 3,
                        offset + size // 3,
                        offset + size // 1.5,
                        offset + size // 1.5), fill='green')
        draw.rectangle(((self.cols - 1) * size + offset + size // 3,
                        (self.rows - 1) * size + offset + size // 3,
                        (self.cols - 1) * size + offset + size // 1.5,
                        (self.rows - 1) * size + offset + size // 1.5), fill='red')
        # Закрываем вход и выход в лабиринт
        self.mazeMap[0][0] |= WALL_TOP
        self.mazeMap[self.rows - 1][self.cols - 1] |= WALL_BOTTOM
        # //

    def printPath(self):
        path = self.path
        size = self.size
        offset = self.offset
        self.solved = self.unsolved.copy()
        draw = ImageDraw.Draw(self.solved)
        path.pop(0)
        for pos in path:
            x = pos.y * size + offset
            y = pos.x * size + offset
            if pos.direction == WALL_TOP:
                draw.polygon(
                    (x + size / 3, y + size / 1.5, x + size / 2, y + size / 3, x + size / 1.5, y + size / 1.5,
                     x + size / 2, y + size / 1.8), fill='blue')
            if pos.direction == WALL_RIGHT:
                draw.polygon(
                    (x + size / 3, y + size / 3, x + size / 1.5, y + size / 2, x + size / 3, y + size / 1.5,
                     x + size / 2.2, y + size / 2), fill='blue')
            if pos.direction == WALL_BOTTOM:
                draw.polygon(
                    (x + size / 3, y + size / 3, x + size / 2, y + size / 2.2, x + size / 1.5, y + size / 3,
                     x + size / 2, y + size / 1.5), fill='blue')
            if pos.direction == WALL_LEFT:
                draw.polygon(
                    (x + size / 1.5, y + size / 3, x + size / 1.8, y + size / 2, x + size / 1.5, y + size / 1.5,
                     x + size / 3, y + size / 2), fill='blue')

            # draw.rectangle((x + size // 3, y + size // 3, x + size // 1.5, y + size // 1.5), fill='blue')
