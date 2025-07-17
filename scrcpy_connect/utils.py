import subprocess
import logging
import re
from typing import Tuple

logger = logging.getLogger(__name__)


def is_valid_ip(ip: str) -> bool:
    pattern = (
        r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}"
        r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
        r"(\/(3[0-2]|[12]?[0-9]))?$"
    )
    return re.fullmatch(pattern, ip) is not None


def is_valid_port(port: int) -> bool:
    return 1 <= port <= 65535


def run_command(name: str, *args: str) -> Tuple[str, str]:
    command = [name] + list(args)

    try:
        logger.debug(f"Running command: {command}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logger.debug("STDOUT: ")
        logger.debug(result.stdout)
        logger.debug("STDERR:")
        logger.debug(result.stderr)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        logger.error(f"Command: {command} failed with error:")
        logger.error(e.stderr)
        return e.stdout or "", e.stderr or ""
    except Exception as e:
        logger.error(f"Command: {command} failed with error:")
        logger.error(e)
        return "", str(e) or ""


def is_device_connected() -> Tuple[bool, str]:
    out, err = run_command("adb", "devices")
    if err:
        logger.error("Can't check if a device is connected")
        return False, ""

    device_ip = ""
    for line in out.splitlines():
        if line.endswith("device") and ":" in line:
            device_ip = line.split("\t")[0]
            return True, device_ip

    return False, device_ip


def get_device_ip(device_serial: str) -> str:
    ip_out, err = run_command(
        "adb", "shell", "ip", "-f", "inet", "addr", "show", "wlan0"
    )
    if err:
        logger.error(f"Error getting device IP: {str(err)}")
        return ""

    device_ip = ""
    for line in ip_out.splitlines():
        if "inet" in line.strip():
            ip_w_mask = line.strip().split(" ")[1]
            ip_candidate = ip_w_mask.split("/")[0]
            if is_valid_ip(ip_candidate):
                device_ip = ip_candidate

    return device_ip

def select_device_menu(connected_devices: list[str]) -> str:
    print("Multiple Android devices detected. Please select one:")
    for idx, serial in enumerate(connected_devices, 1):
        print(f"{idx}. {serial}")
    while True:
        choice = input(f"Enter the number of the device [1-{len(connected_devices)}]: ")
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(connected_devices):
                return connected_devices[idx - 1]
        print("Invalid selection. Please try again.")