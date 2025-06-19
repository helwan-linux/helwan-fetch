# core/system_info.py

import platform
import subprocess
import os
import re

def get_system_info():
    """
    يجمع المعلومات الأساسية عن نظام التشغيل.
    المرجعات:
    - platform: لاستخلاص معلومات النظام الأساسية.
    - subprocess: لتشغيل أوامر shell خارجية.
    - os: للوصول إلى متغيرات البيئة.
    """
    info = {}

    # 1. اسم المستخدم واسم المضيف
    try:
        info['User'] = os.getlogin()
    except OSError:
        # قد يفشل os.getlogin() في بعض البيئات (مثل SSH بدون TTY)
        info['User'] = os.getenv('USER') or 'N/A' # fallback
    info['Host'] = platform.node()

    # 2. نظام التشغيل
    try:
        # يفضل استخدام /etc/os-release للحصول على معلومات دقيقة عن التوزيعة
        with open('/etc/os-release', 'r') as f:
            os_release_content = f.read()
            pretty_name_match = re.search(r'PRETTY_NAME="([^"]+)"', os_release_content)
            if pretty_name_match:
                info['OS'] = pretty_name_match.group(1)
            else:
                info['OS'] = platform.system() # fallback لاسم النظام الأساسي
    except FileNotFoundError:
        info['OS'] = platform.system() # fallback إذا لم يتم العثور على الملف

    # 3. Kernel
    info['Kernel'] = platform.release()

    # 4. وقت التشغيل (Uptime)
    try:
        # الأمر 'uptime -p' يعطي مخرجات سهلة القراءة
        uptime_output = subprocess.check_output(['uptime', '-p'], text=True).strip()
        info['Uptime'] = uptime_output.replace('up ', '') # إزالة "up " من البداية
    except (subprocess.CalledProcessError, FileNotFoundError):
        info['Uptime'] = 'N/A'

    # 5. الـ Shell
    info['Shell'] = os.getenv('SHELL') or 'N/A'
    if info['Shell'] != 'N/A':
        # محاولة الحصول على اسم الـ Shell فقط (مثال: bash, zsh)
        info['Shell'] = os.path.basename(info['Shell'])

    # 6. Terminal
    info['Terminal'] = os.getenv('TERM') or 'N/A'
    if info['Terminal'] == 'xterm':
        # في بعض الأحيان يكون TERM هو xterm، ولكننا نريد اسم Terminal الفعلي
        # هذا الجزء قد يحتاج لتحسين لاحقاً ليكون أدق
        try:
            # محاولة قراءة من متغير VTE_TERMINAL_ID (خاص ببعض الترمينال)
            # أو فحص processes
            pass # في الوقت الحالي نتركه كما هو أو يمكن إضافة logic هنا
        except:
            pass


    # 7. عدد حزم Pacman (خاص بـ Arch Linux)
    try:
        pacman_count = subprocess.check_output(['pacman', '-Qq'], text=True).count('\n')
        info['Packages (Pacman)'] = str(pacman_count)
    except (subprocess.CalledProcessError, FileNotFoundError):
        info['Packages (Pacman)'] = 'N/A' # إذا لم يكن pacman متاحاً أو فشل الأمر

    return info

# عند تشغيل هذا الملف مباشرة للاختبار
if __name__ == "__main__":
    system_data = get_system_info()
    print("--- System Info ---")
    for key, value in system_data.items():
        print(f"{key}: {value}")
