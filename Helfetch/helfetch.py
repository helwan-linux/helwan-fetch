#!/usr/bin/env python3

import sys
import argparse
import os
import re

# هذه هي إضافة المسار الصحيح للموديولات.
# بناءً على PKGBUILD، ملف helfetch.py سيكون في /usr/bin/helfetch
# وباقي الموديولات (core, display, config) ستكون في /usr/lib/helfetch/
# لذا، نحتاج لجعل Python يبحث في /usr/lib/helfetch/
# os.path.dirname(__file__) يعطينا '/usr/bin'
# os.path.join(os.path.dirname(__file__), '..', 'lib', 'helfetch') يقوم ببناء المسار:
# 1. يذهب إلى مجلد /usr/bin/
# 2. يصعد مستوى واحد (..) ليصبح في /usr/
# 3. يدخل إلى مجلد lib/
# 4. يدخل إلى مجلد helfetch/
# ليصبح المسار النهائي هو /usr/lib/helfetch/
project_modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'helfetch'))

# إضافة المسار إلى sys.path (قائمة المسارات التي يبحث فيها بايثون عن الموديولات)
if project_modules_path not in sys.path:
    sys.path.insert(0, project_modules_path)

# استيراد الدالات من الوحدات مباشرة (بما أن المسار الآن صحيح)
from core.system_info import get_system_info, get_inspirational_quote
from core.hardware_info import get_hardware_info
from core.desktop_info import get_desktop_info
from core.network_info import get_network_info

from display.ascii_art import get_ascii_logo, COLORS
from display.formatter import format_info_output

from config.default_config import DEFAULT_COLORS


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
