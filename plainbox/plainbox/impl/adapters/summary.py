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
:mod:`plainbox.impl.adapters.summary` -- summarizing adapter
============================================================

This module contains a summarizing adapter. Is main intent is to handle all
kinds of error cases and convert them to one-line short summaries that can be
printed and remain sensibly human-friendly.
"""

from requests.exceptions import ConnectionError, InvalidSchema, HTTPError

from plainbox.impl.adapters import Adapter, adapter


summary = Adapter()


@adapter
def _InvalidSchema_summary(obj: InvalidSchema) -> summary:
    return "Invalid destination URL: {0}".format(obj)


@adapter
def _ConnectionError_Summary(obj: ConnectionError) -> summary:
    return "Unable to connect to destination URL: {0}".format(obj)


@adapter
def _HttpError_summary(obj: HTTPError) -> summary:
    return ("Server returned an error when "
            "receiving or processing: {0}").format(obj)


@adapter
def _IOError_summary(obj: IOError) -> summary:
    return "Problem reading a file: {0}".format(obj)
