import glob
import os
import re
from rich import print


def modify_svg_fonts(input_file, output_file, family, font_color):
    # Fájl beolvasása
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Font családok cseréje Calibrira
    content = re.sub(r'font-family:\s*"[^"]*"', f'font-family: "{family}"', content)
    content = re.sub(
        r'font-family:\s*[^,;"]*(?=[,;]|\s*\})', f"font-family: {family}", content
    )

    # Keressük a <text vagy <g id="tx elemeket
    text_pattern = r'(<(?:text|g id="tx[^"]*")[^>]*)(fill="[^"]*"|fill:\s*[^;"]*)'
    content = re.sub(text_pattern, f'\1fill="{font_color}"', content)

    style_pattern = r'(<(?:text|g id="tx[^"]*")[^>]*style="[^"]*?)(fill:\s*[^;"]*)'
    content = re.sub(style_pattern, f'\1fill="{font_color}"', content)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(content)


def process_all_svg_files(family="Calibri", font_color="#333333"):
    svg_files = glob.glob("**/*.svg", recursive=True)

    for svg_file in svg_files:
        dirname = os.path.dirname(svg_file)
        basename = os.path.basename(svg_file)
        name, ext = os.path.splitext(basename)
        output_file = os.path.join(dirname, f"{name}-modified{ext}")

        print(f"[bold blue]Feldolgozás:[/bold blue] {svg_file} -> {output_file}")
        modify_svg_fonts(svg_file, output_file, family, font_color)


if __name__ == "__main__":
    process_all_svg_files()
