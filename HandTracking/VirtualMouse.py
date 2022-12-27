import cv2
import numpy as np
import HandTrackingModuleFull as htm
import time
import autopy
import pyautogui


##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x3, y3 = lmList[16][1:]
        x4, y4 = lmList[20][1:]
        # print(x1, y1, x2, y2)

    # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        a = fingers[1]
        b = fingers[2]
        c = fingers[3]
        d = fingers[4]
        e = fingers[0]
        tot = a+b+c+d+e
        print(tot)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] ==  1 and fingers[2] == 1:
            # 5. Convert Coordinates
            x3 = np.interp(x2, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y2, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            length1, img, lineInfo1 = detector.findDistance(4, 8, img)
            length2, img, lineInfo2 = detector.findDistance(15, 20, img)
            # print(length2)

            # print(length)
            # 10. Click mouse if distance short

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           10, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='left', _pause=60)
                # time.sleep(5)
            if length1 < 40:
                cv2.circle(img, (lineInfo[3], lineInfo[0]),
                           10, (0, 255, 255), cv2.FILLED)
                pyautogui.click(button='right')
                # time.sleep(5)
            if length2 < 36:
                cv2.circle(img, (lineInfo[3], lineInfo[0]),
                           10, (0, 255, 255), cv2.FILLED)
                pyautogui.mouseDown();

        if tot == 0 :
            pyautogui.scroll(-10)

        if tot == 1 :
            pyautogui.scroll(10)


    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)