"""Collect details bout the host where habu is running."""
import platform
import socket


def gather_details():
    """Get details about the host that is executing habu."""
    try:
        data = {
            'kernel': platform.uname(),
            'distribution': platform.linux_distribution(),
            'libc': platform.libc_ver(),
            'arch': platform.machine(),
            'python_version': platform.python_version(),
            'os_name': platform.system(),
            'static_hostname': platform.node(),
            'cpu': platform.processor(),
            'fqdn': socket.getfqdn(),
        }
    except AttributeError:
        return {}

    return data
