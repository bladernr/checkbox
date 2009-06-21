#
# This file is part of Checkbox.
#
# Copyright 2008 Canonical Ltd.
#
# Checkbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Checkbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Checkbox.  If not, see <http://www.gnu.org/licenses/>.
#
from checkbox.lib.environ import add_variable, get_variable

from checkbox.properties import String
from checkbox.plugin import Plugin


class ProxyInfo(Plugin):

    # HTTP proxy to use instead of the one specified in environment.
    http_proxy = String(required=False)

    # HTTPS proxy to use instead of the one specified in environment.
    https_proxy = String(required=False)

    def register(self, manager):
        super(ProxyInfo, self).register(manager)
        self._manager.reactor.call_on("gather", self.gather, -1000)

    def gather(self):
        # Config has lowest precedence
        http_proxy = self.http_proxy
        https_proxy = self.https_proxy

        # Gconf has higher precedence
        gconf = self._manager.registry.gconf
        if gconf.system.http_proxy.use_http_proxy:
            if gconf.system.http_proxy.use_authentication:
                http_proxy = "http://%s:%s@%s:%s" % (
                    gconf.system.http_proxy.authentication_user,
                    gconf.system.http_proxy.authentication_password,
                    gconf.system.http_proxy.host,
                    gconf.system.http_proxy.port)
            elif gconf.system.http_proxy.host:
                http_proxy = "http://%s:%s" % (
                    gconf.system.http_proxy.host,
                    gconf.system.http_proxy.port)

            if gconf.system.http_proxy.use_same_proxy:
                https_proxy = http_proxy
            elif gconf.system.proxy.secure_host:
                https_proxy = "https://%s:%s" % (
                    gconf.system.proxy.secure_host,
                    gconf.system.proxy.secure_port)

        # Environment has highest precedence
        http_proxy = get_variable("http_proxy", http_proxy):
        https_proxy = get_variable("https_proxy", https_proxy):

        add_variable("http_proxy", http_proxy)
        add_variable("https_proxy", https_proxy)


factory = ProxyInfo
