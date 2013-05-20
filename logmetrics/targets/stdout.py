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
from logmetrics.shell import ParseCommand
from logmetrics.targets import Target


class StdoutParseCommand(ParseCommand):
    def init_target(self):
        self.target = StdoutTarget()


class StdoutTarget(Target):
    def publish(self, metrics):
        for metric in metrics:
            print('%s: %s %s (%s)' % (
                metric.name,
                metric.value,
                metric.units,
                metric.timestamp,
            ))
