# core/network_info.py

import subprocess
import requests # هنحتاج المكتبة دي
import json # عشان نتعامل مع بيانات JSON من الـ API
import re
def get_network_info():
    """
    Collects network-related information including local IP, public IP, ISP, and location.
    """
    info = {}

    # 1. Local IP Address
    local_ip = 'N/A'
    try:
        # Get default gateway IP for Linux
        result = subprocess.run(['ip', 'route', 'get', '1.1.1.1'], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if 'src' in line:
                match = re.search(r'src (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if match:
                    local_ip = match.group(1)
                    break
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback for systems where 'ip route' might not work or for Windows
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # Connect to a public server to get local IP
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            local_ip = 'N/A'
            
    info['Local IP'] = local_ip

    # 2. Public IP Address, ISP, and Location (City, Country)
    public_ip = 'N/A'
    isp = 'N/A'
    city = 'N/A'
    country = 'N/A'
    
    try:
        # Using ip-api.com for public IP, ISP, city, and country
        # This service has a rate limit for free tier (45 requests per minute from an IP)
        response = requests.get("http://ip-api.com/json/")
        data = json.loads(response.text)
        
        if data and data.get("status") == "success":
            public_ip = data.get("query", "N/A")
            isp = data.get("isp", "N/A")
            city = data.get("city", "N/A")
            country = data.get("country", "N/A")
            
    except requests.exceptions.RequestException:
        # Handle network errors, e.g., no internet connection
        pass
    except json.JSONDecodeError:
        # Handle errors in parsing JSON response
        pass

    info['Public IP'] = public_ip
    info['ISP'] = isp
    info['City'] = city
    info['Country'] = country

    return info

# for testing this module independently
if __name__ == "__main__":
    network_data = get_network_info()
    print("\n--- Network Information ---")
    for key, value in network_data.items():
        print(f"{key}: {value}")
