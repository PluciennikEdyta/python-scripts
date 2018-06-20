#!/usr/bin/python

import os
import subprocess

import xlsxwriter


class CommandNotArtifactableException(RuntimeError):
    pass


class NotEnoughCommandParams(RuntimeError):
    pass


class BaseCommand(object):
    should_gather_artifacts = False
    should_return_value = False
    artifacts_path = ''
    command = ''
    command_params = []

    def prepare(self, *args, **kwargs):
        for param in self.command_params:
            if param not in kwargs:
                raise NotEnoughCommandParams("Parameter {} should be passed.".format(param))
        self.command = self.command.format(**kwargs)

    def execute(self, *args, **kwargs):
        # TODO: introduce live streaming output
        output = subprocess.check_output(self.command.split())
        if self.should_return_value:
            return output

    def collect_artifacts(self, *args, **kwargs):
        if not self.should_gather_artifacts:
            raise CommandNotArtifactableException("Command is not set to be artifactable.")

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


class CommandManager(object):
    # TODO
    pass


COMMANDS = {
    'list_permissions': 'adb shell pm list permissions {package_name}',
    'dumps_state': 'adb shell dumpstate > state.logs',
    'kill_app': 'adb -d shell am force-stop {package_name}',
    'take_screenshot': 'adb shell screencap /sdcard/screen.png',
    'save_on_computer': 'adb pull /sdcard/screen.png',
    'install_app': 'adb install {package_name}',
    'uninstall_app': 'adb unistall {package_name}',
    'upgrade_app': 'adb install -r {package_name}',
}
OMIT_DURING_REGULAR_FLOW = ['dumps_state', ]


def _prepare_commands(**kwargs):
    package_name = kwargs.get('package_name')
    tmp_commands = COMMANDS.copy()

    for command in tmp_commands:
        tmp_commands[command] = tmp_commands[command].format(package_name=package_name)

    return tmp_commands


def _execute_cmd(command):
    return subprocess.check_output(command.split())


def _handle_output(output):
    return [o.decode('utf-8') for o in output.split()[2:]]


def flow():
    ROW = 1
    COL = 0
    package_name = input()
    assert package_name
    print("PACKAGE NAME: " + package_name)

    workbook = xlsxwriter.Workbook('Permissions.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, package_name)

    commands = _prepare_commands(package_name=package_name).values()
    for command in commands:
        if command in OMIT_DURING_REGULAR_FLOW:
            continue

        output = _execute_cmd(command)
        result = _handle_output(output)

        for record in result:
            worksheet.write(ROW, COL, record)
            ROW += 1

    workbook.close()
    _execute_cmd(COMMANDS['kill_app'])


if __name__ == "__main__":
    flow()
