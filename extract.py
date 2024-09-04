"""
A simple script to extract AtlasTexture image using xml file provided
Author: @nickphilomath
"""

import os
import sys
import xml.etree.ElementTree as ET
from PIL import Image


def get_arg(
        args: list[str],
        name: str,
        defauld_name: str = None,
        raise_error=False
    ) -> str | None:

    for index in range(len(args)):
        if args[index] == f"-{name}":
            return args[index + 1]

    if not raise_error:
        return defauld_name
    
    print(f'error: -{name} is requider.')
    sys.exit(1)


def extract() -> None:
    args = sys.argv[1:]

    # print manual when there is --help argv
    if args and args[0] == '--help':
        print("usage: python extract.py [-s source file] [-i source image] [-d destination folder]")
        return

    # Parse the XML file
    tree = ET.parse(get_arg(args, 's', raise_error=True))
    root = tree.getroot()

    # try to get image name from xml root or else require from args
    sprite_sheet_name = root.get('imagePath')
    if not sprite_sheet_name: sprite_sheet_name = get_arg(args, 'i', raise_error=True)
    
    # Load the sprite sheet
    sprite_sheet = Image.open(sprite_sheet_name)

    count = 0

    # Iterate over each SubTexture in the XML file
    for subtexture in root.findall('sprite'):
        name = subtexture.get('n')
        x = int(subtexture.get('x'))
        y = int(subtexture.get('y'))
        width = int(subtexture.get('w'))
        height = int(subtexture.get('h'))

        # # Extract the texture from the sprite sheet
        texture = sprite_sheet.crop((x, y, x + width, y + height))

        # get destinations folder name and create
        destination_folder = get_arg(args, 'd', defauld_name='extracted_images')
        os.makedirs(destination_folder, exist_ok=True)

        # # Save the extracted texture as a separate PNG file
        texture.save(f'{destination_folder}/{name}.png')

        print(f'> Extrated {name}.png')
        count += 1

    print(f'\n{count} images are extracted.')


if __name__ == '__main__':
    extract()