import leap
import time
from pynput.keyboard import Controller


class MyListener(leap.Listener):
    def __init__(self):
        self.starting_x = None
        self.ending_x = None
        self.swipe_direction = None
        self.hand_ack = True
        self.gesture_ack = False
        self.keyboard = Controller()

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
            self.starting_x = None
            self.ending_x = None
            self.hand_ack = False
            self.gesture_ack = False
            print("No hands detected")

        for hand in event.hands:
            self.hand_ack = True
            hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
            
            # if gesture is starting
            if not self.starting_x:
                self.starting_x = hand.palm.position.x
                print(f"Starting x position: {self.starting_x}")

                # determine direction of gesture from starting position
                if hand.palm.position.x > 100 and hand.palm.position.x < 200:
                    self.swipe_direction = "forward"  
                elif hand.palm.position.x > -200 and hand.palm.position.x < -100:
                    self.swipe_direction = "back"

            # if gesture is ending
            else:
                # translate gesture to keypress
                if self.swipe_direction == "forward" and hand.palm.position.x < -100 and not self.gesture_ack:
                    self.ending_x = hand.palm.position.x
                    print(f"Swiped {hand_type} hand {self.swipe_direction} from {self.starting_x} to {self.ending_x}")
                    self.keyboard.press('a')
                    self.keyboard.release('a')
                    self.gesture_ack = True
                elif self.swipe_direction == "back" and hand.palm.position.x > 100 and not self.gesture_ack:
                    self.ending_x = hand.palm.position.x
                    print(f"Swiped {hand_type} hand {self.swipe_direction} from {self.starting_x} to {self.ending_x}")
                    self.keyboard.press('d')
                    self.keyboard.release('d')
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
