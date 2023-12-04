# leap-motion-python包需要的Python版本是2.7.x、3.6.x、>=3.7,<3.8.0a0或>=3.8,<3.9.0a0
# conda install -c speleo3 leap-motion-python


import Leap, sys

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):
        frame = controller.frame()

        if not frame.hands.is_empty:
            hand_data = []
            for hand in frame.hands:
                hand_id = hand.id
                palm_y = hand.palm_position.y
                hand_data.append(f"Hand ID: {hand_id}, Palm Y-Position: {palm_y}")

            print(", ".join(hand_data))
        else:
            print("No hands detected")

def main():
    listener = SampleListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press Enter to quit...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
