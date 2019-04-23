import cv2 as cv
from IPython.display import Image

import sys, random, argparse 
import numpy as np 
import math 

def findDarkSpots(img, limit=50):
    """ Find spots darker than the limit in the grayscale img."""
    posList = []
    for row in range(len(img)):
        for col in range(len(img[0])):
            if (img[row][col] <= limit):
                pos = (row, col, img[row][col])
                posList.append(pos)
    return posList    

def drawCenters(frame, centers):
    """ Draws centers onto frames."""
    # https://www.programcreek.com/python/example/77058/cv2.KeyPoint
    keypoints = []
    for center in centers:
        y = center[0]
        x = center[1]
        keypoints.append(cv.KeyPoint(x=x,y=y,_size=10))
    kpFrame = cv.drawKeypoints(frame, keypoints, None, color=(0, 255, 0))
    return kpFrame

def euclideanDistance(pointA, pointB):
    """ Finds euclidean distance from point A to point B."""
    x = pointA[0] - pointB[0]
    y = pointA[1] - pointB[1]
    return (x**2 + y**2)**.5

def greedySetCoverAlgorithm(points, trashcanCount = 5, trashDist = 200):
    """ Greedy algorithm for set cover. Takes key points and we want to get the most objects
    we can with each iteration."""
    
    sets = []
    while points and trashcanCount > 0: 
        maxPoints = []
        for point in points:
            tempSet = [point]
            for otherPoint in points:
                if otherPoint != point and euclideanDistance(point, otherPoint) < trashDist:
                    tempSet.append(otherPoint)
            if len(tempSet) > len(maxPoints):
                maxPoints = tempSet[:]
        sets.append(maxPoints)
        print(sets)
        
        for point in maxPoints:
            for p in range(len(points)):
                if euclideanDistance(point, points[p]) == 0:
                    points.pop(p)
                    break 
        trashcanCount = trashcanCount - 1
    return sets

def setCenters(sets):
    """ Find center of each set."""
    centers = []
    for setter in sets:
        centers.append(setter[0])
    return centers 

def visualizeRadius(imgFile, centers, radius):
    """ Draw centers and corresponding circles on img."""
    tempImg = cv.imread(imgFile)
    for center in centers:
        circle = cv.circle(tempImg, (center[0], center[1]), radius, (0, 255, 0), 5)
        cv.imwrite(imgFile, circle)
        tempImg = cv.imread(imgFile)
    return tempImg

def main():
    """ 
    1) Construct args parse.
    2) Read in files.
    3) Find dark spot positions.
    4) Find sets using greedy set cover algorithm.
    5) Get center of sets.
    6) Draw the trash radii.
    """

    parser = argparse.ArgumentParser(description=" Determine Optimal Positions for TrashCans using Greedy Set Cover Algorithm.") 
    parser.add_argument('--file', dest='file', required=True) 
    parser.add_argument('--trashCanCount', dest='trashCanCount', required=False) 
    parser.add_argument('--darkThresh', dest='darkThresh', required=False) 
    parser.add_argument('--trashDist',dest='trashDist', required=False) 
    args = parser.parse_args() 
    imgFile = args.file
    
    beachFile = cv.imread(imgFile)
    grayBeach = cv.cvtColor(beachFile, cv.COLOR_BGR2GRAY)

    pos = findDarkSpots(grayBeach, int(args.darkThresh))
    sets = greedySetCoverAlgorithm(pos, int(args.trashCanCount), int(args.trashDist))
    centers = setCenters(sets)
    print(centers)
    final = visualizeRadius(imgFile, centers, int(args.trashDist))
    cv.imshow("final", final)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__': 
    main() 
        