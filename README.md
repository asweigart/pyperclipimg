# pyperclipimg
Python copy() and paste() clipboard functions for images on Windows, macOS, and Linux.

This module has Pillow as a dependency, as well as the following dependencies:

Windows: The pywin32 Python package. Install with `pip install pywin32`

macOS: The pyobjc-framework-quartz Python package. Install with `pip install pyobjc-framework-quartz`

Linux: Either the xclip or wl-copy commands. Install these with `sudo apt install xclip` or `sudo apt install wl-clipboard`

# Quickstart

To copy an image in a file to the clipboard, pass the filename as a str or Path object to `copy()`. A Pillow `Image` object can also be passed. Any image format that Pillow supports can be used (png, jpg, gif, bmp, webp)

```
>>> import pyperclipimg as pci
>>> pci.copy('example.png')  # Copy by filename.

>>> import pyperclip as pci
>>> from pathlib import Path
>>> pci.copy(Path('example.png'))  # Copy by Path object.

>>> import pyperclip as pci
>>> from PIL import Image
>>> pci.copy(Image.open('example.png'))  # Copy by Image object.
```

To paste the image (that is, get the image from the clipboard), call `paste()`. The image on the clipboard is returned as a Pillow `Image` object.

```
>>> import pyperclipimg as pci
>>> im = pci.paste()  # Get the clipboard image as an Image object.
>>> im.show()  # Display the image on the screen.
```

The `paste()` function depends entirely on Pillow's `ImageGrab.grabclipboard()` function.

Pyperclipimg also has `show()` and `save()` functions as a convennient shortcut for the Pillow functions of the same name:

```
>>> import pyperclipimg as pci
>>> pci.show()  # Display the clipboard's image on the screen.
>>> pci.paste().show()  # (Also displays the clipboard's image on the screen.)

>>> import pyperclipimg as pci
>>> pci.save()  # Saves the clipboard's image with a name like clipboard-2024-12-17_11-10-51-412737.png.
>>> pci.save('foo.png')  # Saves the clipboard's image named foo.png.
>>> pci.save('some_folder')  # Saves the clipboard's image with a name like some_folder/clipboard-2024-12-17_11-10-51-412737.png.
```

**Note**: On Windows, copying an image with transparency makes use of registering PNG as a new clipboard format. This has the following consequences:
- You might not be able to paste it in everywhere you can with a non-transparent image, since supporting custom clipboard formats is up to applications themselves.
- The image won't be displayed in the clipboard history (Win+V).


This module is by Al Sweigart, the creator of pyperclip which copies and pastes text to the clipboard. This module is separate because it has some heavy dependencies (pywin32, Quartz, etc.)
