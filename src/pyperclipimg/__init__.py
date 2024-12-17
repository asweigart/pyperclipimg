"""pyperclipimg
By Al Sweigart al@inventwithpython.com

Cross-platform copy() and paste() Python functions for images."""

__version__ = '0.2.0'

import sys
import subprocess
import shutil
import os
import tempfile
import datetime
from pathlib import Path

from PIL import Image, ImageGrab
import PIL


class PyperclipImgException(Exception):
    pass


def _get_image_from_arg_if_arg_is_filename(arg):
    """Return a PIL.Image.Image object if `arg` refers to an image filename. If `arg`
    is already an Image object, just return `arg`."""
    if isinstance(arg, PIL.Image.Image):
        return arg  # Return the image object
    if isinstance(arg, (str, Path)):
        if not os.path.isfile(arg):
            raise PyperclipImgException('No file named ' + str(arg))
        try:
            return Image.open(arg)  # Get an Image object from the filename and return it.
        except PIL.UnidentifiedImageError:
            raise PyperclipImgException('File ' + str(arg) + ' is not an image file.')
    else:
        raise PyperclipImgException('arg ' + str(arg) + ' is not an Image or filename of an image.')


def _copy_windows(image):
    """On Windows, copy the `image` to the clipboard. The `image` arg can either be
    a PIL.Image.Image object or a str/Path refering to an image file.

    This function uses the pywin32 module and is aliased as pyperclipimg.copy()"""

    # TODO - see if there's a way to do this from Pillow so we can drop the
    # Pywin32 dependency.

    image = _get_image_from_arg_if_arg_is_filename(image)

    # Get the image as bmp bitmap data:
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    # Copy the bitmap to the clipboard:
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def _copy_macos(image):
    """On macOS, copy the `image` to the clipboard. The `image` arg can either be
    a PIL.Image.Image object or a str/Path refering to an image file.

    This function uses the Quartz module and is aliased as pyperclipimg.copy()"""

    image = _get_image_from_arg_if_arg_is_filename(image)

    # Convert the Pillow image object to TIFF format:
    output = io.BytesIO()
    image.save(output, format="TIFF")
    tiff_data = output.getvalue()
    output.close()

    # Create an NSImage from the TIFF data:
    NSImage.alloc().initWithData_(tiff_data)

    # Create a bitmap representation:
    image_rep = NSBitmapImageRep.alloc().initWithData_(tiff_data)

    # Set the image to the clipboard:
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.declareTypes_owner_([NSPasteboardTypeTIFF], None)
    pasteboard.setData_forType_(image_rep.TIFFRepresentation(), NSPasteboardTypeTIFF)


def _copy_linux_xclip(image):
    """On Linux, copy the `image` to the clipboard. The `image` arg can either be
    a PIL.Image.Image object or a str/Path refering to an image file.

    This function uses the xclip command and is aliased as pyperclipimg.copy()"""
    image = _get_image_from_arg_if_arg_is_filename(image)

    with tempfile.NamedTemporaryFile() as temp_file_obj:
        image.save(temp_file_obj.name, format='png')
        subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', temp_file_obj.name])


def _copy_linux_wlcopy(image):
    """On Linux, copy the `image` to the clipboard. The `image` arg can either be
    a PIL.Image.Image object or a str/Path refering to an image file.

    This function uses the wl-copy command and is aliased as pyperclipimg.copy()"""
    image = _get_image_from_arg_if_arg_is_filename(image)

    with tempfile.NamedTemporaryFile() as temp_file_obj:
        image.save(temp_file_obj.name, format='png')
        with open(temp_file_obj.name, 'rb') as image_file:
            subprocess.run(['wl-copy'], stdin=image_file)


def paste():
    # ImageGrab.grabclipboard() is new in Pillow version 1.1.4: (Windows), 3.3.0 (macOS), 9.4.0 (Linux)
    return ImageGrab.grabclipboard()


# For the current OS, import modules and alias the copy() function:
if sys.platform == 'win32':
    import win32clipboard
    import io

    copy = _copy_windows

elif sys.platform == 'darwin':
    from Quartz import NSPasteboard, NSPasteboardTypeTIFF
    from Cocoa import NSImage, NSBitmapImageRep
    import io

    copy = _copy_macos

elif sys.platform == 'linux':
    # Prefer xclip first, then check for wl-copy. (wl-copy causes a window to appear briefly.)
    if shutil.which('xclip'):
        copy = _copy_linux_xclip
    elif shutil.which('wl-copy'):
        copy = _copy_linux_wlcopy
    else:
        raise NotImplementedError(
            'pyperclipimg on Linux requires the xclip or wl-copy command. Run either '
            '`sudo apt install xclip` or `sudo apt install wl-clipboard` and restart'
        )

else:
    assert False, "pyperclipimg cannot run on this platform " + sys.platform


def show(filename=None):
    """If there's an image on the clipboard, display the image using
    Pillow's show() method. If filename is not None, display the image
    file instead."""

    if filename is not None:
        Image.open(filename).show()
        return

    im = ImageGrab.grabclipboard()
    if im is not None:
        im.show()


def save(filename=None):
    """If there's an image on the clipboard, save it using Pillow's
    save() method. If filename is None, use the format
    clipboard-2025-12-31_12-00-00-000000.png for the filename. Use
    this format also if filename is a folder to save to that folder."""

    im = ImageGrab.grabclipboard()
    if im is None:
        return

    if filename is None:
        filename = Path('clipboard-' + str(datetime.datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_') + '.png')
    else:
        filename = Path(filename)
        if filename.is_dir():
            filename = filename / Path('clipboard-' + str(datetime.datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_') + '.png')

    im.save(filename)
