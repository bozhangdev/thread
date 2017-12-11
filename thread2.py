#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import random
import resource
import time

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


def generate_crowd():
    a = 0
    while a < 2 ** 5 + 1:
        b = random.randint(0, 511)
        c = random.randint(0, 127)
        if terrain[(b, c)] == 0:
            terrain[(b, c)] = 1
            crowd.append([b, c, 0])
            a += 1


def has_people(position1, position2):
    x1 = position1[0]
    y1 = position1[1]
    x2 = position2[0]
    y2 = position1[1]
    for i in range(len(crowd)):
        if x1 <= crowd[i][0] < x2 and y1 <= crowd[i][1] < y2:
            if crowd[i] != [0, 0, 0] or crowd[i] != [0, 0, 1]:
                return True
    return False


def can_move(position):
    if terrain[(position[0] - 1, position[1])] == 0 or terrain[(position[0] - 1, position[1] - 1)] == 0 or terrain[(position[0], position[1] - 1)] == 0:
        return True
    return False


def move_people(n):
    x = crowd[n][0]
    y = crowd[n][1]
    if y == 0:
        choice = (x - 1, 0)

        if terrain[choice] == 0:
            crowd[n] = [x - 1, 0, 1]
            terrain[(x - 1, 0)] = 1
            terrain[(x, y)] = 0
            print("%d move along the northern wall" % n)
            return True
        elif terrain[choice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive through the northern wall" % n)
            crowd[n] = [0, 0, 0]
            return True
        else:
            print("error")
            return False

    elif x == 0:
        choice = (x, y - 1)
        if terrain[choice] == 0:
            crowd[n] = [0, y - 1, 1]
            terrain[(0, y - 1)] = 1
            terrain[(0, y)] = 0
            print("%d move along the western wall" % (n))
            return True
        elif terrain[choice] == 3:
            terrain[(x, y)] = 0
            print("%d arrive through the western wall" % (n))
            crowd[n] = [0, 0, 0]
            return True
        else:
            print("error")
            return True
    else:
        fistChoice = (x - 1, y - 1)
        secondChoice = (x - 1, y)
        thirdChoice = (x, y - 1)
        if fistChoice == 3 or secondChoice == 3 or thirdChoice == 3:
            terrain[(x, y)] = 0
            print("%d arrive" % (n))
            crowd[n] = [0, 0, 0]
            return True
        if terrain[fistChoice] == 0:
            terrain[fistChoice] = 1
            terrain[(x, y)] = 0
            crowd[n] = [x - 1, y - 1, 1]
            print("%d move toward the northwest" % (n))
            return True
        if terrain[fistChoice] == 2:
            if terrain[secondChoice] == 0:
                terrain[secondChoice] = 1
                terrain[(x, y)] = 0
                crowd[n] = [x - 1, y, 1]
                print("%d move toward the west" % (n))
                return True
            elif terrain[secondChoice] == 2:
                if terrain[thirdChoice] == 0:
                    terrain[thirdChoice] = 1
                    terrain[(x, y)] = 0
                    crowd[n] = [x, y - 1, 1]
                    print("%d move toward the north" % (n))
                    return True
                else:
                    print("error")
                    return False


class Part(threading.Thread):
    def __init__(self, threadID, name, condition, position1, position2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.position1 = position1
        self.position2 = position2
        self.condition = condition
        x1 = position1[0]
        y1 = position1[1]
        x2 = position2[0]
        y2 = position1[1]

    def run(self):
        while has_people(self.position1, self.position2):
            self.condition.acquire()
            is_all_moved = True
            for i in range(len(crowd)):
                if x1 <= crowd[i][0] < x2 and y1 <= crowd[i][1] < y2:
                    if crowd[i][2] == 0:
                        is_all_moved == False
            if is_all_moved:
                for j in range(len(crowd)):
                    if x1 <= crowd[j][0] < x2 and y1 <= crowd[j][1] < y2:
                        crowd[j][2] == 0
            is_all_moved == True
            a = 0
            position = [0, 0, 0]
            index = 0
            for k in range(len(crowd)):
                if x1 <= crowd[k][0] < x2 and y1 <= crowd[k][1] < y2 and crowd[k][2] == 0:
                    if (crowd[k][0] + crowd[k][1]) > a:
                        a = crowd[k][0] + crowd[k][1]
                        position = crowd[k]
                        index = k
            while not can_move(position) and (position[0] == x1 or position[1] == y1):
                self.condition.wait()
            moved = move_people(index)
            if moved:
                self.condition.notifyAll()
            self.condition.release()


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