import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

import cv2
import numpy as np
import time
pyautogui.FAILSAFE=False
def handTrack():
    import cv2
    import mediapipe as mp
    import time
    import pyautogui
    import math
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    cTime = 0
    pTime = 0
    frameR=0
    wScr, hScr = pyautogui.size()
    lmList=[]
    xlist=[]
    ylist=[]
    bbox=[]
    tipIds = [4, 8, 12, 16, 20]
    while True:
        success, img=cap.read()
        img = cv2.flip(img, 1)
        wCam,hCam = 500,300
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id,lm in enumerate(handLms.landmark):
                    plocX, plocY = 0, 0
                    clocX, clocY = 0, 0
                    smoothening=1
                    #print(id,lm)
                    h,w,c=img.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    xlist.append(cx)
                    ylist.append(cy)
                    lmList.append([id,cx,cy])
                bbox=min(xlist),min(ylist),max(xlist),max(ylist)
                if len(lmList) != 0:
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]

                fingers=[]
                for id in range(1,5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                cv2.rectangle(img, (frameR, frameR), (wCam, hCam),(255, 0, 255), 2)
                if fingers[0]==1 and fingers[1]==0:
                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening
                        pyautogui.moveTo(clocX, clocY)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY
                if fingers[0]==1 and fingers[1]==1:
                    x1,y1=lmList[8][1:]
                    x2,y2=lmList[12][1:]
                    cx,cy=(x1+x2)//2,(y1+y2)//2
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x2 - x1, y2 - y1)
                    lineInfo=[x1,y1,x2,y2,cx,cy]
                    if length<40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
                        pyautogui.sleep(1)

                if fingers[0]==1 and fingers[2]==1:
                    x1,y1=lmList[8][1:]
                    x2,y2=lmList[16][1:]
                    cx,cy=(x1+x2)//2,(y1+y2)//2
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x2 - x1, y2 - y1)
                    lineInfo=[x1,y1,x2,y2,cx,cy]
                    if length<70:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click(button='right')
                        pyautogui.sleep(1.5)

                scroll_up = [lmList[5], lmList[8]]
                for landmark in scroll_up:
                    x3 = int(landmark[1] *w)
                    y3 = int(landmark[2] *h)
                    cv2.circle(img, (x3, y3), 3, (255, 0, 255))
                if (scroll_up[0][2] - scroll_up[1][2]) < 0.03:
                    pyautogui.scroll(500)
                    pyautogui.sleep(1.0)

                fingers=[]
                lmList=[]
                xlist=[]
                ylist=[]
                plocX, plocY = 0, 0
                clocX, clocY = 0, 0
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(255,0,255),2)

        cv2.imshow("img",img)
        cv2.waitKey(1)
handTrack()
    
