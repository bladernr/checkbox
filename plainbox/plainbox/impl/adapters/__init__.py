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
:mod:`plainbox.impl.adapters` -- adapter class
==============================================

.. warning::

    THIS MODULE DOES NOT HAVE A STABLE PUBLIC API

Adapters are small utility classes that allow for decentralized conversion of
particular class instances (e.g. particular exceptions) into other form that is
appropriate to a particular use case.

Different adapter objects can be used to convert the same type instance into
different values.  For example the same exception can be adapted into a short
text message, a log record, a piece of data that is displayed in a graphical
application.

All instances of the :class:`Adapter` class can used as function for
transforming objects of particular classes into other objects. For example here
the ``summary`` object will be used as a means to summarize errors.

>>> summary = Adaper()

Particular adapters can be added to a context using a simple decorator. The
decorator is used the same way in all cases, the decorated function must take
one argument called 'obj' and needs to have annotations on both that argument
and the return type. The annotation of the ``obj`` can be any type. The
annotation of the return value must be an Adapter instance.

>>> @adapter
... def _SyntaxError_adapter(obj:SyntaxError) -> summary:
...     return "{filename}:{lineno}: {msg}".format(
...         filename=error.filename, lineno=error.lineno, msg=error.msg)

All Adapter instances are callable. For example, using the summary object, we
can now convert any SyntaxError instance to a short summary message.

>>> summary(SyntaxError(
...     "expected variable", ('job.txt', 12, 156, "something")))
"job.txt:12: expected variable"

This mechanism is polymorphic. An adapter on base type will adapt derived types
as well. An adapter on more specialized derivation overrides adapters for the
the more basic derivation.

This adapter shows how to summarize any object.

>>> @adapter
... def _object_adapter(obj:object) -> summary:
...     return "summary of {}".format(obj)

Using that generic adapter we can now summarize anything:

>>> summary(10)
"summary of 10"

>>> summary("foo")
"summary of foo"
"""


class Adapter:
    """
    Adapter class for converting objects of specific classes into other
    values as defined by the adapter instance itself.
    """

    def __init__(self):
        self._adapter_map = {}

    @property
    def class_list(self):
        return self._adapter_map.keys()

    def _register(self, from_cls, func):
        self._adapter_map[from_cls] = func

    def __call__(self, obj):
        cls_list = type(obj).__mro__
        for cls in cls_list:
            if cls in self._adapter_map:
                return self._adapter_map[cls](obj)
        raise TypeError("no adapter for {0}".format(cls_list[0]))


def adapter(func):
    """
    Decorator for adapter functions
    """
    if 'obj' not in func.__annotations__:
        raise TypeError("obj type annotation not specified")
    from_cls = func.__annotations__['obj']
    if 'return' not in func.__annotations__:
        raise TypeError("return type annotation not specified")
    to_adapter = func.__annotations__['return']
    if not isinstance(to_adapter, Adapter):
        raise TypeError("return type annotation must be an Adapter instance")
    to_adapter._register(from_cls, func)
