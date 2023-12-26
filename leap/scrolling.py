import leap
import time


class MyListener(leap.Listener):
    def __init__(self):
        self.starting_x = None
        self.ending_x = None
        self.swipe_direction = None
        self.ack = True

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
        # print(f"Frame {event.tracking_frame_id} with {len(event.hands)} hands.")
        if len(event.hands) == 0 and self.ack:
            self.starting_x = None
            self.ending_x = None
            print("No hands detected")
            self.ack = False

        for hand in event.hands:
            self.ack = True
            hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
            
            if not self.starting_x:
                self.starting_x = hand.palm.position.x
                print(f"Starting x position: {self.starting_x}")

                if hand.palm.position.x > 100 and hand.palm.position.x < 200:
                    self.swipe_direction = "back"  
                elif hand.palm.position.x > -200 and hand.palm.position.x < -100:
                    self.swipe_direction = "forward"
            else:
                if self.swipe_direction == "back" and hand.palm.position.x < -100:
                    self.ending_x = hand.palm.position.x
                    print(f"Swiped {hand_type} hand {self.swipe_direction} from {self.starting_x} to {self.ending_x}")
                elif self.swipe_direction == "forward" and hand.palm.position.x > 100:
                    self.ending_x = hand.palm.position.x
                    print(f"Swiped {hand_type} hand {self.swipe_direction} from {self.starting_x} to {self.ending_x}")


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
