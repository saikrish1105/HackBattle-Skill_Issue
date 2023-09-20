import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
pyautogui.FAILSAFE=False
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
frame_r = 200
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 1
def fps():
    global pTime
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    cv2.rectangle(frame, (frame_r, frame_r), (frame_w -frame_r, frame_h - frame_r), (255,0,0), 2)
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            #print(x,y)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = np.interp(x,(frame_r, frame_w-frame_r),(0,screen_w))
                screen_y = np.interp(y,(frame_r, frame_h-frame_r),(0,screen_h))
                '''
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y'''
                clocX = plocX + (screen_x - plocX) / smoothening
                clocY = plocY + (screen_y - plocY) / smoothening
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.009:
            pyautogui.click()
            pyautogui.sleep(1)
        right = [landmarks[374], landmarks[386]]
        for landmark in right:
            x2 = int(landmark.x * frame_w)
            y2 = int(landmark.y * frame_h)
            cv2.circle(frame, (x2, y2), 3, (0, 255, 255))
           # print(right[0].y - right[1].y)
        if (right[0].y - right[1].y) < 0.003:

           pyautogui.click(button='right')
           pyautogui.sleep(0.5)
        scroll_up = [landmarks[348], landmarks[443]]
        for landmark in scroll_up:
            x3 = int(landmark.x * frame_w)
            y3 = int(landmark.y * frame_h)
            cv2.circle(frame, (x3, y3), 3, (255, 0, 255))
            #print(scroll_up[0].y - scroll_up[1].y)
        if (scroll_up[0].y - scroll_up[1].y) > 0.08:
           pyautogui.scroll(500)
           pyautogui.sleep(1.0)
    fps()
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
