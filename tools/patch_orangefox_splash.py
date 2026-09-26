#!/usr/bin/env python3
"""Set device-specific defaults in the OrangeFox fox_16.0 splash UI."""

from pathlib import Path
import sys


GOOGLE_DARK = "#202124"


def replace_count(text: str, old: str, new: str, expected: int, label: str) -> str:
    old_count = text.count(old)
    if old_count == 0 and text.count(new) == expected:
        return text
    if old_count != expected:
        raise SystemExit(
            f"{label}: expected {expected} source occurrence(s), found {old_count}"
        )
    return text.replace(old, new)


def patch_splash(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_count(
        text,
        'splash_logo_w',
        'splash_logo_d',
        2,
        "dark logo resource",
    )
    text = replace_count(
        text,
        'filename="Splash/logo_w"',
        'filename="Splash/logo_d"',
        1,
        "dark logo asset",
    )
    text = replace_count(
        text,
        '\t\t<image name="splash_bg" filename="Splash/original" retainaspect="1"/>\n',
        "",
        1,
        "default OrangeFox background image resource",
    )
    text = replace_count(
        text,
        '\n\t\t\t<image>\n'
        '\t\t\t\t<image resource="splash_bg"/>\n'
        '\t\t\t\t<placement x="540" y="%center_y%" placement="4"/>\n'
        '\t\t\t</image>\n',
        "\n",
        1,
        "default OrangeFox background image page",
    )
    text = replace_count(
        text,
        'value="#FF8038"',
        f'value="{GOOGLE_DARK}"',
        1,
        "splash fill color",
    )
    text = replace_count(
        text,
        'value="#D34E38"',
        f'value="{GOOGLE_DARK}"',
        1,
        "splash background color",
    )

    for label, block in (
        (
            "OrangeFox title",
            '\n\t\t\t<text style="menu_text">\n'
            '\t\t\t\t<placement x="540" y="%of%" placement="4"/>\n'
            '\t\t\t\t<font resource="of" color="#ffffff"/>\n'
            '\t\t\t\t<text>OrangeFox</text>\n'
            '\t\t\t</text>\n',
        ),
        (
            "Recovery title",
            '\n\t\t\t<text style="menu_text">\n'
            '\t\t\t\t<placement x="540" y="%rec%" placement="4"/>\n'
            '\t\t\t\t<font resource="recovery" color="#ffffff"/>\n'
            '\t\t\t\t<text>Recovery</text>\n'
            '\t\t\t</text>\n',
        ),
    ):
        text = replace_count(text, block, "\n", 1, label)

    path.write_text(text, encoding="utf-8", newline="\n")


def patch_customization(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    reset_old = (
        '\t\t\t\t<action function="set">spl_bg_user=0</action>\n'
        '\t\t\t\t<action function="set">spl_bg_on=0</action>\n'
        '\t\t\t\t<action function="set">spl_logo_type=w</action>\n'
        '\t\t\t\t<action function="set">spl_ofr=1</action>\n'
        '\t\t\t\t<action function="set">spl_bg_color=#1E1F22</action>\n'
    )
    reset_new = (
        '\t\t\t\t<action function="set">spl_bg_user=0</action>\n'
        '\t\t\t\t<action function="set">spl_bg_on=0</action>\n'
        '\t\t\t\t<action function="set">spl_logo_type=d</action>\n'
        '\t\t\t\t<action function="set">spl_ofr=0</action>\n'
        f'\t\t\t\t<action function="set">spl_bg_color={GOOGLE_DARK}</action>\n'
    )
    text = replace_count(text, reset_old, reset_new, 1, "splash reset defaults")

    info_old = (
        '\t\t\t\t<action function="set">spl_logo_type=w</action>\n'
        '\t\t\t\t<action function="set">spl_bg_color=#1E1F22</action>\n'
        '\t\t\t\t<action function="set">spl_bg_user=0</action>\n'
        '\t\t\t\t<action function="set">spl_bg_on=0</action>\n'
        '\t\t\t\t<action function="set">spl_ofr=1</action>\n'
    )
    info_new = (
        '\t\t\t\t<action function="set">spl_logo_type=d</action>\n'
        f'\t\t\t\t<action function="set">spl_bg_color={GOOGLE_DARK}</action>\n'
        '\t\t\t\t<action function="set">spl_bg_user=0</action>\n'
        '\t\t\t\t<action function="set">spl_bg_on=0</action>\n'
        '\t\t\t\t<action function="set">spl_ofr=0</action>\n'
    )
    text = replace_count(text, info_old, info_new, 2, "splash initial defaults")
    text = replace_count(
        text,
        'spl_bg_color=#1E1F22',
        f'spl_bg_color={GOOGLE_DARK}',
        1,
        "uploaded splash background default",
    )

    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <bootable/recovery directory>")

    recovery = Path(sys.argv[1])
    splash = recovery / "gui/theme/portrait_hdpi/splash.xml"
    customization = recovery / "gui/theme/portrait_hdpi/pages/customization.xml"
    if not splash.is_file() or not customization.is_file():
        raise SystemExit(f"Not an OrangeFox source tree: {recovery}")

    patch_splash(splash)
    patch_customization(customization)
    print("Applied Google Dark splash, dark logo, and unchecked title defaults.")


if __name__ == "__main__":
    main()
