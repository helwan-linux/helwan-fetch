# core/system_info.py

import platform
import subprocess
import os
import re
import random # استيراد مكتبة random لاختيار الرسائل عشوائيا

# استيراد قائمة الرسائل من ملف quotes.py
from config.quotes import QUOTES

def get_system_info():
    """
    Collects basic system-related information.
    """
    info = {}

    # 1. User
    try:
        info['User'] = os.getlogin()
    except OSError:
        info['User'] = os.getenv('USER') or os.getenv('USERNAME') or 'N/A'

    # 2. Host
    info['Host'] = platform.node()

    # 3. OS
    os_name = 'N/A'
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    os_name = line.strip().split('=')[1].strip('"')
                    break
        if "Arch Linux" in os_name:
            os_name = os_name.replace("Arch Linux", "Helwan Linux")
            # يمكنك إضافة إصدار مخصص لـ Helwan Linux هنا
            # os_name += " (Ver. 1.0 'Phoenix')"
    except FileNotFoundError:
        os_name = platform.system()
        if os_name == "Windows":
            os_name = "Windows"
    info['OS'] = os_name

    # 4. Kernel
    info['Kernel'] = platform.release()

    # 5. Uptime
    uptime_val = 'N/A'
    try:
        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True, check=True)
        uptime_val = result.stdout.strip().replace('up ', '')
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                days = int(uptime_seconds // 86400)
                hours = int((uptime_seconds % 86400) // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                if days > 0:
                    uptime_val = f"{days}d {hours}h {minutes}m"
                elif hours > 0:
                    uptime_val = f"{hours}h {minutes}m"
                else:
                    uptime_val = f"{minutes}m"
        except (FileNotFoundError, ValueError):
            uptime_val = 'N/A'
    info['Uptime'] = uptime_val

    # 6. Shell
    shell_val = 'N/A'
    try:
        shell_val = os.getenv('SHELL')
        if shell_val:
            shell_val = os.path.basename(shell_val)
    except Exception:
        pass
    info['Shell'] = shell_val

    # 7. Terminal
    terminal_val = 'N/A'
    try:
        terminal_val = os.getenv('TERM') or os.getenv('COLORTERM')
    except Exception:
        pass
    info['Terminal'] = terminal_val

    # 8. Packages (Pacman) - This section remains unchanged from previous step
    packages_val = 'N/A'
    package_manager = 'N/A'
    try:
        pacman_count = subprocess.run(['pacman', '-Qq'], capture_output=True, text=True).stdout.count('\n')
        if pacman_count > 0:
            packages_val = str(pacman_count)
            package_manager = 'Pacman'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    if package_manager != 'N/A':
        info[f'Packages ({package_manager})'] = packages_val
    else:
        info['Packages'] = 'N/A'

    return info

def get_inspirational_quote():
    """
    Returns a random inspirational quote from the QUOTES list.
    """
    if QUOTES:
        return random.choice(QUOTES)
    return "" # ارجع سلسلة فارغة لو مفيش اقتباسات
