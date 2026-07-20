"""
AudioPulse Spectrum
Audio Processing Engine
"""

import numpy as np
import sounddevice as sd
from collections import deque

from config import *

class AudioEngine:

    def __init__(self):

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            blocksize=BLOCK_SIZE,
            dtype='float32'
        )

        self.stream.start()

        self.previous_levels = np.zeros(NUM_BANDS)

        self.energy_history = deque(maxlen=BEAT_HISTORY)

    def process_audio(self):

        audio, overflow = self.stream.read(BLOCK_SIZE)

        if overflow:
            return np.zeros(NUM_BANDS), 0, False

        audio = audio[:, 0]

        # Remove DC Offset
        audio -= np.mean(audio)

        # Apply Hanning Window
        audio *= np.hanning(len(audio))

        # FFT
        fft = np.fft.rfft(audio)

        magnitude = np.abs(fft)

        frequencies = np.fft.rfftfreq(
            len(audio),
            1 / SAMPLE_RATE
        )

        levels = []

        for low, high in FREQUENCY_BANDS:

            idx = np.where(
                (frequencies >= low) &
                (frequencies < high)
            )[0]

            if len(idx) == 0:
                levels.append(0)
            else:
                levels.append(np.mean(magnitude[idx]))

        levels = np.array(levels)

        # -----------------------------
        # Automatic Gain Control
        # -----------------------------

        max_level = np.max(levels)

        if max_level > 0:
            levels /= max_level

        # -----------------------------
        # Noise Gate
        # -----------------------------

        levels[levels < NOISE_THRESHOLD] = 0

        # -----------------------------
        # Exponential Smoothing
        # -----------------------------

        levels = (
            SMOOTHING_FACTOR * self.previous_levels +
            (1 - SMOOTHING_FACTOR) * levels
        )

        self.previous_levels = levels

        # -----------------------------
        # Volume Calculation
        # -----------------------------

        volume = int(np.mean(levels) * 100)

        if volume > 100:
            volume = 100

        if volume < 0:
            volume = 0

        # -----------------------------
        # Beat Detection
        # -----------------------------

        energy = np.mean(levels)

        self.energy_history.append(energy)

        beat = False

        if len(self.energy_history) >= 10:

            average = np.mean(self.energy_history)

            if average > 0:

                if energy > average * BEAT_THRESHOLD:

                    beat = True

        return levels, volume, beat

    def close(self):

        self.stream.stop()

        self.stream.close()