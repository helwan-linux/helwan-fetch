# helfetch.py

import sys
import argparse

# استيراد الدالات من وحدات جمع المعلومات
from core.system_info import get_system_info
from core.hardware_info import get_hardware_info
from core.desktop_info import get_desktop_info
from core.network_info import get_network_info

# استيراد وحدات العرض والتنسيق
from display.ascii_art import get_ascii_logo, COLORS
from display.formatter import format_info_output

# استيراد الإعدادات الافتراضية
from config.default_config import DEFAULT_COLORS # استيراد قاموس الألوان الافتراضية

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
    # يمكن إضافة خيارات لتخصيص الألوان لاحقاً هنا، إذا أردت
    # parser.add_argument("--key-color", help="Set the color for information keys.")
    # parser.add_argument("--value-color", help="Set the color for information values.")

    args = parser.parse_args()

    # 2. جمع جميع معلومات النظام
    system_data = get_system_info()
    hardware_data = get_hardware_info()
    desktop_data = get_desktop_info()
    network_data = get_network_info()

    # دمج كل المعلومات في قاموس واحد
    all_info = {
        **system_data,
        **hardware_data,
        **desktop_data,
        **network_data
    }

    # 3. الحصول على شعار Helwan Linux ASCII Art (إذا لم يتم تعطيله)
    helwan_logo = None
    if not args.no_logo:
        helwan_logo = get_ascii_logo("Helwan Linux")

    # 4. تنسيق ودمج المعلومات مع الشعار باستخدام الألوان الافتراضية
    # استخدم الألوان من DEFAULT_COLORS
    formatted_output = format_info_output(
        info_data=all_info,
        logo_lines=helwan_logo,
        info_key_color=DEFAULT_COLORS["info_key_color"], # استخدام اللون الافتراضي للمفاتيح
        info_value_color=DEFAULT_COLORS["info_value_color"] # استخدام اللون الافتراضي للقيم
    )

    # 5. طباعة الإخراج النهائي
    print(formatted_output)

# نقطة الدخول الرئيسية للبرنامج
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{COLORS['red']}An error occurred while running Helfetch: {e}{COLORS['reset']}", file=sys.stderr)
        sys.exit(1)
