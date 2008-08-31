#
# Copyright (c) 2008 Canonical
#
# Written by Marc Tardif <marc@interunion.ca>
#
# This file is part of Checkbox.
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
import re
import sys
import termios

from gettext import gettext as _

from checkbox.result import Result, PASS, FAIL, SKIP
from checkbox.test import ALL_CATEGORIES
from checkbox.user_interface import UserInterface


class CLIDialog(object):
    """Command line dialog wrapper."""

    def __init__(self, heading, text):
        self.heading = heading
        self.text = text
        self.visible = False

    def put(self, text):
        sys.stdout.write(text)

    def put_line(self, line):
        self.put("%s\n" % line)

    def put_newline(self):
        self.put("\n")

    def get(self, label=None, limit=1, separator=termios.CEOT):
        if label is not None:
            self.put(label)

        fileno = sys.stdin.fileno()
        saved_attributes = termios.tcgetattr(fileno)
        attributes = termios.tcgetattr(fileno)
        attributes[3] = attributes[3] & ~(termios.ICANON | termios.ECHO)
        attributes[6][termios.VMIN] = 1
        attributes[6][termios.VTIME] = 0
        termios.tcsetattr(fileno, termios.TCSANOW, attributes)

        input = []
        escape = 0
        try:
            while len(input) < limit:
                ch = str(sys.stdin.read(1))
                if ord(ch) == separator:
                    break
                elif ord(ch) == 033: # ESC
                    escape = 1
                elif ord(ch) == termios.CERASE or ord(ch) == 010:
                    if len(input):
                        self.put("\010 \010")
                        del input[-1]
                elif ord(ch) == termios.CKILL:
                    self.put("\010 \010" * len(input))
                    input = []
                else:
                    if not escape:
                        input.append(ch)
                        self.put(ch)
                    elif escape == 1:
                        if ch == "[":
                            escape = 2
                        else:
                            escape = 0
                    elif escape == 2:
                        escape = 0 
        finally:
            termios.tcsetattr(fileno, termios.TCSANOW, saved_attributes)

        self.put_newline()
        return "".join(input)

    def show(self):
        self.visible = True
        self.put_newline()
        self.put_line("*** %s" % self.heading)
        self.put_newline()
        self.put_line(self.text)


class CLIChoiceDialog(CLIDialog):

    def __init__(self, heading, text):
        super(CLIChoiceDialog, self).__init__(heading, text)
        self.keys = []
        self.buttons = []

    def run(self, label=None):
        if not self.visible:
            self.show()

        self.put_newline()
        try:
            # Only one button
            if len (self.keys) <= 1:
                self.get(_("Press any key to continue..."))
                return 0
            # Multiple choices
            while True:
                if label is not None:
                    self.put_line(label)
                for index, button in enumerate(self.buttons):
                    self.put_line("  %s: %s" % (self.keys[index], button))

                response = self.get(_("Please choose (%s): ") % ("/".join(self.keys)))
                try:
                    return self.keys.index(response[0].upper()) + 1
                except ValueError:
                    pass
        except KeyboardInterrupt:
            self.put_newline()
            sys.exit(1)

    def add_button(self, button):
        self.keys.append(re.search("&(.)", button).group(1).upper())
        self.buttons.append(re.sub("&", "", button))
        return len(self.keys)


class CLITextDialog(CLIDialog):

    limit = 255
    separator = termios.CEOT

    def run(self, label=None):
        if not self.visible:
            self.show()

        self.put_newline()
        try:
            response = self.get(label, self.limit, self.separator)
            return response
        except KeyboardInterrupt:
            self.put_newline()
            sys.exit(1)


class CLILineDialog(CLITextDialog):

    limit = 80
    separator = ord("\n")


class CLIProgressDialog(CLIDialog):
    """Command line progress dialog wrapper."""

    def __init__(self, heading, text):
        super(CLIProgressDialog, self).__init__(heading, text)
        self.progress_count = 0

    def set(self, progress=None):
        self.progress_count = (self.progress_count + 1) % 5
        if self.progress_count:
            return

        if progress != None:
            self.put("\r%u%%" % (progress * 100))
        else:
            self.put(".")
        sys.stdout.flush()


class CLIInterface(UserInterface):

    def show_wait(self, message, function, *args, **kwargs):
        title = _("System Testing")
        self.progress = CLIProgressDialog(title, message)
        self.progress.show()
        self.do_function(function, *args, **kwargs)

    def show_pulse(self):
        self.progress.set()

    def show_intro(self, title, text):
        dialog = CLIChoiceDialog(title, text)
        dialog.run()

    def show_category(self, title, text, category=None):
        dialog = CLIChoiceDialog(title, text)
        for category in ALL_CATEGORIES:
            dialog.add_button("&%s" % category)

        # show categories dialog
        response = dialog.run()
        return ALL_CATEGORIES[response - 1]

    def show_test(self, test, result=None):
        if str(test.command):
            title = _("System Testing")
            self.progress = CLIProgressDialog(title,
                _("Running test: %s") % test.name)
            self.progress.show()

            result = self.do_function(test.command)
        else:
            result = None

        # show answer dialog
        dialog = CLIChoiceDialog(test.name, test.description(result).data)
        answers = [_("yes"), _("no"), _("skip")]
        for answer in answers:
            dialog.add_button("&%s" % answer)

        # get answer from dialog
        response = dialog.run()
        answer = answers[response - 1]
        data = ""
        if answer == _("no"):
            text = _("Please provide comments about the failure.")
            dialog = CLITextDialog(test.name, text)
            data = dialog.run(_("Please type here and press"
                " Ctrl-D when finished:\n"))

        status = {_("no"): FAIL, _("yes"): PASS, _("skip"): SKIP}[answer]
        return Result(test, status=status, data=data)

    def show_exchange(self, authentication, reports=[], message=None,
                      error=None):
        title = _("Authentication")
        text = message or _("Please provide your Launchpad email address:")
        dialog = CLILineDialog(title, text)

        if error:
            dialog.put("Error: %s" % error)

        authentication = dialog.run()
        return authentication

    def show_final(self, message=None):
        title = _("Done")
        text = _("Successfully sent information to server!")
        dialog = CLIChoiceDialog(title, text)

        return dialog.run()

    def show_error(self, title, text):
        dialog = CLIChoiceDialog("Error: %s" % title, text)
        dialog.run()