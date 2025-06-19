# core/network_info.py
# pip install requests
import subprocess
import re
import requests # For external IP, requires 'requests' library (pip install requests)

def get_network_info():
    """
    Collects network-related information, primarily local and public IP addresses.
    """
    info = {}

    # 1. Local IP Address (IPv4)
    # Using 'ip a' or 'ip addr show' which is common on Linux.
    # We'll look for an IP that's not localhost (127.0.0.1) and is active.
    local_ip = 'N/A'
    try:
        ip_output = subprocess.check_output(['ip', '-4', 'addr', 'show'], text=True).strip()
        # Regex to find IP addresses, excluding localhost and looking for 'scope global'
        # or 'dynamic' to filter for active network interfaces.
        ip_matches = re.findall(r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d+ (?:scope global|dynamic)', ip_output)
        if ip_matches:
            # Prefer non-loopback address
            for ip in ip_matches:
                if not ip.startswith('127.'):
                    local_ip = ip
                    break
            if local_ip == 'N/A' and ip_matches: # If only loopback found, take it
                local_ip = ip_matches[0]
        else:
            # Fallback for simpler cases or if 'ip' command output is different
            # Can also parse 'ifconfig' if available (though less standard on modern Linux)
            # For simplicity, if 'ip' fails to parse, we stick to N/A for now.
            pass

    except (subprocess.CalledProcessError, FileNotFoundError):
        # 'ip' command not found or failed
        local_ip = 'N/A'
    info['Local IP'] = local_ip

    # 2. Public IP Address
    # This requires an external service. We'll use a common one.
    # Note: This part requires the 'requests' library (pip install requests).
    public_ip = 'N/A'
    try:
        # Using ipify.org as a free and common service
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors
        public_ip = response.json()['ip']
    except requests.exceptions.RequestException:
        # Handles connection errors, timeouts, invalid JSON, etc.
        public_ip = 'N/A'
    info['Public IP'] = public_ip

    return info

# For testing this module independently
if __name__ == "__main__":
    network_data = get_network_info()
    print("\n--- Network Information ---")
    for key, value in network_data.items():
        print(f"{key}: {value}")
