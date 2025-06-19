# display/formatter.py

import re
from display.ascii_art import COLORS # استيراد قاموس الألوان من ascii_art

def create_progress_bar(percentage, bar_length=20, filled_char="█", empty_char="-", bar_color="green", empty_color="white"):
    """
    Creates an ASCII art progress bar based on a percentage.

    Args:
        percentage (float/int): The percentage value (e.g., 75 for 75%).
        bar_length (int): The total length of the progress bar.
        filled_char (str): The character to use for the filled portion of the bar.
        empty_char (str): The character to use for the empty portion of the bar.
        bar_color (str): The color key for the filled portion.
        empty_color (str): The color key for the empty portion.

    Returns:
        str: The ASCII art progress bar string.
    """
    if not 0 <= percentage <= 100:
        percentage = max(0, min(100, percentage)) # Clamp percentage to be within 0-100

    filled_chars_count = int(bar_length * percentage / 100)
    empty_chars_count = bar_length - filled_chars_count

    filled_bar = COLORS.get(bar_color, COLORS["reset"]) + (filled_char * filled_chars_count)
    empty_bar = COLORS.get(empty_color, COLORS["reset"]) + (empty_char * empty_chars_count)

    return f"[{filled_bar}{empty_bar}{COLORS['reset']}]"


def format_info_output(info_data, logo_lines=None, logo_color="light_cyan", info_key_color="light_yellow", info_value_color="white"):
    """
    Formats the system information and combines it with an ASCII art logo.

    Args:
        info_data (dict): A dictionary containing all the system information.
        logo_lines (list, optional): A list of strings representing the ASCII art logo, line by line.
                                     If None, no logo will be displayed.
        logo_color (str): The color key from COLORS to apply to the logo (if not already colored).
        info_key_color (str): The color key for the information labels (e.g., "OS", "CPU").
        info_value_color (str): The color key for the information values (e.g., "Arch Linux", "Intel i7").

    Returns:
        str: The formatted output ready to be printed to the console.
    """
    formatted_lines = []
    
    colored_info_lines = []
    max_key_length = 0
    
    # Calculate max key length for alignment
    for key in info_data.keys():
        if key and info_data.get(key) not in [None, '', 'N/A']:
            if len(key) > max_key_length:
                max_key_length = len(key)

    for key, value in info_data.items():
        if value is None or value == '' or value == 'N/A':
            continue
        
        display_value = value # القيمة التي سيتم عرضها

        # **التعديل هنا: معالجة الذاكرة (RAM) والقرص (Disk) لشريط التقدم**
        # Process RAM and Disk for progress bar display
        if key == "RAM":
            try:
                # Expected format: "UsedGi/TotalGi" e.g., "8.0Gi/16Gi"
                # أو "Used%/Total" if we change system_info to give percentage directly
                if '/' in value:
                    parts = value.replace('Gi', '').replace('Mi', '').split('/')
                    used = float(parts[0])
                    total = float(parts[1])
                    if total > 0:
                        percentage = (used / total) * 100
                        bar = create_progress_bar(percentage, bar_length=15, bar_color="blue", empty_color="white")
                        display_value = f"{value} {bar}"
                elif value.endswith('%'): # If the value is already a percentage
                    percentage = float(value.strip('%'))
                    bar = create_progress_bar(percentage, bar_length=15, bar_color="blue", empty_color="white")
                    display_value = f"{value} {bar}"
            except (ValueError, IndexError):
                pass # Fallback to original value if parsing fails

        elif key == "Disk":
            try:
                # Expected format: "XX%" e.g., "35%"
                if value.endswith('%'):
                    percentage = float(value.strip('%'))
                    # يمكن تغيير لون شريط القرص إذا أردت
                    bar = create_progress_bar(percentage, bar_length=15, bar_color="yellow", empty_color="white")
                    display_value = f"{value} {bar}"
            except ValueError:
                pass # Fallback to original value if parsing fails
        # **نهاية التعديل**

        padding = " " * (max_key_length - len(key))
        colored_info_lines.append(
            f"{COLORS.get(info_key_color, COLORS['reset'])}{key}:{padding}{COLORS.get(info_value_color, COLORS['reset'])} {display_value}{COLORS['reset']}"
        )

    max_lines = max(len(logo_lines.split('\n')) if logo_lines else 0, len(colored_info_lines))

    combined_lines = []
    logo_lines_list = logo_lines.split('\n') if logo_lines else []

    # حساب أقصى طول مرئي للشعار لتنسيق المحاذاة بدقة
    max_logo_visual_width = 0
    for logo_line in logo_lines_list:
        stripped_logo_line_len = len(strip_ansi_codes(logo_line))
        if stripped_logo_line_len > max_logo_visual_width:
            max_logo_visual_width = stripped_logo_line_len

    for i in range(max_lines):
        logo_line = logo_lines_list[i] if i < len(logo_lines_list) else ""
        info_line = colored_info_lines[i] if i < len(colored_info_lines) else ""
        
        # استخدام الطول المرئي للشعار لتحديد المسافة
        stripped_logo_line_len = len(strip_ansi_codes(logo_line))
        # نستخدم 4 مسافات إضافية كفاصل ثابت
        padding_between = " " * ((max_logo_visual_width - stripped_logo_line_len) + 4)
        
        combined_lines.append(f"{logo_line}{padding_between}{info_line}")

    return "\n".join(combined_lines)

def strip_ansi_codes(text):
    """
    Removes ANSI escape codes from a string to get its 'visual' length.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# For testing this module independently
if __name__ == "__main__":
    # Example system data
    example_info = {
        "User": "youruser",
        "Host": "helwan-pc",
        "OS": "Helwan Linux",
        "Kernel": "6.8.9-arch1-1",
        "Uptime": "2h 30m",
        "Shell": "zsh",
        "Terminal": "kitty",
        "Packages (Pacman)": "1234",
        "CPU": "Intel Core i7-10750H",
        "RAM": "8.0Gi/16.0Gi", # مثال للذاكرة
        "Disk": "35%",        # مثال للقرص
        "GPU": "NVIDIA GeForce RTX 3050",
        "Desktop Environment": "KDE Plasma",
        "Window Manager": "KWin",
        "GTK Theme": "WhiteSur-Dark",
        "Icons": "WhiteSur-dark",
        "Font": "Roboto Regular 10",
        "Local IP": "192.168.1.100",
        "Public IP": "203.0.113.45",
        "Empty Key": "",
        "NA Key": "N/A"
    }

    from display.ascii_art import get_ascii_logo
    logo = get_ascii_logo("Helwan Linux")

    formatted_output = format_info_output(example_info, logo_lines=logo)
    print(formatted_output)

    print("\n--- Testing with different RAM/Disk values ---")
    example_info_2 = example_info.copy()
    example_info_2["RAM"] = "1.0Gi/10.0Gi"
    example_info_2["Disk"] = "90%"
    formatted_output_2 = format_info_output(example_info_2, logo_lines=logo)
    print(formatted_output_2)
