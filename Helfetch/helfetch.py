# helfetch.py

import sys
import argparse
import re
# استيراد الدالات من وحدات جمع المعلومات
from core.system_info import get_system_info, get_inspirational_quote
from core.hardware_info import get_hardware_info
from core.desktop_info import get_desktop_info
from core.network_info import get_network_info

# استيراد وحدات العرض والتنسيق
from display.ascii_art import get_ascii_logo, COLORS
from display.formatter import format_info_output

# استيراد الإعدادات الافتراضية
from config.default_config import DEFAULT_COLORS

def main():
    """
    The main function to run Helfetch.
    It collects all system information, formats it with the logo, and prints it.
    Supports command-line arguments for customization.
    """
    # 1. إعداد محلل وسائط سطر الأوامر
    parser = argparse.ArgumentParser(
        description="A custom system information fetcher for Helwan Linux."
    )
    parser.add_argument(
        "--no-logo",
        action="store_true",
        help="Do not display the Helwan Linux ASCII art logo."
    )
    args = parser.parse_args()

    # 2. جمع جميع معلومات النظام
    system_data = get_system_info()
    hardware_data = get_hardware_info()
    desktop_data = get_desktop_info()
    network_data = get_network_info()
    
    # 3. جلب الاقتباس الملهم
    inspirational_quote = get_inspirational_quote()

    # دمج كل المعلومات في قاموس واحد
    all_info = {
        **system_data,
        **hardware_data,
        **desktop_data,
        **network_data
    }

    # 4. الحصول على شعار Helwan Linux ASCII Art (إذا لم يتم تعطيله)
    helwan_logo = None
    if not args.no_logo:
        helwan_logo = get_ascii_logo("Helwan Linux")

    # 5. تنسيق ودمج المعلومات مع الشعار والاقتباس
    formatted_output = format_info_output(
        info_data=all_info,
        logo_lines=helwan_logo,
        inspirational_quote=inspirational_quote,
        info_key_color=DEFAULT_COLORS["info_key_color"],
        info_value_color=DEFAULT_COLORS["info_value_color"]
    )

    # 6. طباعة الإخراج النهائي
    print(formatted_output)

# نقطة الدخول الرئيسية للبرنامج
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{COLORS['red']}An error occurred while running Helfetch: {e}{COLORS['reset']}", file=sys.stderr)
        sys.exit(1)
