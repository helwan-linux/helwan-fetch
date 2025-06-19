# display/ascii_art.py

# ANSI escape codes for colors
COLORS = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "magenta": "\033[0;35m",
    "cyan": "\033[0;36m",
    "white": "\033[0;37m",
    "light_red": "\033[1;31m",
    "light_green": "\033[1;32m",
    "light_yellow": "\033[1;33m",
    "light_blue": "\033[1;34m",
    "light_magenta": "\033[1;35m",
    "light_cyan": "\033[1;36m",
    "light_white": "\033[1;37m",
    "reset": "\033[0m" # Reset color to default
}

# Helwan Linux ASCII Art (Colored using ANSI escape codes)
# Your unique Helwan Linux logo!
HELWAN_LOGO = f"""\
{COLORS["light_cyan"]}▖▖   ▜
▙▌█▌▐ ▌▌▌▀▌▛▌
▌▌▙▖▐▖▚▚▘█▌▌▌{COLORS["reset"]}
"""

def get_ascii_logo(os_name="Helwan Linux"):
    """
    Returns the ASCII art logo for Helwan Linux.
    Currently, only the Helwan Linux logo is supported.
    """
    # بما أننا نركز على Helwan Linux فقط، يمكننا إرجاع هذا الشعار مباشرةً
    # Since we are focusing only on Helwan Linux, we can return this logo directly.
    return HELWAN_LOGO

# For testing this module independently
if __name__ == "__main__":
    print(get_ascii_logo("Helwan Linux"))
    print("\n--- Example Colors ---")
    print(f"{COLORS['red']}This is red.{COLORS['reset']}")
    print(f"{COLORS['blue']}This is blue.{COLORS['reset']}")
    print(f"{COLORS['light_green']}This is light green.{COLORS['reset']}")
