import cv2
import numpy as np
import time
import HandTrackingModule as htm
import subprocess
import math
import threading
import speech_recognition as sr

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

# ---------------- Volume control -------------------
def set_volume_mac(volume_percent):
    volume_percent = max(min(volume_percent, 100), 0)
    script = f"set volume output volume {int(volume_percent)}"
    subprocess.call(["osascript", "-e", script])

# ---------------- Voice Command Thread -------------------
def voice_control_thread():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎤 Voice control is active...")

    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for voice commands...")
                audio = recognizer.listen(source, timeout=4)

            command = recognizer.recognize_google(audio).lower()
            print("Recognized:", command)

            if "volume up" in command:
                subprocess.call(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) + 10)"])
            elif "volume down" in command:
                subprocess.call(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) - 10)"])
            elif "mute" in command:
                subprocess.call(["osascript", "-e", "set volume output muted true"])
            elif "unmute" in command:
                subprocess.call(["osascript", "-e", "set volume output muted false"])
            elif "stop video" in command:  # <-- Changed from "pause video"
                subprocess.call(["osascript", "-e", 'tell application "System Events" to key code 49'])  # Spacebar
            elif "play video" in command:
                subprocess.call(["osascript", "-e", 'tell application "System Events" to key code 49'])  # Spacebar

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.WaitTimeoutError:
            print("Voice Error: Listening timed out while waiting for phrase to start")
        except sr.RequestError as e:
            print(f"Voice Error: {e}")

# ---------------- Start voice thread -------------------
threading.Thread(target=voice_control_thread, daemon=True).start()

# ---------------- Main loop -------------------
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
