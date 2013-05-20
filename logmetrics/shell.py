# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Author: Kiall Mac Innes <kiall@hp.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import abc
import logging
from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager
from pygtail import Pygtail
from stevedore.driver import DriverManager
from logmetrics.version import version_info as version


class LogmetricsShell(App):
    CONSOLE_MESSAGE_FORMAT = '%(levelname)s: %(message)s'

    def __init__(self):
        super(LogmetricsShell, self).__init__(
            description='Log Metrics',
            version=version.version_string(),
            command_manager=CommandManager('logmetrics.cli'),
        )

        self.log = logging.getLogger(__name__)


class ParseCommand(Command):
    __metaclass__ = abc.ABCMeta

    def get_parser(self, prog_name):
        parser = super(ParseCommand, self).get_parser(prog_name)

        parser.add_argument('logfile', help="Logfile to parse")
        parser.add_argument('--offset-file', help="")
        parser.add_argument('--parser', help="", required=True)

        return parser

    def take_action(self, parsed_args):
        self.parsed_args = parsed_args

        self.init_parser()
        self.init_target()

        self.process_file()
        self.send_metrics()

    def init_parser(self):
        manager = DriverManager('logmetrics.parser',
                                self.parsed_args.parser)

        self.parser = manager.driver()

    def process_file(self):
        pygtail = Pygtail(self.parsed_args.logfile,
                          offset_file=self.parsed_args.offset_file)

        for line in pygtail:
            try:
                self.parser.parse_line(line)
            except Exception, e:
                self.app.log.warn(e)

    @abc.abstractmethod
    def init_target(self):
        pass

    def send_metrics(self):
        metrics = self.parser.get_state(0)

        self.target.publish(metrics)

