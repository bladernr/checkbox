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
from checkbox.plugin import Plugin


class ManualTest(Plugin):

    def register(self, manager):
        super(ManualTest, self).register(manager)

        # Manual tests should be asked first.
        self._manager.reactor.call_on("prompt-test-manual",
            self.prompt_test_manual)

    def prompt_test_manual(self, interface, test):
        interface.show_test(test)


factory = ManualTest