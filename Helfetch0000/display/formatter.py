# display/formatter.py

import re
from display.ascii_art import COLORS # استيراد قاموس الألوان من ascii_art
from config.default_config import DEFAULT_COLORS # استيراد الألوان الافتراضية، بما في ذلك لون الاقتباس

def create_progress_bar(percentage, bar_length=20, filled_char="█", empty_char="-", bar_color="green", empty_color="white"):
    """
    Creates an ASCII art progress bar based on a percentage.
    """
    if not 0 <= percentage <= 100:
        percentage = max(0, min(100, percentage))

    filled_chars_count = int(bar_length * percentage / 100)
    empty_chars_count = bar_length - filled_chars_count

    filled_bar = COLORS.get(bar_color, COLORS["reset"]) + (filled_char * filled_chars_count)
    empty_bar = COLORS.get(empty_color, COLORS["reset"]) + (empty_char * empty_chars_count)

    return f"[{filled_bar}{empty_bar}{COLORS['reset']}]"


def format_info_output(info_data, logo_lines=None, inspirational_quote="", logo_color="light_cyan", info_key_color="light_yellow", info_value_color="white"):
    """
    Formats the system information, combines it with an ASCII art logo, and includes an inspirational quote.

    Args:
        info_data (dict): A dictionary containing all the system information.
        logo_lines (list, optional): A list of strings representing the ASCII art logo, line by line.
                                     If None, no logo will be displayed.
        inspirational_quote (str): An optional inspirational quote to display below info.
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
        # Ensure key is not empty and value is relevant before considering for max_key_length
        if key and info_data.get(key) not in [None, '', 'N/A']:
            if len(key) > max_key_length:
                max_key_length = len(key)

    for key, value in info_data.items():
        if value is None or value == '' or value == 'N/A':
            continue
        
        display_value = value

        # Process RAM and Disk for progress bar display
        if key == "RAM":
            try:
                if '/' in value:
                    parts = value.replace('Gi', '').replace('Mi', '').split('/')
                    used = float(parts[0])
                    total = float(parts[1])
                    if total > 0:
                        percentage = (used / total) * 100
                        bar = create_progress_bar(percentage, bar_length=15, bar_color="blue", empty_color="white")
                        display_value = f"{value} {bar}"
                elif value.endswith('%'):
                    percentage = float(value.strip('%'))
                    bar = create_progress_bar(percentage, bar_length=15, bar_color="blue", empty_color="white")
                    display_value = f"{value} {bar}"
            except (ValueError, IndexError):
                pass

        elif key == "Disk":
            try:
                if value.endswith('%'):
                    percentage = float(value.strip('%'))
                    bar = create_progress_bar(percentage, bar_length=15, bar_color="yellow", empty_color="white")
                    display_value = f"{value} {bar}"
            except ValueError:
                pass

        padding = " " * (max_key_length - len(key))
        colored_info_lines.append(
            f"{COLORS.get(info_key_color, COLORS['reset'])}{key}:{padding}{COLORS.get(info_value_color, COLORS['reset'])} {display_value}{COLORS['reset']}"
        )

    max_lines = max(len(logo_lines.split('\n')) if logo_lines else 0, len(colored_info_lines))

    combined_lines = []
    logo_lines_list = logo_lines.split('\n') if logo_lines else []

    max_logo_visual_width = 0
    for logo_line in logo_lines_list:
        stripped_logo_line_len = len(strip_ansi_codes(logo_line))
        if stripped_logo_line_len > max_logo_visual_width:
            max_logo_visual_width = stripped_logo_line_len

    for i in range(max_lines):
        logo_line = logo_lines_list[i] if i < len(logo_lines_list) else ""
        info_line = colored_info_lines[i] if i < len(colored_info_lines) else ""
        
        stripped_logo_line_len = len(strip_ansi_codes(logo_line))
        padding_between = " " * ((max_logo_visual_width - stripped_logo_line_len) + 4)
        
        combined_lines.append(f"{logo_line}{padding_between}{info_line}")

    # إضافة الاقتباس بعد معلومات النظام
    if inspirational_quote:
        combined_lines.append("") # سطر فارغ للفاصل
        quote_padding = " " * (max_logo_visual_width + 4) # نفس المسافة بين الشعار والمعلومات
        
        # استخدام اللون من DEFAULT_COLORS
        combined_lines.append(f"{quote_padding}{COLORS.get(DEFAULT_COLORS['quote_color'], COLORS['reset'])}{inspirational_quote}{COLORS['reset']}")

    return "\n".join(combined_lines)

def strip_ansi_codes(text):
    """
    Removes ANSI escape codes from a string to get its 'visual' length.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# For testing this module independently (يجب أن يعمل هذا القسم بشكل صحيح للاختبار)
if __name__ == "__main__":
    # هذا الجزء يستخدم لغرض الاختبار المباشر لـ formatter.py فقط
    # لا تعتمد عليه لإخراج Helfetch بالكامل
    example_info = {
        "User": "testuser",
        "Host": "testhost",
        "OS": "Test OS",
        "Kernel": "1.0",
        "RAM": "4.0Gi/8.0Gi",
        "Disk": "50%",
        "Public IP": "127.0.0.1",
        "ISP": "Test ISP",
        "City": "Test City",
        "Country": "Test Country"
    }

    from display.ascii_art import get_ascii_logo
    logo = get_ascii_logo("Helwan Linux")

    # تأكد من وجود default_config.py في المسار الصحيح للاختبار المستقل
    # أو قم بتعريف DEFAULT_COLORS هنا لأغراض الاختبار
    class MockDefaultColors:
        DEFAULT_COLORS = {
            "info_key_color": "light_yellow",
            "info_value_color": "white",
            "logo_color": "light_cyan",
            "quote_color": "light_green"
        }
    
    # استبدال الاستيراد الفعلي لـ DEFAULT_COLORS بهذا الكائن الوهمي للاختبار المستقل
    # هذا فقط للاختبار المباشر لـ formatter.py
    # في الاستخدام الفعلي لـ Helfetch.py سيتم استيرادها بشكل طبيعي
    global DEFAULT_COLORS 
    DEFAULT_COLORS = MockDefaultColors.DEFAULT_COLORS

    formatted_output = format_info_output(example_info, logo_lines=logo, inspirational_quote="This is a test quote.")
    print(formatted_output)

    print("\n--- Testing without quote ---")
    formatted_output_no_quote = format_info_output(example_info, logo_lines=logo)
    print(formatted_output_no_quote)
