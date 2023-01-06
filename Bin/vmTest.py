import cv2
import numpy as np
import HandTrackingModuleFull as htm
import time
import autopy
import pyautogui
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from math import hypot
from pconst import const

import mediapipe as mp

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

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

# media controll
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

start_init = False

prev = -1

drawing = mp.solutions.drawing_utils

while True:

    end_time = time.time()
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)


    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x33, y33 = lmList[16][1:]
        x4, y4 = lmList[20][1:]
        x5, y5 = lmList[4][1:]
        x6, y6 = lmList[15][1:]

        x11, y11 = lmList[4][1], lmList[4][2]
        x22, y22 = lmList[8][1], lmList[8][2]

        cx, cy = (x11 + x22) // 2, (y11 + y22) // 2
        cx2, cy2 = (x33 + x2) // 2, (y33 + y2) // 2
        cx3, cy3 = (x6+x4) // 2, (y6+y4) // 2

        lengthvol = hypot(x22 - x11, y22 - y11)


        fingers = detector.fingersUp()

        a = fingers[1]
        b = fingers[2]
        c = fingers[3]
        d = fingers[4]
        e = fingers[0]
        tot = a + b + c + d + e


        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        if fingers[1] == 1 and fingers[2] == 1:
            #  Convert Coordinates
            x3 = np.interp(x2, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y2, (frameR, hCam - frameR), (0, hScr))
            # Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            #  Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY


        if fingers[1] == 1 and fingers[2] == 1:
            # Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            length1, img, lineInfo1 = detector.findDistance(12, 16, img)
            length2, img, lineInfo2 = detector.findDistance(15, 20, img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           10, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

            if length1 < 35:
                cv2.circle(img, (cx2, cy2),
                           10, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='right')


            if length2 < 35:
                cv2.circle(img, (cx3, cy3),
                           10, (0, 255, 0), cv2.FILLED)
                pyautogui.mouseDown()

        if lengthvol < 30:
            if(y1>270):
                cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
                vol = np.interp(-cx, [-450, -250], [volMin, volMax])

                volume.SetMasterVolumeLevel(vol, None)

        if lengthvol < 30:
            if (y1 < 270):
                cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
                brit = np.interp(-cy, [-200, -180], [20, 100])
                sbc.fade_brightness(brit)

        print(-cx)

        if fingers[0] == 0 and tot == 4:
            pyautogui.scroll(30)

        if fingers[1] == 0 and tot == 4 and lengthvol > 40:
            pyautogui.scroll(-30)


        # media player
        cnt = tot

        if not (prev == cnt):
            if not (start_init):
                start_time = time.time()
                start_init = True

            elif (end_time - start_time) > 0.1:
                if (fingers[0] == 1 and cnt == 1):
                    pyautogui.press("left")

                elif (fingers[1] == 1 and cnt == 2):
                    pyautogui.press("right")

                elif (cnt == 0):
                    pyautogui.press("space")
                prev = cnt
                start_init = False

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)