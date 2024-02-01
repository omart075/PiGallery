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
        self.starting_x = None
        self.ending_x = None
        self.swipe_direction = None
        self.keyboard = Controller()
        self.display_width = pyautogui.size().width
        self.display_height = pyautogui.size().height
        self.hand = None
        self.hand_type = None

        # flags are for logging only
        self.hand_ack = True
        self.gesture_ack = False
        self.particle_mode = False

        self._pinching = False
        self._grabbing = False

    @property
    def grabbing(self):
        return self._grabbing
    
    @grabbing.setter
    def grabbing(self, update):
        if self._grabbing != update and update == True:
            self._grabbing = update
            # self.keyboard.press('s')
            # self.keyboard.release('s')
            print(f"Gesture: fist | Hand: {self.hand_type} | Position: {self.hand.palm.position.x} | Strength: {self.hand.grab_strength}")
        else:
            self._grabbing = update

    @property
    def pinching(self):
        return self._pinching
    
    @pinching.setter
    def pinching(self, update):
        if self._pinching != update and update == True:
            self._pinching = update
            self.particle_mode = not self.particle_mode
            # pyautogui.click()
            print(f"Gesture: pinch | Hand: {self.hand_type} | Position: {self.hand.palm.position.x}")
        else:
            self._pinching = update

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
        if len(event.hands) == 0 and self.hand_ack:
            self.hand_ack = False

            self.starting_x = None
            self.ending_x = None
            self.gesture_ack = False
            self.swipe_direction = None
            print("No hands detected")

        for hand in event.hands:
            self.hand_ack = True
            self.hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
            self.hand = hand

            # check for static gestures
            if hand.palm.position.x > -60 and hand.palm.position.x < 60 and not self.swipe_direction:
                if hand.grab_strength == 0:
                    self.grabbing = False
                    self.pinching = False
                elif hand.grab_strength > 0.8 and not self.particle_mode:
                    self.grabbing = True

                # left hand pinch requires some adjustments due to inaccuracy
                elif (self.hand_type == "left" and hand.pinch_distance - 10 < 10) or (self.hand_type == "right" and hand.pinch_distance < 10):
                    self.pinching = True
            
            if self.particle_mode:
                x = 0
                y = 0
                tracking_range = 200

                # ratio = res/tracking range
                # divide res by 2 in order to split the +- conversion
                x_ratio = (self.display_width / 2) / tracking_range
                y_ratio = (self.display_height / 2) / tracking_range

                
                if hand.palm.position.x < 0 and hand.palm.position.x >= -200:
                    hand_x = hand.palm.position.x + tracking_range
                    x = round(hand_x * x_ratio)
                elif hand.palm.position.x == 0:
                    x = self.display_width / 2
                elif hand.palm.position.x > 0 and hand.palm.position.x <= 200:
                    x = round((self.display_width / 2) + hand.palm.position.x * x_ratio)
                
                if hand.palm.position.z < 0 and hand.palm.position.z >= -200:
                    hand_z = hand.palm.position.z + tracking_range
                    y = round(hand_z * y_ratio)
                elif hand.palm.position.z == 0:
                    y = self.display_height / 2
                elif hand.palm.position.z > 0 and hand.palm.position.z <= 200:
                    y = round((self.display_height / 2) + hand.palm.position.z * y_ratio)

                pyautogui.moveTo(x, y)

            else:
                # if gesture is starting
                if not self.swipe_direction:
                    # determine direction of gesture from starting position
                    if hand.palm.position.x > 100:
                        self.swipe_direction = "forward"
                        self.starting_x = hand.palm.position.x

                    elif hand.palm.position.x < -100:
                        self.swipe_direction = "back"
                        self.starting_x = hand.palm.position.x

                # if gesture is ending
                else:
                    # translate gesture to keypress
                    if self.swipe_direction == "forward" and hand.palm.position.x < 0 and not self.gesture_ack:
                        self.ending_x = hand.palm.position.x
                        print(f"Gesture: swipe | Hand: {self.hand_type} | Direction: {self.swipe_direction} | Position: {self.starting_x} to {self.ending_x}")
                        self.keyboard.press('d')
                        self.keyboard.release('d')
                        self.gesture_ack = True
                    elif self.swipe_direction == "back" and hand.palm.position.x > 0 and not self.gesture_ack:
                        self.ending_x = hand.palm.position.x
                        print(f"Gesture: swipe | Hand: {self.hand_type} | Direction: {self.swipe_direction} | Position: {self.starting_x} to {self.ending_x}")
                        self.keyboard.press('a')
                        self.keyboard.release('a')
                        self.gesture_ack = True


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
