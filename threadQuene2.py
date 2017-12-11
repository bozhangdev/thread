#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import random
import resource
import time

local = threading.local()
lock = threading.Lock()
terrain = {(0, 0): 0}
crowd_left_top = []
crowd_right_top = []
crowd_left_buttom = []
crowd_right_buttom = []
k = 0


def generateTerrain():
    a = 0
    while (a < 512):
        b = 0
        while (b < 127):
            terrain[(a, b)] = 0
            b = b + 1
        a = a + 1


def generateObstacle(a, b, c, d):
    for i in range(a, b):
        for j in range(c, d):
            terrain[(i, j)] = 2


def generateObstacles():
    generateObstacle(10, 41, 20, 121)
    generateObstacle(200, 401, 50, 71)
    generateObstacle(50, 56, 5, 51)
    generateObstacle(100, 151, 40, 81)
    b = 0
    while (b < 2):
        c = 0
        while (c < 2):
            terrain[(b, c)] = 3
            c = c + 1
        b = b + 1


def generateCrowd():
    a = 0
    while (a < 2 ** 7 + 1):
        b = random.randint(0, 510)
        c = random.randint(0, 125)
        if terrain[(b, c)] == 0:
            terrain[(b, c)] = 1
            if b >= 0 and b <= 255 and c >= 0 and c <= 63:
                crowd_left_top.append([b, c])
            if b >= 256 and b <= 511 and c >= 0 and c <= 63:
                crowd_right_top.append([b, c])
            if b >= 0 and b <= 255 and c >= 64 and c <= 127:
                crowd_left_buttom.append([b, c])
            if b >= 256 and b <= 511 and c >= 64 and c <= 127:
                crowd_right_buttom.append([b, c])
            a += 1


class part(threading.Thread):
    def __init__(self, threadID, name, crowd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.crowd_temp = crowd
        self.a = [0, 0]

    def run(self):
        print ("Starting " + self.name)
        ok = True
        while ok:
            ok = False
            for i in self.crowd_temp:
                if i != [0, 0]:
                    ok = True
            for index in range(0, len(self.crowd_temp)):
                if self.crowd_temp[index] != [0, 0]:
                    if self.crowd_temp[index][0] == 256 or self.crowd_temp[index][1] == 64:
                        lock.acquire()
                        try:
                            self.crowd_temp[index] = self.movePeople(index, self.crowd_temp)
                        finally:
                            lock.release()
                    else:
                        self.crowd_temp[index] = self.movePeople(index, self.crowd_temp)

    def movePeople(self, n, crowd):
        global k
        k = k + 1
        x = crowd[n][0]
        y = crowd[n][1]
        if y == 0:
            choice = (x - 1, 0)
            if terrain[choice] == 0:
                crowd[n] = [x - 1, 0]
                terrain[(x - 1, 0)] = 1
                terrain[(x, y)] = 0
                print("%d move along the northern wall" % (n))
                return crowd[n]
            elif terrain[choice] == 1:
                print("%d wait at the northern wall" % (n))
                return crowd[n]
            elif terrain[choice] == 3:
                terrain[(x, y)] = 0
                print("%d arrive through the northern wall" % (n))
                crowd[n] = [0, 0]
                return crowd[n]
            else:
                print("error")
                return crowd[n]
        elif x == 0:
            choice = (x, y - 1)
            if terrain[choice] == 0:
                crowd[n] = [0, y - 1]
                terrain[(0, y - 1)] = 1
                terrain[(0, y)] = 0
                print("%d move along the western wall" % (n))
                return crowd[n]
            elif terrain[choice] == 1:
                print("%d wait at the western wall" % (n))
                return crowd[n]
            elif terrain[choice] == 3:
                terrain[(x, y)] = 0
                print("%d arrive through the western wall" % (n))
                crowd[n] = [0, 0]
                return crowd[n]
            else:
                print("error")
                return crowd[n]
        else:
            fistChoice = (x - 1, y - 1)
            secondChoice = (x - 1, y)
            thirdChoice = (x, y - 1)
            if fistChoice == 3 or secondChoice == 3 or thirdChoice == 3:
                terrain[(x, y)] = 0
                print("%d arrive" % (n))
                crowd[n] = [0, 0]
                return crowd[n]
            if terrain[fistChoice] == 0:
                terrain[fistChoice] = 1
                terrain[(x, y)] = 0
                crowd[n] = [x - 1, y - 1]
                print("%d move toward the northwest" % (n))
                return crowd[n]
            if terrain[fistChoice] == 1:
                print("%d wait for the northwest place" % (n))
                return crowd[n]
            if terrain[fistChoice] == 2:
                if terrain[secondChoice] == 0:
                    terrain[secondChoice] = 1
                    terrain[(x, y)] = 0
                    crowd[n] = [x - 1, y]
                    print("%d move toward the west" % (n))
                    return crowd[n]
                elif terrain[secondChoice] == 1:
                    print("%d wait for the west place" % (n))
                    return crowd[n]
                elif terrain[secondChoice] == 2:
                    if terrain[thirdChoice] == 0:
                        terrain[thirdChoice] = 1
                        terrain[(x, y)] = 0
                        crowd[n] = [x, y - 1]
                        print("%d move toward the north" % (n))
                        return crowd[n]
                    elif terrain[thirdChoice] == 1:
                        print("%d wait for the north place" % (n))
                        return crowd[n]
                    else:
                        print("error")
                        return crowd[n]


if __name__ == '__main__':
    generateTerrain()
    generateObstacles()
    generateCrowd()
    start = resource.getrusage(resource.RUSAGE_SELF)[0] + resource.getrusage(resource.RUSAGE_SELF)[1]
    startTime = time.time()

    ThreadList = []
    t1 = part("part1 on left top", "1", crowd_left_top)
    t2 = part("part1 on right top", "2", crowd_right_top)
    t3 = part("part1 on left bottom", "3", crowd_left_buttom)
    t4 = part("part1 on right bottom", "4", crowd_right_buttom)
    ThreadList.append(t1)
    ThreadList.append(t2)
    ThreadList.append(t3)
    ThreadList.append(t4)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()

    global k
    print ("moved %d steps" % (k))
    print (len(crowd_right_buttom) + len(crowd_left_buttom) + len(crowd_left_top) + len(crowd_right_top))

    endTime = time.time()
    end = resource.getrusage(resource.RUSAGE_SELF)[0] + resource.getrusage(resource.RUSAGE_SELF)[1]
    print("Finish")
    print("The usage of CPU is: %s" % (end - start))
    print("The time of response is: %s" % (endTime - startTime))
