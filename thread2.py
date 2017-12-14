#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import random
import resource
import time

terrain = {(0, 0): 0}
crowd = []
con = threading.Condition()


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


def generate_crowd():
    a = 0
    while a < 512:
        b = random.randint(0, 511)
        c = random.randint(0, 127)
        if terrain[(b, c)] == 0:
            terrain[(b, c)] = 1
            if 0 <= b < 256 and 0 <= c < 64:
                crowd.append([b, c, 0, "1"])
            if 256 <= b < 512 and 0 <= c < 64:
                crowd.append([b, c, 0, "2"])
            if 0 <= b < 256 and 64 <= c < 128:
                crowd.append([b, c, 0, "3"])
            if 256 <= b < 512 and 64 <= c < 128:
                crowd.append([b, c, 0, "4"])
            a += 1


def has_people(n):
    for i in range(len(crowd)):
        if crowd[i][3] == n and crowd[i][2] != 2:
            return True
    return False


def decide_region(n):
    b = crowd[n][0]
    c = crowd[n][1]
    if 0 <= b < 256 and 0 <= c < 64:
        crowd[n][3] = "1"
    if 256 <= b < 512 and 0 <= c < 64:
        crowd[n][3] = "2"
    if 0 <= b < 256 and 64 <= c < 128:
        crowd[n][3] = "3"
    if 256 <= b < 512 and 64 <= c < 128:
        crowd[n][3] = "4"

def can_move(position):
    if position[2] != 2:
        if position[1] != 0 and position[0] != 0:
            if terrain[(position[0] - 1, position[1])] == 0 or terrain[(position[0] - 1, position[1] - 1)] == 0 or \
                    terrain[(position[0], position[1] - 1)] == 0:
                return True
        if position[1] == 0 and position[0] != 0 and (terrain[(position[0] - 1, position[1])] == 0 or terrain[(position[0] - 1, position[1])] == 3):
            return True
        if position[0] == 0 and position[1] != 0 and (terrain[(position[0], position[1] - 1)] == 0 or terrain[(position[0], position[1] - 1)] == 3):
            return True
    return False


def move_people(n):
    x = crowd[n][0]
    y = crowd[n][1]
    if y == 0:
        choice = (x - 1, 0)

        if terrain[choice] == 0:
            crowd[n][0] -= 1
            crowd[n][2] = 1
            terrain[(x - 1, 0)] = 1
            terrain[(x, y)] = 0
            decide_region(n)
            print("%d move along the northern wall" % n)
            return True
        if terrain[choice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive through the northern wall" % n)
            crowd[n][2] = 2
            return True
        else:
            print("No")
            return False

    elif x == 0:
        choice = (x, y - 1)
        if terrain[choice] == 0:
            crowd[n][1] -= 1
            crowd[n][2] = 1
            terrain[(0, y - 1)] = 1
            terrain[(0, y)] = 0
            print("%d move along the western wall" % (n))
            decide_region(n)
            return True
        elif terrain[choice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive through the western wall" % (n))
            decide_region(n)
            crowd[n][2] = 2
            return True
        else:
            print("error")
            return True
    else:
        fistChoice = (x - 1, y - 1)
        secondChoice = (x - 1, y)
        thirdChoice = (x, y - 1)
        if terrain[fistChoice] == 3 or terrain[secondChoice] == 3 or terrain[thirdChoice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive" % (n))
            crowd[n][2] = 2
            return True
        if terrain[fistChoice] == 0:
            terrain[fistChoice] = 1
            terrain[(x, y)] = 0
            crowd[n][0] -= 1
            crowd[n][1] -= 1
            crowd[n][2] = 1
            print("%d move toward the northwest" % (n))
            decide_region(n)
            return True
        if terrain[fistChoice] == 2 or terrain[fistChoice] == 1:
            if terrain[secondChoice] == 0:
                terrain[secondChoice] = 1
                terrain[(x, y)] = 0
                crowd[n][0] -= 1
                crowd[n][2] = 1
                print("%d move toward the west" % (n))
                decide_region(n)
                return True
            elif terrain[secondChoice] == 2 or terrain[secondChoice] == 1:
                if terrain[thirdChoice] == 0:
                    terrain[thirdChoice] = 1
                    terrain[(x, y)] = 0
                    crowd[n][1] -= 1
                    crowd[n][2] = 1
                    print("%d move toward the north" % (n))
                    decide_region(n)
                    return True
                else:
                    print("wait for: %s, %d" %(x, y))
                    return False


class part(threading.Thread):
    def __init__(self, threadID, name, position1, position2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.position1 = position1
        self.position2 = position2
        self.x1 = position1[0]
        self.y1 = position1[1]
        self.x2 = position2[0]
        self.y2 = position1[1]
        print ("init")

    def run(self):
        while has_people(self.name):
            if con.acquire():
                is_all_moved = True
                for i in range(len(crowd)):
                    if crowd[i][3] == self.name and crowd[i][2] == 0:
                        is_all_moved = False
                        break
                if is_all_moved:
                    for j in range(len(crowd)):
                        if crowd[j][3] == self.name:
                            crowd[j][2] = 0
                a = 640
                position = [0, 0, "0", 0]
                index = 0
                for k in range(len(crowd)):
                    if crowd[k][3] == self.name and crowd[k][2] == 0 and (crowd[k][0] + crowd[k][1]) < a:
                        a = crowd[k][0] + crowd[k][1]
                        position = crowd[k]
                        index = k
                while (not can_move(position)) and (position[0] == self.x1 or position[1] == self.y1):
                    con.wait()
                moved = move_people(index)
                if moved:
                    con.notifyAll()
                if not moved:
                    for j in range(len(crowd)):
                        if crowd[j][2] != 2:
                            crowd[j][2] = 0
                con.release()


if __name__ == '__main__':
    generate_terrain()
    generate_obstacles()
    generate_crowd()
    start = resource.getrusage(resource.RUSAGE_SELF)[0] + resource.getrusage(resource.RUSAGE_SELF)[1]
    startTime = time.time()

    ThreadList = []
    t1 = part("part1 on left top", "1", [0, 0], [256, 64])
    t2 = part("part1 on left bottom", "2", [256, 0], [512, 64])
    t3 = part("part1 on right top", "3", [0, 64], [256, 128])
    t4 = part("part1 on right bottom", "4", [256, 64], [512, 128])
    ThreadList.append(t1)
    ThreadList.append(t2)
    ThreadList.append(t3)
    ThreadList.append(t4)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()


    endTime = time.time()
    end = resource.getrusage(resource.RUSAGE_SELF)[0] + resource.getrusage(resource.RUSAGE_SELF)[1]
    print("Finish")
    print("The usage of CPU is: %s" % (end - start))
    print("The time of response is: %s" % (endTime - startTime))
