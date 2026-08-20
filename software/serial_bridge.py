import serial
import time


class SerialBridge:
    """
    Handles the serial connection to the ESP32 and sends action commands.
    """

    def __init__(self, port, baud_rate=9600, timeout=1):
        self.connection = None
        try:
            self.connection = serial.Serial(port, baud_rate, timeout=timeout)
            time.sleep(2)  # ESP32 resets on serial connect; wait for it to boot
            print(f"Connected to ESP32 on {port}")
        except serial.SerialException as e:
            print(f"Could not open serial port {port}: {e}")

    def send_command(self, action):
        """Sends an action string (e.g. 'FAN_ON') to the ESP32, newline-terminated."""
        if self.connection is None or not self.connection.is_open:
            print("Serial connection not available - command not sent.")
            return

        try:
            self.connection.write((action + "\n").encode("utf-8"))
        except serial.SerialException as e:
            print(f"Serial write failed: {e}")

    def read_response(self):
        """Reads any available response line from the ESP32 (non-blocking-ish)."""
        if self.connection is None or not self.connection.is_open:
            return None
        if self.connection.in_waiting > 0:
            try:
                return self.connection.readline().decode("utf-8").strip()
            except serial.SerialException:
                return None
        return None

    @property
    def is_connected(self):
        return self.connection is not None and self.connection.is_open

    def close(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close()