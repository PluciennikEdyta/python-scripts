#!/usr/bin/python
from __future__ import unicode_literals

import logging
import os
import subprocess

from permissions import exceptions
from permissions.utils import log

logger = logging.getLogger(__name__)


class BaseCommand(object):
    command = ''
    command_params = []
    artifacts_path = ''
    should_gather_artifacts = False
    should_return_value = False
    should_stream_output = False

    @log(logger)
    def prepare(self, *args, **kwargs):
        for param in self.command_params:
            if param not in kwargs:
                raise exceptions.NotEnoughCommandParams(
                    "Parameter `{}` should be passed.".format(param)
                )
        self.command = self.command.format(**kwargs)

    @log(logger)
    def execute(self, dry_run=False, **kwargs):
        if dry_run:
            return

        output = []

        proc = subprocess.Popen(self.command.split(), stdout=subprocess.PIPE, bufsize=1)
        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                output.append(line)

                if self.should_stream_output:
                    print line,

        proc.wait()

        if self.should_return_value:
            return ''.join(output)

    @log(logger)
    def collect_artifacts(self, *args, **kwargs):
        if not self.should_gather_artifacts:
            raise exceptions.CommandNotArtifactableException(
                "Command is not set to be artifactable."
            )

    @log(logger)
    def clean(self, *args, **kwargs):
        raise NotImplementedError()


class ListPermissionsCommand(BaseCommand):
    command = 'adb shell pm list permissions {package_name}'
    command_params = ['package_name', ]
    artifacts_path = os.getcwd()
    should_gather_artifacts = True
    should_return_value = True


class DumpsStateCommand(BaseCommand):
    command = 'adb shell dumpstate > state.logs'


class KillAppCommand(BaseCommand):
    command = 'adb -d shell am force-stop {package_name}'
    command_params = ['package_name', ]


class TakeScreenshotCommand(BaseCommand):
    command = 'adb shell screencap {path}'
    command_params = ['path', ]


class RecordScreenCommand(BaseCommand):
    command = 'adb shell screenrecord {path}'
    command_params = ['path', ]


class KillallCommand(BaseCommand):
    command = 'killall {process_name}'
    command_params = ['process_name', ]


class SaveOnComputerCommand(BaseCommand):
    command = 'adb pull {path}'
    command_params = ['path', ]


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
    should_stream_output = True


class DummyCommand(BaseCommand):
    command = 'echo Dummy'
