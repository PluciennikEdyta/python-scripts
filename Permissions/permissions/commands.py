#!/usr/bin/python
from __future__ import unicode_literals

import logging
import os
import subprocess

from permissions.exceptions import NotEnoughCommandParams, CommandNotArtifactableException
from permissions.utils import log_debug

logger = logging.getLogger(__name__)


class BaseCommand(object):
    should_gather_artifacts = False
    should_return_value = False
    artifacts_path = ''
    command = ''
    command_params = []

    @log_debug(logger)
    def prepare(self, *args, **kwargs):
        for param in self.command_params:
            if param not in kwargs:
                raise NotEnoughCommandParams("Parameter {} should be passed.".format(param))
        self.command = self.command.format(**kwargs)

    @log_debug(logger)
    def execute(self, *args, **kwargs):
        # TODO: introduce live streaming output
        output = subprocess.check_output(self.command.split())
        if self.should_return_value:
            return output

    @log_debug(logger)
    def collect_artifacts(self, *args, **kwargs):
        if not self.should_gather_artifacts:
            raise CommandNotArtifactableException("Command is not set to be artifactable.")

    @log_debug(logger)
    def clean(self, *args, **kwargs):
        raise NotImplementedError()


class ListPermissionsCommand(BaseCommand):
    should_gather_artifacts = True
    should_return_value = True
    artifacts_path = os.getcwd()
    command = 'adb shell pm list permissions {package_name}'
    command_params = ['package_name', ]


class DumpsStateCommand(BaseCommand):
    command = 'adb shell dumpstate > state.logs'


class KillAppCommand(BaseCommand):
    command = 'adb -d shell am force-stop {package_name}'
    command_params = ['package_name', ]


class TakeScreenshotCommand(BaseCommand):
    command = 'adb shell screencap /sdcard/screen.png'


class SaveOnComputerCommand(BaseCommand):
    command = 'adb pull /sdcard/screen.png'


class InstallAppCommand(BaseCommand):
    command = 'adb install {package_name}'
    command_params = ['package_name', ]


class UninstallAppCommand(BaseCommand):
    command = 'adb unistall {package_name}'
    command_params = ['package_name', ]


class UpgradeAppCommand(BaseCommand):
    command = 'adb install -r {package_name}'
    command_params = ['package_name', ]


class CountedPingCommand(BaseCommand):
    """
    Example of usage:

    p = CountedPingCommand()
    p.prepare(host='www.google.com', count=3)
    print p.execute()
    """

    command = 'ping {host} -c {count}'
    command_params = ['host', 'count', ]
    should_return_value = True


class DummyCommand(BaseCommand):
    command = 'echo Dummy'


class CommandManager(object):
    # TODO
    pass
