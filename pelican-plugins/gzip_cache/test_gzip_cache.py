# -*- coding: utf-8 -*-
"""Core plugins unit tests"""

import os
import tempfile
import time
import unittest
from contextlib import contextmanager
from hashlib import md5
from shutil import rmtree
from tempfile import mkdtemp

import gzip_cache


@contextmanager
def temporary_folder():
    """creates a temporary folder, return it and delete it afterwards.

    This allows to do something like this in tests:

        >>> with temporary_folder() as d:
            # do whatever you want
    """
    tempdir = mkdtemp()
    try:
        yield tempdir
    finally:
        rmtree(tempdir)


class TestGzipCache(unittest.TestCase):
    def test_should_compress(self):
        # Some filetypes should compress and others shouldn't.
        self.assertTrue(gzip_cache.should_compress("foo.html"))
        self.assertTrue(gzip_cache.should_compress("bar.css"))
        self.assertTrue(gzip_cache.should_compress("baz.js"))
        self.assertTrue(gzip_cache.should_compress("foo.txt"))

        self.assertFalse(gzip_cache.should_compress("foo.gz"))
        self.assertFalse(gzip_cache.should_compress("bar.png"))
        self.assertFalse(gzip_cache.should_compress("baz.mp3"))
        self.assertFalse(gzip_cache.should_compress("foo.mov"))

    def test_should_overwrite(self):
        # Default to false if GZIP_CACHE_OVERWRITE is not set
        settings = {}
        self.assertFalse(gzip_cache.should_overwrite(settings))
        settings = {"GZIP_CACHE_OVERWRITE": False}
        self.assertFalse(gzip_cache.should_overwrite(settings))
        settings = {"GZIP_CACHE_OVERWRITE": True}
        self.assertTrue(gzip_cache.should_overwrite(settings))

    def test_creates_gzip_file(self):
        # A file matching the input filename with a .gz extension is created.

        # The plugin walks over the output content after the finalized signal
        # so it is safe to assume that the file exists (otherwise walk would
        # not report it). Therefore, create a dummy file to use.
        with temporary_folder() as tempdir:
            _, a_html_filename = tempfile.mkstemp(suffix=".html", dir=tempdir)
            gzip_cache.create_gzip_file(a_html_filename, False)
            self.assertTrue(os.path.exists(a_html_filename + ".gz"))

    def test_creates_same_gzip_file(self):
        # Should create the same gzip file from the same contents.

        # gzip will create a slightly different file because it includes
        # a timestamp in the compressed file by default. This can cause
        # problems for some caching strategies.
        with temporary_folder() as tempdir:
            _, a_html_filename = tempfile.mkstemp(suffix=".html", dir=tempdir)
            a_gz_filename = a_html_filename + ".gz"
            gzip_cache.create_gzip_file(a_html_filename, False)
            gzip_hash = get_md5(a_gz_filename)
            time.sleep(1)
            gzip_cache.create_gzip_file(a_html_filename, False)
            self.assertEqual(gzip_hash, get_md5(a_gz_filename))

    def test_overwrites_gzip_file(self):
        # A file matching the input filename with a .gz extension is not created.

        # The plugin walks over the output content after the finalized signal
        # so it is safe to assume that the file exists (otherwise walk would
        # not report it). Therefore, create a dummy file to use.
        with temporary_folder() as tempdir:
            _, a_html_filename = tempfile.mkstemp(suffix=".html", dir=tempdir)
            gzip_cache.create_gzip_file(a_html_filename, True)
            self.assertFalse(os.path.exists(a_html_filename + ".gz"))


def get_md5(filepath):
    with open(filepath, "rb") as fh:
        return md5(fh.read()).hexdigest()
