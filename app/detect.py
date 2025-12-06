import cv2
import math
import asyncio

import mediapipe as mp
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import requests
from app.config import MODEL_PATH

app = FastAPI()
connected_clients = set()   


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

class Gesture_Detector:
    def __init__(self, model_path, mapper):
        self.model_path = MODEL_PATH
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

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

                result = recognizer.recognize(mp_image)

                await self.handle_result(result)

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

        # index finger 
        x = landmarks[8].x
        y = landmarks[8].y

   
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

