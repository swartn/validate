"""
decorators
===============

This module is contains some decorators used in validate
"""
import contextlib
import sys
import cStringIO


class NoWriteFile(object):
    def write(self, x):
        pass

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = NoWriteFile()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

def silence(function):
    def wrapper(*args, **kwargs):
        with nostdout():
           return function(*args, **kwargs)
    return wrapper
