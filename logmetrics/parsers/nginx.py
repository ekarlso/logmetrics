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
import re
from logmetrics.metric import Metric
from logmetrics.parsers import Parser


class NginxStatusParser(Parser):
    REGEX = re.compile('.*HTTP/1.\d" (?P<http_status_code>\d{3}) .*')

    def __init__(self):
        super(NginxStatusParser, self).__init__()

        self.http_1xx = 0

        self.http_2xx = 0
        self.http_200 = 0
        self.http_201 = 0
        self.http_202 = 0
        self.http_203 = 0
        self.http_204 = 0

        self.http_3xx = 0

        self.http_4xx = 0
        self.http_400 = 0
        self.http_401 = 0
        self.http_403 = 0
        self.http_404 = 0
        self.http_405 = 0
        self.http_406 = 0
        self.http_408 = 0
        self.http_409 = 0
        self.http_413 = 0

        self.http_5xx = 0
        self.http_500 = 0
        self.http_501 = 0
        self.http_502 = 0
        self.http_503 = 0
        self.http_504 = 0

    def parse_line(self, line):
        try:
            # Apply regular expression to each line and extract interesting
            # fields
            regMatch = self.REGEX.match(line)

            if regMatch:
                linebits = regMatch.groupdict()
                status = int(linebits['http_status_code'])

                # Outer if/else buckets the lines into smaller groups
                # Inner if/else checks the specific status code

                if (status < 100):
                    # HTTP 000 -> 099
                    pass
                elif (status < 200):
                    # HTTP 100 -> 199
                    self.http_1xx += 1
                elif (status < 300):
                    # HTTP 200 -> 299
                    if status == 200:
                        self.http_200 += 1
                    elif status == 201:
                        self.http_201 += 1
                    elif status == 202:
                        self.http_202 += 1
                    elif status == 203:
                        self.http_203 += 1
                    elif status == 204:
                        self.http_204 += 1
                    else:
                        self.http_2xx += 1
                elif (status < 400):
                    # HTTP 300 -> 399
                    self.http_3xx += 1
                elif (status < 500):
                    # HTTP 400 -> 499
                    if status == 400:
                        self.http_400 += 1
                    elif status == 401:
                        self.http_401 += 1
                    elif status == 403:
                        self.http_403 += 1
                    elif status == 404:
                        self.http_404 += 1
                    elif status == 405:
                        self.http_405 += 1
                    elif status == 406:
                        self.http_406 += 1
                    elif status == 408:
                        self.http_408 += 1
                    elif status == 409:
                        self.http_409 += 1
                    elif status == 413:
                        self.http_413 += 1
                    else:
                        self.http_4xx += 1
                else:
                    # HTTP 500+
                    if status == 500:
                        self.http_500 += 1
                    elif status == 501:
                        self.http_501 += 1
                    elif status == 502:
                        self.http_502 += 1
                    elif status == 503:
                        self.http_503 += 1
                    elif status == 504:
                        self.http_504 += 1
                    else:
                        self.http_5xx += 1

            else:
                raise Exception("regmatch failed to match")

        except Exception, e:
            raise Exception("regmatch or contents failed with %s" % e)

    def get_state(self, duration):
        return [
            Metric("http_1xx", self.http_1xx, "Response Count"),

            Metric("http_2xx", self.http_2xx, "Response Count"),
            Metric("http_200", self.http_200, "Response Count"),
            Metric("http_201", self.http_201, "Response Count"),
            Metric("http_202", self.http_202, "Response Count"),
            Metric("http_203", self.http_203, "Response Count"),
            Metric("http_204", self.http_204, "Response Count"),

            Metric("http_3xx", self.http_3xx, "Response Count"),

            Metric("http_4xx", self.http_4xx, "Response Count"),
            Metric("http_400", self.http_400, "Response Count"),
            Metric("http_401", self.http_401, "Response Count"),
            Metric("http_403", self.http_403, "Response Count"),
            Metric("http_404", self.http_404, "Response Count"),
            Metric("http_405", self.http_405, "Response Count"),
            Metric("http_406", self.http_406, "Response Count"),
            Metric("http_408", self.http_408, "Response Count"),
            Metric("http_409", self.http_409, "Response Count"),
            Metric("http_413", self.http_413, "Response Count"),

            Metric("http_5xx", self.http_5xx, "Response Count"),
            Metric("http_500", self.http_500, "Response Count"),
            Metric("http_501", self.http_501, "Response Count"),
            Metric("http_502", self.http_502, "Response Count"),
            Metric("http_503", self.http_503, "Response Count"),
            Metric("http_504", self.http_504, "Response Count"),
        ]
