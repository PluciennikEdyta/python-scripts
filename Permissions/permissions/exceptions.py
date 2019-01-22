#!/usr/bin/python
from __future__ import unicode_literals


# Command runtime errors

class CommandNotArtifactableException(RuntimeError):
    pass


class NotEnoughCommandParams(RuntimeError):
    pass


# Manager runtime errors

class NoCommandSetException(RuntimeError):
    pass


class NotACommandException(RuntimeError):
    pass
