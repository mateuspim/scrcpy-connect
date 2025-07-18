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
    parser.add_argument(
        "--retries", type=int, default=3, help="SCRCPY connection retries (default: 3)"
    )
    args, scrcpy_args = parser.parse_known_args()

    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting scrcpy-connect CLI")

    try:
        connect_and_mirror_device(
            device_ip=args.ip,
            device_port=args.port,
            scrcpy_args=scrcpy_args,
            retries=args.retries,
        )
    except KeyboardInterrupt as e:
        logger.info("Exiting program via CTRL + C")
    except Exception as e:
        logger.error(f"Error while trying to mirror device screen: {e}")


if __name__ == "__main__":
    main()
