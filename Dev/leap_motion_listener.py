import Leap

class SampleListener(Leap.Listener):
    def __init__(self):
        super(SampleListener, self).__init__()
        self.hand1_ty = 0
        self.hand0_ty = 0

    def on_frame(self, controller):
        frame = controller.frame()
        hands = frame.hands

        self.hand1_ty = 0  # Reset to default
        self.hand0_ty = 0  # Reset to default

        for hand in hands:
            if hand.is_left:
                self.hand1_ty = hand.palm_position.y
            elif hand.is_right:
                self.hand0_ty = hand.palm_position.y

    def get_hand_positions(self):
        return self.hand1_ty, self.hand0_ty
