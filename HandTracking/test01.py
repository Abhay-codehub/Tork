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
# print(wScr, hScr)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]


#media controll
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

start_init = False

prev = -1

drawing = mp.solutions.drawing_utils

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
        x5, y5 = lmList[4][1:]

        x11, y11 = lmList[4][1], lmList[4][2]
        x22, y22 = lmList[8][1], lmList[8][2]
        cx, cy = (x11 + x22) // 2, (y11 + y22) // 2

        cx2, cy2 = (x1+x5) // 2 , (y1+y5) // 2
        # print(x1, y1, x2, y2)
        lengthvol = hypot(x22 - x11, y22 - y11)


    # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        a = fingers[1]
        b = fingers[2]
        c = fingers[3]
        d = fingers[4]
        e = fingers[0]
        tot = a+b+c+d+e
        # print(tot)

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
            # cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
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
            # if length1 < 40:
            #     cv2.circle(img, (cx2, cy2),
            #                10, (0, 255, 255), cv2.FILLED)
            #     pyautogui.click(button='right')
            #     # time.sleep(5)
            if length2 < 36:
                cv2.circle(img, (lineInfo[3], lineInfo[0]),
                           10, (0, 255, 255), cv2.FILLED)
                pyautogui.mouseDown();

            if lengthvol < 30:
                cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
                print("CX CY: ", cx, cy)
                vol = np.interp(cx, [250, 350], [volMin, volMax])
                print(vol)
                volume.SetMasterVolumeLevel(vol, None)

            if lengthvol < 30:
                cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
                # print("CX CY: ", cx, cy)
                brit = np.interp(-cy, [-350, -250], [20, 100])
                # print(vol)
                sbc.fade_brightness(brit)

        if tot == 0 :
            pyautogui.scroll(-20)

        if tot == 1 :
            pyautogui.scroll(20)

#Media Controll

    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))


    def count_fingers(lst):
        cnt = 0

        thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

        if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
            cnt += 1

        if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
            cnt += 1

        return cnt



    if res.multi_hand_landmarks:

        hand_keyPoints = res.multi_hand_landmarks[0]

        cnt = count_fingers(hand_keyPoints)

        if not (prev == cnt):
            if not (start_init):
                start_time = time.time()
                start_init = True

            elif (end_time - start_time) > 0.2:
                if (cnt == 1):
                    pyautogui.press("right")

                elif (cnt == 2):
                    pyautogui.press("left")

                elif (cnt == 3):
                    pyautogui.press("up")

                elif (cnt == 4):
                    pyautogui.press("down")

                elif (cnt == 5):
                    pyautogui.press("space")

                prev = cnt
                start_init = False

        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)




    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)