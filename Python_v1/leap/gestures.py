import leap
import time
import pyautogui
from pynput.keyboard import Controller

'''
Leap tracking server commands:

sudo systemctl <start/stop/status/restart> libtrack_server
'''

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

class MyListener(leap.Listener):
    def __init__(self):
        self.keyboard = Controller()
        self.display_width = pyautogui.size().width
        self.display_height = pyautogui.size().height

        self.hand = None
        self.hand_type = None
        self.hand_detected = True

        self.moving_mouse = False
        self.starting_x = None
        self.ending_x = None
        self.swipe_direction = None
        self.tracking_range = 200
        self.forward_swipe_threshold = 100
        self.back_swipe_threshold = -100
        self.pinching_threshold = 10

        self.valid_gestures = ["", "grabbing", "pinching"]
        self._pinching = False
        self._grabbing = False

    @property
    def grabbing(self):
        return self._grabbing
    
    @grabbing.setter
    def grabbing(self, update):
        if self._grabbing != update and update == True:
            self.keyboard.press('s')
            self.keyboard.release('s')
            print(f"Gesture: fist | Hand: {self.hand_type} | Position: {self.hand.palm.position.x} | Strength: {self.hand.grab_strength}")
        self._grabbing = update

    @property
    def pinching(self):
        return self._pinching
    
    @pinching.setter
    def pinching(self, update):
        if self._pinching != update and update == True:
            self.moving_mouse = not self.moving_mouse
            pyautogui.click()
            print(f"Gesture: pinch | Hand: {self.hand_type} | Position: {self.hand.palm.position.x}")
        
        self._pinching = update

    def handle_static_gesture(self, gesture=""):
        valid = gesture in self.valid_gestures

        # reset gestures by opening hand at center
        if valid and self.hand.grab_strength == 0:
            self.grabbing = False
            self.pinching = False
        elif valid and self.hand.grab_strength > 0.8 and not self.moving_mouse:
            if gesture == "grabbing":
                return True
            self.grabbing = True
        # left hand pinch requires some adjustments due to inaccuracy
        elif valid and self.hand.grab_strength < 0.5 and ((self.hand_type == "left" and self.hand.pinch_distance - 10 < self.pinching_threshold) or (self.hand_type == "right" and self.hand.pinch_distance < self.pinching_threshold)):
            self.pinching = True

        return False

    def handle_moving_mouse(self):
        x = 0
        y = 0

        # ratio = resolution/tracking range
        # divide resolution by 2 in order to split the +- conversion
        x_ratio = (self.display_width / 2) / self.tracking_range
        y_ratio = (self.display_height / 2) / self.tracking_range

        
        if self.hand.palm.position.x < 0 and self.hand.palm.position.x >= -200:
            hand_x = self.hand.palm.position.x + self.tracking_range
            x = round(hand_x * x_ratio)
        elif self.hand.palm.position.x == 0:
            x = self.display_width / 2
        elif self.hand.palm.position.x > 0 and self.hand.palm.position.x <= 200:
            x = round((self.display_width / 2) + self.hand.palm.position.x * x_ratio)
        
        if self.hand.palm.position.z < 0 and self.hand.palm.position.z >= -200:
            hand_z = self.hand.palm.position.z + self.tracking_range
            y = round(hand_z * y_ratio)
        elif self.hand.palm.position.z == 0:
            y = self.display_height / 2
        elif self.hand.palm.position.z > 0 and self.hand.palm.position.z <= 200:
            y = round((self.display_height / 2) + self.hand.palm.position.z * y_ratio)

        pyautogui.moveTo(x, y)

    def handle_swiping(self):
        # if gesture is starting
        if self.swipe_direction == None:
            # determine direction of gesture from starting position
            if self.hand.palm.position.x > self.forward_swipe_threshold and self.handle_static_gesture("grabbing"):
                self.swipe_direction = "forward"
                self.starting_x = self.hand.palm.position.x
            elif self.hand.palm.position.x < self.back_swipe_threshold and self.handle_static_gesture("grabbing"):
                self.swipe_direction = "back"
                self.starting_x = self.hand.palm.position.x

        else:
            # translate gesture to keypress
            if self.swipe_direction == "forward" and self.hand.palm.position.x < self.back_swipe_threshold and not self.handle_static_gesture("grabbing"):
                self.ending_x = self.hand.palm.position.x
                print(f"Gesture: swipe | Hand: {self.hand_type} | Direction: {self.swipe_direction} | Position: {self.starting_x} to {self.ending_x}")
                self.keyboard.press('d')
                self.keyboard.release('d')
                self.swipe_direction = None
            elif self.swipe_direction == "back" and self.hand.palm.position.x > self.forward_swipe_threshold and not self.handle_static_gesture("grabbing"):
                self.ending_x = self.hand.palm.position.x
                print(f"Gesture: swipe | Hand: {self.hand_type} | Direction: {self.swipe_direction} | Position: {self.starting_x} to {self.ending_x}")
                self.keyboard.press('a')
                self.keyboard.release('a')
                self.swipe_direction = None
            elif not self.handle_static_gesture("grabbing"):
                self.swipe_direction = None

    def on_connection_event(self, event):
        print("Connected")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()

        print(f"Found device {info.serial}")

    def on_tracking_event(self, event):
        # reset if hands are not visible
        if len(event.hands) == 0 and self.hand_detected:
            self.hand_detected = False

            self.starting_x = None
            self.ending_x = None
            self.swipe_direction = None
            print("No hands detected")

        for hand in event.hands:
            self.hand_detected = True
            self.hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
            self.hand = hand

            # check for static gestures
            if self.swipe_direction == None and self.hand.palm.position.x > -60 and self.hand.palm.position.x < 60:
                self.handle_static_gesture()
            
            # check for dynamic gestures
            if self.moving_mouse:
                self.handle_moving_mouse()
            else:
                self.handle_swiping()


def main():
    my_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True

    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        while running:
            time.sleep(1)


if __name__ == "__main__":
    main()
