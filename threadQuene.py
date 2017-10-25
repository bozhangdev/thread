#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import random

local = threading.local()
lock = threading.Lock()
terrain = {(0, 0): 0}
crowd = []


def generateTerrain():
    a = 0
    while (a < 512):
        b = 0
        while (b < 127):
            terrain[(a, b)] = 0
            b = b + 1
        a = a + 1


def generateObstacle():
    a = 0
    b = 0

    while (a < 1000):
        terrain[(random.randint(1, 510), random.randint(1, 125))] = 2
        a = a + 1

    while (b < 2):
        c = 0
        while (c < 2):
            terrain[(b, c)] = 3
            c = c + 1
        b = b + 1


def generateCrowd():
    a = 0
    while (a < 10):
        b = random.randint(0, 511)
        c = random.randint(0, 126)
        if terrain[(b, c)] == 0:
            terrain[(b, c)] = 1
            crowd.append([b, c])
            a += 1


def moveCrowd(index):
    lock.acquire()
    try:
        movePeople(index)
    finally:
        lock.release()


def movePeople(n):
    x = crowd[n][0]
    y = crowd[n][1]
    if y == 0:
        choice = (x - 1, 0)

        if terrain[(x - 1, 0)] == 0:
            crowd[n] = [x - 1, 0]
            terrain[(x - 1, 0)] = 1
            terrain[(x, y)] = 0
            print("%d move" % (n))
            return
        elif terrain[(x - 1, 0)] == 1:
            print("%d wait" % (n))
            return
        else:
            terrain[(x, y)] = 0
            print("%d arrive" % (n))
            del crowd[n]

    elif x == 0:
        if terrain[(0, y - 1)] == 0:
            crowd[n] = [0, y - 1]
            terrain[(0, y - 1)] = 1
            terrain[(0, y)] = 0
            print("%d move" % (n))
            return
        elif terrain[(0, y - 1)] == 1:
            print("%d wait" % (n))
            return
        else:
            terrain[(x, y)] = 0
            print("%d arrive" % (n))
            del crowd[n]
    else:
        fistChoice = (x - 1, y - 1)
        secondChoice = (x - 1, y)
        thirdChoice = (x, y - 1)
        if fistChoice == 3 or secondChoice == 3 or thirdChoice == 3:
            terrain[(x, y)] = 0
            print("%d arrive" % (n))
            del crowd[n]
        if terrain[fistChoice] == 0:
            terrain[fistChoice] = 1
            terrain[(x, y)] = 0
            crowd[n] = [x - 1, y - 1]
            print("%d bestmove" % (n))
            return
        if terrain[fistChoice] == 1:
            print("%d bestwait" % (n))
            return
        if terrain[fistChoice] == 2:
            if terrain[secondChoice] == 0:
                terrain[secondChoice] = 1
                terrain[(x, y)] = 0
                crowd[n] = [x - 1, y]
                print("%d secondmove" % (n))
                return
            elif terrain[secondChoice] == 1:
                print("%d secondwait" % (n))
                return
            else:
                if terrain[thirdChoice] == 0:
                    terrain[thirdChoice] = 1
                    terrain[(x, y)] = 0
                    crowd[n] = [x, y - 1]
                    print("%d thirdmove" % (n))
                    return
                elif terrain[thirdChoice] == 1:
                    print("%d thirdwait" % (n))
                    return


def hasPeople():
    for (d, x) in terrain.items():
        if x == 1:
            return True
    return False


if __name__ == '__main__':
    generateTerrain()
    generateObstacle()
    generateCrowd()
    index = 0
    while hasPeople():
        while index < len(crowd):
            t = threading.Thread(target=moveCrowd, args=(index,))
            t.start()
            t.join()
            index += 1
        index = 0
    print("finish")
