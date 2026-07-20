"""
AudioPulse Spectrum
Main Application

"""

import sys
import time

from audio_engine import AudioEngine
from serial_manager import SerialManager
from config import FPS


def print_header():
    print("=" * 60)
    print("            AudioPulse Spectrum")
    print("     Real-Time Audio Spectrum Analyzer")
    print("=" * 60)
    print()


def display_terminal(levels, volume, beat):

    lines = []

    names = [
        "Bass",
        "Low Mid",
        "Mid",
        "High Mid",
        "Presence",
        "Treble"
    ]

    for name, level in zip(names, levels):

        length = int(level * 20)

        bar = "█" * length

        lines.append(
            f"{name:<10}: {bar:<20} {int(level*100):3d}%"
        )

    output = (
        "\033[H\033[J" +
        "\n".join(lines) +
        "\n\n" +
        f"Volume : {volume:3d}%\n" +
        f"Beat   : {'YES' if beat else 'NO'}\n"
    )

    sys.stdout.write(output)
    sys.stdout.flush()


def main():

    print_header()

    audio = None
    serial = None

    frame_time = 1.0 / FPS

    try:

        audio = AudioEngine()
        serial = SerialManager()

        print("[INFO] Audio Engine Started")
        print("[INFO] Serial Connected")
        print("[INFO] Listening...\n")

        time.sleep(1)

        while True:

            start = time.perf_counter()

            levels, volume, beat = audio.process_audio()

            serial.reconnect()
            serial.send(levels, volume, beat)

            display_terminal(levels, volume, beat)

            elapsed = time.perf_counter() - start

            delay = frame_time - elapsed

            if delay > 0:
                time.sleep(delay)

    except KeyboardInterrupt:

        print("\n\nStopping AudioPulse Spectrum...")

    except Exception as e:

        print(f"\n[ERROR] {e}")

    finally:

        if audio is not None:
            audio.close()

        if serial is not None:
            serial.close()

        print("Resources Released.")


if __name__ == "__main__":
    main()