# AudioPulse Spectrum
## Real-Time Audio Spectrum Analyzer with Music Reactive LED Visualization

## Overview

AudioPulse Spectrum is a real-time audio visualization system that analyzes audio signals and converts them into dynamic LED spectrum patterns.

The system captures live audio input, processes the signal using Digital Signal Processing (DSP) techniques, performs Fast Fourier Transform (FFT) analysis to extract frequency components, and communicates the processed data to a microcontroller for LED and OLED visualization.

This project combines Python-based audio processing with embedded hardware to create an interactive music-reactive lighting system.

---

## Features

- Real-time audio signal processing
- FFT-based frequency spectrum analysis
- Six-band frequency visualization
- Beat detection for music synchronization
- Automatic gain control for different audio levels
- Noise filtering and signal smoothing
- Serial communication between Python and microcontroller
- PWM-based LED brightness control
- Real-time OLED spectrum display

---

## Working Principle

```
Audio Input
     |
     ↓
Python Audio Processing
     |
     ↓
Signal Filtering & FFT Analysis
     |
     ↓
Frequency Band Extraction
     |
     ↓
Beat Detection
     |
     ↓
Serial Communication
     |
     ↓
Microcontroller
     |
     ↓
LED Spectrum + OLED Display
```

---

## Audio Spectrum Analysis

The audio signal is divided into six frequency bands:

| Frequency Band | Range |
|---|---|
| Bass | 20Hz - 120Hz |
| Low Mid | 120Hz - 300Hz |
| Mid | 300Hz - 800Hz |
| Upper Mid | 800Hz - 2500Hz |
| Presence | 2500Hz - 6000Hz |
| Treble | 6000Hz - 12000Hz |

Each frequency band controls the brightness of a corresponding LED.

---

## Signal Processing

The project implements:

- **DC Offset Removal** to remove unwanted signal bias
- **Hanning Window** to improve FFT accuracy
- **Fast Fourier Transform (FFT)** for frequency analysis
- **Automatic Gain Control** for signal normalization
- **Noise Gate** to reduce background noise
- **Exponential Smoothing** for stable LED transitions
- **Beat Detection** using audio energy comparison

---

## Hardware Implementation

### Components Used

- Arduino / ESP32 Microcontroller
- PWM Controlled LEDs
- 128x64 OLED Display
- Audio Input Device
- Breadboard Prototype

The microcontroller receives processed audio data through serial communication and controls LED brightness according to frequency intensity.

---

## Communication Format

Python sends processed data to the microcontroller using serial communication.

Example packet:

```
L:10,55,180,255,120,30;V:64;B:1
```

Format:

- `L` → LED brightness values for six frequency bands
- `V` → Audio volume level
- `B` → Beat detection status

---

## Technologies Used

### Software
- Python
- NumPy
- SoundDevice
- PySerial

### Hardware
- Arduino / ESP32
- PWM LED Control
- OLED Display Interface

### Concepts
- Digital Signal Processing
- Fast Fourier Transform
- Real-Time Data Processing
- Embedded Systems
- Serial Communication

---


## Installation & Execution

Install required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

The system starts audio processing, analyzes frequency components, detects beats, and updates LED and OLED visualization in real time.

---

## Current Status

✅ Real-time audio processing completed  
✅ FFT-based spectrum analysis implemented  
✅ Beat detection implemented  
✅ Serial communication working  
✅ LED spectrum visualization working  
✅ OLED display integration completed  

---

## Future Improvements

- RGB LED visualization
- Wireless ESP32 communication
- Improved beat detection algorithms
- Web-based audio visualization dashboard
- Mobile control interface

---

