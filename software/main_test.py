import cv2
import config
from gesture_detector import GestureDetector
from gesture_classifier import classify_fingers, get_action
from stability_filter import StabilityFilter
from device_state import DeviceStateManager
from ui_overlay import OverlayUI
from serial_bridge import SerialBridge


def main():
    bridge = SerialBridge(config.SERIAL_PORT, config.SERIAL_BAUD_RATE)

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: requested {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}, "
          f"got {actual_w}x{actual_h}")

    cv2.namedWindow(config.WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    if config.FULLSCREEN:
        cv2.setWindowProperty(config.WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    detector = GestureDetector(
        max_hands=config.MAX_HANDS,
        detection_conf=config.DETECTION_CONFIDENCE,
        tracking_conf=config.TRACKING_CONFIDENCE,
    )
    stability = StabilityFilter(hold_seconds=config.GESTURE_HOLD_SECONDS)
    device_state = DeviceStateManager()
    overlay = OverlayUI()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        landmarks, handedness = detector.process(frame)

        gesture_name = "UNKNOWN"
        if landmarks is not None:
            fingers = detector.get_finger_states(landmarks, handedness)
            gesture_name = classify_fingers(fingers)

        confirmed = stability.update(gesture_name)

        if confirmed:
            overlay.notify_confirmed()
            action = get_action(confirmed)
            if action:
                should_send, message = device_state.handle_action(action)
                print(message)
                if should_send:
                    bridge.send_command(action)

        overlay.draw(frame, gesture_name, device_state, stability.progress(), bridge.is_connected)
        cv2.imshow(config.WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    bridge.close()


if __name__ == "__main__":
    main()