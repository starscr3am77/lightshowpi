# LightShowPi - Audio-Synchronized Light Show System

LightShowPi is a comprehensive Raspberry Pi-based system that synchronizes lights to music by analyzing audio frequencies and controlling GPIO pins or LED strips. This system transforms any space into a synchronized light show, perfect for parties, events, or home automation projects.

## How It Works

### Core Architecture

1. **Audio Analysis Engine**
   - Uses **FFT (Fast Fourier Transform)** to analyze audio frequency content in real-time
   - Breaks down audio into frequency bands (typically 8-24 channels)
   - Each frequency band corresponds to a light channel
   - Supports various audio formats: MP3, WAV, OGG, and streaming sources

2. **Hardware Control**
   - **GPIO Control**: Direct control of Raspberry Pi GPIO pins (0-7 by default)
   - **Port Expanders**: Support for I2C/SPI expanders (MCP23017, MCP23S17, etc.) to add more channels
   - **LED Strips**: RGB LED control via Arduino/NodeMCU for advanced lighting effects
   - **Relay Control**: Can control solid-state or mechanical relays for AC/DC loads

3. **Configuration System**
   - `config/defaults.cfg`: Base configuration with all available settings
   - `config/overrides.cfg`: User-specific customizations
   - Supports per-song configuration overrides
   - Configurable pin modes: PWM (fading) or on/off switching

### Key Components

#### 1. **Main Application** (`py/synchronized_lights.py`)
- Orchestrates the entire light show
- Handles audio playback and analysis
- Manages light synchronization
- Supports playlists and individual songs
- Includes caching system for FFT calculations

#### 2. **Audio Processing** (`py/fft.py`)
- Performs real-time frequency analysis
- Maps frequency ranges to light channels
- Optimized with GPU acceleration when available
- Caches FFT results for performance

#### 3. **Hardware Interface** (`py/hardware_controller.py`)
- Manages GPIO pin states
- Handles PWM for fading effects
- Supports multiple hardware configurations
- Network client/server capabilities

#### 4. **Web Interface** (`web_flask_2023/`)
- Flask-based web control panel
- Start/stop light shows
- Control speakers and system power
- SMS integration for remote control

#### 5. **Arduino Integration** (`Arduino/`)
- Controls RGB LED strips
- Supports multiple LED chipset types (WS2811, APA102, etc.)
- Receives commands from Raspberry Pi via serial communication

### How It Works

1. **Setup Phase**:
   - Audio file is loaded and analyzed using FFT
   - Frequency ranges are mapped to light channels
   - FFT data is cached for future playback

2. **Playback Phase**:
   - Audio is played through speakers/headphones
   - Real-time frequency analysis of audio stream
   - Each frequency band triggers corresponding light channel
   - Lights fade or switch based on audio amplitude

3. **Control Options**:
   - **Web Interface**: Browser-based control panel
   - **Command Line**: Direct script execution
   - **SMS**: Remote control via text messages
   - **Scheduling**: Automated shows via cron jobs

### Advanced Features

- **Network Mode**: Client/server architecture for distributed light shows
- **FM Broadcasting**: Transmit audio to FM radio for wireless speakers
- **LED Strip Support**: Full RGB color control with custom patterns
- **Audio Input**: Real-time analysis of live audio sources
- **Multiple Audio Sources**: Pandora, AirPlay, streaming services
- **Performance Optimizations**: GPU acceleration, FFT caching

## Directory Structure

```
lightshowpi/
├── py/                    # Python source code
│   ├── synchronized_lights.py  # Main application
│   ├── fft.py            # Audio frequency analysis
│   ├── hardware_controller.py  # GPIO and hardware control
│   └── ...
├── config/               # Configuration files
│   ├── defaults.cfg      # Base configuration
│   ├── overrides.cfg     # User customizations
│   └── contrib/          # Hardware-specific configs
├── bin/                  # Shell scripts and utilities
├── web_flask_2023/       # Web interface
├── Arduino/              # Arduino/NodeMCU code for LED strips
├── music/                # Audio files
├── tools/                # Configuration and testing tools
└── logs/                 # System logs
```

## Installation

The system includes comprehensive installation scripts that:
- Detect the Linux distribution (Raspbian/Arch ARM)
- Install system dependencies
- Configure Python packages
- Set up GPIO permissions
- Create necessary directories and configurations

### Quick Start

1. Clone the repository
2. Run `sudo ./install.sh`
3. Configure your hardware in `config/overrides.cfg`
4. Add music files to `music/` directory
5. Start the light show with `sudo python py/synchronized_lights.py --file=music/song.mp3`

## Usage Examples

### Play a single song
```bash
sudo python py/synchronized_lights.py --file=music/song.mp3
```

### Play from playlist
```bash
sudo python py/synchronized_lights.py --playlist=music/.playlist
```

### Web interface
Access the web control panel at `http://your-pi-ip:8283`

### SMS control
Send commands via SMS to control the system remotely

## Hardware Support

### GPIO Pins
- Default: 8 GPIO pins (0-7)
- Expandable via I2C/SPI port expanders
- Support for up to 24+ channels

### LED Strips
- WS2811, WS2812, APA102, LPD8806
- Full RGB color control
- Custom patterns and effects

### Audio Sources
- Local audio files (MP3, WAV, OGG)
- Streaming services (Pandora, AirPlay)
- Live audio input
- FM broadcasting capability

## Configuration

Key configuration options in `config/overrides.cfg`:

- `gpio_pins`: Define which GPIO pins to use
- `pin_modes`: Set PWM or on/off mode for each pin
- `channels`: Configure frequency ranges for each channel
- `audio`: Audio device and format settings
- `hardware`: Port expander and device configurations

## License

All files are free to use under the BSD License. See the LICENSE file for details.

## Community

- [Official Website](http://lightshowpi.org/)
- [Reddit Community](https://www.reddit.com/r/LightShowPi/)
- [Facebook Page](https://www.facebook.com/lightshowpi)

## Contributors

A huge thanks to all contributors who have helped build and improve LightShowPi over the years. This project represents the collaborative effort of many developers and enthusiasts in the Raspberry Pi and audio-visual communities.

---

*LightShowPi transforms your Raspberry Pi into a powerful audio-synchronized light show controller, bringing music to life through synchronized lighting effects.*
