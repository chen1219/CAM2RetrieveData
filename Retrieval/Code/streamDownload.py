import cv2
import sys
import time


def loadStreams():
    print ("Loading Streams")
    tick = time.time()
    streamQueue = []
    inputFile = open("m3u8s.txt", 'r')
    streamNo=0
    for line in inputFile:
        cap = cv2.VideoCapture(line)
        if(cap.isOpened()):
            streamQueue.append(cap)
            streamNo += 1
    print (str(streamNo) + " streams opened")
    print ("Ellapsed time: " + str(time.time() - tick))
    downloadImages(streamQueue, streamNo)


def downloadImages(streamQueue, streamNo):
    raw_input("Press enter to download images")
    sys.stdout.flush()
    tick = time.time()
    imageData = []
    # framesSaved = 0
    breaker = False
    totalNumImages = 500
    totalNumStreams = len(streamQueue)

    while (True):
        try:
            stream = streamQueue.pop()
            for x in range(totalNumImages/totalNumStreams):
                image = stream.read()[1]
                imageData.append(image)
        except Exception as e:
            if (e != "pop from empty list"):
                print ("Breaking Exception: " + str(e))
            else:
                print ("Downloaded All Images")
            breaker=True
            break
        if breaker:
            break
    print ("Ellapsed time: " + str(time.time()-tick))
    saveImages(imageData, streamNo)


def saveImages(imageData, streamNo):
    raw_input("Press enter to save images")
    sys.stdout.flush()
    tick = time.time()
    fileNumber = 0
    for frame in imageData:
        fileName = ("z_Camera" + str(streamNo) + "img no" + str(fileNumber) + ".jpg")
        cv2.imwrite(fileName, frame)
        fileNumber += 1
    print ("Ellapsed time: " + str(time.time() - tick))


if __name__ == '__main__':
    print ("Starting")
    loadStreams()
    print ("Ending")








