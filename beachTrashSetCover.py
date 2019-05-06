import cv2 as cv
from IPython.display import Image

import sys, random, argparse 
import numpy as np 
import math 

def findDarkSpots(img, limit=50):
    """ 
    Find spots darker than the limit in the grayscale img.
    
    Inputs: 'img' - the image file
            'limit' - how dark our threshold is to quality a pixel value. 
    Ouputs: 'posList' - list of positions / pixels such that it is below the 'limit' value.
    """

    posList = []
    for row in range(len(img)):
        for col in range(len(img[0])):
            if (img[row][col] <= limit):
                pos = (row, col, img[row][col])
                posList.append(pos)
    print(posList)
    return posList    

def drawCenters(frame, centers):
    """ 
    Draws centers onto frames.
    
    Inputs: 'frame' - an image file we want to draw on.
            'centers' - list of positions such that they will be centers for circles drawn on frame.
    Output: 'kpFrame' - an image file with the drawn cicles. 
    """
    # https://www.programcreek.com/python/example/77058/cv2.KeyPoint

    keypoints = []
    for center in centers:
        x = center[0]
        y = center[1]
        keypoints.append(cv.KeyPoint(x=x,y=y,_size=10))
    kpFrame = cv.drawKeypoints(frame, keypoints, None, color=(0, 255, 0))
    return kpFrame

def euclideanDistance(pointA, pointB):
    """ 
    Finds euclidean distance from point A to point B.
    
    Inputs: 'pointA' - a position.
            'pointB' - a position.
    Output: Return - distance between the two points. 
    """

    x = pointA[0] - pointB[0]
    y = pointA[1] - pointB[1]
    return (x**2 + y**2)**.5

def greedySetCoverAlgorithm(points, aidDropCount = 5, trashDist = 200):
    """ 
    Greedy algorithm for set cover. Takes key points and we want to get the most objects we can with each iteration.
    
    Inputs: 'points' - list of positions / pixels such that it is below the 'limit' value.
            'aidDropCount' - number of aid packages we can drop. 
            'trashDist' - how much distance each aid package can cover.
    Outputs: 'sets' - the set of different circles and the points associated to each center.
    """
    
    sets = []
    while points and aidDropCount > 0: 
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
    print(sets)
    return sets

def setCenters(sets):
    """ 
    Find center of each set.
    
    Input: 'sets' - a set of sets each containing the different values associated with each circle.
    Output: 'centers' - a list of centers of the circles.
    """
    centers = []
    for setter in sets:
        x = []
        y = []
        for s in setter:
            x.append(s[0])
            y.append(s[1])
        avgX = np.average(x)
        avgY = np.average(y)
        centers.append((int(avgX), int(avgY)))
    return centers 

def visualizeRadius(imgFile, centers, radius):
    """ 
    Draw centers and corresponding circles on img.
    
    Inputs: 'imgFile' - the image file we want to edit.
            'centers' - the list of centers of the circles.
            'radius' - radius for the circles.
    Output: 'tempImg' - the edited image.
    """
    tempImg = cv.imread(imgFile)
    for center in centers:
        circle = cv.circle(tempImg, (center[1], center[0]), radius, (0, 255, 0), 5)
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
    6) Draw the aid radii.
    """

    parser = argparse.ArgumentParser(description=" Determine Optimal Positions for aid drops using Greedy Set Cover Algorithm.") 
    parser.add_argument('--file', dest='file', required=True) 
    parser.add_argument('--aidDropCount', dest='aidDropCount', required=False) 
    parser.add_argument('--darkThresh', dest='darkThresh', required=False) 
    parser.add_argument('--aidDist',dest='aidDist', required=False) 
    args = parser.parse_args() 
    imgFile = args.file
    
    beachFile = cv.imread(imgFile)
    grayBeach = cv.cvtColor(beachFile, cv.COLOR_BGR2GRAY)

    pos = findDarkSpots(grayBeach, int(args.darkThresh))
    sets = greedySetCoverAlgorithm(pos, int(args.aidDropCount), int(args.aidDist))
    centers = setCenters(sets)
    print(centers)
    final = visualizeRadius(imgFile, centers, int(args.aidDist))
    cv.imshow("final", final)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__': 
    main() 
        