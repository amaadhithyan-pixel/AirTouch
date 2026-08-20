import time


class StabilityFilter:
    """
    Only confirms a gesture once it has been seen consistently
    for `hold_seconds`, and avoids re-triggering the same action
    repeatedly while the gesture is still held.
    """

    def __init__(self, hold_seconds=1.0):
        self.hold_seconds = hold_seconds
        self.current_gesture = None
        self.start_time = None
        self.last_confirmed = None

    def update(self, gesture_name):
        """
        Call every frame with the raw detected gesture (or "UNKNOWN"/None).
        Returns the gesture name if it just became confirmed this frame,
        otherwise returns None.
        """
        if gesture_name is None or gesture_name == "UNKNOWN":
            self.current_gesture = None
            self.start_time = None
            return None

        if gesture_name != self.current_gesture:
            self.current_gesture = gesture_name
            self.start_time = time.time()
            return None

        held_duration = time.time() - self.start_time

        if held_duration >= self.hold_seconds and self.last_confirmed != gesture_name:
            self.last_confirmed = gesture_name
            return gesture_name

        return None

    def progress(self):
        """Returns 0.0-1.0 fraction of how long the current gesture has been held."""
        if self.current_gesture is None or self.start_time is None:
            return 0.0
        elapsed = time.time() - self.start_time
        return min(elapsed / self.hold_seconds, 1.0)

    def reset(self):
        self.current_gesture = None
        self.start_time = None
        self.last_confirmed = None