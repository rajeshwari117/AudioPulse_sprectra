"""
AudioPulse Spectrum
Serial Communication Manager

"""

import serial
import time

from config import SERIAL_PORT, BAUD_RATE


class SerialManager:

    def __init__(self):

        self.serial = None
        self.connect()

    def connect(self):

        try:

            self.serial = serial.Serial(
                SERIAL_PORT,
                BAUD_RATE,
                timeout=1
            )

            # Give Arduino time to reset
            time.sleep(2)

            print(f"[INFO] Connected to {SERIAL_PORT}")

        except Exception as e:

            print("[ERROR] Unable to connect to Arduino")
            print(e)

            self.serial = None

    def send(self, levels, volume, beat):

        if self.serial is None:
            return

        # Convert spectrum values (0.0-1.0) → PWM (0-255)
        brightness = []

        for level in levels:

            value = int(level * 255)

            if value < 0:
                value = 0

            if value > 255:
                value = 255

            brightness.append(value)

        beat_flag = 1 if beat else 0

        # Packet Format:
        #
        # L:10,55,180,255,120,30;V:64;B:1
        #

        packet = (
            f"L:{brightness[0]},"
            f"{brightness[1]},"
            f"{brightness[2]},"
            f"{brightness[3]},"
            f"{brightness[4]},"
            f"{brightness[5]};"
            f"V:{volume};"
            f"B:{beat_flag}\n"
        )

        try:

            self.serial.write(packet.encode())

        except serial.SerialException:

            print("[ERROR] Serial communication failed.")

            try:
                self.serial.close()
            except:
                pass

            self.serial = None

    def reconnect(self):

        if self.serial is None:

            self.connect()

    def close(self):

        if self.serial is not None:

            self.serial.close()

            print("[INFO] Serial Port Closed")