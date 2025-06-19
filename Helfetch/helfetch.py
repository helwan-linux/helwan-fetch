#!/usr/bin/env python3

import sys
import argparse
import os
import re

# بما أننا الآن سنثبت مجلد 'helfetch' بالكامل كحزمة بايثون في site-packages،
# Python هيقدر يلاقي الموديولات بشكل مباشر.
# وبالتالي، مفيش داعي لتعديل sys.path يدوياً هنا.

# استيراد الدالات من وحدات جمع المعلومات
# لازم نحدد "helfetch." قبل اسم كل موديول فرعي، لأنها جزء من حزمة "helfetch"
from helfetch.core.system_info import get_system_info, get_inspirational_quote
from helfetch.core.hardware_info import get_hardware_info
from helfetch.core.desktop_info import get_desktop_info
from helfetch.core.network_info import get_network_info

# استيراد وحدات العرض والتنسيق
from helfetch.display.ascii_art import get_ascii_logo, COLORS
from helfetch.display.formatter import format_info_output

# استيراد الإعدادات الافتراضية
from helfetch.config.default_config import DEFAULT_COLORS

# استيراد من مجلد utils الجديد
# from helfetch.utils.helpers import some_helper_function # لو محتاج تستورد حاجة من utils

def main():
    """
    The main function to run Helfetch.
    It collects all system information, formats it with the logo, and prints it.
    Supports command-line arguments for customization.
    """
    parser = argparse.ArgumentParser(
        description="A custom system information fetcher for Helwan Linux."
    )
    parser.add_argument(
        "--no-logo",
        action="store_true",
        help="Do not display the Helwan Linux ASCII art logo."
    )
    args = parser.parse_args()

    system_data = get_system_info()
    hardware_data = get_hardware_info()
    desktop_data = get_desktop_info()
    network_data = get_network_info()
    
    inspirational_quote = get_inspirational_quote()

    all_info = {
        **system_data,
        **hardware_data,
        **desktop_data,
        **network_data
    }

    helwan_logo = None
    if not args.no_logo:
        helwan_logo = get_ascii_logo("Helwan Linux")

    formatted_output = format_info_output(
        info_data=all_info,
        logo_lines=helwan_logo,
        inspirational_quote=inspirational_quote,
        info_key_color=DEFAULT_COLORS["info_key_color"],
        info_value_color=DEFAULT_COLORS["info_value_color"]
    )

    print(formatted_output)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{COLORS['red']}An error occurred while running Helfetch: {e}{COLORS['reset']}", file=sys.stderr)
        sys.exit(1)
