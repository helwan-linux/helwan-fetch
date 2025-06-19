# core/hardware_info.py

import subprocess
import re

def get_hardware_info():
    """
    Collects essential hardware information (CPU, RAM, Disk).
    Utilizes subprocess to run system commands and parse their output.
    """
    info = {}

    # 1. CPU Information
    try:
        # Get CPU model name from /proc/cpuinfo
        with open('/proc/cpuinfo', 'r') as f:
            cpu_info_content = f.read()
            model_name_match = re.search(r'model name\s*:\s*(.*)', cpu_info_content)
            if model_name_match:
                info['CPU'] = model_name_match.group(1).strip()
            else:
                info['CPU'] = 'N/A'
    except FileNotFoundError:
        info['CPU'] = 'N/A'

    # 2. RAM Information (Total, Used, Free)
    try:
        # Use 'free -h' for human-readable output
        ram_output = subprocess.check_output(['free', '-h'], text=True).strip()
        # Example output:
        #               total        used        free      shared  buff/cache   available
        # Mem:          15Gi       4.0Gi       9.0Gi       1.0Gi       3.0Gi        10Gi
        lines = ram_output.split('\n')
        if len(lines) > 1:
            mem_line = lines[1]
            parts = mem_line.split()
            if len(parts) >= 7:
                total_ram = parts[1]
                used_ram = parts[2]
                info['RAM'] = f"{used_ram}/{total_ram}" # e.g., 4.0Gi/15Gi
            else:
                info['RAM'] = 'N/A'
        else:
            info['RAM'] = 'N/A'
    except (subprocess.CalledProcessError, FileNotFoundError):
        info['RAM'] = 'N/A'

    # 3. Disk Usage (Root partition only for simplicity)
    try:
        # Use 'df -h /' for human-readable output of root partition
        disk_output = subprocess.check_output(['df', '-h', '/'], text=True).strip()
        # Example output:
        # Filesystem      Size  Used Avail Use% Mounted on
        # /dev/sda2       200G  50G  140G  27% /
        lines = disk_output.split('\n')
        if len(lines) > 1:
            disk_line = lines[1]
            parts = disk_line.split()
            if len(parts) >= 5:
                used_disk_percent = parts[4]
                info['Disk'] = used_disk_percent # e.g., 27%
            else:
                info['Disk'] = 'N/A'
        else:
            info['Disk'] = 'N/A'
    except (subprocess.CalledProcessError, FileNotFoundError):
        info['Disk'] = 'N/A'

    # 4. GPU Information (More complex, placeholder for now)
    # Getting accurate GPU info can be challenging and often requires parsing 'lspci'
    # or specific tools like 'nvidia-smi' for Nvidia.
    # For a basic fetch tool, 'lspci' output is a common starting point.
    try:
        # This command attempts to find VGA/3D controllers
        gpu_output = subprocess.check_output(['lspci', '-k'], text=True).strip()
        gpu_lines = []
        for line in gpu_output.split('\n'):
            if 'VGA compatible controller' in line or '3D controller' in line:
                gpu_lines.append(line.split(':', 2)[-1].strip()) # Extract description
        info['GPU'] = ", ".join(gpu_lines) if gpu_lines else 'N/A'

    except (subprocess.CalledProcessError, FileNotFoundError):
        info['GPU'] = 'N/A' # lspci might not be available or command fails

    return info

# For testing this module independently
if __name__ == "__main__":
    hardware_data = get_hardware_info()
    print("\n--- Hardware Information ---")
    for key, value in hardware_data.items():
        print(f"{key}: {value}")
