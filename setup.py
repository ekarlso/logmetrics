#!/usr/bin/env python
# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
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
import textwrap
from setuptools import setup, find_packages
from logmetrics.openstack.common import setup as common_setup

install_requires = common_setup.parse_requirements(['tools/pip-requires'])
tests_require = common_setup.parse_requirements(['tools/test-requires'])
setup_require = common_setup.parse_requirements(['tools/setup-requires'])
dependency_links = common_setup.parse_dependency_links([
    'tools/pip-requires',
    'tools/test-requires',
    'tools/setup-requires'
])

setup(
    name='logmetrics',
    version=common_setup.get_version('logmetrics'),
    description='Generate Metrics from Logs',
    author='Kiall Mac Innes',
    author_email='kiall@hp.com',
    url='',
    packages=find_packages(exclude=['bin']),
    include_package_data=True,
    test_suite='nose.collector',
    setup_requires=setup_require,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    dependency_links=dependency_links,
    scripts=[
        'bin/logmetrics',
    ],
    cmdclass=common_setup.get_cmdclass(),
    entry_points=textwrap.dedent("""
        [logmetrics.cli]
        parse = logmetrics.shell:ParseCommand

        [logmetrics.parser]
        nginx-status = logmetrics.parsers.nginx:NginxStatusParser

        [logmetrics.target]
        stdout = logmetrics.targets.stdout:StdoutTarget
        """),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
    ],
)
