import ipaddress

def ip_version(s: str) -> int | None:
    try:
        return ipaddress.ip_address(s).version  # 4 o 6
    except ValueError:
        return None  # no es IP literal (probablemente hostname)
