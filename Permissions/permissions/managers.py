from commands import BaseCommand
from permissions import exceptions


class CommandManager(object):
    """
    A simple command manager that makes it easy to execute command
    without getting into its definition, just based on a knowledge
    that each command needs parameters. So basically, you need to
    know what parameters the command is expecting and pass it into
    `set_parameters` method. But even if you don't, meaningful
    exceptions will be raised.

    Example of usage:

    cm = CommandManager()
    cm.set_command(CountedPingCommand())
    cm.set_parameters(host='www.google.com', count=3)
    cm.run()
    """

    def __init__(self):
        self._command = None
        self._parameters = dict()

    def set_command(self, command):
        if not isinstance(command, BaseCommand):
            raise exceptions.NotACommandException("Command should be an instance of BaseCommand.")

        self._command = command

    def set_parameters(self, **params):
        self._parameters = params

    def run(self, dry_run=False):
        if not self._command:
            raise exceptions.NoCommandSetException("You should set_command first.")

        self._command.prepare(**self._parameters)
        self._command.execute(dry_run=dry_run)
