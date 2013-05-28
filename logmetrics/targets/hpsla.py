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
import os
import socket
import calendar
from maasclient import exceptions
from maasclient.v1 import Client as MaasClient
from maasclient.v1.metrics import Metric as MaasMetric
from logmetrics.shell import ParseCommand
from logmetrics.targets import Target


class HpslaParseCommand(ParseCommand):
    def get_parser(self, prog_name):
        parser = super(HpslaParseCommand, self).get_parser(prog_name)

        parser.add_argument('--namespace', required=True)
        parser.add_argument('--region', required=True)
        parser.add_argument('--az', type=int, required=True)
        parser.add_argument('--hostname', default=socket.gethostname())


        parser.add_argument('--os-endpoint',
                            default=os.environ.get('OS_MON_ENDPOINT'),
                            help="Defaults to env[OS_MON_ENDPOINT]")

        parser.add_argument('--os-auth-url',
                            default=os.environ.get('OS_AUTH_URL'),
                            help="Defaults to env[OS_AUTH_URL]")

        parser.add_argument('--os-username',
                            default=os.environ.get('OS_USERNAME'),
                            help="Defaults to env[OS_USERNAME]")

        parser.add_argument('--os-password',
                            default=os.environ.get('OS_PASSWORD'),
                            help="Defaults to env[OS_PASSWORD]")

        parser.add_argument('--os-tenant-id',
                            default=os.environ.get('OS_TENANT_ID'),
                            help="Defaults to env[OS_TENANT_ID]")

        parser.add_argument('--os-tenant-name',
                            default=os.environ.get('OS_TENANT_NAME'),
                            help="Defaults to env[OS_TENANT_NAME]")

        parser.add_argument('--os-token',
                            default=os.environ.get('OS_SERVICE_TOKEN'),
                            help="Defaults to env[OS_SERVICE_TOKEN]")

        parser.add_argument('--os-service-type',
                            default=os.environ.get('OS_MON_SERVICE_TYPE',
                                                   'hpext:monitoring'),
                            help=("Defaults to env[OS_MON_SERVICE_TYPE], or "
                                  "'hpext:monitoring'"))

        parser.add_argument('--os-region-name',
                            default=os.environ.get('OS_REGION_NAME'),
                            help="Defaults to env[OS_REGION_NAME]")

        return parser

    def init_target(self):
        maasclient_args = {
            'endpoint': self.parsed_args.os_endpoint,
            'auth_url': self.parsed_args.os_auth_url,
            'username': self.parsed_args.os_username,
            'password': self.parsed_args.os_password,
            'tenant_id': self.parsed_args.os_tenant_id,
            'tenant_name': self.parsed_args.os_tenant_name,
            'token': self.parsed_args.os_token,
            'service_type': self.parsed_args.os_service_type,
            'region_name': self.parsed_args.os_region_name
        }

        self.target = HpslaTarget(maasclient_args,
                                  self.parsed_args.namespace,
                                  self.parsed_args.region,
                                  self.parsed_args.az,
                                  self.parsed_args.hostname)


class HpslaTarget(Target):
    def __init__(self, maasclient_args, namespace, region, az, hostname):
        self.maasclient_args = maasclient_args
        self._client = None
        self.namespace = namespace
        self.region = region
        self.az = az
        self.hostname = hostname

    @property
    def client(self):
        if not self._client:
            self._client = MaasClient(**self.maasclient_args)

        return self._client

    def publish(self, metrics):
        time_values = []

        for metric in metrics:
            timestamp = calendar.timegm(metric.timestamp.timetuple())
            time_values.append([timestamp, metric.value])

        print time_values

    def publish(self, metrics):
        for metric in metrics:
            try:
                self.send_metric(metric.name, metric.value, metric.timestamp)
            except Exception, e:
                print "Failed to send metric: %r" % e


    def send_metric(self, name, value, timestamp):
        metric = MaasMetric(**{
            'namespace': self.namespace,
            'type': name,
            'timestamp': calendar.timegm(timestamp.timetuple()),
            'value': value,
            'dimensions': {
                'sla': 'sla',
                'region': self.region,
                'az': self.az,
                'hostname': self.hostname
            }
        })

        self.client.metrics.create(metric)
