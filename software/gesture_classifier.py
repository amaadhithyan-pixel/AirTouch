GESTURE_MAP = {
    (1, 1, 1, 1, 1): "OPEN_PALM",       # Fan ON
    (0, 0, 0, 0, 0): "FIST",            # Fan OFF
    (0, 1, 0, 0, 0): "ONE_FINGER",      # Red LED
    (0, 1, 1, 0, 0): "TWO_FINGERS",     # Green LED
    (0, 1, 1, 1, 0): "THREE_FINGERS",   # Blue LED
    (0, 1, 1, 1, 1): "FOUR_FINGERS",    # LED OFF
    (1, 1, 0, 0, 1): "LOCK_SIGN",       # Lock Door (thumb + index + pinky)
    (1, 0, 0, 0, 1): "SHAKA",           # Unlock Door (thumb + pinky)
}

ACTION_MAP = {
    "OPEN_PALM": "FAN_ON",
    "FIST": "FAN_OFF",
    "ONE_FINGER": "LED_RED",
    "TWO_FINGERS": "LED_GREEN",
    "THREE_FINGERS": "LED_BLUE",
    "FOUR_FINGERS": "LED_OFF",
    "LOCK_SIGN": "LOCK_DOOR",
    "SHAKA": "UNLOCK_DOOR",
    "UNKNOWN": None,
}


def classify_fingers(fingers):
    """Takes [thumb, index, middle, ring, pinky] -> gesture name string."""
    return GESTURE_MAP.get(tuple(fingers), "UNKNOWN")


def get_action(gesture_name):
    return ACTION_MAP.get(gesture_name, None)