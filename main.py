
import asyncio
from app.server import start_server
from app.mapping import Gesture_Mapping
from app.detect import Gesture_Detector
from app.config import MODEL_PATH


async def main():
    
    start_server()

    
    mapper = Gesture_Mapping()
    detector = Gesture_Detector(MODEL_PATH, mapper)

    await detector.run()

asyncio.run(main())
