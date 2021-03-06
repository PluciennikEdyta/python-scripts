#!/usr/bin/python
import sys
sys.path.append("..")

import logging
import subprocess

import xlsxwriter

from permissions.utils import setup_logging

logger = logging.getLogger(__name__)


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
    setup_logging()

    logger.info("===== | PERMISSION START | =====")
    flow()
    logger.info("===== | PERMISSION END | =====")
