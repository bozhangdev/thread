#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import random
import resource
import time

local = threading.local()
condition = threading.Condition()
terrain = {(0, 0): 0}
crowd = []


def generate_terrain():
    a = 0
    while a < 512:
        b = 0
        while b < 128:
            terrain[(a, b)] = 0
            b = b + 1
        a = a + 1


def generate_obstacle(a, b, c, d):
    for i in range(a, b):
        for j in range(c, d):
            terrain[(i, j)] = 2


def generate_obstacles():
    generate_obstacle(10, 41, 20, 121)
    generate_obstacle(200, 401, 50, 71)
    generate_obstacle(50, 56, 5, 51)
    generate_obstacle(100, 151, 40, 81)
    b = 0
    while b < 2:
        c = 0
        while c < 2:
            terrain[(b, c)] = 3
            c = c + 1
        b = b + 1


def generateCrowd():
    a = 0
    while a < 2 ** 5 + 1:
        b = random.randint(0, 511)
        c = random.randint(0, 127)
        if terrain[(b, c)] == 0:
            terrain[(b, c)] = 1
            crowd.append([b, c])
            a += 1


def move_crowd(index):
    condition.acquire()
    movePeople(index)
    condition.release()


def movePeople(n):
    x = crowd[n][0]
    y = crowd[n][1]
    if y == 0:
        choice = (x - 1, 0)

        if terrain[choice] == 0:
            crowd[n] = [x - 1, 0]
            terrain[(x - 1, 0)] = 1
            terrain[(x, y)] = 0
            print("%d move along the northern wall" % n)
            condition.notifyAll()
            return
        elif terrain[choice] == 1:
            print("%d wait at the northern wall" % n)
            condition.wait()
            return
        elif terrain[choice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive through the northern wall" % n)
            crowd[n] = [0, 0]
            return
        else:
            print("error")
            return

    elif x == 0:
        choice = (x, y - 1)
        if terrain[choice] == 0:
            crowd[n] = [0, y - 1]
            terrain[(0, y - 1)] = 1
            terrain[(0, y)] = 0
            print("%d move along the western wall" % (n))
            return
        elif terrain[choice] == 1:
            print("%d wait at the western wall" % (n))
            return
        elif terrain[choice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive through the western wall" % (n))
            crowd[n] = [0, 0]
            return
        else:
            print("error")
            return
    else:
        fistChoice = (x - 1, y - 1)
        secondChoice = (x - 1, y)
        thirdChoice = (x, y - 1)
        if fistChoice == 3 or secondChoice == 3 or thirdChoice == 3:
            terrain[(x, y)] = 0
            print("%d arrive" % (n))
            crowd[n] = [0, 0]
            return
        if terrain[fistChoice] == 0:
            terrain[fistChoice] = 1
            terrain[(x, y)] = 0
            crowd[n] = [x - 1, y - 1]
            print("%d move toward the northwest" % (n))
            return
        if terrain[fistChoice] == 1:
            print("%d wait for the northwest place" % (n))
            return
        if terrain[fistChoice] == 2:
            if terrain[secondChoice] == 0:
                terrain[secondChoice] = 1
                terrain[(x, y)] = 0
                crowd[n] = [x - 1, y]
                print("%d move toward the west" % (n))
                return
            elif terrain[secondChoice] == 1:
                print("%d wait for the west place" % (n))
                return
            elif terrain[secondChoice] == 2:
                if terrain[thirdChoice] == 0:
                    terrain[thirdChoice] = 1
                    terrain[(x, y)] = 0
                    crowd[n] = [x, y - 1]
                    print("%d move toward the north" % (n))
                    return
                elif terrain[thirdChoice] == 1:
                    print("%d wait for the north place" % (n))
                    return
                else:
                    print("error")
                    return


def has_people():
    for i in range(len(crowd)):
        if crowd[i] != [0, 0]:
            return True
    return False


if __name__ == '__main__':
    generate_terrain()
    generate_obstacles()
    generateCrowd()
    start = resource.getrusage(resource.RUSAGE_SELF)[0] + resource.getrusage(resource.RUSAGE_SELF)[1]
    startTime = time.time()
    while has_people():
        for index in range(len(crowd)):
            if crowd[index] != [0, 0]:
                t = threading.Thread(target=move_crowd, args=(index,))
                t.start()
                t.join()
    endTime = time.time()
    end = resource.getrusage(resource.RUSAGE_SELF)[0] + resource.getrusage(resource.RUSAGE_SELF)[1]
    print("Finish")
    print("The usage of CPU is: %s" % (end - start))
    print("The time of response is: %s" % (endTime - startTime))
