from typing import Optional, List
from scrcpy_connect.utils import (
    run_command,
    is_device_connected,
    get_device_ip,
    is_valid_ip,
    is_valid_port,
    select_device_menu,
)
import logging

logger = logging.getLogger(__name__)


def connect_and_mirror_device(
    retries: int,
    device_ip: Optional[str] = None,
    device_port: Optional[int] = None,
    scrcpy_args: Optional[List[str]] = None,
) -> None:
    """
    Connects to the Android device via ADB, checks connection, and runs scrcpy.
    """
    if scrcpy_args is None:
        scrcpy_args = []
    if device_port is None or not is_valid_port(device_port):
        device_port = 5555
    device_ip = (device_ip or "").strip()

    ip_only = device_ip.split(":")[0] if device_ip else ""

    if is_valid_ip(ip=ip_only) and ":" not in device_ip:
        device_ip = f"{ip_only}:{device_port}"
    elif not device_ip or ":" not in device_ip or not is_valid_ip(ip=ip_only):
        logger.info("Checking if device is connected")
        connected, device_ip = is_device_connected()
        if not connected:
            logger.info("Device not connected over WIFI. Connecting via USB...")
            logger.info("Waiting for USB connection")
            _, err = run_command("adb", "wait-for-device")
            if err:
                logger.error(f"Error waiting for device: {str(err)}")
                return

            logger.info("Getting connected devices list")
            out, err = run_command("adb", "devices")
            if err:
                logger.error(f"Error getting connected devices list: {str(err)}")
                return

            connected_devices = [
                line.split("\t")[0]
                for line in out.splitlines()
                if line.endswith("device")
            ]

            if len(connected_devices) > 1:
                logger.info(
                    "More than one android device connected via USB choose a device:"
                )
                device_serial = select_device_menu(connected_devices=connected_devices)
            else:
                device_serial = connected_devices[0]

            logger.info("Getting connected device ip")
            device_ip = get_device_ip(device_serial=device_serial)
            if not device_ip:
                logger.error(
                    "Could not find device IP address. Make sure Wi-Fi is enabled on the device."
                )
                return
            logger.info(f"Device IP Address: {device_ip}")

            logger.info("Enabling ADB over TCP/IP...")
            out, err = run_command("adb", "-s", device_serial, "tcpip", "5555")
            if err:
                logger.error(f"Error enabling tcpip mode: {str(err)}")
                return

            device_ip = f"{device_ip}:{device_port}"
            logger.info(f"Connecting to device over Wi-Fi at {device_ip}...")
            out, err = run_command("adb", "connect", f"{device_ip}")
            if err:
                logger.error(f"Error connecting over Wi-Fi: {str(err)}")
                return

    num_tries = 0
    while num_tries < retries:
        num_tries += 1
        logger.info("Device connected over WIFI")
        logger.info(
            f"Starting SCRCPY with args: -s {device_ip} {' '.join(scrcpy_args)}"
        )
        out, err = run_command("scrcpy", "-s", str(device_ip), *scrcpy_args)
        if out:
            logger.info(f"SCRCPY output: {out}")
        if err:
            logger.error(f"SCRCPY error: {err}")
        logger.info(f"Stopped running SCRCPY with {out} {err}")
