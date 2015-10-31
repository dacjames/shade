# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import keystoneauth1.exceptions
import os_client_config
import pbr.version

# Disable the Rackspace warnings about deprecated certificates. We are aware
import warnings
try:
    from requests.packages.urllib3.exceptions import SubjectAltNameWarning
except ImportError:
    try:
        from urllib3.exceptions import SubjectAltNameWarning
    except ImportError:
        SubjectAltNameWarning = None

if SubjectAltNameWarning:
    warnings.filterwarnings('ignore', category=SubjectAltNameWarning)

from shade.exc import *  # noqa
from shade.openstackcloud import OpenStackCloud
from shade.operatorcloud import OperatorCloud
from shade import _log


__version__ = pbr.version.VersionInfo('shade').version_string()


def simple_logging(debug=False):
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    log = _log.setup_logging('shade')
    log.addHandler(logging.StreamHandler())
    log.setLevel(log_level)
    # Suppress warning about keystoneauth loggers
    log = _log.setup_logging('keystoneauth.identity.base')


def openstack_clouds(config=None, debug=False):
    if not config:
        config = os_client_config.OpenStackConfig()
    try:
        return [
            OpenStackCloud(
                cloud=f.name, debug=debug,
                cloud_config=f,
                **f.config)
            for f in config.get_all_clouds()
        ]
    except keystoneauth1.exceptions.auth_plugins.NoMatchingPlugin as e:
        raise OpenStackCloudException(
            "Invalid cloud configuration: {exc}".format(exc=str(e)))


def openstack_cloud(config=None, **kwargs):
    if not config:
        config = os_client_config.OpenStackConfig()
    try:
        cloud_config = config.get_one_cloud(**kwargs)
    except keystoneauth1.exceptions.auth_plugins.NoMatchingPlugin as e:
        raise OpenStackCloudException(
            "Invalid cloud configuration: {exc}".format(exc=str(e)))
    return OpenStackCloud(cloud_config=cloud_config)


def operator_cloud(config=None, **kwargs):
    if 'interface' not in kwargs:
        kwargs['interface'] = 'admin'
    if not config:
        config = os_client_config.OpenStackConfig()
    try:
        cloud_config = config.get_one_cloud(**kwargs)
    except keystoneauth1.exceptions.auth_plugins.NoMatchingPlugin as e:
        raise OpenStackCloudException(
            "Invalid cloud configuration: {exc}".format(exc=str(e)))
    return OperatorCloud(cloud_config=cloud_config)
