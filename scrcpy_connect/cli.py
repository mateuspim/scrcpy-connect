from scrcpy_connect.logger import setup_logging
from scrcpy_connect.core import connect_and_mirror_device
import argparse
import logging


def main():
    parser = argparse.ArgumentParser(
        description="Mirror android screen over WiFi using adb & scrcpy."
    )
    parser.add_argument(
        "--log-level",
        default="ERROR",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: ERROR)",
    )
    parser.add_argument("--ip", required=False, help="IP address of the Android device")
    parser.add_argument(
        "--port", type=int, default=5555, help="Port number (default: 5555)"
    )
    args, scrcpy_args = parser.parse_known_args()

    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting scrcpy-connect CLI")

    connect_and_mirror_device(
        device_ip=args.ip, device_port=args.port, scrcpy_args=scrcpy_args
    )


if __name__ == "__main__":
    main()
