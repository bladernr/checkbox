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
import logging

from checkbox.log import format_object


class EventID(object):

    def __init__(self, event_type, pair):
        self._event_type = event_type
        self._pair = pair


class StopException(Exception):

    pass


class StopAllException(Exception):

    pass


class Reactor(object):

    def __init__(self):
        self._event_handlers = {}

    def call_on(self, event_type, handler, priority=0):
        pair = (handler, priority)

        logging.debug("Calling on %s.", event_type)
        handlers = self._event_handlers.setdefault(event_type, [])
        handlers.append(pair)

        return EventID(event_type, pair)

    def fire(self, event_type, *args, **kwargs):
        logging.debug("Started firing %s.", event_type)

        results = []
        handlers = []
        for key, value in self._event_handlers.items():
            if re.match("^%s$" % key, event_type):
                handlers.extend(value)

        handlers = sorted(handlers, key=lambda pair: pair[1])
        if not handlers:
            logging.debug("No handlers found for event type: %s", event_type)

        for handler, priority in handlers:
            try:
                logging.debug("Calling %s for %s with priority %d.",
                              format_object(handler), event_type, priority)
                results.append(handler(*args, **kwargs))
            except StopException:
                break
            except StopAllException:
                raise
            except KeyboardInterrupt:
                logging.exception("Keyboard interrupt while running event "
                                  "handler %s for event type %r with "
                                  "args %r %r.", format_object(handler),
                                  event_type, args, kwargs)
                raise
            except:
                logging.exception("Error running event handler %s for "
                                  "event type %r with args %r %r.",
                                  format_object(handler), event_type,
                                  args, kwargs)

        logging.debug("Finished firing %s.", event_type)
        return results

    def cancel_call(self, id):
        if type(id) is EventID:
            self._event_handlers[id._event_type].remove(id._pair)
        else:
            raise Exception, "EventID instance expected, received %r" % id

    def cancel_all_calls(self, event_type):
        del self._event_handlers[event_type]

    def run(self):
        try:
            self.fire("run")
        except StopAllException:
            pass

    def stop(self):
        raise StopException

    def stop_all(self):
        raise StopAllException