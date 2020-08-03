import threading
import pprint as pp
from MarkovChain import *

# globals
ENERGY_COST = [0, 1, 2, 3]
MAP = np.loadtxt("Terrain.txt", dtype = 'i', delimiter = ',')

class Robot(threading.Thread):

    def __init__(self, battery, motor, camera, behaviour):
        threading.Thread.__init__(self)
        self.isRunning = True
        self.position = [SIZE - 1, 0]
        self.battery = battery
        self.motor = motor
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * 60)
        self.cost = (battery * 100) + (motor * 100) + (camera * 100)
        self.progressMap = np.copy(MAP)
        self.progressMap[self.position[0], self.position[1]] = 5
        self.printInfo()

    def move(self, moveX, moveY):
        x = self.position[0]
        y = self.position[1]
        movementCost = ENERGY_COST[MAP[x, y]]
        if movementCost > self.batteryLeft:
            self.batteryLeft = 0
            self.isRunning = False
        else:
            self.batteryLeft -= movementCost
            self.position[0] += moveX
            self.position[1] += moveY
            self.progressMap[self.position[0], self.position[1]] = 5
        self.printInfo()

    def run(self):
        # get current node
        # get next nodes
        # select a node based on probability
        # (to read arc probability use: self.behaviour[currentNode][nextNode])
        # move
        pass

    def printInfo(self):
        print(self.progressMap)
        print("Motor:", self.motor, "Battery:", self.battery, "Remaining:", self.batteryLeft, "Camera:", self.camera)

    def printMarkovChain(self):
        pp.pprint(self.behaviour)

    def getNextNodes(self):
        x = self.position[0]
        y = self.position[1]
        nodes = []
        if y - 1 >= 0:
            nodes += self.getNodeCode(x, y - 1, 1)
        if y + 1 < SIZE:
            nodes += self.getNodeCode(x, y + 1, 2)
        if x - 1 >= 0:
            nodes += self.getNodeCode(x - 1, y, 3)
        if x + 1 < SIZE:
            nodes += self.getNodeCode(x + 1, y, 4)
        return nodes

    def getNodeCode(self, x, y, direction):
        terrain = MAP[x, y]
        if terrain != 0 and terrain <= self.motor:
            return [direction + (self.battery * 10) + (self.motor * 100) + (terrain * 1000)]