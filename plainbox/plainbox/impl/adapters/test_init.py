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
plainbox.impl.adapters.test_init
================================

Test definitions for plainbox.impl.adapters module
"""

from unittest import TestCase

from plainbox.impl.adapters import Adapter, adapter


class AdapterTests(TestCase):

    def test_smoke(self):
        summary = Adapter()

        @adapter
        def SyntaxError_summary(obj: SyntaxError) -> summary:
            return obj.msg

        @adapter
        def ValueError_summary(obj: ValueError) -> summary:
            return str(obj)

        self.assertEqual(summary(SyntaxError("message")), "message")
        self.assertEqual(summary(ValueError("other message")), "other message")

    def test_polymorphism(self):
        some_adapter = Adapter()

        @adapter
        def _obj(obj: object) -> some_adapter:
            return 1

        @adapter
        def _exception(obj: Exception) -> some_adapter:
            return 2

        @adapter
        def _value_error(obj: ValueError) -> some_adapter:
            return 3
        # The adapters work when invoked directly
        self.assertEqual(some_adapter(object()), 1)
        self.assertEqual(some_adapter(Exception()), 2)
        self.assertEqual(some_adapter(ValueError()), 3)
        # Adapters also pick other objects of derived classes
        # str is an object so we get 1
        self.assertEqual(some_adapter("foo"), 1)
        # IOError is an Exception so we get 2
        self.assertEqual(some_adapter(IOError()), 2)
        # custom error is a ValueError so we get 3

        class CustomError(ValueError):
            pass
        self.assertEqual(some_adapter(CustomError()), 3)

    def test_no_adapter_for_type(self):
        some_adapter = Adapter()
        with self.assertRaises(TypeError) as call:
            some_adapter("foo")
        self.assertEqual(str(call.exception), "no adapter for <class 'str'>")

    def test_missing_obj_annotation(self):
        with self.assertRaises(TypeError) as call:
            @adapter
            def foo(obj):
                pass
        self.assertEqual(
            str(call.exception), "obj type annotation not specified")

    def test_missing_return_annotation(self):
        with self.assertRaises(TypeError) as call:
            @adapter
            def foo(obj: object):
                pass
        self.assertEqual(
            str(call.exception), "return type annotation not specified")

    def test_wrong_return_annotation(self):
        with self.assertRaises(TypeError) as call:
            @adapter
            def foo(obj: object) -> object:
                pass
        self.assertEqual(
            str(call.exception),
            "return type annotation must be an Adapter instance")
