import cv2
import numpy as np
import time
import HandTrackingModule as htm
import subprocess
import math

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0

pTime = 0

def set_volume_mac(volume_percent):
    volume_percent = max(min(volume_percent, 100), 0)
    script = f"set volume output volume {int(volume_percent)}"
    subprocess.call(["osascript", "-e", script])

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 2)
        cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)


        vol = np.interp(length, [30, 200], [minVol, maxVol])
        volBar = np.interp(length, [30, 200], [400, 150])
        volPer = np.interp(length, [30, 200], [0, 100])

        set_volume_mac(volPer)

        if length < 30:
            cv2.circle(img, (cx, cy), 10, (0,0,255), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0,255,0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (500, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) == ord('q'):
        break
