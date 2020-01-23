# Modules used 

import sys
import numpy as np 
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#A temporary fix for warnings when saving images
plt.rcParams.update({'figure.max_open_warning': 0})

class PathFinderClass:
    def __init__(self,shape,start,end):
        
        # Error handler (Beta)
        if shape in start or shape in end:
            print("ERROR! - Start or End points must be inside the map")
            sys.exit(1)
        
        
        self.start = start
        self.end = end
        self.shape = (shape,shape)
        self.maze = np.zeros(self.shape)
        self.neighbours = [(-1,0),(0,1) ,(1,0),(0,-1)]
        self.walls = []
       
    

    # method for quick run. Can be set number of walls and to show or not distance values from start
    def run(self, nWalls=0, showDistValues = True):
        self.resetMaze()
        self.randWalls(nWalls)
        distancesMap = self.calcDistances()
        path = self.calcPath()
        finalMap = self.plotMap(showDistValues)

        return {"bestPath": path[0], "costPath": path[1], "finalMap": finalMap}


    #Method for reseting the maze map characteristics
    def resetMaze(self):
        self.maze = np.zeros(self.shape)
        self.walls = []

    # Calculates all distances from start point
    def calcDistances(self, saveFig = False):
        openNodes = [self.start]
        checkedNodes = []
        inf = float("inf")
        f = 0

        while openNodes:
            node = openNodes.pop(0)
            checkedNodes.append(node)

            for n in self.neighbours:
                newNode = tuple(sum(i) for i in zip(node, n))
                
                #needs enhancements
                if (-1 not in newNode and newNode not in checkedNodes and self.shape[0] not in newNode
                 and inf != self.maze[newNode] and -1 != self.maze[newNode] and newNode not in openNodes):
                    self.maze[newNode] = self.maze[node] + 1
                    openNodes.append(newNode)
 
            # Condition to save maze figures if True 
            if saveFig:
                fig = self.plotMap(False)
                plt.savefig('Figure/figs' + str(f) + '.png')
                f = f + 1 
          
        return self.maze


    #Method to generate random walls at the maze (Beta Solution) 
    def randWalls(self, nBlocks):
        
        # Error handle (Beta)
        if nBlocks >= self.shape[0]*self.shape[1]:
            print("ERROR! - Number of walls must be smaller than the max number of tiles")
            sys.exit(1)

        size = len(self.maze)
        inf = float("inf") # not used anymore

        for i in range(nBlocks):
            node = (random.randint(0,size-1),random.randint(0,size-1))
            if node not in self.walls and node != self.start and node != self.end:
                self.walls.append(node)
                self.maze[node] = -1

        return self.maze

    #Calculates the best path from end to start (must have calculated the distances)
    def calcPath(self, saveFig = False):
        self.bestPath = []
        self.costPath = self.maze[self.end]
        
        cost = self.maze[self.end]
        bestPath = [self.end]
        inf = float("inf") # not used anymore!
        f = 0
        

        node = self.end
        while cost != 0:
            for n in self.neighbours:
                newNode = tuple(sum(i) for i in zip(node, n))
                if (-1 not in newNode and self.shape[0] not in newNode and
                 inf != self.maze[newNode] and -1 != self.maze[newNode]):

                    if self.maze[newNode] < cost:
                        cost = self.maze[newNode]
                        bestNode = newNode

            self.costPath += self.maze[bestNode]
            node = bestNode
            self.bestPath.append(node)

            # Condition to save maze figures if True 
            if saveFig:
                fig = self.plotMap(False)
                plt.savefig('Figure/2figs' + str(f) + '.png')
                f = f + 1 
 
        return (self.bestPath, self.costPath)

    # Method to plot the final map and the path 
    def plotMap(self,showValues = True):
        
        #Heatmap and path colors
        cmap = plt.cm.rainbow
        norm = plt.Normalize(self.maze.min(), self.maze.max())
        rgba = cmap(norm(self.maze))

        rgba[self.start[0], self.start[1], :3] = 0.7, 0.5, 0
        rgba[self.end[0], self.end[1], :3] = 0.7, 0.5, 0
        
        #Path colors
        for bestNode in self.bestPath:
            rgba[bestNode[0], bestNode[1], :3] = 0.59, 0.4, 0

        #Walls colors
        for wall in self.walls:
            rgba[wall[0], wall[1], :3] = 0.66, 0.66, 0.66

        fig, ax = plt.subplots()
        fig.suptitle(("Path Cost: ", self.costPath))
        ax.imshow(rgba, interpolation='nearest')

        if showValues:
            #Generate distances values
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if self.maze[j,i] == -1:
                        pass
                    elif (j,i) in self.bestPath:
                        ax.text(i,j, self.maze[j,i], ha = "center", va = "center", weight='bold')
                    else: 
                        ax.text(i,j, self.maze[j,i], ha = "center", va = "center")

        
      
        return fig