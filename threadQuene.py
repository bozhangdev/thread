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
    while (a < 513):
        b = random.randint(0, 511)
        c = random.randint(0, 126)
        if terrain[(b, c)] == 0:
            terrain[(b, c)] = 1
            crowd.append([b, c])
            a += 1


def moveCrowd(*n):
    lock.acquire()
    try:
        print("ffff")
    finally:
        lock.release()


def movePeople():
    print("aaaaa")


def hasPeople():
    for (d, x) in terrain.items():
        if x == 1:
            return True
    return False


if __name__ == '__main__':
    generateTerrain()
    generateObstacle()
    generateCrowd()
    while (hasPeople()):
        for a in crowd:
            t = threading.Thread(target=moveCrowd, args=(a))
            t.start()
            t.join()
