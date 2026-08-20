import cv2
import time

PANEL_COLOR = (35, 35, 38)
SHADOW_COLOR = (0, 0, 0)
TEXT_COLOR = (235, 235, 235)
LABEL_COLOR = (170, 170, 170)
ACCENT_COLOR = (60, 220, 130)
FLASH_COLOR = (215, 215, 210)
BAR_BG = (70, 70, 70)

ON_COLOR = (60, 220, 130)     # green - BGR
OFF_COLOR = (70, 70, 220)     # red - BGR
CONNECTED_COLOR = (60, 220, 130)
DISCONNECTED_COLOR = (70, 70, 220)

LED_COLORS = {
    "RED": (60, 60, 230),
    "GREEN": (60, 200, 60),
    "BLUE": (220, 120, 60),
    "OFF": (140, 140, 140),
}

GESTURE_LABELS = {
    "OPEN_PALM": "Palm Open",
    "FIST": "Fist Closed",
    "ONE_FINGER": "One Finger",
    "TWO_FINGERS": "Two Fingers",
    "THREE_FINGERS": "Three Fingers",
    "FOUR_FINGERS": "Four Fingers",
    "LOCK_SIGN": "Lock Sign",
    "SHAKA": "Unlock Sign",
    "UNKNOWN": "...",
}

FLASH_DURATION = 0.35


def _draw_rounded_rect(img, top_left, bottom_right, color, radius):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, -1)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, -1)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, -1)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, -1)


class OverlayUI:
    """
    Draws the AirTouch status panel: gesture, device states with
    color-coded dots, hold-progress bar, and ESP32 connection status.
    Also tracks a brief flash effect when a gesture is confirmed.
    """

    def __init__(self):
        self.flash_until = 0.0

    def notify_confirmed(self):
        """Call this once when a gesture is newly confirmed, to trigger the flash."""
        self.flash_until = time.time() + FLASH_DURATION

    def draw(self, frame, gesture_name, device_state, hold_progress, connected):
        h, w, _ = frame.shape
        panel_w, panel_h = 340, 215
        x, y = 15, 15
        radius = 14

        # Drop shadow
        shadow = frame.copy()
        _draw_rounded_rect(shadow, (x + 6, y + 6), (x + panel_w + 6, y + panel_h + 6),
                            SHADOW_COLOR, radius)
        frame[:] = cv2.addWeighted(shadow, 0.25, frame, 0.75, 0)

        # Main panel
        overlay = frame.copy()
        is_flashing = time.time() < self.flash_until
        panel_color = FLASH_COLOR if is_flashing else PANEL_COLOR
        panel_alpha = 0.75 if is_flashing else 0.55
        _draw_rounded_rect(overlay, (x, y), (x + panel_w, y + panel_h), panel_color, radius)
        frame[:] = cv2.addWeighted(overlay, panel_alpha, frame, 1 - panel_alpha, 0)

        # Connection status dot (top-right of panel)
        conn_color = CONNECTED_COLOR if connected else DISCONNECTED_COLOR
        conn_center = (x + panel_w - 20, y + 20)
        cv2.circle(frame, conn_center, 6, conn_color, -1)
        cv2.putText(frame, "ESP32", (conn_center[0] - 60, conn_center[1] + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, LABEL_COLOR, 1)

        # Gesture name (big, bold)
        friendly = GESTURE_LABELS.get(gesture_name, gesture_name)
        text_color = (20, 20, 20) if is_flashing else ACCENT_COLOR
        cv2.putText(frame, friendly, (x + 15, y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)

        # Device state rows with color dots
        rows = [
            ("Fan", device_state.state['fan'], ON_COLOR if device_state.state['fan'] == "ON" else OFF_COLOR),
            ("LED", device_state.state['led'], LED_COLORS.get(device_state.state['led'], OFF_COLOR)),
            ("Door", device_state.state['door'], ON_COLOR if device_state.state['door'] == "UNLOCKED" else OFF_COLOR),
        ]

        row_y = y + 75
        for label, value, dot_color in rows:
            cv2.circle(frame, (x + 22, row_y - 5), 6, dot_color, -1)
            cv2.putText(frame, f"{label}:", (x + 40, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, LABEL_COLOR, 1)
            cv2.putText(frame, value, (x + 115, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 1)
            row_y += 32

        # Hold-progress bar
        bar_x, bar_y = x + 15, y + panel_h - 25
        bar_w, bar_h = panel_w - 30, 12
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), BAR_BG, -1)
        fill_w = int(bar_w * hold_progress)
        if fill_w > 0:
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), ACCENT_COLOR, -1)