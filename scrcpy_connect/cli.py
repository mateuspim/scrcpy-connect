import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Mirror android screen over WiFi using adb & scrcpy."
    )
    parser.add_argument(
        "--ip",
        required=False,
        help="IP address of the Android device"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5555,
        help="Port number (default: 5555)"
    )
    parser.add_argument(
        "adb_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to adb"
    )
    args = parser.parse_args()


if __name__ == "__main__":
    main()