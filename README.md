# Napkin

A simple Python library that helps clean your svg images downloaded from Napkin.ai
The function changes the font family and the font color of the svg images.

## Installation

Install using pip:

```bash
pip install git+https://github.com/marcellgranat/napkin.git
```

## Usage

```python
from napkin import modify_svg_fonts

# convert the family on all svg files
process_all_svg_files(family="Calibri", font_color="#333333")
```
