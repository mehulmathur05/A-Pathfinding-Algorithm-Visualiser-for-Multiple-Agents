from AStar import *
import pygame

class Agent:
    def __init__(self, sNo, start, end, path):
        self.sNo = sNo
        self.start = start
        self.end = end
        self.path = path
        self.row = start.row
        self.column = start.column
        self.x = start.x
        self.y = start.y

    def draw(self, win):
        self.circle = pygame.draw.circle(win, PURPLE, (self.x + self.start.width//2, self.y + self.start.height//2), min(self.start.width/2, self.start.height/2), 0)

        font = pygame.font.SysFont("Arial", int(min(self.start.width, self.start.height)*0.9))
        text = font.render(str(self.sNo), True, WHITE)
        self.text = win.blit(text, (self.x + text.get_width()/2, self.y))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.x = row*self.start.width
        self.y = column*self.start.height
        # self.circle.move((self.x + self.start.width//2, self.y + self.start.height//2))
        # self.text.move()



# def invertPath(path):
#     pathInv = path
#     length = len(path)
#     for i in range(length):
#         pathInv[length-1-i] = path[i]
#     return pathInv

def moveAgents(agents, win):
    maxLen = 0
    for agent in agents:
        maxLen = max(len(agent.path), maxLen)
    for i in range(maxLen):
        for agent in agents:
            if (i < len(agent.path) - 1):
                step = agent.path[i+1]
                agent.path[i].draw(win)
                # pygame.display.update()
                agent.move(step.row, step.column)
                agent.draw(win)
        pygame.display.update()
        pygame.time.wait(500)

def master():
    Grids = []
    paths = []
    Agents = []
    n = 2
    Grid = newGrid()
    for i in range(n):
        Grid, path_ = main(Grid)
        Grids.append(Grid)
        paths.append(path_)
        Grid = obstaclesGrid(Grid)

    count = 0
    pygame.init()
    win = pygame.display.set_mode((totalWidth, totalHeight))
    draw(Grid, win)
    Running = True

    for path_ in paths:
        count+=1
        path = path_[::-1]
        #print(len(path))
        agent = Agent(count, path[0], path[-1], path)
        Agents.append(agent)
        path[0].setStatus('start')      #change accly later
        path[-1].setStatus('goal')      #change accly later
        for block in path:
            print(block.status != 'start' and block.status != 'goal')
            if block.status != 'start' and block.status != 'goal':
                block.setStatus('path')
            block.draw(win)
        agent.draw(win)
        pygame.display.update()

    moveAgents(Agents, win)
    while Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                pygame.quit()
                break

master()