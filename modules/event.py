"""
http://www.valuedlessons.com/2008/04/events-in-python.html
by Peter Thatcher
"""


class Event(object):
    def __init__(self):
        self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)
        return self

    def remove_handler(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler not found.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    __call__ = fire
