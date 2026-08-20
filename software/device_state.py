class DeviceStateManager:
    """
    Tracks current state of each device and prevents sending a redundant
    command if the requested action matches the device's current state.
    """

    def __init__(self):
        self.state = {
            "fan": "OFF",
            "led": "OFF",       # OFF, RED, GREEN, BLUE
            "door": "LOCKED",
        }

    def handle_action(self, action):
        """
        Takes an action string (e.g. "FAN_ON", "LED_RED", "LOCK_DOOR")
        Returns a tuple: (should_send: bool, message: str)
        """
        if action == "FAN_ON":
            if self.state["fan"] == "ON":
                return False, "Fan is already ON"
            self.state["fan"] = "ON"
            return True, "Turning fan ON"

        if action == "FAN_OFF":
            if self.state["fan"] == "OFF":
                return False, "Fan is already OFF"
            self.state["fan"] = "OFF"
            return True, "Turning fan OFF"

        if action in ("LED_RED", "LED_GREEN", "LED_BLUE", "LED_OFF"):
            color = action.replace("LED_", "")
            if self.state["led"] == color:
                return False, f"LED is already {color}"
            self.state["led"] = color
            return True, f"Setting LED to {color}"

        if action == "LOCK_DOOR":
            if self.state["door"] == "LOCKED":
                return False, "Door is already LOCKED"
            self.state["door"] = "LOCKED"
            return True, "Locking door"

        if action == "UNLOCK_DOOR":
            if self.state["door"] == "UNLOCKED":
                return False, "Door is already UNLOCKED"
            self.state["door"] = "UNLOCKED"
            return True, "Unlocking door"

        return False, f"Unknown action: {action}"