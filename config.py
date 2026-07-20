"""
AudioPulse Spectrum
Configuration File
"""


SERIAL_PORT = "/dev/cu.usbserial-A5069RR4"
BAUD_RATE = 9600

# ===========================
# Audio Configuration
# ===========================

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
CHANNELS = 1

# ===========================
# Spectrum Configuration
# ===========================

NUM_BANDS = 6

# Frequency Bands (Hz)
FREQUENCY_BANDS = [
    (20, 120),        # Bass
    (120, 300),       # Low Mid
    (300, 800),       # Mid
    (800, 2500),      # Upper Mid
    (2500, 6000),     # Presence
    (6000, 12000)     # Treble
]

# ===========================
# Processing Parameters
# ===========================

SMOOTHING_FACTOR = 0.85
NOISE_THRESHOLD = 0.05
BEAT_HISTORY = 20
BEAT_THRESHOLD = 1.35

# ===========================
# Visualization
# ===========================

MAX_BRIGHTNESS = 255
FPS = 30