import Leap, sys

class SampleListener(Leap.Listener):
    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):
        frame = controller.frame()
        hands = frame.hands

        # 默认值
        hand1_ty = 400
        hand0_ty = 400

        if len(hands) > 0:
            for hand in hands:
                if hand.is_left and len(hands) > 1:
                    hand1_ty = hand.palm_position.y
                elif hand.is_right:
                    hand0_ty = hand.palm_position.y
        
        # 输出数据
        print("Hand 1 (Left) Palm Position Y:", hand1_ty)
        print("Hand 0 (Right) Palm Position Y:", hand0_ty)

def main():
    listener = SampleListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
