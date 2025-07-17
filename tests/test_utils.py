import subprocess
from unittest.mock import Mock
from scrcpy_connect.utils import (
    is_valid_ip,
    is_valid_port,
    run_command,
    is_device_connected,
    get_device_ip,
    select_device_menu,
)


def test_is_valid_ip():
    """Test various valid and invalid IPv4 addresses and CIDR notation."""
    assert is_valid_ip("192.168.1.1")
    assert is_valid_ip("10.0.0.1")
    assert not is_valid_ip("256.168.1.1")
    assert not is_valid_ip("192.168.1")
    assert is_valid_ip("192.168.1.1/24")
    assert not is_valid_ip("192.168.1.1/33")
    assert not is_valid_ip("not.an.ip")


def test_is_valid_port():
    """Test valid and invalid port numbers."""
    assert is_valid_port(1)
    assert is_valid_port(65535)
    assert not is_valid_port(0)
    assert not is_valid_port(70000)
    assert not is_valid_port(-1)


def test_run_command_success(mocker):
    """Test run_command returns correct output on success."""
    dummy_result = Mock(stdout="output", stderr="", returncode=0)
    mocker.patch("scrcpy_connect.utils.subprocess.run", return_value=dummy_result)
    out, err = run_command("echo", "hello")
    assert out == "output"
    assert err == ""


def test_run_command_failure(mocker):
    """Test run_command returns correct output on subprocess failure."""
    def dummy_run(*args, **kwargs):
        raise subprocess.CalledProcessError(
            returncode=1, cmd="echo hello", output="output", stderr="error"
        )
    mocker.patch("scrcpy_connect.utils.subprocess.run", side_effect=dummy_run)
    out, err = run_command("echo", "hello")
    assert out == "output"
    assert err == "error"


def test_is_device_connected_success(mocker):
    """Test is_device_connected returns True and correct IP when a device is connected."""
    mocker.patch(
        "scrcpy_connect.utils.run_command",
        return_value=("192.168.1.2:5555\tdevice\n", ""),
    )
    connected, device_ip = is_device_connected()
    assert connected is True
    assert device_ip == "192.168.1.2:5555"


def test_is_device_connected_no_device(mocker):
    """Test is_device_connected returns False when no device is connected."""
    mocker.patch("scrcpy_connect.utils.run_command", return_value=("", ""))
    connected, device_ip = is_device_connected()
    assert connected is False
    assert device_ip == ""


def test_is_device_connected_error(mocker):
    """Test is_device_connected returns False on error."""
    mocker.patch("scrcpy_connect.utils.run_command", return_value=("", "some error"))
    connected, device_ip = is_device_connected()
    assert connected is False
    assert device_ip == ""


def test_select_device_menu(mocker, capsys):
    """Test select_device_menu returns the correct device based on user input."""
    devices = ["dev1", "dev2", "dev3"]
    mocker.patch("builtins.input", return_value="2")
    selected = select_device_menu(devices)
    assert selected == "dev2"
    captured = capsys.readouterr()
    assert "Multiple Android devices detected" in captured.out


def test_get_device_ip_success(mocker):
    """Test get_device_ip returns the correct IP when present in command output."""
    mocker.patch(
        "scrcpy_connect.utils.run_command",
        return_value=(
            "    inet 192.168.1.2/24 brd 192.168.1.255 scope global wlan0\n",
            "",
        ),
    )
    ip = get_device_ip("serial")
    assert ip == "192.168.1.2"


def test_get_device_ip_error(mocker):
    """Test get_device_ip returns empty string on error."""
    mocker.patch("scrcpy_connect.utils.run_command", return_value=("", "error"))
    ip = get_device_ip("serial")
    assert ip == ""
