import cv2
import numpy as np
import hand_tracker as hand
from config import *
import autopy

SCREEN_WIDTH, SCREEN_HEIGHT = autopy.screen.size()
prevLocX, prevLocY = 0, 0
currLocX, currLocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

detector = hand.HandDetector(maxHands=2)
print("Virtual Mouse program started.")

while True:
    success, img = cap.read()
    if FLIP:
        img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        if fingers[1]==1:
            if fingers[2]==0:
                if x1>FRAME_REDUCTION and x1<CAM_WIDTH-FRAME_REDUCTION and y1>FRAME_REDUCTION and y1<CAM_HEIGHT-FRAME_REDUCTION:
                    x3 = np.interp(x1, (FRAME_REDUCTION,CAM_WIDTH-FRAME_REDUCTION), (0, SCREEN_WIDTH))
                    y3 = np.interp(y1, (FRAME_REDUCTION,CAM_HEIGHT-FRAME_REDUCTION), (0, SCREEN_HEIGHT))

                    currLocX = prevLocX + (x3-prevLocX)/SMOOTHENING
                    currLocY = currLocY + (y3-prevLocY)/SMOOTHENING

                    autopy.mouse.move(currLocX, currLocY)
                    cv2.circle(img, (x1,y1), 15, (0,0,255), cv2.FILLED)
                    prevLocX, prevLocY = currLocX, currLocY
            else:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < SENSITIVITY:
                    cv2.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)
                    autopy.mouse.click()

    cv2.rectangle(img, (FRAME_REDUCTION,FRAME_REDUCTION), (CAM_WIDTH-FRAME_REDUCTION,CAM_HEIGHT-FRAME_REDUCTION), (255,0,0), 2)
    if SHOW_FEED:
        cv2.imshow("Virtual Mouse", img)
        cv2.waitKey(1)