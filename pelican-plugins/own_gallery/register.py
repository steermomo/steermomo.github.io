from pelican import signals

from .gallery import StaticGalleryGenerator


def get_generators(pelican_object):
    # define a new generator here if you need to
    return StaticGalleryGenerator


def register():
    signals.get_generators.connect(get_generators)
