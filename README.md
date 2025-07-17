# scrcpy-connect

**scrcpy-connect** is a Python tool that helps you connect Android devices to your computer over WiFi using ADB, and then mirror and control their screens with [scrcpy](https://github.com/Genymobile/scrcpy).

## Features

- Connect Android devices via ADB over WiFi
- Launch scrcpy for screen mirroring and control
- Simple command-line interface

## Requirements

- Python 3.12 or newer
- [ADB](https://developer.android.com/tools/adb) installed and available in your system PATH
- [scrcpy](https://github.com/Genymobile/scrcpy) installed and available in your system PATH
- Android device with USB debugging enabled

## Installation

Clone the repository and install with pip:

```bash
git clone https://github.com/mateuspim/scrcpy-connect.git
cd scrcpy-connect
pip install .
```

## Usage

Connect your Android device to your computer via USB, then run:

```bash
scrcpy-connect <device_ip_address>
```

Or, if you want to use additional scrcpy options:

```bash
scrcpy-connect <device_ip_address> --no-video-playback --bit-rate 2M
```

If you omit the IP address, the tool will try to automatically connect a USB device to WiFi if possible.

## License

[MIT](LICENSE)

## Author

Mateus Pim
mateuspimsantos@gmail.com