"""
http://www.valuedlessons.com/2008/04/events-in-python.html
by Peter Thatcher
"""


class Event(object):
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)
        return self

    def remove_handler(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler not found")
        return self

    def fire(self, *args):
        for handler in self.handlers:
            override_args = handler(*args)
            if override_args is not None:
                if type(override_args) is not tuple:
                    raise ValueError("Handler must return tuple")
                args = override_args

    __call__ = fire
