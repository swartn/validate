"""
directory_tools
===============

This module contains several functions used
throughout the validate package.

.. moduleauthor:: David Fallis
"""

def setdefault(value, newkey, dictionary):
    if newkey not in dictionary:
        dictionary[newkey] = value
