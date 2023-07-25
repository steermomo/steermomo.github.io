from pelican import signals
from .gallery import Gallery


def get_generators(pelican_object):
    # define a new generator here if you need to
    return Gallery


def register():
    signals.get_generators.connect(get_generators)
