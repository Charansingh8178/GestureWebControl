# Hand Gesture Webpage Controller with MediaPipe + FastAPI + WebSocket

This project is detects gestures from hand and using those gestutres will be able to control WebPage. Using pre-defined gestures it will be able to control the webpage.

## List of Gestures
- Pointing_up :- Scroll Upwards
- Closed_fist :- Stop Scrolling
- pinch :- Click/ Select

## Features
- Real-Time gesture detection ( Open-palm, closed fist, Pinch, Pointing_Up)

- WebSocket broadcast to browser UI
- Modular Architecture 

## Tech Stack
- Python 3.10+
- FastAPI
- MediaPipe
- WebSocket
- HTML

## How to Run
1. Install Dependencies 
' pip install -r requirements.txt'

2. Download model from 
" https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/index#models "

3. Specify Paths in config.py

4. Run Main.py

5. Open browser: "http://localhost:8000/" or site1.html provided.

6. It would open camera footage as well as browser and performing specific gestures will be seen the gesture performed in browser
