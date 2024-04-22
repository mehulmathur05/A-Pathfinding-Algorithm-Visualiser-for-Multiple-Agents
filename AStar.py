import pygame
import numpy as np
from queue import PriorityQueue

GRAY = (100, 100, 100)
DARKGRAY = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TURQUOISE = (64, 224, 208)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

nRows = 20
nCols = 20
totalWidth = 800
totalHeight = 800

class Block:
    def __init__(self, row, column, width, height, status = 'unexplored'):
        self.x = row*width
        self.y = column*height
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.setStatus(status)

    def setStatus(self, status = 'unexplored'):
        self.status = status
        self.setColor(status)

    def setColor(self, status):
        if (status == 'unexplored'):  self.color = GRAY
        if (status == 'exploring'):   self.color = TURQUOISE
        if (status == 'explored'):    self.color = GREEN
        if (status == 'obstacle'):    self.color = DARKGRAY
        if (status == 'start'):       self.color = BLUE
        if (status == 'goal'):        self.color = RED
        if (status == 'path'):        self.color = WHITE

    def isObstacle(self):
        return self.status == 'obstacle'
    
    def draw(self, win, padding = 1):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width-padding, self.height-padding))

    def getPos(self):
        return (self.row, self.column)
    
    def updateNeighbors(self, Grid):
        self.neighbors = []
        if self.row < nRows - 1 and not Grid[self.row+1][self.column].isObstacle():
            self.neighbors.append(Grid[self.row+1][self.column])

        if self.row > 0 and not Grid[self.row-1][self.column].isObstacle():
            self.neighbors.append(Grid[self.row-1][self.column])

        if self.column < nCols - 1 and not Grid[self.row][self.column+1].isObstacle():
            self.neighbors.append(Grid[self.row][self.column+1])

        if self.column > 0 and not Grid[self.row][self.column-1].isObstacle():
            self.neighbors.append(Grid[self.row][self.column-1])

def newGrid():
    Grid = []
    for i in range(nRows):
        row = []
        for j in range(nCols):
            row.append(Block(i, j, totalWidth/nRows, totalHeight/nCols))
        Grid.append(row)
    return Grid

def obstaclesGrid(Grid):
    obsGrid = Grid
    for i in range(len(obsGrid)):
        for j in range(len(obsGrid[0])):
            if obsGrid[i][j].status != 'obstacle':
                obsGrid[i][j].setStatus('unexplored')
                # obsGrid.append(block)

    return obsGrid


def draw(Grid, window):
    for row in Grid:
        for block in row:
            block.draw(window)
    pygame.display.update()

def h(node1, end):      #heuristic function using manhattan dist
    return (abs(node1[1] - end[1]) + abs(node1[0] - end[0]))

def retracePath(parent, end, Grid, win):
    path = [end]
    node = parent[end]
    while node in parent:
        node.setStatus('path')
        path.append(node)
        node = parent[node]
        #draw(Grid, win)
    path.append(node)
    return path

def A_Star(start, end, Grid, win):
    openSet = PriorityQueue()       #for all the nodes were interested in exploring next
    #closedSet = PriorityQueue()    #for all the explored nodes (already tracked by the status of Block)
    openSetHash = {start}                #a set to efficiently seach em (since difficult to search from the priority queue)
    parent = {}
    gScore = {}             # dictionary with key as the node and the value as the gscore of that node
    fScore = {}             # dictionary with key as the node and the value as the fscore of the node
    count = 0               # keeps track of nodes in the priority queue and serves as tiebreaker in case of draws in f val
    openSet.put((0,count, start))       # (fValue, count, node)
    for row in Grid:
        for block in row:
            gScore[block] = float("inf")
            fScore[block] = float("inf")

    gScore[start] = 0
    fScore[start] = h(start.getPos(), end.getPos())

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = openSet.get()[2]      #to get the first block in the open set
        openSetHash.remove(current)
        # print(current.getPos(), fScore[current], gScore[current], h(neighbor.getPos(), end.getPos()))

        if current == end:
            end.setStatus('goal')
            path = retracePath(parent, end, Grid, win)
            return path
        
        for neighbor in current.neighbors:
            gScoreTemp = gScore[current] + 1
            if gScoreTemp < gScore[neighbor]:
                parent[neighbor] = current
                gScore[neighbor] = gScoreTemp
                fScore[neighbor] = gScoreTemp + h(neighbor.getPos(), end.getPos())
                if neighbor not in openSetHash:
                    count+=1 
                    openSet.put((fScore[neighbor],-count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.setStatus('exploring')
        
        draw(Grid, win)

        if current!= start:
            current.setStatus('explored')
    
    return False


def main(Grid):
    pygame.init()
    win = pygame.display.set_mode((totalWidth, totalHeight))
    Working = True
    start = None
    end = None
    while True:
        draw(Grid, win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Working = False
                print("cut")
                pygame.quit()
                break

            elif pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row = int(pos[0] // (totalHeight/nRows))
                col = int(pos[1] // (totalWidth/nCols))
                block = Grid[row][col]
                if not start and block != end:
                    start = block
                    start.setStatus('start')

                elif not end and block != start:
                    end = block
                    end.setStatus('goal')

                elif block != end and block != start:
                    block.setStatus('obstacle')

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in Grid:
                        for block in row:
                            block.updateNeighbors(Grid)

                    path = A_Star(start, end, Grid, win)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    Grid = newGrid()
        if not Working: break
    
    if __name__ != '__main__': 
        # print("running")
        # print(Grid[0][0], path[0])
        return Grid, path
    
if __name__ == '__main__':
    Grid = newGrid()
    main(Grid)