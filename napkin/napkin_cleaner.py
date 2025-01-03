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


def remove_svg_whitespace(input_file, output_file):
    from xml.etree import ElementTree as ET

    tree = ET.parse(input_file)
    root = tree.getroot()

    # Get the bounding box of all elements
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
    for elem in root.iter():
        if 'x' in elem.attrib and 'y' in elem.attrib:
            x, y = float(elem.attrib['x']), float(elem.attrib['y'])
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)

    # Adjust the viewBox and all elements' positions
    if min_x < float('inf') and min_y < float('inf'):
        for elem in root.iter():
            if 'x' in elem.attrib and 'y' in elem.attrib:
                elem.attrib['x'] = str(float(elem.attrib['x']) - min_x)
                elem.attrib['y'] = str(float(elem.attrib['y']) - min_y)

        if 'viewBox' in root.attrib:
            viewBox = root.attrib['viewBox'].split()
            viewBox[0] = str(float(viewBox[0]) - min_x)
            viewBox[1] = str(float(viewBox[1]) - min_y)
            root.attrib['viewBox'] = ' '.join(viewBox)

    tree.write(output_file)

def process_all_svg_files(family="Calibri", font_color="#333333"):
    svg_files = glob.glob("**/*.svg", recursive=True)

    for svg_file in svg_files:
        dirname = os.path.dirname(svg_file)
        basename = os.path.basename(svg_file)
        name, ext = os.path.splitext(basename)
        output_file = os.path.join(dirname, f"{name}-modified{ext}")

        print(f"[bold blue]Feldolgozás:[/bold blue] {svg_file} -> {output_file}")
        modify_svg_fonts(svg_file, output_file, family, font_color)
        remove_svg_whitespace(output_file, output_file)


if __name__ == "__main__":
    process_all_svg_files()
