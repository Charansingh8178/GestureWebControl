import threading
import requests


class Gesture_Mapping:
    def __init__(self,server='http://localhost:8000'):
        self.server_url= server

        pass

    async def mapping(self, gesture_name, x, y, pinch):
        print(f"[MAP] {gesture_name}, X={x:.3f}, Y={y:.3f}, PINCH={pinch}")

        # 
        if gesture_name == "Pointing_Up":
            print("SCROLLING_UP")
        elif gesture_name == "Closed_Fist":
            print("STOP_SCROLLING")
        elif pinch:
            print("CLICK")

        #global msg

        msg = f"{gesture_name},{x:.3f},{y:.3f},{pinch}"

       
        threading.Thread(
            target=self.send_msg,
            args=(msg,),
            daemon=True
        ).start()

    def send_msg(self, message):   
        requests.post("http://localhost:8000/broadcast", data={"msg": message})
