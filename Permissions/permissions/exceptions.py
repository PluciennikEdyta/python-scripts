#!/usr/bin/python
from __future__ import unicode_literals


class CommandNotArtifactableException(RuntimeError):
    pass


class NotEnoughCommandParams(RuntimeError):
    pass