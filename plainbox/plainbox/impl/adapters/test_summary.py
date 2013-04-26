# This file is part of Checkbox.
#
# Copyright 2013 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
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

"""
plainbox.impl.adapters.test_summary
===================================

Test definitions for plainbox.impl.adapters.summary module
"""

from unittest import TestCase

from requests.exceptions import ConnectionError, InvalidSchema, HTTPError

from plainbox.impl.adapters.summary import summary


class SummaryTests(TestCase):

    def test_invalid_schema(self):
        self.assertEqual(
            summary(InvalidSchema("message")),
            "Invalid destination URL: message")

    def test_connection_error(self):
        self.assertEqual(
            summary(ConnectionError("message")),
            "Unable to connect to destination URL: message")

    def test_http_error(self):
        self.assertEqual(
            summary(HTTPError("message")),
            "Server returned an error when receiving or processing: message")
