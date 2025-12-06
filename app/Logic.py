import cv2
import time
import math
import asyncio
import threading
import nest_asyncio
import uvicorn
import mediapipe as mp
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
connected_clients = set()   

model_path = r"C:\Users\Charan singh\Desktop\Hand_detection\model\gesture_recognizer.task"

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

class Gesture_Detector:
    def __init__(self, model_path, mapper):
        self.model_path = model_path
        self.mapper = mapper

    async def run(self):
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.IMAGE,
        )

        with GestureRecognizer.create_from_options(options) as recognizer:
            cap = cv2.VideoCapture(0)

            if cap.isOpened():
                print("Camera_Opened")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # convert for mediapipe
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

                # perform detection
                result = recognizer.recognize(mp_image)

                # handle gesture result
                await self.handle_result(result)

                # show frame
                cv2.imshow("FRAME", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                await asyncio.sleep(0.005)

            cap.release()
            cv2.destroyAllWindows()

    async def handle_result(self, result):
        if not result.hand_landmarks:
            return

        landmarks = result.hand_landmarks[0]

        # index finger position
        x = landmarks[8].x
        y = landmarks[8].y

        # gesture name
        if result.gestures:
            gesture_name = result.gestures[0][0].category_name
        else:
            gesture_name = "Unknown"

        # pinch detection
        thumb = landmarks[4]
        index = landmarks[8]
        dist = math.hypot(thumb.x - index.x, thumb.y - index.y)
        pinch = dist < 0.05

        await self.mapper.mapping(gesture_name, x, y, pinch)


#nest_asyncio.apply()


#threading.Thread(target=start_server, daemon=True).start()

async def main():
    mapper = Gesture_Mapping()
    detector = Gesture_Detector(model_path, mapper)
    await detector.run()

asyncio.run(main())
