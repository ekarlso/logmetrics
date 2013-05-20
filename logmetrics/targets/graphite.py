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
import socket
import calendar
from logmetrics.shell import ParseCommand
from logmetrics.targets import Target


class GraphiteParseCommand(ParseCommand):
    def get_parser(self, prog_name):
        parser = super(GraphiteParseCommand, self).get_parser(prog_name)

        parser.add_argument('--graphite-host', default="127.0.0.1")
        parser.add_argument('--graphite-port', default=2003)

        return parser

    def init_target(self):
        self.target = GraphiteTarget(self.parsed_args.graphite_host,
                                     self.parsed_args.graphite_port)


class GraphiteTarget(Target):
    def __init__(self, host, port):
        self._addr = (host, port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(self._addr)

    def publish(self, metrics):
        for metric in metrics:
            self.send_metric(metric.name, metric.value, metric.timestamp)

    def send_metric(self, name, value, timestamp):
        ts = calendar.timegm(timestamp.timetuple())
        try:
            self._sock.send("%s %g %s\n\n" % (name, value, ts))
        except socket.error, e:
            raise Exception("Failed to send metric: %s", e)
