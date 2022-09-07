import os
from os.path import join
import logging

def get_thumb(settings, filename):
    """Return the path to the thumb.

    examples:
    >>> default_settings = create_settings()
    >>> get_thumb(default_settings, "bar/foo.jpg")
    "bar/thumbnails/foo.jpg"
    >>> get_thumb(default_settings, "bar/foo.png")
    "bar/thumbnails/foo.png"

    for videos, it returns a jpg file:
    >>> get_thumb(default_settings, "bar/foo.webm")
    "bar/thumbnails/foo.jpg"
    """

    path, filename = os.path.split(filename)
    logging.info(f'Path & filename is {path} & {filename}')
    name, ext = os.path.splitext(filename)

    if ext.lower() in settings['GALLERY_V_EXT']:
        ext = '.jpg'
    return join(path, settings['GALLERY_THUMB_DIR'], settings['GALLERY_THUMB_PREFIX'] +
                name + settings['GALLERY_THUMB_SUFFIX'] + ext)

class Status:
    SUCCESS = 0
    FAILURE = 1