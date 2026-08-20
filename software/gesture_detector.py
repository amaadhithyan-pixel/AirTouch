import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

TIP_IDS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky


class GestureDetector:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.7):
        self.hands = mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )

    def process(self, frame):
        """Takes a BGR frame, returns (landmarks, handedness) or (None, None)."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if not result.multi_hand_landmarks:
            return None, None

        landmarks = result.multi_hand_landmarks[0].landmark
        handedness = result.multi_handedness[0].classification[0].label  # "Left" or "Right"

        mp_draw.draw_landmarks(
            frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS
        )

        return landmarks, handedness

    def get_finger_states(self, landmarks, handedness):
        """Returns list of 5 ints (0/1): [thumb, index, middle, ring, pinky]."""
        fingers = []

        if handedness == "Right":
            fingers.append(1 if landmarks[TIP_IDS[0]].x < landmarks[TIP_IDS[0] - 1].x else 0)
        else:
            fingers.append(1 if landmarks[TIP_IDS[0]].x > landmarks[TIP_IDS[0] - 1].x else 0)

        for i in range(1, 5):
            fingers.append(1 if landmarks[TIP_IDS[i]].y < landmarks[TIP_IDS[i] - 2].y else 0)

        return fingers